def evaluate_response(response):
    score = 0

    if "Advice:" in response:
        score += 1
    if "Reasoning:" in response:
        score += 1
    if "Question:" in response or "Follow-up" in response:
        score += 1

    return round(score / 3, 2)