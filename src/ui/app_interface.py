import time
from ai.openai_client import OpenAIClient

class AppInterface:
    def __init__(self, alarm_manager, goal_handler):
        self.alarm_manager = alarm_manager
        self.goal_handler = goal_handler
        self.running = True
        # Register the alarm callback
        self.alarm_manager.register_alarm_callback(self.handle_alarm)
        # Flag to determine if we're in the alarm flow
        self.handling_alarm = False
    
    def display_prompt(self, message):
        print(message)
        user_input = input("Your input: ")
        return user_input

    def display_tasks(self, tasks):
        print("Here are your tasks for the day:")
        for task in tasks:
            print(f"- {task}")

    def display_menu(self):
        """Display the main menu options"""
        print("\n===== Mental Health App =====")
        print("1. Set an alarm")
        print("2. View all alarms")
        print("3. Remove an alarm")
        print("4. View goal history")
        print("5. View today's tasks")
        print("6. Update task completion")
        print("7. Trigger alarm now")
        print("8. Exit")
        print("============================")
    
    def run(self):
        """Run the main application loop"""
        print("Welcome to Mental Health App!")
        print("This app helps you set daily goals and break them into manageable tasks.")
        
        while self.running:
            if not self.handling_alarm:
                self.display_menu()
                choice = input("Enter your choice (1-8): ")  # Updated prompt
                
                if choice == "1":
                    self.set_alarm()
                elif choice == "2":
                    self.view_alarms()
                elif choice == "3":
                    self.remove_alarm()
                elif choice == "4":
                    self.view_goal_history()
                elif choice == "5":
                    self.view_todays_tasks()
                elif choice == "6":
                    self.update_task_completion()
                elif choice == "7":
                    self.trigger_alarm_manually()  
                elif choice == "8":  
                    self.exit_app()
                else:
                    print("Invalid choice. Please try again.")
            else:
                # We're in the alarm handling flow, do nothing and wait for it to complete
                time.sleep(0.1)
    
    def view_todays_tasks(self):
        """View today's tasks and their completion status"""
        today_goal_tasks = self.goal_handler.get_todays_goals_and_tasks()
        
        if not today_goal_tasks:
            print("\nNo tasks set for today yet. Use 'Trigger alarm now' to set today's goals and tasks.")
            return
            
        goal, tasks_data = today_goal_tasks
        
        print(f"\n=== Today's Goal ===")
        print(f"Goal: {goal}")
        print(f"\n=== Today's Tasks ===")
        
        # Display tasks with their completion status
        if isinstance(tasks_data, list):
            for i, task_info in enumerate(tasks_data, 1):
                status = "✓" if task_info.get("completed", False) else "□"
                task = task_info.get("task", "")
                print(f"{i}. [{status}] {task}")
        else:
            # If tasks_data is not a list, display the raw text
            print(tasks_data)
    
    def update_task_completion(self):
        """Update completion status of today's tasks"""
        today_goal_tasks = self.goal_handler.get_todays_goals_and_tasks()
        
        if not today_goal_tasks:
            print("\nNo tasks set for today yet. Use 'Trigger alarm now' to set today's goals and tasks.")
            return
            
        goal, tasks_data = today_goal_tasks
        
        # Convert tasks to list format if it's not already
        task_list = []
        if not isinstance(tasks_data, list):
            # Parse tasks from text if needed
            lines = tasks_data.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or 
                            line.startswith('*') or 
                            (len(line) > 2 and line[0].isdigit() and line[1] in ['.', ')'])):
                    task_text = line.lstrip('- •*0123456789.) ')
                    task_list.append({"task": task_text, "completed": False})
            
            # Update the goal handler with the parsed task list
            if task_list:
                self.goal_handler.update_todays_tasks(task_list)
        else:
            task_list = tasks_data
        
        if not task_list:
            print("\nNo tasks available to update.")
            return
        
        # Display current tasks
        print("\n=== Update Task Completion ===")
        for i, task_info in enumerate(task_list, 1):
            status = "✓" if task_info.get("completed", False) else "□"
            task = task_info.get("task", "")
            print(f"{i}. [{status}] {task}")
        
        # Let user select task to toggle
        try:
            task_num = int(input("\nEnter task number to toggle completion (0 to cancel): "))
            if task_num == 0:
                return
            
            if 1 <= task_num <= len(task_list):
                # Toggle completion status
                task_list[task_num-1]["completed"] = not task_list[task_num-1].get("completed", False)
                
                # Update the goal handler with the modified task list
                self.goal_handler.update_todays_tasks(task_list)
                
                # Confirm the update
                status = "completed" if task_list[task_num-1].get("completed", False) else "not completed"
                print(f"\nTask {task_num} marked as {status}.")
            else:
                print("\nInvalid task number.")
        except ValueError:
            print("\nPlease enter a valid number.")
    
    def trigger_alarm_manually(self):
        """Manually trigger the alarm process"""
        print("\nManually triggering alarm...")
        self.handle_alarm()
    
    def handle_alarm(self):
        """Handle alarm event"""
        self.handling_alarm = True
        try:
            # Get goal from user
            goal = self.goal_handler.get_goal_from_user()
            if goal:
                print("\nGenerating tasks based on your goal...")
                # Generate improved prompt for more specific tasks
                prompt = (
                    f"Based on the goal: '{goal}', generate a list of 5-7 specific, measurable, "
                    f"achievable tasks for today. Make each task concrete and actionable so the user "
                    f"can check it off when completed. Format as a numbered list."
                )
                
                # Generate tasks based on the improved prompt
                tasks = self.alarm_manager.task_generator.generate_tasks(prompt)
                
                # Try to parse the tasks into a list if it's a string
                task_list = []
                if isinstance(tasks, str):
                    # Try to extract tasks from the OpenAI response
                    for line in tasks.split('\n'):
                        line = line.strip()
                        if line and (line.startswith('-') or line.startswith('•') or 
                                    line.startswith('*') or 
                                    (len(line) > 2 and line[0].isdigit() and line[1] in ['.', ')'])):
                            task_text = line.lstrip('- •*0123456789.) ')
                            task_list.append({"task": task_text, "completed": False})
                
                # Save the goal and tasks
                if task_list:
                    self.goal_handler.save_goal_and_structured_tasks(goal, task_list)
                else:
                    self.goal_handler.save_goal_and_tasks(goal, tasks)
                
                # Display the tasks in a user-friendly way
                print("\nYour tasks for today:")
                if task_list:
                    for i, task_info in enumerate(task_list, 1):
                        print(f"{i}. [{' '}] {task_info['task']}")
                else:
                    print(tasks)  # Print raw response if parsing failed
                
                print("\nYou can check off tasks as you complete them throughout the day.")
                input("\nPress Enter to continue...")  # Wait for user acknowledgment
        finally:
            self.handling_alarm = False
    
    def set_alarm(self):
        """Set a new alarm"""
        time_str = input("Enter alarm time (HH:MM format): ")
        if self.alarm_manager.add_alarm(time_str):
            print(f"Alarm set for {time_str}")
        else:
            print("Failed to set alarm. Please use HH:MM format.")
    
    def view_alarms(self):
        """View all set alarms"""
        if not self.alarm_manager.alarms:
            print("No alarms set.")
        else:
            print("\nCurrent alarms:")
            for i, alarm in enumerate(self.alarm_manager.alarms, 1):
                print(f"{i}. {alarm.strftime('%H:%M')}")
    
    def remove_alarm(self):
        """Remove an existing alarm"""
        self.view_alarms()
        if self.alarm_manager.alarms:
            time_str = input("Enter alarm time to remove (HH:MM format): ")
            if self.alarm_manager.remove_alarm(time_str):
                print(f"Alarm at {time_str} removed.")
            else:
                print(f"No alarm found at {time_str}.")
    
    def view_goal_history(self):
        """View history of goals and tasks"""
        goals = self.goal_handler.get_goals_history()
        if not goals:
            print("No goal history found.")
        else:
            print("\n=== Goal History ===")
            for entry in goals:
                print(f"\nDate: {entry['date']}")
                print(f"Goal: {entry['goal']}")
                print("Tasks:")
                
                # Handle both structured task lists and raw text
                tasks_data = entry.get('tasks', [])
                if isinstance(tasks_data, list):
                    for i, task_info in enumerate(tasks_data, 1):
                        if isinstance(task_info, dict):
                            status = "✓" if task_info.get("completed", False) else "□"
                            task = task_info.get("task", "")
                            print(f"{i}. [{status}] {task}")
                        else:
                            print(f"{i}. {task_info}")
                else:
                    print(tasks_data)
    
    def exit_app(self):
        """Exit the application"""
        self.running = False
        self.alarm_manager.stop()
        print("Thank you for using Mental Health App. Goodbye!")