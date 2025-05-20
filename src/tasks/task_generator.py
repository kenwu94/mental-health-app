class TaskGenerator:
    def __init__(self, openai_client):
        self.openai_client = openai_client

    def generate_tasks(self, goal):
        prompt = f"Based on the goal: '{goal}', generate a list of tasks for the day."
        tasks = self.openai_client.call_openai(prompt)
        return tasks