from bertopic import BERTopic
from setfit import SetFitModel

from collections import Counter
from enum import Enum, auto

from schema.conversation import ChatSession

TOPIC_PROB_THRESHOLD = 0.3
CONCEPT_MODEL = "MaartenGr/BERTopic_Wikipedia"
SUBJECT_MODEL = "bew/setfit-subject-model-basic"
ENGAGEMENT_MODEL = "bew/setfit-engagement-model-basic"

class Subject(Enum):
    ENGLISH = auto()
    MATH = auto()
    ART = auto()
    SCIENCE = auto()
    HISTORY = auto()
    TECHNOLOGY = auto()


# Concepts
concept_model = BERTopic.load(CONCEPT_MODEL)

def get_concept(text: str) -> str:
    topic, prob = topic_model.transform(text)
    topic = topic[0]
    if topic == -1 or prob < TOPIC_PROB_THRESHOLD:
        return None

    return topic_model.get_topic_info(topic)['Name'].item()


# Subjects
subject_model = SetFitModel.from_pretrained(SUBJECT_MODEL)

def get_subject(text: str) -> Subject:
    pred = subject_model.predict(text)
    if pred == 'NONE':
        return None

    return Subject[pred.upper()]


# Engagement
engagement_model = SetFitModel.from_pretrained(ENGAGEMENT_MODEL)

def measure_engagement(student_text: str) -> float:
    '''
    returns a float from 0 to 1, where 1 is the most engaged
    '''
    probs = engagement_model.predict_proba(student_text)
    return float(probs[1])


def measure_convo_topics(conversation: ChatSession) -> dict[str, int]:
    """
    Returns a dictionary of the form

    {topic: num_times_appeared}
    """
    topics_counter = Counter()
    total = 0

    for msg in conversation:
        if msg.type == "human":
            engagement = measure_engagement(msg.contents)
            if engagement < 0.5:
                continue

            concept = get_concept(msg.contents)
            subject = get_subject(msg.contents)
            topics_counter[concept] += 1
            topics_counter[subject] += 1

    return topics_counter