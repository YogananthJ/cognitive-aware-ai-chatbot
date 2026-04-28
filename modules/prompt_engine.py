def build_prompt(user_input, analysis, version="v1"):

    prompt = f"""
You are a cognitive-aware AI assistant.

A user says:
"{user_input}"

User emotion: {analysis['emotion']}
Confidence level: {analysis['confidence']}

Your task:
Analyze the user's mental state and respond helpfully.

STRICT RULES:
- You MUST follow the format exactly
- Do NOT skip any section
- Be clear and supportive
- Keep answer short (3–5 lines per section)

FORMAT:
Advice: <clear actionable advice>
Reasoning: <why this advice makes sense>
Question: <ask a thoughtful follow-up>

Now generate the response:
"""
    return prompt