import tkinter as tk
from tkinter import messagebox

# Modern Color Palette
COLORS = {
    "bg": "#121212",        # Main background
    "card": "#1E1E1E",      # Content frames
    "text": "#E0E0E0",      # Primary text
    "accent": "#3B82F6",    # Blue accent
    "accent_hover": "#2563EB",
    "danger": "#EF4444",    # Red for submit
    "timer": "#FBBF24",     # Gold/Yellow for clock
    "border": "#333333"
}

QUIZ_DATA = {
    "Computer Science (COS 102)": [
        {"question": "What does CPU stand for?", "options": ["Central Processing Unit", "Central Process Unit", "Computer Personal Unit", "Central Processor Unifier"], "answer": "Central Processing Unit"},
        {"question": "Which of the following is an OOP concept?", "options": ["Inheritance", "Compilation", "Linking", "Streaming"], "answer": "Inheritance"},
        {"question": "What is the default GUI library in Python?", "options": ["PyQt", "Tkinter", "Kivy", "wxPython"], "answer": "Tkinter"},
        {"question": "Which protocol is used to secure data over the internet?", "options": ["HTTP", "FTP", "HTTPS", "SMTP"], "answer": "HTTPS"},
        {"question": "What is the time complexity of searching in a balanced BST?", "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"], "answer": "O(log n)"}
    ],
    "Mathematics (MTH 102)": [
        {"question": "What is the derivative of sin(x)?", "options": ["cos(x)", "-cos(x)", "sin(x)", "-sin(x)"], "answer": "cos(x)"},
        {"question": "Evaluate the limit: lim (x->0) [sin(x)/x]", "options": ["0", "1", "Undefined", "Infinity"], "answer": "1"},
        {"question": "Which method is best for integrating the product of an algebraic and exponential function?", "options": ["U-Substitution", "Tabular Method / Parts", "Partial Fractions", "Trig Substitution"], "answer": "Tabular Method / Parts"},
        {"question": "What is the integral of 1/x dx?", "options": ["ln|x| + C", "x^2 + C", "e^x + C", "-1/x^2 + C"], "answer": "ln|x| + C"}
    ]
}

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Arena Pro")
        self.root.geometry("700x550")
        self.root.configure(bg=COLORS["bg"])
        
        self.selected_course = ""
        self.total_time_seconds = 0
        self.questions_to_load = []
        self.user_answers = {}
        self.current_index = 0
        self.timer_running = False
        
        self.show_welcome_page()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_modern_button(self, parent, text, color, command, width=15):
        """Helper to create consistent styled buttons with hover effects."""
        btn = tk.Button(
            parent, text=text, command=command, font=("Helvetica", 10, "bold"),
            bg=color, fg="white", activebackground=color, activeforeground="white",
            relief="flat", cursor="hand2", width=width, pady=8
        )
        return btn

    def show_welcome_page(self):
        self.clear_screen()
        
        # Main Card
        main_frame = tk.Frame(self.root, bg=COLORS["card"], padx=40, pady=40, highlightbackground=COLORS["border"], highlightthickness=1)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="QUIZ ARENA", font=("Verdana", 24, "bold"), bg=COLORS["card"], fg=COLORS["accent"]).pack(pady=(0, 20))
        
        # Course Selection
        tk.Label(main_frame, text="Select Subject", font=("Helvetica", 10), bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w")
        self.course_var = tk.StringVar(value=list(QUIZ_DATA.keys())[0])
        course_dropdown = tk.OptionMenu(main_frame, self.course_var, *QUIZ_DATA.keys(), command=self.update_question_range_label)
        course_dropdown.config(bg=COLORS["bg"], fg=COLORS["text"], highlightthickness=0, relief="flat", font=("Helvetica", 10), width=35)
        course_dropdown["menu"].config(bg=COLORS["card"], fg=COLORS["text"])
        course_dropdown.pack(pady=(5, 20))
        
        # Spinboxes Row
        spin_frame = tk.Frame(main_frame, bg=COLORS["card"])
        spin_frame.pack(fill="x", pady=10)

        # Time
        tk.Label(spin_frame, text="Time (Min):", font=("Helvetica", 10), bg=COLORS["card"], fg=COLORS["text"]).grid(row=0, column=0, sticky="w")
        self.time_spinbox = tk.Spinbox(spin_frame, from_=1, to=120, width=5, bg=COLORS["bg"], fg=COLORS["text"], insertbackground="white", relief="flat")
        self.time_spinbox.delete(0, "end")
        self.time_spinbox.insert(0, "5")
        self.time_spinbox.grid(row=0, column=1, padx=10)

        # Count
        tk.Label(spin_frame, text="Questions:", font=("Helvetica", 10), bg=COLORS["card"], fg=COLORS["text"]).grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.range_spinbox = tk.Spinbox(spin_frame, from_=1, to=10, width=5, bg=COLORS["bg"], fg=COLORS["text"], relief="flat")
        self.range_spinbox.grid(row=0, column=3, padx=10)

        self.pool_info_label = tk.Label(main_frame, text="", font=("Helvetica", 8), bg=COLORS["card"], fg="#777")
        self.pool_info_label.pack()
        
        self.update_question_range_label(self.course_var.get())

        start_btn = self.create_modern_button(main_frame, "START SESSION", COLORS["accent"], self.validate_and_start, width=25)
        start_btn.pack(pady=(30, 0))

    def update_question_range_label(self, selected_course):
        max_questions = len(QUIZ_DATA[selected_course])
        self.range_spinbox.config(from_=1, to=max_questions)
        self.range_spinbox.delete(0, "end")
        self.range_spinbox.insert(0, str(max_questions))
        self.pool_info_label.config(text=f"Available in bank: {max_questions}")

    def validate_and_start(self):
        self.selected_course = self.course_var.get()
        try:
            minutes = int(self.time_spinbox.get())
            num_questions = int(self.range_spinbox.get())
        except ValueError:
            messagebox.showerror("Error", "Enter numbers for time and range.")
            return

        self.questions_to_load = QUIZ_DATA[self.selected_course][:num_questions]
        self.total_time_seconds = minutes * 60
        self.current_index = 0
        self.user_answers = {}
        self.show_quiz_page()

    def show_quiz_page(self):
        self.clear_screen()
        self.timer_running = True
        
        # Modern Top Bar
        header = tk.Frame(self.root, bg=COLORS["card"], height=60)
        header.pack(fill="x")
        
        tk.Label(header, text=self.selected_course, font=("Helvetica", 12, "bold"), fg=COLORS["accent"], bg=COLORS["card"]).pack(side="left", padx=20)
        self.timer_lbl = tk.Label(header, text="00:00", font=("Consolas", 14, "bold"), fg=COLORS["timer"], bg=COLORS["card"])
        self.timer_lbl.pack(side="right", padx=20)

        # Question Content
        content_frame = tk.Frame(self.root, bg=COLORS["bg"], padx=40, pady=30)
        content_frame.pack(fill="both", expand=True)

        self.q_num_lbl = tk.Label(content_frame, text="", font=("Helvetica", 10), bg=COLORS["bg"], fg="#888")
        self.q_num_lbl.pack(anchor="w")

        self.question_lbl = tk.Label(content_frame, text="", font=("Helvetica", 15), bg=COLORS["bg"], fg=COLORS["text"], wraplength=600, justify="left")
        self.question_lbl.pack(pady=20, anchor="w")

        self.option_var = tk.StringVar()
        self.option_buttons = []
        for _ in range(4):
            rb = tk.Radiobutton(
                content_frame, text="", variable=self.option_var, value="",
                font=("Helvetica", 11), bg=COLORS["bg"], fg=COLORS["text"],
                selectcolor="#333", activebackground=COLORS["bg"], activeforeground=COLORS["accent"],
                padx=10, pady=5, command=self.save_answer
            )
            rb.pack(anchor="w", pady=5)
            self.option_buttons.append(rb)

        # Footer Nav
        footer = tk.Frame(self.root, bg=COLORS["card"], pady=15, padx=30)
        footer.pack(fill="x", side="bottom")

        self.prev_btn = self.create_modern_button(footer, "PREVIOUS", "#444", self.prev_question, width=12)
        self.prev_btn.pack(side="left")

        self.next_btn = self.create_modern_button(footer, "NEXT", COLORS["accent"], self.next_question, width=12)
        self.next_btn.pack(side="left", padx=10)

        self.submit_btn = self.create_modern_button(footer, "SUBMIT", COLORS["danger"], self.confirm_submission, width=12)
        self.submit_btn.pack(side="right")

        self.update_timer_ticker()
        self.display_current_question()

    def display_current_question(self):
        q_data = self.questions_to_load[self.current_index]
        self.q_num_lbl.config(text=f"QUESTION {self.current_index + 1} OF {len(self.questions_to_load)}")
        self.question_lbl.config(text=q_data["question"])
        
        for i, option in enumerate(q_data["options"]):
            self.option_buttons[i].config(text=option, value=option)
            
        self.option_var.set(self.user_answers.get(self.current_index, ""))
        
        self.prev_btn.config(state="disabled" if self.current_index == 0 else "normal")
        if self.current_index == len(self.questions_to_load) - 1:
            self.next_btn.config(text="FINISH", bg="#10B981") # Green for finish
        else:
            self.next_btn.config(text="NEXT", bg=COLORS["accent"])

    def save_answer(self):
        self.user_answers[self.current_index] = self.option_var.get()

    def next_question(self):
        if self.current_index < len(self.questions_to_load) - 1:
            self.current_index += 1
            self.display_current_question()
        else:
            self.confirm_submission()

    def prev_question(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_current_question()

    def update_timer_ticker(self):
        if self.timer_running and self.total_time_seconds >= 0:
            mins, secs = divmod(self.total_time_seconds, 60)
            self.timer_lbl.config(text=f"{mins:02d}:{secs:02d}")
            if self.total_time_seconds == 0:
                self.evaluate_results()
                return
            self.total_time_seconds -= 1
            self.root.after(1000, self.update_timer_ticker)

    def confirm_submission(self):
        unanswered = len(self.questions_to_load) - len(self.user_answers)
        msg = f"Ready to submit? You have {unanswered} unanswered items." if unanswered > 0 else "Ready to submit your answers?"
        if messagebox.askyesno("Submit Quiz", msg):
            self.timer_running = False
            self.evaluate_results()

    def evaluate_results(self):
        score = sum(1 for idx, q in enumerate(self.questions_to_load) if self.user_answers.get(idx) == q["answer"])
        messagebox.showinfo("Result", f"Course: {self.selected_course}\nFinal Score: {score} / {len(self.questions_to_load)}")
        self.show_welcome_page()

if __name__ == "__main__":
    window = tk.Tk()
    app = QuizApp(window)
    window.mainloop()