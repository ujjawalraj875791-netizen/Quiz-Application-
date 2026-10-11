import tkinter as tk
from tkinter import ttk, messagebox
from .config import (
    APP_TITLE, QUESTION_TIME_SECONDS, DEFAULT_QUESTION_COUNT,
    DATABASE_PATH, QUESTION_FILE
)
from .database import Database
from .question_bank import QuestionBank
from .quiz_engine import QuizEngine

class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("820x620")
        self.minsize(760, 560)

        self.bank = QuestionBank(QUESTION_FILE)
        self.db = Database(DATABASE_PATH)
        self.engine = None
        self.player = ""
        self.category = ""
        self.remaining = QUESTION_TIME_SECONDS
        self.timer_job = None

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"))
        self.style.configure("Question.TLabel", font=("Segoe UI", 15, "bold"))
        self.style.configure("Info.TLabel", font=("Segoe UI", 11))

        self.show_start()

    def clear(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        for widget in self.winfo_children():
            widget.destroy()

    def show_start(self):
        self.clear()
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Quiz Master", style="Title.TLabel").pack(pady=(30, 8))
        ttk.Label(frame, text="Intermediate Python Quiz Application",
                  style="Info.TLabel").pack(pady=(0, 25))

        form = ttk.Frame(frame)
        form.pack(pady=10)

        ttk.Label(form, text="Player name:").grid(row=0, column=0, sticky="w", pady=8)
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var, width=35).grid(
            row=0, column=1, padx=10, pady=8
        )

        ttk.Label(form, text="Category:").grid(row=1, column=0, sticky="w", pady=8)
        cats = ["All"] + self.bank.categories()
        self.category_var = tk.StringVar(value="All")
        ttk.Combobox(form, textvariable=self.category_var,
                     values=cats, state="readonly", width=32).grid(
                         row=1, column=1, padx=10, pady=8)

        ttk.Label(form, text="Questions:").grid(row=2, column=0, sticky="w", pady=8)
        counts = [5, 10, 15]
        self.count_var = tk.IntVar(value=DEFAULT_QUESTION_COUNT)
        ttk.Combobox(form, textvariable=self.count_var,
                     values=counts, state="readonly", width=32).grid(
                         row=2, column=1, padx=10, pady=8)

        info = (
            "Scoring: +1 for correct, -0.25 for wrong, 0 for unanswered\n"
            f"Time: {QUESTION_TIME_SECONDS} seconds per question\n"
            "If time reaches zero, the question is marked unanswered."
        )
        ttk.Label(frame, text=info, justify="center").pack(pady=20)

        buttons = ttk.Frame(frame)
        buttons.pack(pady=10)
        ttk.Button(buttons, text="Start Quiz", command=self.start_quiz).grid(
            row=0, column=0, padx=8
        )
        ttk.Button(buttons, text="Leaderboard", command=self.show_leaderboard).grid(
            row=0, column=1, padx=8
        )
        ttk.Button(buttons, text="Exit", command=self.destroy).grid(
            row=0, column=2, padx=8
        )

    def start_quiz(self):
        self.player = self.name_var.get().strip()
        if not self.player:
            messagebox.showwarning("Missing name", "Please enter your name.")
            return

        self.category = self.category_var.get()
        count = int(self.count_var.get())
        try:
            questions = self.bank.get_random(self.category, count)
        except ValueError as exc:
            messagebox.showerror("Quiz setup", str(exc))
            return

        self.engine = QuizEngine(questions)
        self.show_question()

    def show_question(self):
        self.clear()
        if self.engine.finished:
            self.finish_quiz()
            return

        self.remaining = QUESTION_TIME_SECONDS
        q = self.engine.current

        top = ttk.Frame(self, padding=(25, 20, 25, 5))
        top.pack(fill="x")
        ttk.Label(
            top,
            text=f"Question {self.engine.index + 1} of {len(self.engine.questions)}"
        ).pack(side="left")
        self.timer_label = ttk.Label(top, text="", style="Info.TLabel")
        self.timer_label.pack(side="right")

        main = ttk.Frame(self, padding=25)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text=q.category, style="Info.TLabel").pack(anchor="w", pady=(5, 12))
        ttk.Label(main, text=q.text, style="Question.TLabel",
                  wraplength=720, justify="left").pack(anchor="w", pady=(0, 20))

        self.option_var = tk.IntVar(value=-1)
        for i, option in enumerate(q.options):
            ttk.Radiobutton(
                main, text=option, value=i, variable=self.option_var
            ).pack(anchor="w", fill="x", pady=7, padx=10)

        bottom = ttk.Frame(main)
        bottom.pack(fill="x", pady=25)
        ttk.Button(bottom, text="Next", command=self.next_question).pack(side="right")

        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time: {self.remaining}s")
        if self.remaining <= 0:
            self.engine.answer(None)
            self.engine.next()
            self.show_question()
            return
        self.remaining -= 1
        self.timer_job = self.after(1000, self.update_timer)

    def next_question(self):
        selected = self.option_var.get()
        if selected == -1:
            if not messagebox.askyesno(
                "Unanswered", "Leave this question unanswered?"
            ):
                return
            selected = None

        self.engine.answer(selected)
        self.engine.next()
        self.show_question()

    def finish_quiz(self):
        result = self.engine.result(self.player, self.category)
        self.db.save_result(result)
        self.show_result(result)

    def show_result(self, result):
        self.clear()
        frame = ttk.Frame(self, padding=30)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Quiz Completed!", style="Title.TLabel").pack(pady=10)
        ttk.Label(frame, text=f"Player: {result.player}",
                  style="Info.TLabel").pack(pady=5)
        ttk.Label(frame, text=f"Category: {result.category}",
                  style="Info.TLabel").pack(pady=5)

        stats = (
            f"Score: {result.score:.2f}\n"
            f"Percentage: {result.percentage:.2f}%\n\n"
            f"Correct: {result.correct}\n"
            f"Wrong: {result.wrong}\n"
            f"Unanswered: {result.unanswered}\n"
            f"Time taken: {result.time_taken} seconds"
        )
        ttk.Label(frame, text=stats, justify="center",
                  font=("Segoe UI", 13)).pack(pady=20)

        buttons = ttk.Frame(frame)
        buttons.pack(pady=10)
        ttk.Button(buttons, text="Leaderboard",
                   command=self.show_leaderboard).grid(row=0, column=0, padx=8)
        ttk.Button(buttons, text="Play Again",
                   command=self.show_start).grid(row=0, column=1, padx=8)
        ttk.Button(buttons, text="Exit",
                   command=self.destroy).grid(row=0, column=2, padx=8)

    def show_leaderboard(self):
        self.clear()
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Leaderboard", style="Title.TLabel").pack(pady=(5, 15))

        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=5)
        cats = ["All"] + self.bank.categories()
        lb_cat = tk.StringVar(value="All")
        ttk.Label(controls, text="Category:").pack(side="left")
        combo = ttk.Combobox(controls, textvariable=lb_cat,
                             values=cats, state="readonly", width=25)
        combo.pack(side="left", padx=8)

        columns = ("rank", "player", "category", "score", "%", "correct",
                   "wrong", "unanswered", "time")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=16)
        headings = {
            "rank": "#", "player": "Player", "category": "Category",
            "score": "Score", "%": "%", "correct": "Correct",
            "wrong": "Wrong", "unanswered": "Unanswered", "time": "Time(s)"
        }
        widths = {"rank": 40, "player": 130, "category": 120, "score": 65,
                  "%": 65, "correct": 65, "wrong": 65, "unanswered": 85, "time": 70}
        for col in columns:
            tree.heading(col, text=headings[col])
            tree.column(col, width=widths[col], anchor="center")
        tree.pack(fill="both", expand=True, pady=10)

        def refresh(*_):
            for item in tree.get_children():
                tree.delete(item)
            rows = self.db.top_scores(lb_cat.get())
            for rank, row in enumerate(rows, 1):
                player, cat, score, pct, correct, wrong, unanswered, time_taken, _ = row
                tree.insert("", "end", values=(
                    rank, player, cat, f"{score:.2f}", f"{pct:.2f}",
                    correct, wrong, unanswered, time_taken
                ))

        combo.bind("<<ComboboxSelected>>", refresh)
        refresh()

        ttk.Button(frame, text="Back", command=self.show_start).pack(pady=8)

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
