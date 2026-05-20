import customtkinter as ctk
from datetime import datetime

# Safe import fallbacks for nested vs flat directories
try:
    from core.models import User
    from core.engine import MathEngine
except ModuleNotFoundError:
    from models import User
    from engine import MathEngine

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

UNITS_CONFIGURATION = [
    {"title": "Unit 1 - Core Mathematics", "topics": ["Arithmetic", "Powers", "Equations"]},
    {"title": "Unit 2 - High School Mathematics", "topics": ["Algebra", "Geometry", "Trigonometry"]},
    {"title": "Unit 3 - Logic", "topics": ["Probability", "Logic"]},
    {"title": "Unit 4 - Higher Math", "topics": ["Calculus", "Discrete Math"]},
    {"title": "Unit 5 - Pure Mathematics", "topics": ["Real World Math", "Competitive Math"]}
]

ALL_TOPICS = []
for unit in UNITS_CONFIGURATION:
    ALL_TOPICS.extend(unit["topics"])

class MathLingoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MathLingo")
        self.geometry("480x780")
        self.resizable(False, False)
        
        self.engine = MathEngine()
        
        # User is None until they authenticate via the Login Screen
        self.user = None
        
        self.active_topic = None
        self.active_question = None
        self.progress_score = 0
        
        # Explicit tracker for user-facing UI elements to clean up memory
        self.view_elements = []
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Base scrollable wrapper configuration
        self.viewport_frame = ctk.CTkScrollableFrame(self, fg_color="#F9FAFB", corner_radius=0)
        self.viewport_frame.grid(row=1, column=0, sticky="nsew")
        
        # App boots directly into the login view
        self.render_login_view()

    # ------------------------------------------------------------------------
    # CORE UI COMPONENTS
    # ------------------------------------------------------------------------

    def initialize_top_bar(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", height=60, corner_radius=0, border_width=1, border_color="#E5E7EB")
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.pack_propagate(False)
        
        self.xp_lbl = ctk.CTkLabel(self.header_frame, text="⚡ 0 XP", font=("Arial", 16, "bold"), text_color="#EAB308")
        self.xp_lbl.pack(side="left", padx=25)
        
        self.hearts_lbl = ctk.CTkLabel(self.header_frame, text="", font=("Arial", 16, "bold"), text_color="#EF4444")
        self.hearts_lbl.pack(side="right", padx=25)
        self.refresh_header_stats()

    def initialize_bottom_navigation(self):
        self.dock_frame = ctk.CTkFrame(self, height=65, fg_color="#FFFFFF", corner_radius=0, border_width=1, border_color="#E5E7EB")
        self.dock_frame.grid(row=2, column=0, sticky="ew")
        self.dock_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(self.dock_frame, text="MAP", font=("Arial", 13, "bold"), fg_color="transparent", text_color="#6B7280", hover_color="#F3F4F6", command=self.render_map_view).grid(row=0, column=0, sticky="nsew", pady=5)
        ctk.CTkButton(self.dock_frame, text="PROFILE", font=("Arial", 13, "bold"), fg_color="transparent", text_color="#6B7280", hover_color="#F3F4F6", command=self.render_profile_view).grid(row=0, column=1, sticky="nsew", pady=5)

    def clear_viewport(self):
        """Destroys layout components explicitly while keeping canvas structures intact."""
        for element in self.view_elements:
            try:
                element.destroy()
            except Exception:
                pass
        self.view_elements.clear()

    def refresh_header_stats(self):
        if not self.user:
            return
        self.xp_lbl.configure(text=f"⚡ {self.user.xp} XP")
        heart_symbol = "❤️" * self.user.hearts if self.user.hearts > 0 else "💔 Empty"
        self.hearts_lbl.configure(text=f"{heart_symbol}")

    # ------------------------------------------------------------------------
    # LOGIN VIEW
    # ------------------------------------------------------------------------

    def render_login_view(self):
        self.clear_viewport()
        
        ctk.CTkLabel(self.viewport_frame, text="").pack(pady=40) # Spacer
        
        logo_lbl = ctk.CTkLabel(self.viewport_frame, text="MathLingo", font=("Arial", 36, "bold"), text_color="#3B82F6")
        logo_lbl.pack(pady=(20, 5))
        self.view_elements.append(logo_lbl)
        
        sub_lbl = ctk.CTkLabel(self.viewport_frame, text="Learn math the fun way.", font=("Arial", 16), text_color="#6B7280")
        sub_lbl.pack(pady=(0, 40))
        self.view_elements.append(sub_lbl)

        self.username_entry = ctk.CTkEntry(
            self.viewport_frame, placeholder_text="Enter your username", 
            width=300, height=50, font=("Arial", 16), corner_radius=12,
            border_color="#E5E7EB", border_width=2
        )
        self.username_entry.pack(pady=10)
        self.view_elements.append(self.username_entry)

        self.login_error_lbl = ctk.CTkLabel(self.viewport_frame, text="", font=("Arial", 12), text_color="#EF4444")
        self.login_error_lbl.pack(pady=5)
        self.view_elements.append(self.login_error_lbl)

        login_btn = ctk.CTkButton(
            self.viewport_frame, text="GET STARTED", font=("Arial", 16, "bold"), 
            width=300, height=50, corner_radius=12, fg_color="#58CC02", hover_color="#58a700",
            command=self.handle_login
        )
        login_btn.pack(pady=10)
        self.view_elements.append(login_btn)

    def handle_login(self):
        username = self.username_entry.get().strip()
        
        if not username:
            self.login_error_lbl.configure(text="Username cannot be empty!")
            return
            
        if len(username) < 3:
            self.login_error_lbl.configure(text="Username must be at least 3 characters.")
            return

        # Authenticate / Load Profile
        self.user = User(username)
        
        # Build UI and route to Map
        self.initialize_top_bar()
        self.initialize_bottom_navigation()
        self.render_map_view()

    # ------------------------------------------------------------------------
    # MAP VIEW
    # ------------------------------------------------------------------------

    def render_map_view(self):
        self.user.check_and_recover_hearts()
        self.clear_viewport()
        self.refresh_header_stats()
        
        title_lbl = ctk.CTkLabel(self.viewport_frame, text="Math Path", font=("Arial", 24, "bold"), text_color="#1F2937")
        title_lbl.pack(pady=(25, 10))
        self.view_elements.append(title_lbl)
        
        for unit_idx, unit_info in enumerate(UNITS_CONFIGURATION):
            unit_card = ctk.CTkFrame(self.viewport_frame, fg_color="#3B82F6", width=380, height=85, corner_radius=16)
            unit_card.pack(pady=(20, 12))
            unit_card.pack_propagate(False)
            self.view_elements.append(unit_card)
            
            ctk.CTkLabel(unit_card, text=f"UNIT {unit_idx + 1}", font=("Arial", 11, "bold"), text_color="#93C5FD").pack(anchor="w", padx=20, pady=(12, 0))
            clean_title = unit_info["title"].split(" - ")[1] if " - " in unit_info["title"] else unit_info["title"]
            ctk.CTkLabel(unit_card, text=clean_title, font=("Arial", 18, "bold"), text_color="#FFFFFF").pack(anchor="w", padx=20)
            
            for name in unit_info["topics"]:
                idx = ALL_TOPICS.index(name)
                is_unlocked = idx == 0 or ALL_TOPICS[idx-1] in self.user.completed_topics
                
                node_bg = "#22C55E" if is_unlocked else "#E5E7EB"
                hover_bg = "#16A34A" if is_unlocked else "#E5E7EB"
                symbol = "★" if is_unlocked else "🔒"
                text_color = "#1F2937" if is_unlocked else "#9CA3AF"
                
                node_btn = ctk.CTkButton(
                    self.viewport_frame, text=symbol, width=76, height=76, corner_radius=38,
                    font=("Arial", 26, "bold"), fg_color=node_bg, hover_color=hover_bg,
                    text_color="#FFFFFF" if is_unlocked else "#9CA3AF",
                    command=lambda t=name, unlocked=is_unlocked: self.start_lesson_loop(t) if unlocked else None
                )
                node_btn.pack(pady=12)
                self.view_elements.append(node_btn)
                
                lbl = ctk.CTkLabel(self.viewport_frame, text=name, font=("Arial", 14, "bold"), text_color=text_color)
                lbl.pack(pady=(0, 15))
                self.view_elements.append(lbl)
                
                if idx < len(ALL_TOPICS) - 1:
                    connector = ctk.CTkFrame(self.viewport_frame, width=8, height=25, fg_color="#E5E7EB", corner_radius=4)
                    connector.pack(pady=2)
                    self.view_elements.append(connector)

    # ------------------------------------------------------------------------
    # LESSON LOGIC
    # ------------------------------------------------------------------------

    def start_lesson_loop(self, topic_name):
        self.user.check_and_recover_hearts()
        if self.user.hearts <= 0:
            self.render_profile_view()
            return
        self.active_topic = topic_name
        self.progress_score = 0
        self.load_next_eval_question()

    def load_next_eval_question(self):
        self.clear_viewport()
        
        current_tier = 1 if self.active_topic not in self.user.completed_topics else 2
        self.active_question = self.engine.get_fixed_question(self.active_topic, current_tier, self.progress_score)
        
        prog_wrapper = ctk.CTkFrame(self.viewport_frame, fg_color="transparent")
        prog_wrapper.pack(fill="x", padx=30, pady=20)
        self.view_elements.append(prog_wrapper)
        
        exit_btn = ctk.CTkButton(prog_wrapper, text="✕", width=30, height=30, fg_color="transparent", text_color="#9CA3AF", font=("Arial", 18, "bold"), hover_color="#F3F4F6", command=self.render_map_view)
        exit_btn.pack(side="left")
        
        tracker = ctk.CTkProgressBar(prog_wrapper, width=320, height=14, fg_color="#E5E7EB", progress_color="#22C55E")
        tracker.pack(side="right", padx=10)
        tracker.set(self.progress_score / 100)
        
        lbl_title = ctk.CTkLabel(self.viewport_frame, text=f"{self.active_topic.upper()} • DIFFICULTY LEVEL {current_tier}", font=("Arial", 12, "bold"), text_color="#3B82F6")
        lbl_title.pack(pady=(15, 5))
        self.view_elements.append(lbl_title)
        
        prompt_box = ctk.CTkLabel(self.viewport_frame, text=self.active_question["question"], font=("Arial", 24, "bold"), text_color="#1F2937", justify="center")
        prompt_box.pack(pady=35)
        self.view_elements.append(prompt_box)
        
        self.option_buttons = []
        for choice in self.active_question["options"]:
            btn = ctk.CTkButton(
                self.viewport_frame, text=choice, font=("Arial", 18, "bold"),
                width=380, height=58, corner_radius=14, fg_color="#FFFFFF",
                text_color="#1F2937", border_width=2, border_color="#E5E7EB",
                hover_color="#F9FAFB", command=lambda c=choice: self.evaluate_user_selection(c)
            )
            btn.pack(pady=8)
            self.option_buttons.append(btn)
            self.view_elements.append(btn)
            
        self.feedback_banner = ctk.CTkLabel(self.viewport_frame, text="", font=("Arial", 16, "bold"))
        self.feedback_banner.pack(pady=20)
        self.view_elements.append(self.feedback_banner)

    def evaluate_user_selection(self, chosen_value):
        for btn in self.option_buttons:
            btn.configure(state="disabled")

        correct_str = str(self.active_question["answer"])
        is_correct = self.engine.check_answer(chosen_value, correct_str)
        
        self.user.log_attempt(self.active_topic, is_correct)
        
        if is_correct:
            self.progress_score += 25
            self.user.xp += 10
            self.feedback_banner.configure(text="Excellent! +10 XP earned.", text_color="#22C55E")
        else:
            if self.user.hearts == 5:
                self.user.last_heart_update = datetime.now().isoformat()
            self.user.hearts -= 1
            self.feedback_banner.configure(text=f"Incorrect. Correct value: {correct_str}", text_color="#EF4444")
            
        self.user.save_data()
        self.refresh_header_stats()
        self.after(1600, self.route_post_answer_logic)

    def route_post_answer_logic(self):
        if self.user.hearts <= 0:
            self.render_map_view()
        elif self.progress_score >= 100:
            self.user.completed_topics.add(self.active_topic)
            self.user.save_data()
            self.render_map_view()
        else:
            self.load_next_eval_question()

    # ------------------------------------------------------------------------
    # PROFILE VIEW
    # ------------------------------------------------------------------------

    def render_profile_view(self):
        self.user.check_and_recover_hearts()
        self.clear_viewport()
        self.refresh_header_stats()
        
        prof_lbl = ctk.CTkLabel(self.viewport_frame, text="Profile", font=("Arial", 24, "bold"), text_color="#1F2937")
        prof_lbl.pack(pady=20)
        self.view_elements.append(prof_lbl)
        
        card = ctk.CTkFrame(self.viewport_frame, fg_color="#FFFFFF", width=400, border_width=2, border_color="#E5E7EB", corner_radius=16)
        card.pack(pady=10, padx=20, fill="x")
        self.view_elements.append(card)
        
        self.add_profile_stat_row(card, "User Profile Identifier", self.user.username)
        self.add_profile_stat_row(card, "Accumulated Experience", f"{self.user.xp} XP")
        self.add_profile_stat_row(card, "Total Verification Accuracy", f"{self.user.get_accuracy()}%")
        self.add_profile_stat_row(card, "Unlocked Modules Count", f"{len(self.user.completed_topics)} / {len(ALL_TOPICS)}")

        history_title = ctk.CTkLabel(self.viewport_frame, text="Recent Activity Log", font=("Arial", 16, "bold"), text_color="#4B5563")
        history_title.pack(pady=(20, 5))
        self.view_elements.append(history_title)

        history_card = ctk.CTkFrame(self.viewport_frame, fg_color="#F3F4F6", width=400, corner_radius=12)
        history_card.pack(pady=5, padx=20, fill="x")
        self.view_elements.append(history_card)

        # Get the generator iterator
        history_iterator = self.user.generate_history_report()
        has_logs = False

        if history_iterator:
            for count, log_text in enumerate(history_iterator):
                if count >= 4:  # Display the 4 most recent entries
                    break
                has_logs = True
                log_lbl = ctk.CTkLabel(history_card, text=log_text, font=("Courier New", 12), text_color="#374151", anchor="w")
                log_lbl.pack(fill="x", padx=15, pady=6)
                self.view_elements.append(log_lbl)

        if not has_logs:
            no_log_lbl = ctk.CTkLabel(history_card, text="No recent activities recorded.", font=("Arial", 12, "italic"), text_color="#9CA3AF")
            no_log_lbl.pack(pady=15)
            self.view_elements.append(no_log_lbl)

    def add_profile_stat_row(self, parent, metrics_title, metrics_value):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=12)
        ctk.CTkLabel(row, text=metrics_title, font=("Arial", 14), text_color="#6B7280").pack(side="left")
        ctk.CTkLabel(row, text=metrics_value, font=("Arial", 14, "bold"), text_color="#1F2937").pack(side="right")


if __name__ == "__main__":
    app = MathLingoApp()
    app.mainloop()