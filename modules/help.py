import streamlit as st

def show_help_sidebar():

    st.markdown("## ❓ How to Use This Chatbot")

    st.markdown("""
### 🧠 What this chatbot does
- Analyzes your **emotion and confidence**
- Detects hesitation (e.g., *maybe, not sure*)
- Generates structured responses using prompt engineering

---

### 📝 What you get
- **Advice** → What you should do  
- **Reasoning** → Why it helps  
- **Question** → Helps you think deeper  

---

### 📌 How to use
1. Enter your message  
2. Click **Run**  
3. View response + analysis  

---

### 💡 Example inputs
- "I am not sure if I can do this"
- "I feel confident today"
- "Maybe I will try later"
""")

    st.markdown("---")

    # 🔥 NEW SECTION (IMPORTANT – INTERVIEW LEVEL)
    st.markdown("## 🔍 How the Model Works (Example)")

    st.markdown("""
### 🧪 Example Input
> "I am not sure if I can do this"

### 🧠 Step-by-step Processing

1. **Cognitive Analysis**
   - Emotion → *Uncertain / Neutral*
   - Confidence → *Low*
   - Hesitation detected → *Yes*

2. **Prompt Construction**
   The system builds a structured prompt:
   - Role: Cognitive-aware assistant  
   - Context: User input + analysis  
   - Rules: Be supportive, structured output  

3. **Model Response Generation**
   The model (FLAN-T5) generates a response based on the prompt.

4. **Guardrail Layer**
   - If output is weak → fallback response is used  
   - Ensures format: Advice / Reasoning / Question  

---

### 🎯 Final Output

- **Advice:** Break task into smaller steps  
- **Reasoning:** Reduces fear and confusion  
- **Question:** Helps identify difficulty  

---

### 💡 Real-World Impact

#### 👤 For Users
- Helps reduce confusion  
- Improves clarity and confidence  
- Guides decision-making  

#### 🏢 For Development / AI Systems
- Demonstrates **prompt control**
- Shows **LLM evaluation techniques**
- Implements **fallback reliability system**
- Mimics **production-level AI pipelines**

---

### 🚀 Why This Matters

Most chatbots:
❌ Just generate responses  

This system:
✅ Understands user thinking  
✅ Controls output structure  
✅ Ensures reliability  

👉 This is closer to **real-world AI systems**
""")

    st.markdown("---")

    if st.button("❌ Close Help"):
        st.session_state.show_help = False