import json
import random
from pathlib import Path
from .models import Question

class QuestionBank:
    def __init__(self, json_path):
        self.json_path = Path(json_path)

    def load(self):
        if not self.json_path.exists():
            raise FileNotFoundError(f"Question file not found: {self.json_path}")
        data = json.loads(self.json_path.read_text(encoding="utf-8"))
        questions = []
        for item in data:
            questions.append(
                Question(
                    id=int(item["id"]),
                    category=item["category"],
                    text=item["question"],
                    options=item["options"],
                    answer=int(item["answer"]),
                    explanation=item.get("explanation", ""),
                )
            )
        return questions

    def categories(self):
        return sorted({q.category for q in self.load()})

    def get_random(self, category="All", count=10):
        questions = self.load()
        if category != "All":
            questions = [q for q in questions if q.category == category]
        if len(questions) < count:
            raise ValueError(
                f"Only {len(questions)} question(s) available in '{category}'. "
                f"Choose a smaller quiz."
            )
        return random.sample(questions, count)
