import streamlit as st
import json
import time
import datetime
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from adaptive_agent import AdaptiveAgent, TaskContext, PerformanceData, SessionRecommendation

# Page configuration
st.set_page_config(
    page_title="Focus Flow Agent",
    page_icon="⏰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern chatbot interface
st.markdown("""
<style>
    /* Modern Chatbot Interface */
    .main-header {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        letter-spacing: -0.5px;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    .chat-message {
        margin: 1rem 0;
        padding: 1.5rem;
        border-radius: 16px;
        animation: fadeIn 0.5s ease-in;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
        margin-right: 20%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        margin-left: 20%;
        text-align: right;
    }
    
    .timer-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
    
    .timer-circle {
        width: 300px;
        height: 300px;
        border-radius: 50%;
        border: 8px solid #e0e0e0;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        background: conic-gradient(#3498db 0deg, #3498db var(--progress), #e0e0e0 var(--progress));
        box-shadow: 0 8px 32px rgba(52, 152, 219, 0.2);
    }
    
    .timer-display {
        font-size: 3rem;
        font-weight: bold;
        color: #2c3e50;
        z-index: 1;
    }
    
    .session-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        border: 1px solid #f0f0f0;
    }
    
    .reflection-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    }
    
    .emoji-slider {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1rem 0;
    }
    
    .emoji-option {
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        text-align: center;
    }
    
    .emoji-option:hover {
        background: #f8f9fa;
        transform: scale(1.1);
    }
    
    .emoji-option.selected {
        background: #3498db;
        color: white;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .progress-ring {
        width: 300px;
        height: 300px;
        margin: 0 auto;
    }
    
    .motivational-quote {
        text-align: center;
        font-style: italic;
        color: #7f8c8d;
        margin: 1rem 0;
        font-size: 1.1rem;
    }

    /* New styles for dashboard */
    .nav-tabs {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
        border-bottom: 1px solid #e0e0e0;
    }

    .nav-tab {
        padding: 0.75rem 1.5rem;
        cursor: pointer;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
        font-weight: 600;
        color: #7f8c8d;
    }

    .nav-tab.active {
        border-bottom-color: #3498db;
        color: #3498db;
    }

    .section-header {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }

    .metric-card {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }

    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3498db;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #95a5a6;
    }

    .time-range {
        display: flex;
        justify-content: center;
        margin-bottom: 1.5rem;
    }

    .time-btn {
        padding: 0.5rem 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        background-color: #f8f9fa;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 0 0.5rem;
        font-weight: 600;
        color: #7f8c8d;
    }

    .time-btn:hover {
        background-color: #e9ecef;
        border-color: #d0d0d0;
    }

    .time-btn.active {
        background-color: #3498db;
        color: white;
        border-color: #3498db;
    }

    .graph-container {
        background: #f8f9fa;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'task_context' not in st.session_state:
    st.session_state.task_context = {}
if 'session_recommendation' not in st.session_state:
    st.session_state.session_recommendation = None
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'timer_start_time' not in st.session_state:
    st.session_state.timer_start_time = None
if 'session_duration' not in st.session_state:
    st.session_state.session_duration = 25
if 'reflection_mode' not in st.session_state:
    st.session_state.reflection_mode = False
if 'adaptive_agent' not in st.session_state:
    st.session_state.adaptive_agent = AdaptiveAgent()

def load_session_log():
    """Load existing session data from JSON file"""
    log_file = Path("session_log.json")
    if log_file.exists():
        with open(log_file, 'r') as f:
            return json.load(f)
    return {}

def save_session_log(data):
    """Save session data to JSON file"""
    with open("session_log.json", 'w') as f:
        json.dump(data, f, indent=2, default=str)

def format_time(seconds):
    """Format seconds into MM:SS"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def add_bot_message(message):
    """Add a bot message to chat history"""
    st.session_state.chat_history.append({"role": "bot", "message": message})

def add_user_message(message):
    """Add a user message to chat history"""
    st.session_state.chat_history.append({"role": "user", "message": message})

def show_chat_history():
    """Display the chat history"""
    for msg in st.session_state.chat_history:
        if msg["role"] == "bot":
            st.markdown(f"""
            <div class="chat-message bot-message">
                🤖 {msg["message"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message user-message">
                👤 {msg["message"]}
            </div>
            """, unsafe_allow_html=True)

def get_motivational_quote():
    """Get a random motivational quote"""
    quotes = [
        "Focus on progress, not perfection.",
        "The only way to do great work is to love what you do.",
        "Small steps, big impact.",
        "You are capable of amazing things.",
        "Every minute spent planning saves five in execution.",
        "The future depends on what you do today.",
        "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "Your focus determines your reality."
    ]
    import random
    return random.choice(quotes)

def chatbot_interface():
    """Main chatbot interface"""
    st.markdown('<p style="text-align: center; color: #7f8c8d; margin-bottom: 2rem;">Your AI-powered productivity coach</p>', unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Show chat history
    show_chat_history()
    
    # Initialize chatbot if first time
    if not st.session_state.chat_history:
        add_bot_message("Hey there! I'm your Focus Flow Agent. I'm here to help you stay productive and focused.")
        add_bot_message("What are you working on today?")
    
    # Chatbot logic based on current question
    if st.session_state.current_question == 0:
        # Question 1: What are you working on?
        if not st.session_state.chat_history or st.session_state.chat_history[-1]["role"] == "bot":
            task = st.text_input("What are you working on today?", key="task_input")
            if st.button("Continue", key="task_continue"):
                if task.strip():
                    add_user_message(task)
                    st.session_state.task_context['task'] = task
                    st.session_state.current_question = 1
                    add_bot_message("Great! Now, how difficult or intense is this task?")
                    st.rerun()
                else:
                    st.error("Please tell me what you're working on!")
    
    elif st.session_state.current_question == 1:
        # Question 2: Task difficulty
        if st.session_state.chat_history[-1]["role"] == "bot":
            st.markdown("**Select the difficulty level:**")
            difficulty_options = {
                1: "Easy - Simple, routine tasks",
                2: "Moderate - Standard work",
                3: "Challenging - Requires concentration", 
                4: "Complex - Multi-step, detailed work",
                5: "Intense - Very demanding, high-stakes"
            }
            
            difficulty = st.selectbox(
                "How difficult is this task?",
                options=list(difficulty_options.keys()),
                format_func=lambda x: difficulty_options[x],
                key="difficulty_select"
            )
            
            if st.button("Continue", key="difficulty_continue"):
                add_user_message(difficulty_options[difficulty])
                st.session_state.task_context['difficulty'] = difficulty
                st.session_state.current_question = 2
                add_bot_message("Perfect! Now, how focused do you feel right now?")
                st.rerun()
    
    elif st.session_state.current_question == 2:
        # Question 3: Focus level
        if st.session_state.chat_history[-1]["role"] == "bot":
            st.markdown("**Select your current focus level:**")
            focus_options = {
                1: "Distracted - Hard to concentrate",
                2: "Tired - Low energy, sleepy",
                3: "Neutral - Normal focus level",
                4: "Focused - Good concentration",
                5: "Laser Focus - Highly energized and alert"
            }
            
            focus = st.selectbox(
                "How focused do you feel?",
                options=list(focus_options.keys()),
                format_func=lambda x: focus_options[x],
                key="focus_select"
            )
            
            if st.button("Start Session", key="focus_continue"):
                add_user_message(focus_options[focus])
                st.session_state.task_context['focus'] = focus
                generate_recommendation()
                # Automatically start the timer
                st.session_state.timer_running = True
                st.session_state.timer_start_time = datetime.now()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def generate_recommendation():
    """Generate session recommendation based on task context"""
    context = st.session_state.task_context
    
    # Extract values safely
    task = context.get('task', 'Unknown task')
    difficulty = context.get('difficulty', 3)
    focus = context.get('focus', 3)
    
    # Create TaskContext for adaptive agent
    task_context = TaskContext(
        task_name=task,
        difficulty=difficulty,
        energy_level=focus,
        task_type="general"
    )
    
    # Get recommendation from adaptive agent
    recommendation = st.session_state.adaptive_agent.analyze_task_and_plan_session(task_context)
    st.session_state.session_recommendation = recommendation
    st.session_state.session_duration = recommendation.focus_duration
    
    # Add recommendation to chat
    add_bot_message(f"Got it! Let's do {recommendation.focus_duration} minutes of focus, followed by a {recommendation.break_duration}-minute break.")
    add_bot_message(f"Reasoning: {recommendation.reasoning}")
    add_bot_message("Starting your focus session now...")

def timer_interface():
    """Timer interface during focus session"""
    st.markdown('<h1 class="main-header">Focus Session</h1>', unsafe_allow_html=True)
    
    # Get session info
    task = st.session_state.task_context.get('task', 'Focus Session')
    duration = st.session_state.session_duration
    
    # Calculate remaining time
    elapsed = (datetime.now() - st.session_state.timer_start_time).total_seconds()
    remaining = max(0, duration * 60 - elapsed)
    progress = 1 - (remaining / (duration * 60))
    
    # Display task
    st.markdown(f"""
    <div class="session-card">
        <h2 style="text-align: center; color: #2c3e50; margin-bottom: 1rem;">{task}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if remaining > 0:
        # Timer display
        st.markdown(f"""
        <div class="timer-container">
            <div class="timer-circle" style="--progress: {progress * 360}deg">
                <div class="timer-display">{format_time(int(remaining))}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Motivational quote
        st.markdown(f"""
        <div class="motivational-quote">
            "{get_motivational_quote()}"
        </div>
        """, unsafe_allow_html=True)
        
        # Timer controls
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Pause", key="pause_timer"):
                st.session_state.timer_paused = True
                st.session_state.pause_start_time = datetime.now()
                st.rerun()
        with col2:
            if st.button("End Early", key="end_early"):
                st.session_state.timer_running = False
                st.session_state.reflection_mode = True
                st.rerun()
        with col3:
            if st.button("Skip to End", key="skip_timer"):
                st.session_state.timer_running = False
                st.session_state.reflection_mode = True
                st.rerun()
        
        # Auto-refresh timer
        time.sleep(1)
        st.rerun()
    else:
        # Session complete
        st.markdown("""
        <div class="timer-container">
            <div class="timer-circle" style="--progress: 360deg">
                <div class="timer-display">Complete!</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("Great job! Session completed!")
        st.session_state.timer_running = False
        st.session_state.reflection_mode = True
        st.rerun()

def reflection_interface():
    """Post-session reflection interface"""
    st.markdown('<h1 class="main-header">Session Review</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="reflection-card">
        <h3>How did that go?</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Reflection questions
    with st.container():
        completed = st.radio(
            "Did you complete your goal?",
            ["Yes", "Partially", "No"]
        )
        
        focus_rating = st.slider("How focused were you?", 1, 5, 3, help="1=Very distracted, 5=Highly focused")
        
        energy_after = st.slider("How do you feel now?", 1, 5, 3, help="1=Exhausted, 5=Still energized")
        
        distractions = st.text_area(
            "What distracted you? (optional)",
            placeholder="e.g., Phone notifications, Email, Social media, None..."
        )
        
        what_worked = st.text_area(
            "What worked well? (optional)",
            placeholder="e.g., Quiet environment, Clear goal, Good energy..."
        )
    
    # Submit reflection for AI evaluation and auto-start next session
    if st.button("Submit & Start Next Session", type="primary"):
        # Always create performance data for evaluation
        performance = PerformanceData(
            task_completed=completed == "Yes",
            focus_rating=focus_rating,
            energy_after=energy_after,
            distractions=distractions.split(', ') if distractions else [],
            what_worked=what_worked,
            session_duration=st.session_state.session_duration
        )
        
        # Create task context for evaluation
        task_context = TaskContext(
            task_name=st.session_state.task_context.get('task', 'Focus Session'),
            difficulty=st.session_state.task_context.get('difficulty', 3),
            energy_level=st.session_state.task_context.get('focus', 3)
        )
        
        # Get AI adaptation in background
        adaptation = st.session_state.adaptive_agent.adapt_after_session(performance, task_context)
        
        # Update session parameters based on AI recommendation
        st.session_state.session_duration = adaptation['next_session_duration']
        
        # Reset for next session but keep the adapted parameters
        st.session_state.chat_history = []
        st.session_state.current_question = 0
        st.session_state.task_context = {}
        st.session_state.reflection_mode = False
        
        # Automatically start the next timer with AI-determined parameters
        st.session_state.timer_running = True
        st.session_state.timer_start_time = datetime.now()
        st.rerun()
    
    # Alternative options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Skip & Start New Session", key="skip_reflection"):
            # Reset for next session without AI evaluation
            st.session_state.chat_history = []
            st.session_state.current_question = 0
            st.session_state.task_context = {}
            st.session_state.session_recommendation = None
            st.session_state.reflection_mode = False
            st.rerun()
    
    with col2:
        if st.button("View Dashboard", key="view_dashboard_skip"):
            st.session_state.show_dashboard = True
            st.rerun()

def dashboard_interface():
    """Dashboard showing session history and stats"""
    st.markdown('<h1 class="main-header">Your Progress</h1>', unsafe_allow_html=True)
    
    # Navigation tabs
    st.markdown("""
    <div class="nav-tabs">
        <div class="nav-tab active">📊 Summary</div>
        <div class="nav-tab">📋 Detail</div>
        <div class="nav-tab">🏆 Ranking</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Activity Summary Section
    st.markdown('<div class="section-header">📈 Activity Summary</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #7f8c8d; font-size: 0.9rem;">* This report will be available when you are logged in</p>', unsafe_allow_html=True)
    
    # Modern metric cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⏰</div>
            <div class="metric-value">--</div>
            <div class="metric-label">Hours Focused</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📅</div>
            <div class="metric-value">--</div>
            <div class="metric-label">Days Accessed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">🔥</div>
            <div class="metric-value">--</div>
            <div class="metric-label">Day Streak</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Focus Hours Section
    st.markdown('<div class="section-header">⏱️ Focus Hours</div>', unsafe_allow_html=True)
    
    # Time range selector
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown("""
        <div class="time-range">
            <button class="time-btn active">Week</button>
            <button class="time-btn">Month</button>
            <button class="time-btn">Year 🔒</button>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="text-align: center; color: #7f8c8d;">← This Week →</div>', unsafe_allow_html=True)
    
    # Graph container
    st.markdown("""
    <div class="graph-container">
        <div style="text-align: center; padding: 2rem;">
            <h4 style="color: #7f8c8d; margin-bottom: 0.5rem;">Focus Hours This Week</h4>
            <p style="color: #95a5a6; font-size: 0.9rem;">* This report will be available when you are logged in</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load session data for actual stats
    all_sessions = load_session_log()
    
    if all_sessions:
        # Calculate actual stats
        total_sessions = len(all_sessions)
        total_focus_time = sum(len(session_data) * 25 for session_data in all_sessions.values()) / 60  # Convert to hours
        
        # Update the metric cards with real data
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">⏰</div>
                <div class="metric-value">{total_focus_time:.1f}</div>
                <div class="metric-label">Hours Focused</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📅</div>
                <div class="metric-value">{total_sessions}</div>
                <div class="metric-label">Days Accessed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Calculate streak (simplified)
            streak = min(total_sessions, 7)  # Placeholder for actual streak calculation
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🔥</div>
                <div class="metric-value">{streak}</div>
                <div class="metric-label">Day Streak</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show recent sessions
        st.markdown('<div class="section-header">📝 Recent Sessions</div>', unsafe_allow_html=True)
        recent_sessions = list(all_sessions.items())[-5:]  # Show last 5 sessions
        
        for session_id, session_data in recent_sessions:
            st.markdown(f"""
            <div class="session-card">
                <h4>{session_id}</h4>
                <p>Blocks: {len(session_data)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("Back to Chat"):
        st.session_state.show_dashboard = False
        st.rerun()

def main():
    """Main application logic"""
    # Initialize dashboard state
    if 'show_dashboard' not in st.session_state:
        st.session_state.show_dashboard = False
    
    # Add dashboard tab at the top
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<h1 class="main-header">Focus Flow Agent</h1>', unsafe_allow_html=True)
    with col2:
        if st.button("Dashboard", key="dashboard_tab"):
            st.session_state.show_dashboard = True
            st.rerun()
    
    # Route to appropriate interface
    if st.session_state.show_dashboard:
        dashboard_interface()
    elif st.session_state.reflection_mode:
        reflection_interface()
    elif st.session_state.timer_running:
        timer_interface()
    else:
        chatbot_interface()

if __name__ == "__main__":
    main() 