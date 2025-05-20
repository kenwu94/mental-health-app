import streamlit as st
import os
import json
import datetime
import time
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY", "")

# Check if API key is available
if not openai.api_key:
    st.error("OpenAI API key not found. Please set it in your .env file.")
    st.stop()

# Initialize session state for app data
if "alarms" not in st.session_state:
    st.session_state.alarms = []
if "current_tasks" not in st.session_state:
    st.session_state.current_tasks = []
if "goal" not in st.session_state:
    st.session_state.goal = ""
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# File paths
DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "user_data.json")

# Utility functions
def ensure_data_file_exists():
    """Make sure the data directory and file exist"""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as f:
            json.dump({"goals": []}, f)

def load_data():
    """Load data from file with proper error handling"""
    ensure_data_file_exists()
    try:
        with open(USER_DATA_FILE, 'r') as f:
            data = json.load(f)
            # Ensure the data has the expected structure
            if "goals" not in data:
                data["goals"] = []
            return data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return {"goals": []}

def save_data(data):
    """Save data to file"""
    ensure_data_file_exists()
    try:
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False

def save_goal_and_tasks(goal, tasks):
    """Save the goal and tasks for today"""
    data = load_data()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Remove any existing entry for today
    data["goals"] = [g for g in data["goals"] if g.get("date") != today]
    
    data["goals"].append({
        "date": today,
        "goal": goal,
        "tasks": tasks
    })
    
    return save_data(data)

def get_todays_goals_and_tasks():
    """Get today's goal and tasks with proper error handling"""
    data = load_data()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Check if data has the expected structure
    if "goals" not in data:
        return None, []
    
    for entry in data["goals"]:
        if entry.get("date") == today:
            return entry.get("goal", ""), entry.get("tasks", [])
    
    return None, []

def update_task_completion(task_index, completed):
    """Update completion status of a task"""
    data = load_data()
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if "goals" not in data:
        return False
    
    for entry in data["goals"]:
        if entry.get("date") == today:
            tasks = entry.get("tasks", [])
            if isinstance(tasks, list) and 0 <= task_index < len(tasks):
                tasks[task_index]["completed"] = completed
                entry["tasks"] = tasks
                return save_data(data)
    
    return False

def generate_tasks(goal):
    """Generate tasks using OpenAI based on the goal"""
    if not goal:
        return []
    
    prompt = (
        f"Based on the goal: '{goal}', generate a list of 5-7 specific, measurable, "
        f"achievable tasks for today. Make each task concrete and actionable so the user "
        f"can check it off when completed. Return ONLY a JSON array where each element is a "
        f"dictionary with 'task' and 'completed' keys. The 'completed' value should always be false."
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful task planning assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        
        # Extract JSON content if it's wrapped in backticks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].strip()
        
        # Parse JSON
        try:
            tasks = json.loads(content)
            return tasks
        except json.JSONDecodeError:
            # Fall back to text parsing
            tasks = []
            for line in content.split('\n'):
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or 
                            line.startswith('*') or 
                            (len(line) > 2 and line[0].isdigit() and line[1] in ['.', ')'])):
                    task_text = line.lstrip('- •*0123456789.) ')
                    tasks.append({"task": task_text, "completed": False})
            return tasks
            
    except Exception as e:
        st.error(f"Error generating tasks: {str(e)}")
        return []

def load_today_data():
    """Load today's goal and tasks into session state"""
    try:
        goal, tasks = get_todays_goals_and_tasks()
        if goal:
            st.session_state.goal = goal
            st.session_state.current_tasks = tasks
            return True
        return False
    except Exception as e:
        st.error(f"Error loading today's data: {str(e)}")
        return False

# Initialize the app
ensure_data_file_exists()

# App UI
st.title("Mental Health Goal Tracker")
st.subheader("Set daily goals and track your progress")

# Check if data should be loaded (only the first time)
if not st.session_state.data_loaded:
    load_today_data()
    st.session_state.data_loaded = True

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["Today's Goals & Tasks", "Set New Goal", "History"])

# Tab 1: Today's Goals & Tasks
with tab1:
    if st.session_state.goal:
        st.markdown(f"## Today's Goal\n**{st.session_state.goal}**")
        
        st.markdown("## Tasks")
        if st.session_state.current_tasks:
            for i, task in enumerate(st.session_state.current_tasks):
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    st.markdown(f"{task['task']}")
                with col2:
                    # Create a unique key for each checkbox
                    checkbox_key = f"task_{i}"
                    # Only update the value if the checkbox changes
                    if checkbox_key not in st.session_state:
                        st.session_state[checkbox_key] = task.get('completed', False)
                    
                    if st.checkbox("", key=checkbox_key, value=task.get('completed', False)):
                        if not task.get('completed', False):
                            task['completed'] = True
                            update_task_completion(i, True)
                    else:
                        if task.get('completed', False):
                            task['completed'] = False
                            update_task_completion(i, False)
        else:
            st.info("No tasks for today. Set a new goal to generate tasks.")
    else:
        st.info("No goal set for today. Go to 'Set New Goal' tab to create one.")

# Tab 2: Set New Goal
with tab2:
    st.markdown("## Set a New Goal for Today")
    
    new_goal = st.text_input("What's your main goal for today?")
    
    if st.button("Generate Tasks"):
        if new_goal:
            with st.spinner("Generating tasks..."):
                tasks = generate_tasks(new_goal)
                
                if tasks:
                    st.session_state.goal = new_goal
                    st.session_state.current_tasks = tasks
                    if save_goal_and_tasks(new_goal, tasks):
                        st.success("Goal and tasks created successfully!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to save goal and tasks. Please try again.")
                else:
                    st.error("Failed to generate tasks. Please try again.")
        else:
            st.warning("Please enter a goal first.")

# Tab 3: History
with tab3:
    st.markdown("## Goal History")
    
    data = load_data()
    if data and "goals" in data and data["goals"]:
        for entry in reversed(data["goals"]):
            date = entry.get("date", "")
            goal = entry.get("goal", "")
            tasks = entry.get("tasks", [])
            
            st.markdown(f"### {date}")
            st.markdown(f"**Goal:** {goal}")
            
            if tasks:
                st.markdown("**Tasks:**")
                if isinstance(tasks, list):
                    for task in tasks:
                        if isinstance(task, dict):
                            status = "✅" if task.get("completed", False) else "⬜"
                            st.markdown(f"{status} {task.get('task', '')}")
                        else:
                            st.markdown(f"- {task}")
                else:
                    st.markdown(tasks)
            
            st.markdown("---")
    else:
        st.info("No history available yet.")

# Footer
st.markdown("---")
st.markdown("### Mental Health Goal Tracker - POC")