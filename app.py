import streamlit as st
from modules.help import show_help_sidebar
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch

from modules.cognitive import analyze_user_input
from modules.prompt_engine import build_prompt
from modules.evaluator import evaluate_response

# -----------------------------
# Visit Counter (PERSISTENT)
# -----------------------------
def update_visit_count():
    try:
        with open("visits.txt", "r") as f:
            count = int(f.read())
    except:
        count = 0

    count += 1

    with open("visits.txt", "w") as f:
        f.write(str(count))

    return count

# -----------------------------
# Session State
# -----------------------------
if "show_help" not in st.session_state:
    st.session_state.show_help = False

if "confidence_history" not in st.session_state:
    st.session_state.confidence_history = []

if "visit_count" not in st.session_state:
    st.session_state.visit_count = update_visit_count()

# -----------------------------
# Load Models
# -----------------------------
@st.cache_resource
def load_models():
    device = 0 if torch.cuda.is_available() else -1

    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

    if device == 0:
        model.to("cuda")

    def generator_fn(prompt, max_length=200):
        inputs = tokenizer(prompt, return_tensors="pt")

        if device == 0:
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            do_sample=True,
            top_p=0.9
        )

        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return [{"generated_text": text}]

    emotion_model = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=True
    )

    return generator_fn, emotion_model


generator, emotion_model = load_models()

# -----------------------------
# UI - Header
# -----------------------------
col1, col2, col3 = st.columns([5, 1, 1])

with col1:
    st.title("🧠 Cognitive-Aware AI Chatbot")

with col2:
    if st.button("❓ Help"):
        st.session_state.show_help = True

with col3:
    st.markdown(
        f"<span style='font-size:23px;'>👁 </span> "
        f"<span style='font-size:20px;'>{st.session_state.visit_count}</span>",
        unsafe_allow_html=True
    )

# -----------------------------
# Help Sidebar
# -----------------------------
if st.session_state.show_help:
    with st.sidebar:
        show_help_sidebar()

# -----------------------------
# Input UI
# -----------------------------
user_input = st.text_input("Enter your message")
version = st.selectbox("Prompt Version", ["v1", "v2", "v3"])

# -----------------------------
# Run Logic
# -----------------------------
if st.button("Run"):

    if user_input.strip() == "":
        st.warning("Please enter a message")

    else:
        # Step 1: Analyze
        analysis = analyze_user_input(user_input, emotion_model)
        st.session_state.confidence_history.append(analysis["confidence"])

        # Step 2: Prompt
        prompt = build_prompt(user_input, analysis, version)

        # Step 3: Generate
        response = generator(prompt, max_length=200)
        raw_output = response[0]['generated_text']

        # Fallback
        advice = "Try breaking your task into smaller steps and start with one simple action."
        reasoning = "When you feel unsure, it's often due to lack of clarity or fear of failure. Small steps reduce pressure."
        question = "What part of this task feels most difficult to you?"

        if "Advice:" not in raw_output:
            output = f"""
Advice: {advice}

Reasoning: {reasoning}

Question: {question}
"""
        else:
            output = raw_output

        # Clean
        if "Advice:" in output:
            output = output[output.index("Advice:"):]

        # Step 4: Evaluate
        score = evaluate_response(output)

        # -----------------------------
        # Display
        # -----------------------------
        st.markdown("### 🤖 Response")
        st.markdown(output)

        st.subheader("🧠 Cognitive Analysis")
        st.json(analysis)

        st.subheader("📈 Confidence Over Time")
        st.line_chart(st.session_state.confidence_history)

        st.subheader("📊 Evaluation Score")
        st.write(score)

        st.subheader("🧪 Prompt Used")
        st.code(prompt)