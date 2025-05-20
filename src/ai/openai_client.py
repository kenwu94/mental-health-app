import openai

class OpenAIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def call_openai(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use the appropriate model
                messages=[
                    {"role": "system", "content": "You are a helpful task planning assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return "Failed to generate tasks. Please try again."