# Mental Health Goal Tracker - POC

A simple web application that helps users set daily goals and track their progress through specific, actionable tasks.

## Features

- Set daily goals
- Generate specific, actionable tasks based on your goal using AI
- Check off tasks as you complete them
- View your goal history

## Setup and Installation

1. Clone this repository
2. Install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```

## Usage

1. Go to the "Set New Goal" tab to create a goal for today
2. The app will generate tasks for you based on your goal
3. Check off tasks as you complete them throughout the day
4. View your past goals and tasks in the "History" tab

## Technologies Used

- Python
- Streamlit
- OpenAI API

## Project Structure
```
mental-health-app
├── src
│   ├── main.py                # Entry point of the application
│   ├── alarm
│   │   ├── __init__.py
│   │   └── alarm_manager.py    # Manages alarm functionalities
│   ├── goals
│   │   ├── __init__.py
│   │   └── goal_handler.py     # Handles user goals
│   ├── tasks
│   │   ├── __init__.py
│   │   └── task_generator.py    # Generates tasks based on goals
│   ├── ai
│   │   ├── __init__.py
│   │   └── openai_client.py     # Interacts with OpenAI API
│   └── ui
│       ├── __init__.py
│       └── app_interface.py     # Manages user interface interactions
├── data
│   └── user_data.json          # Stores user data in JSON format
├── requirements.txt             # Lists project dependencies
├── config.py                    # Contains configuration settings
└── README.md                    # Documentation for the project
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.