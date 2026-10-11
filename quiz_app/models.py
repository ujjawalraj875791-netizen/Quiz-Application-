from dataclasses import dataclass
from typing import List

@dataclass
class Question:
    id: int
    category: str
    text: str
    options: List[str]
    answer: int
    explanation: str = ""

@dataclass
class QuizResult:
    player: str
    category: str
    total_questions: int
    correct: int
    wrong: int
    unanswered: int
    score: float
    percentage: float
    time_taken: int
