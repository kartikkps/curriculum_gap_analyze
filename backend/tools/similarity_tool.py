from models.curriculum import Curriculum

def calculate_similarity(target: Curriculum, student: Curriculum) -> float:
    target_names = {t.name.lower() for t in target.topics}
    student_names = {t.name.lower() for t in student.topics}
    if not target_names:
        return 1.0
    intersection = target_names.intersection(student_names)
    score = len(intersection) / len(target_names)
    return round(score, 2)
