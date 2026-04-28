def analyze_user_input(text, emotion_model):
    results = emotion_model(text)[0]

    # pick highest emotion
    best = max(results, key=lambda x: x['score'])

    emotion = best['label']
    confidence_score = best['score']

    # hesitation detection
    hesitation_words = ["maybe", "i guess", "not sure", "probably"]
    hesitation = sum(1 for w in hesitation_words if w in text.lower())

    # improve emotion interpretation
    if hesitation > 0 and emotion.lower() == "neutral":
        emotion = "uncertain"

    confidence = round(confidence_score - (0.2 * hesitation), 2)

    return {
        "confidence": max(confidence, 0),
        "hesitation": hesitation,
        "emotion": emotion
    }