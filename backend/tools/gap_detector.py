from typing import Tuple, List
from models.curriculum import Curriculum
from models.analysis import MissingTopic

def detect_gaps(target: Curriculum, student: Curriculum) -> Tuple[List[MissingTopic], List[str], float]:
    target_names = {t.name.lower(): t for t in target.topics}
    student_names = {t.name.lower(): t for t in student.topics}
    missing_topics = []
    weak_topics = []
    for t_name, t_topic in target_names.items():
        if t_name not in student_names:
            severity = (hash(t_name) % 10) + 1
            missing_topics.append(
                MissingTopic(
                    topic_name=t_topic.name,
                    reason="Not found in student curriculum.",
                    severity_score=severity
                )
            )
        else:
            if hash(t_name) % 5 == 0:
                weak_topics.append(t_topic.name)
    if not target_names:
        gap_score = 0.0
    else:
        gap_score = round(len(missing_topics) / len(target_names), 2)
    return missing_topics, weak_topics, gap_score
