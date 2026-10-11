# Quiz Master — Intermediate Python Project

A complete desktop quiz application built with **Python + Tkinter + SQLite + JSON**.

## Features

- Random question selection
- Questions stored in `data/questions.json`
- Persistent leaderboard stored in SQLite
- Category-based quizzes
- 5, 10, or 15 question quizzes
- 15-second timer for every question
- Negative marking: **+1 correct, -0.25 wrong, 0 unanswered**
- Automatic timeout handling
- Results screen with score, percentage, correct/wrong/unanswered counts
- Category-filtered leaderboard
- Clean multi-file architecture
- Standard Python library only — no external packages required

## Requirements

- Python 3.10+ recommended
- Tkinter (normally included with standard Python on Windows/macOS)
- No pip packages are required

## Run

From the project folder:

```bash
python main.py
```

If your system uses `python3`:

```bash
python3 main.py
```

## Project Structure

```text
quiz_application/
├── main.py
├── README.md
├── data/
│   └── questions.json
└── quiz_app/
    ├── __init__.py
    ├── config.py
    ├── models.py
    ├── question_bank.py
    ├── database.py
    ├── quiz_engine.py
    └── gui.py
```

`data/quiz.db` is created automatically the first time the application starts.

## How the scoring works

For each question:

- Correct answer: +1
- Wrong answer: -0.25
- Unanswered / timeout: 0

Example:

```text
10 questions
7 correct  = +7.00
2 wrong    = -0.50
1 unanswered = 0
Final score = 6.50
```

Percentage is calculated against the maximum possible score.

## Adding Questions

Open:

```text
data/questions.json
```

Each question follows this structure:

```json
{
  "id": 31,
  "category": "Python",
  "question": "Your question?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "answer": 0,
  "explanation": "Explanation of the correct answer."
}
```

Important: `answer` is zero-based:

- `0` = first option
- `1` = second option
- `2` = third option
- `3` = fourth option

You can create new categories simply by changing the `"category"` value.

## Main Concepts Demonstrated

This project is suitable as an intermediate Python project because it demonstrates:

1. Object-oriented programming
2. Classes and dataclasses
3. Tkinter GUI programming
4. Event-driven programming
5. SQLite database CRUD/persistence
6. JSON file handling
7. Random selection
8. Timers using Tkinter `after()`
9. Exception handling
10. Modular project structure
11. Separation of GUI, business logic, database, and data
12. Leaderboard sorting
13. Input validation

## Suggested Future Improvements

- Login/register system
- Admin panel for adding questions
- Difficulty levels
- Question explanations after every answer
- Progress bar
- Sound effects
- Image-based questions
- Export leaderboard to CSV
- Question management using SQLite instead of JSON
- Dark mode
- Per-category statistics
- High-score badge system
