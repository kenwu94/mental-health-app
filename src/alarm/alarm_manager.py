import time
import threading
import datetime

class AlarmManager:
    def __init__(self, goal_handler, task_generator):
        self.alarms = []
        self.running = True
        self.goal_handler = goal_handler
        self.task_generator = task_generator
        self.alarm_thread = threading.Thread(target=self._alarm_loop)
        self.alarm_thread.daemon = True
        self.alarm_thread.start()
        # Add a callback that UI can register to handle alarm events
        self.alarm_callback = None
    
    def add_alarm(self, time_str):
        """Add a new alarm with the specified time (HH:MM format)"""
        try:
            alarm_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            self.alarms.append(alarm_time)
            self.alarms.sort()
            return True
        except ValueError:
            print("Invalid time format. Please use HH:MM format.")
            return False
    
    def remove_alarm(self, time_str):
        """Remove an alarm with the specified time"""
        try:
            alarm_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            if alarm_time in self.alarms:
                self.alarms.remove(alarm_time)
                return True
            return False
        except ValueError:
            return False
    
    def register_alarm_callback(self, callback):
        """Register a callback function to be called when an alarm triggers"""
        self.alarm_callback = callback
    
    def _alarm_loop(self):
        """Background thread to check for alarms"""
        while self.running:
            now = datetime.datetime.now().time()
            current_time = datetime.time(now.hour, now.minute)
            
            for alarm_time in self.alarms:
                if alarm_time.hour == current_time.hour and alarm_time.minute == current_time.minute:
                    self._trigger_alarm()
            
            # Sleep until the next minute
            time.sleep(60 - datetime.datetime.now().second)
    
    def _trigger_alarm(self):
        """Trigger the alarm process - get goal and generate tasks"""
        if self.alarm_callback:
            # Use the callback to handle the alarm in the UI
            self.alarm_callback()
        else:
            # Fallback behavior if no callback is registered
            self.handle_alarm_now()
    
    def handle_alarm_now(self):
        """Directly handle the alarm (when triggered outside the UI flow)"""
        goal = self.goal_handler.get_goal_from_user()
        if goal:
            print("\nGenerating tasks based on your goal...")
            tasks = self.task_generator.generate_tasks(goal)
            self.goal_handler.save_goal_and_tasks(goal, tasks)
            print("\nYour tasks for today:")
            print(tasks)
            input("\nPress Enter to continue...")  # Pause to let the user read the tasks
    
    def stop(self):
        self.running = False