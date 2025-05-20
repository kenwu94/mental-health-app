import json
import os
import datetime

class GoalHandler:
    def __init__(self):
        self.data_file = os.path.join("data", "user_data.json")
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Make sure the data directory and file exist"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump({"goals": []}, f)
    
    def get_goal_from_user(self):
        """Prompt the user to set their goal for the day"""
        print("\n🔔 Alarm triggered! Time to set your goal for today.")
        goal = input("What's your main goal for today? ")
        return goal.strip() if goal.strip() else None
    
    def save_goal_and_tasks(self, goal, tasks):
        """Save the goal and associated tasks"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Remove any existing entry for today before adding new one
            data["goals"] = [g for g in data["goals"] if g.get("date") != today]
            
            data["goals"].append({
                "date": today,
                "goal": goal,
                "tasks": tasks
            })
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
            
            print(f"Goal and tasks saved for {today}")
            return True
        except Exception as e:
            print(f"Error saving goal and tasks: {e}")
            return False
    
    def save_goal_and_structured_tasks(self, goal, task_list):
        """Save the goal and associated structured tasks with completion status"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Remove any existing entry for today before adding new one
            data["goals"] = [g for g in data["goals"] if g.get("date") != today]
            
            data["goals"].append({
                "date": today,
                "goal": goal,
                "tasks": task_list
            })
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
            
            print(f"Goal and structured tasks saved for {today}")
            return True
        except Exception as e:
            print(f"Error saving goal and structured tasks: {e}")
            return False
    
    def get_todays_goals_and_tasks(self):
        """Get today's goal and tasks"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            for entry in data["goals"]:
                if entry.get("date") == today:
                    return entry.get("goal", ""), entry.get("tasks", [])
            
            return None
        except Exception as e:
            print(f"Error getting today's goals and tasks: {e}")
            return None
    
    def update_todays_tasks(self, task_list):
        """Update today's tasks with new completion statuses"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            
            for entry in data["goals"]:
                if entry.get("date") == today:
                    entry["tasks"] = task_list
                    break
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
            
            return True
        except Exception as e:
            print(f"Error updating task completion: {e}")
            return False
    
    def get_goals_history(self):
        """Get the history of goals and tasks"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
            return data["goals"]
        except Exception:
            return []