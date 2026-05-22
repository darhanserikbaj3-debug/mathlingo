import json
import csv
import os
from datetime import datetime, timedelta

# Global file paths
USER_FILE = os.path.join('data', 'users.json')
LOG_FILE = os.path.join('data', 'progress_log.csv')

class User:
    def __init__(self, username=None):
        self.username = username
        self.xp = 0
        self.hearts = 5
        self.last_heart_update = datetime.now().isoformat()
        self.completed_topics = set()
        
        if not os.path.exists('data'):
            os.makedirs('data')
            
        self.load_data()
        self.check_and_recover_hearts()

    def load_data(self):
        """Loads specific user data from a multi-user JSON file."""
        if os.path.exists(USER_FILE):
            try:
                with open(USER_FILE, 'r', encoding='utf-8') as f:
                    all_users = json.load(f)
                    if self.username in all_users:
                        # Load existing user
                        data = all_users[self.username]
                        self.xp = data.get("xp", 0)
                        self.hearts = data.get("hearts", 5)
                        self.completed_topics = set(data.get("completed_topics", []))
                        self.last_heart_update = data.get("last_heart_update", self.last_heart_update)
                        return
            except json.JSONDecodeError:
                pass 
        
        self.save_data()

    def save_data(self):
        """Saves current user data without overwriting other users."""
        all_users = {}
        if os.path.exists(USER_FILE):
            try:
                with open(USER_FILE, "r", encoding='utf-8') as f:
                    all_users = json.load(f)
            except json.JSONDecodeError:
                pass
        
        all_users[self.username] = {
            "username": self.username,
            "xp": self.xp,
            "hearts": self.hearts,
            "completed_topics": list(self.completed_topics),
            "last_heart_update": self.last_heart_update
        }
        
        with open(USER_FILE, "w", encoding='utf-8') as f:
            json.dump(all_users, f, indent=4)

    def check_and_recover_hearts(self):
        """Calculates 15-minute regeneration increments to restore missing hearts."""
        if self.hearts >= 5:
            self.last_heart_update = datetime.now().isoformat()
            return

        try:
            last_time = datetime.fromisoformat(self.last_heart_update)
            now = datetime.now()
            elapsed_seconds = (now - last_time).total_seconds()
            intervals_earned = int(elapsed_seconds // 900)  
            
            if intervals_earned > 0:
                self.hearts = min(5, self.hearts + intervals_earned)
                if self.hearts == 5:
                    self.last_heart_update = now.isoformat()
                else:
                    self.last_heart_update = (last_time + timedelta(seconds=intervals_earned * 900)).isoformat()
                self.save_data()
        except Exception:
            self.last_heart_update = datetime.now().isoformat()
            self.save_data()

    def log_attempt(self, topic, success):
        """Logs attempt to CSV."""
        file_exists = os.path.isfile(LOG_FILE)
        with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['timestamp', 'username', 'topic', 'success'])
            writer.writerow([datetime.now().isoformat(), self.username, topic, success])

    def get_accuracy(self):
        """Calculates accuracy using functional programming concepts."""
        if not os.path.exists(LOG_FILE):
            return 0
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                attempts = list(filter(lambda row: row['username'] == self.username, reader))
                
            if not attempts:
                return 0
                
            correct_count = len(list(filter(lambda r: r['success'] == 'True', attempts)))
            return round((correct_count / len(attempts)) * 100)
        except Exception:
            return 0
        
    def generate_history_report(self):
        """A Generator that yields cleanly mapped string records of user logs."""
        if not os.path.exists(LOG_FILE):
            return
        
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Filter logs for current user
            user_attempts = filter(lambda row: row['username'] == self.username, reader)
            # Map raw rows into clean presentation strings
            formatted_logs = map(lambda r: f"[{r['timestamp'][:10]}] {r['topic']}: {'✓' if r['success'] == 'True' else '✗'}", user_attempts)
            
            for log_entry in reversed(list(formatted_logs)):
                yield log_entry