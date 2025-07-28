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

# Custom CSS for modern aesthetic dashboard
st.markdown("""
<style>
    /* Modern Dashboard Styling */
    .main-header {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        letter-spacing: -0.5px;
    }
    
    .session-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        border: 1px solid #f0f0f0;
    }
    
    .goal-input {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    }
    
    .reflection-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    }
    
    .dashboard-section {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        margin-top: 2rem;
        border: 1px solid #f0f0f0;
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
    
    /* Modern Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        text-align: center;
        margin: 0.5rem;
        border: 1px solid #f0f0f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0.5rem 0;
        letter-spacing: -0.5px;
    }
    
    .metric-label {
        color: #7f8c8d;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Navigation Tabs */
    .nav-tabs {
        display: flex;
        background: #f8f9fa;
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 2rem;
    }
    
    .nav-tab {
        flex: 1;
        text-align: center;
        padding: 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        font-weight: 500;
    }
    
    .nav-tab.active {
        background: white;
        color: #3498db;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .nav-tab:not(.active) {
        color: #7f8c8d;
    }
    
    /* Time Range Selector */
    .time-range {
        display: flex;
        background: #f8f9fa;
        border-radius: 8px;
        padding: 0.25rem;
        margin-bottom: 1rem;
    }
    
    .time-btn {
        padding: 0.5rem 1rem;
        border-radius: 6px;
        border: none;
        background: transparent;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .time-btn.active {
        background: white;
        color: #3498db;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .time-btn:not(.active) {
        color: #7f8c8d;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-icon {
        font-size: 1.2rem;
        opacity: 0.7;
    }
    
    /* Status Indicators */
    .status-completed {
        color: #27ae60;
        font-weight: 600;
    }
    
    .status-partial {
        color: #f39c12;
        font-weight: 600;
    }
    
    .status-incomplete {
        color: #e74c3c;
        font-weight: 600;
    }
    
    /* Graph Container */
    .graph-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
        border: 1px solid #f0f0f0;
    }
    
    /* Stats Cards */
    .stats-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0f0f0;
        margin: 1rem 0;
    }
    
    /* Compact Session Cards */
    .session-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        margin-bottom: 1rem;
        border: 1px solid #f0f0f0;
        transition: box-shadow 0.2s ease;
    }
    
    .session-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Block Items */
    .block-item {
        margin: 0.25rem 0;
        padding: 0.75rem;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 3px solid #e9ecef;
        transition: background-color 0.2s ease;
    }
    
    .block-item:hover {
        background: #f1f3f4;
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
if 'adaptive_agent' not in st.session_state:
    st.session_state.adaptive_agent = AdaptiveAgent()
if 'current_task_context' not in st.session_state:
    st.session_state.current_task_context = None
if 'session_recommendation' not in st.session_state:
    st.session_state.session_recommendation = None

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
    # Modern header
    st.markdown('<h1 class="main-header">Focus Flow Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #7f8c8d; margin-bottom: 2rem;">Intelligent productivity coaching with AI-powered session optimization</p>', unsafe_allow_html=True)
    
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
            st.subheader(f"Block {st.session_state.current_block} - Intelligent Session Planning")
            
            # Task input with adaptive features
            col1, col2 = st.columns(2)
            
            with col1:
                goal = st.text_area(
                    "What do you want to accomplish?",
                    placeholder="e.g., Write history essay, Study physics Chapter 4, Review notes...",
                    height=80
                )
                
                task_type = st.selectbox(
                    "Task Type",
                    ["general", "writing", "reading", "coding", "reviewing", "planning", "creative"]
                )
                
                difficulty = st.slider("Task Difficulty", 1, 5, 3, help="1=Easy, 5=Very Complex")
                
            with col2:
                energy_level = st.slider("Your Energy Level", 1, 5, 3, help="1=Tired, 5=Very Energized")
                
                urgency = st.slider("Urgency", 1, 5, 3, help="1=Low priority, 5=Critical deadline")
                
                deadline = st.date_input("Deadline (optional)", value=None)
                
                if deadline:
                    deadline_time = datetime.combine(deadline, datetime.min.time())
                else:
                    deadline_time = None
            
            # Get adaptive recommendation
            if goal and st.button("Get Intelligent Recommendation", type="primary"):
                task_context = TaskContext(
                    task_name=goal,
                    difficulty=difficulty,
                    energy_level=energy_level,
                    deadline=deadline_time,
                    task_type=task_type,
                    urgency=urgency
                )
                
                st.session_state.current_task_context = task_context
                recommendation = st.session_state.adaptive_agent.analyze_task_and_plan_session(task_context)
                st.session_state.session_recommendation = recommendation
                st.rerun()
            
            # Show recommendation if available
            if st.session_state.session_recommendation:
                rec = st.session_state.session_recommendation
                st.markdown(f"""
                <div class="reflection-card">
                    <h4>Intelligent Recommendation</h4>
                    <p><strong>Focus Duration:</strong> {rec.focus_duration} minutes</p>
                    <p><strong>Break Duration:</strong> {rec.break_duration} minutes</p>
                    <p><strong>Reasoning:</strong> {rec.reasoning}</p>
                    <p><strong>Approach:</strong> {rec.suggested_approach}</p>
                    <p><strong>Confidence:</strong> {rec.confidence:.1%}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Start Adaptive Session", type="primary"):
                        st.session_state.timer_running = True
                        st.session_state.timer_start_time = datetime.now()
                        st.session_state.session_data[f"block_{st.session_state.current_block}"] = {
                            'goal': goal,
                            'start_time': datetime.now(),
                            'task_context': st.session_state.current_task_context,
                            'recommendation': st.session_state.session_recommendation
                        }
                        st.rerun()
                
                with col2:
                    if st.button("Use Standard 25min", type="secondary"):
                        st.session_state.timer_running = True
                        st.session_state.timer_start_time = datetime.now()
                        st.session_state.session_data[f"block_{st.session_state.current_block}"] = {
                            'goal': goal,
                            'start_time': datetime.now()
                        }
                        st.rerun()
            
            # Fallback for when no recommendation is available
            elif goal:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Start Standard Session", type="primary"):
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
                # Get session duration from recommendation or use default
                current_block_data = st.session_state.session_data.get(f"block_{st.session_state.current_block}", {})
                recommendation = current_block_data.get('recommendation')
                session_duration = recommendation.focus_duration if recommendation else 25
                
                elapsed = (datetime.now() - st.session_state.timer_start_time).total_seconds()
                remaining = max(0, session_duration * 60 - elapsed)
                progress = 1 - (remaining / (session_duration * 60))
                
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
            
            col1, col2 = st.columns(2)
            
            with col1:
                completed = st.radio(
                    "Did you complete your goal?",
                    ["Yes", "Partially", "No"]
                )
                
                focus_rating = st.slider("How focused were you?", 1, 5, 3, help="1=Very distracted, 5=Highly focused")
                
                energy_after = st.slider("Energy level after session", 1, 5, 3, help="1=Exhausted, 5=Still energized")
            
            with col2:
                distractions = st.text_area(
                    "What distracted you?",
                    placeholder="e.g., Phone notifications, Email, Social media, None...",
                    height=80
                )
                
                what_worked = st.text_area(
                    "What worked well?",
                    placeholder="e.g., Quiet environment, Clear goal, Good energy...",
                    height=80
                )
            
            # Adaptive feedback section
            if st.session_state.current_task_context:
                st.markdown("### Intelligent Adaptation")
                
                # Get adaptive feedback
                performance = PerformanceData(
                    task_completed=completed == "Yes",
                    focus_rating=focus_rating,
                    energy_after=energy_after,
                    distractions=distractions.split(', ') if distractions else [],
                    what_worked=what_worked,
                    session_duration=current_block_data.get('recommendation', SessionRecommendation(25, 5, "", 0.5, "")).focus_duration
                )
                
                adaptation = st.session_state.adaptive_agent.adapt_after_session(
                    performance, st.session_state.current_task_context
                )
                
                st.markdown(f"""
                <div class="reflection-card">
                    <h4>Adaptive Recommendations</h4>
                    <p><strong>Next Session Duration:</strong> {adaptation['next_session_duration']} minutes</p>
                    <p><strong>Break Duration:</strong> {adaptation['break_duration']} minutes</p>
                    <p><strong>Energy Management:</strong> {adaptation['energy_management']}</p>
                    <p><strong>AI Suggestion:</strong> {adaptation['suggestions']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if adaptation['distraction_strategies']:
                    st.markdown("**Distraction Strategies:**")
                    for strategy in adaptation['distraction_strategies']:
                        st.markdown(f"- {strategy}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Reflection", type="primary"):
                    # Save reflection data
                    current_block_data.update({
                        'completed': completed == "Yes",
                        'partially_completed': completed == "Partially",
                        'focus_rating': focus_rating,
                        'energy_after': energy_after,
                        'distractions': distractions,
                        'what_worked': what_worked,
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
    
    # Modern header with navigation tabs
    st.markdown("""
    <div class="nav-tabs">
        <div class="nav-tab active">📊 Summary</div>
        <div class="nav-tab">📈 Detail</div>
        <div class="nav-tab">🏆 Ranking</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load session data
    all_sessions = load_session_log()
    
    if not all_sessions:
        st.markdown("""
        <div class="graph-container">
            <div style="text-align: center; padding: 3rem;">
                <h3 style="color: #7f8c8d; margin-bottom: 1rem;">No sessions completed yet</h3>
                <p style="color: #95a5a6;">Start your first session to see your progress!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Calculate overall stats
    total_blocks = 0
    completed_blocks = 0
    total_focus_time = 0
    total_sessions = len(all_sessions)
    
    for session_id, session_data in all_sessions.items():
        for block_id, block_data in session_data.items():
            total_blocks += 1
            if block_data.get('completed', False):
                completed_blocks += 1
            if 'start_time' in block_data and 'end_time' in block_data:
                start = datetime.fromisoformat(block_data['start_time'])
                end = datetime.fromisoformat(block_data['end_time'])
                total_focus_time += (end - start).total_seconds() / 60
    
    success_rate = (completed_blocks / total_blocks * 100) if total_blocks > 0 else 0
    
    # Activity Summary Section
    st.markdown('<div class="section-header">📈 Activity Summary</div>', unsafe_allow_html=True)
    
    # Modern metric cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">⏰</div>
            <div class="metric-value">{int(total_focus_time)}</div>
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
    
    # Weekly insights with modern styling
    weekly_insights = st.session_state.adaptive_agent.get_weekly_insights()
    if "message" not in weekly_insights:
        st.markdown('<div class="section-header">🧠 AI Insights</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-value">{weekly_insights["total_sessions"]}</div>
                <div class="metric-label">This Week</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">✅</div>
                <div class="metric-value">{weekly_insights['success_rate']:.0%}</div>
                <div class="metric-label">Success Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🎯</div>
                <div class="metric-value">{weekly_insights['average_focus']:.1f}</div>
                <div class="metric-label">Avg Focus</div>
            </div>
            """, unsafe_allow_html=True)
        
        if weekly_insights["recommendations"]:
            st.markdown('<div class="section-header">💡 AI Recommendations</div>', unsafe_allow_html=True)
            for rec in weekly_insights["recommendations"]:
                st.markdown(f"""
                <div class="stats-card">
                    <p style="margin: 0; color: #2c3e50;">{rec}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Recent sessions with modern styling
    st.markdown('<div class="section-header">📝 Recent Sessions</div>', unsafe_allow_html=True)
    
    # Create a compact session list
    recent_sessions = list(all_sessions.items())[-3:]  # Show last 3 sessions
    
    if recent_sessions:
        for session_id, session_data in recent_sessions:
            # Parse session ID for date
            try:
                date_str = session_id.split('_')[1] + '_' + session_id.split('_')[2]
                session_date = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
                session_date_str = session_date.strftime('%B %d, %Y at %I:%M %p')
            except:
                session_date_str = session_id
            
            # Count completed blocks
            completed_blocks = sum(1 for block_data in session_data.values() if block_data.get('completed', False))
            total_blocks = len(session_data)
            
            # Create session summary
            st.markdown(f"""
            <div class="session-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h4 style="color: #2c3e50; margin: 0; font-size: 1.1rem;">{session_date_str}</h4>
                    <span style="color: #7f8c8d; font-size: 0.9rem; background: #f8f9fa; padding: 0.25rem 0.5rem; border-radius: 4px;">{completed_blocks}/{total_blocks} completed</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Show blocks in a compact format
            for block_id, block_data in session_data.items():
                if block_data.get('completed', False):
                    status_class = "status-completed"
                    status_icon = "✓"
                elif block_data.get('partially_completed', False):
                    status_class = "status-partial"
                    status_icon = "○"
                else:
                    status_class = "status-incomplete"
                    status_icon = "✗"
                
                goal_text = block_data.get('goal', 'No goal')
                if len(goal_text) > 60:
                    goal_text = goal_text[:57] + "..."
                
                st.markdown(f"""
                <div class="block-item">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span class="{status_class}" style="font-size: 1.1rem;">{status_icon}</span>
                        <div style="flex: 1;">
                            <div style="font-weight: 500; color: #2c3e50; margin-bottom: 0.25rem;">
                                {block_id.replace('_', ' ').title()}
                            </div>
                            <div style="color: #7f8c8d; font-size: 0.9rem;">
                                {goal_text}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="graph-container">
            <div style="text-align: center; padding: 2rem;">
                <h4 style="color: #7f8c8d; margin-bottom: 0.5rem;">No sessions yet</h4>
                <p style="color: #95a5a6; font-size: 0.9rem;">Complete your first session to see it here!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)



if __name__ == "__main__":
    main() 