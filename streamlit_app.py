import streamlit as st
import json
import time
import datetime
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Focus Flow Agent",
    page_icon="⏰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .session-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
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
        background: conic-gradient(#1f77b4 0deg, #1f77b4 var(--progress), #e0e0e0 var(--progress));
    }
    .timer-display {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        z-index: 1;
    }
    .goal-input {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    .reflection-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    .stats-card {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #17a2b8;
        margin: 1rem 0;
    }
    .dashboard-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_session' not in st.session_state:
    st.session_state.current_session = None
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'timer_paused' not in st.session_state:
    st.session_state.timer_paused = False
if 'timer_start_time' not in st.session_state:
    st.session_state.timer_start_time = None
if 'pause_start_time' not in st.session_state:
    st.session_state.pause_start_time = None
if 'current_block' not in st.session_state:
    st.session_state.current_block = 1
if 'session_data' not in st.session_state:
    st.session_state.session_data = {}
if 'reflection_mode' not in st.session_state:
    st.session_state.reflection_mode = False

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

def calculate_pomodoros(available_minutes):
    """Calculate how many Pomodoros fit in available time"""
    pomodoro_time = 30  # 25 min work + 5 min break
    return available_minutes // pomodoro_time

def format_time(seconds):
    """Format seconds into MM:SS"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def get_adaptation_suggestion(previous_blocks):
    """Get adaptation suggestion based on previous performance"""
    if not previous_blocks:
        return "Let's start with a standard 25-minute session!"
    
    completed = sum(1 for block in previous_blocks.values() if block.get('completed', False))
    total = len(previous_blocks)
    success_rate = completed / total if total > 0 else 0
    
    if success_rate >= 0.8:
        return "Great job! You're doing excellent. Consider extending to 30 minutes for the next session."
    elif success_rate >= 0.6:
        return "Good progress! Keep up the momentum with another 25-minute session."
    elif success_rate >= 0.4:
        return "Let's try a shorter 20-minute session to build confidence."
    else:
        return "Let's try a 15-minute session to get back on track. You can do this!"

def main():
    # Header
    st.markdown('<h1 class="main-header">Focus Flow Agent</h1>', unsafe_allow_html=True)
    
    # Main session area (like ChatGPT)
    show_session_page()
    
    # Dashboard at bottom (like ChatGPT)
    st.markdown("---")
    show_dashboard_page()

def show_session_page():
    """Main session page"""
    
    # Session setup
    if st.session_state.current_session is None:
        st.markdown('<div class="session-card">', unsafe_allow_html=True)
        st.header("Start a New Focus Session")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Available Time")
            time_input = st.text_input(
                "Enter your available time (e.g., 2pm-4pm or 120 minutes)",
                placeholder="2pm-4pm"
            )
            
            if st.button("Calculate Pomodoros", type="primary"):
                if time_input:
                    # Parse time input
                    if "pm" in time_input.lower() or "am" in time_input.lower():
                        # Time range format
                        try:
                            start_time, end_time = time_input.split("-")
                            start_time = start_time.strip()
                            end_time = end_time.strip()
                            
                            # Convert to datetime and calculate minutes
                            start_dt = datetime.strptime(start_time, "%I%p").replace(
                                year=datetime.now().year, 
                                month=datetime.now().month, 
                                day=datetime.now().day
                            )
                            end_dt = datetime.strptime(end_time, "%I%p").replace(
                                year=datetime.now().year, 
                                month=datetime.now().month, 
                                day=datetime.now().day
                            )
                            
                            if end_dt < start_dt:
                                end_dt += timedelta(days=1)
                            
                            available_minutes = int((end_dt - start_dt).total_seconds() / 60)
                        except:
                            st.error("Please enter time in format: 2pm-4pm")
                            return
                    else:
                        # Minutes format
                        try:
                            available_minutes = int(time_input)
                        except:
                            st.error("Please enter a valid number of minutes")
                            return
                    
                    pomodoros = calculate_pomodoros(available_minutes)
                    
                    if pomodoros > 0:
                        st.session_state.current_session = {
                            'start_time': datetime.now(),
                            'available_minutes': available_minutes,
                            'total_pomodoros': pomodoros,
                            'blocks': {}
                        }
                        st.success(f"{pomodoros} Pomodoro blocks planned!")
                        st.rerun()
                    else:
                        st.error("Not enough time for a Pomodoro session (minimum 30 minutes)")
        
        with col2:
            st.subheader("Quick Start")
            st.markdown("""
            **How it works:**
            1. Enter your available time
            2. Set a goal for each 25-minute block
            3. Focus with the timer
            4. Reflect on your session
            5. Get adaptive suggestions
            
            **Example:** 2pm-4pm = 120 minutes = 4 Pomodoros
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Active session
    else:
        session = st.session_state.current_session
        
        # Session info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Blocks", session['total_pomodoros'])
        with col2:
            st.metric("Current Block", st.session_state.current_block)
        with col3:
            elapsed = datetime.now() - session['start_time']
            st.metric("Session Time", f"{int(elapsed.total_seconds() / 60)}m")
        
        # Timer and goal setting
        if not st.session_state.timer_running and not st.session_state.reflection_mode:
            st.markdown('<div class="goal-input">', unsafe_allow_html=True)
            st.subheader(f"Block {st.session_state.current_block} Goal")
            
            goal = st.text_area(
                "What do you want to accomplish in this 25-minute session?",
                placeholder="e.g., Study Chapter 3, Write introduction, Review notes...",
                height=100
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Start Focus Session", type="primary", disabled=not goal):
                    st.session_state.timer_running = True
                    st.session_state.timer_start_time = datetime.now()
                    st.session_state.session_data[f"block_{st.session_state.current_block}"] = {
                        'goal': goal,
                        'start_time': datetime.now()
                    }
                    st.rerun()
            
            with col2:
                if st.button("End Session"):
                    st.session_state.current_session = None
                    st.session_state.current_block = 1
                    st.session_state.session_data = {}
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Show adaptation suggestion
            if st.session_state.session_data:
                suggestion = get_adaptation_suggestion(st.session_state.session_data)
                st.markdown(f'<div class="reflection-card"><strong>Suggestion:</strong> {suggestion}</div>', unsafe_allow_html=True)
        
        # Timer display
        elif st.session_state.timer_running:
            # Calculate remaining time
            elapsed = (datetime.now() - st.session_state.timer_start_time).total_seconds()
            remaining = max(0, 25 * 60 - elapsed)
            progress = 1 - (remaining / (25 * 60))
            
            if st.session_state.timer_paused:
                # Timer is paused
                st.markdown(f"""
                <div class="timer-container">
                    <div class="timer-circle" style="--progress: {progress * 360}deg">
                        <div class="timer-display">{format_time(int(remaining))}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Pause controls
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Resume", type="primary"):
                        # Adjust start time to account for pause
                        pause_duration = (datetime.now() - st.session_state.pause_start_time).total_seconds()
                        st.session_state.timer_start_time += timedelta(seconds=pause_duration)
                        st.session_state.timer_paused = False
                        st.rerun()
                with col2:
                    if st.button("Stop", type="secondary"):
                        st.session_state.timer_running = False
                        st.session_state.timer_paused = False
                        st.session_state.reflection_mode = True
                        st.rerun()
            else:
                # Timer is running
                elapsed = (datetime.now() - st.session_state.timer_start_time).total_seconds()
                remaining = max(0, 25 * 60 - elapsed)
                progress = 1 - (remaining / (25 * 60))
                
                if remaining > 0:
                    # Circular timer
                    st.markdown(f"""
                    <div class="timer-container">
                        <div class="timer-circle" style="--progress: {progress * 360}deg">
                            <div class="timer-display">{format_time(int(remaining))}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Timer controls
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("Pause", type="secondary"):
                            st.session_state.timer_paused = True
                            st.session_state.pause_start_time = datetime.now()
                            st.rerun()
                    with col2:
                        if st.button("Stop", type="secondary"):
                            st.session_state.timer_running = False
                            st.session_state.reflection_mode = True
                            st.rerun()
                    with col3:
                        if st.button("Skip to End", type="secondary"):
                            st.session_state.timer_running = False
                            st.session_state.reflection_mode = True
                            st.rerun()
                    
                    # Auto-refresh timer
                    time.sleep(1)
                    st.rerun()
                else:
                    st.markdown("""
                    <div class="timer-container">
                        <div class="timer-circle" style="--progress: 360deg">
                            <div class="timer-display">Complete!</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.timer_running = False
                    st.session_state.reflection_mode = True
                    st.rerun()
        
        # Reflection mode
        elif st.session_state.reflection_mode:
            st.markdown('<div class="reflection-card">', unsafe_allow_html=True)
            st.subheader("Session Reflection")
            
            current_block_data = st.session_state.session_data[f"block_{st.session_state.current_block}"]
            
            completed = st.radio(
                "Did you complete your goal?",
                ["Yes", "Partially", "No"]
            )
            
            distractions = st.text_area(
                "What distracted you during this session?",
                placeholder="e.g., Phone notifications, Email, Social media, None..."
            )
            
            what_worked = st.text_area(
                "What worked well?",
                placeholder="e.g., Quiet environment, Clear goal, Good energy..."
            )
            
            improvements = st.text_area(
                "What would you do differently next time?",
                placeholder="e.g., Put phone away, Use website blocker, Set smaller goal..."
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Reflection", type="primary"):
                    # Save reflection data
                    current_block_data.update({
                        'completed': completed == "Yes",
                        'partially_completed': completed == "Partially",
                        'distractions': distractions,
                        'what_worked': what_worked,
                        'improvements': improvements,
                        'end_time': datetime.now()
                    })
                    
                    # Save to file
                    all_sessions = load_session_log()
                    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    all_sessions[session_id] = st.session_state.session_data
                    save_session_log(all_sessions)
                    
                    st.session_state.reflection_mode = False
                    st.session_state.current_block += 1
                    
                    if st.session_state.current_block > session['total_pomodoros']:
                        st.success("Session completed! Check the dashboard for your progress.")
                        st.session_state.current_session = None
                        st.session_state.current_block = 1
                        st.session_state.session_data = {}
                    else:
                        st.success("Reflection saved! Ready for next block.")
                    
                    st.rerun()
            
            with col2:
                if st.button("Skip Reflection"):
                    st.session_state.reflection_mode = False
                    st.session_state.current_block += 1
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard_page():
    """Dashboard showing recent sessions and stats"""
    st.markdown('<div class="dashboard-section">', unsafe_allow_html=True)
    st.header("Dashboard")
    
    # Load session data
    all_sessions = load_session_log()
    
    if not all_sessions:
        st.info("No sessions completed yet. Start your first session!")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Calculate overall stats
    total_blocks = 0
    completed_blocks = 0
    total_focus_time = 0
    
    for session_id, session_data in all_sessions.items():
        for block_id, block_data in session_data.items():
            total_blocks += 1
            if block_data.get('completed', False):
                completed_blocks += 1
            if 'start_time' in block_data and 'end_time' in block_data:
                start = datetime.fromisoformat(block_data['start_time'])
                end = datetime.fromisoformat(block_data['end_time'])
                total_focus_time += (end - start).total_seconds() / 60
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sessions", len(all_sessions))
    with col2:
        st.metric("Total Blocks", total_blocks)
    with col3:
        success_rate = (completed_blocks / total_blocks * 100) if total_blocks > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")
    with col4:
        st.metric("Total Focus Time", f"{int(total_focus_time)}m")
    
    # Recent sessions
    st.subheader("Recent Sessions")
    
    for session_id, session_data in list(all_sessions.items())[-3:]:  # Show last 3 sessions
        st.markdown('<div class="session-card">', unsafe_allow_html=True)
        
        # Parse session ID for date
        try:
            date_str = session_id.split('_')[1] + '_' + session_id.split('_')[2]
            session_date = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
            st.write(f"**Session:** {session_date.strftime('%B %d, %Y at %I:%M %p')}")
        except:
            st.write(f"**Session:** {session_id}")
        
        # Show blocks in this session
        for block_id, block_data in session_data.items():
            status = "✓" if block_data.get('completed', False) else "✗"
            st.write(f"{status} **{block_id.replace('_', ' ').title()}:** {block_data.get('goal', 'No goal')}")
            
            if block_data.get('distractions'):
                st.write(f"   Distractions: {block_data['distractions']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)



if __name__ == "__main__":
    main() 