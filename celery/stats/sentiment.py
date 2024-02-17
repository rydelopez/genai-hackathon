from enum import Enum, auto
from collections import Counter


SENTIMENT_MODEL_NAME = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"


class Sentiment(Enum):
    POSITIVE = auto()
    NEUTRAL = auto()
    NEGATIVE = auto()


distilled_student_sentiment_classifier = pipeline(
    model=SENTIMENT_MODEL_NAME, 
    return_all_scores=True
)

def measure_sentiment(student_text: str) -> Sentiment:
    sentiment_label_scores = distilled_student_sentiment_classifier(student_text)[0]

    # Get the label with the highest score
    best_score = 0
    best_label = None
    for c in sentiment_label_scores:
        if c['score'] > best_score:
            best_score = c['score']
            best_label = c['label']

    return Sentiment[best_label.upper()]

  
def measure_convo_sentiment(conversation: ChatSession) -> dict[str, int]:
    sentiment_ratios = Counter()
    total = 0

    for msg in conversation:
        if msg.type == "human":
            sentiment = measure_sentiment(msg.contents)
            sentiment_tracker[sentiment] += 1
            total += 1

    return {
        "positive": sentiment_tracker[POSITIVE] / total,
        "neutral": sentiment_tracker[NEUTRAL] / total,
        "negative": sentiment_tracker[NEGATIVE] / total,
    }