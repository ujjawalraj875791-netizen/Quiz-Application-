import time
from .config import POSITIVE_MARK, NEGATIVE_MARK
from .models import QuizResult

class QuizEngine:
    def __init__(self, questions):
        self.questions = questions
        self.index = 0
        self.answers = [None] * len(questions)
        self.started_at = time.monotonic()

    @property
    def current(self):
        return self.questions[self.index]

    @property
    def finished(self):
        return self.index >= len(self.questions)

    def answer(self, option_index):
        self.answers[self.index] = option_index

    def next(self):
        self.index += 1

    def result(self, player, category):
        correct = wrong = unanswered = 0
        score = 0.0

        for q, selected in zip(self.questions, self.answers):
            if selected is None:
                unanswered += 1
            elif selected == q.answer:
                correct += 1
                score += POSITIVE_MARK
            else:
                wrong += 1
                score -= NEGATIVE_MARK

        max_score = len(self.questions) * POSITIVE_MARK
        percentage = max(0.0, score / max_score * 100) if max_score else 0.0
        time_taken = int(time.monotonic() - self.started_at)

        return QuizResult(
            player=player,
            category=category,
            total_questions=len(self.questions),
            correct=correct,
            wrong=wrong,
            unanswered=unanswered,
            score=round(score, 2),
            percentage=round(percentage, 2),
            time_taken=time_taken,
        )
