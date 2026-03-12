from models.curriculum import Curriculum, Topic

def parse_syllabus(text: str) -> Curriculum:
    lines = [line.strip() for line in text.replace(',', '\n').split('\n') if line.strip()]
    topics = []
    for line in lines:
        topics.append(Topic(name=line, description=f"Parsed from text: {line}"))
    return Curriculum(topics=topics)
