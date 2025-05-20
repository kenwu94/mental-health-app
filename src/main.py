import sys
import os

# Add the parent directory to path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alarm.alarm_manager import AlarmManager
from goals.goal_handler import GoalHandler
from tasks.task_generator import TaskGenerator
from ai.openai_client import OpenAIClient
from ui.app_interface import AppInterface
import config

def main():
    # Initialize OpenAI client
    openai_client = OpenAIClient(api_key=config.OPENAI_API_KEY)
    
    # Initialize components
    task_generator = TaskGenerator(openai_client)
    goal_handler = GoalHandler()
    alarm_manager = AlarmManager(goal_handler, task_generator)
    
    # Initialize UI
    app = AppInterface(alarm_manager, goal_handler)
    app.run()

if __name__ == "__main__":
    main()