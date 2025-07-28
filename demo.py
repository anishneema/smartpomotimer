#!/usr/bin/env python3
"""
Demo script for Focus Flow Agent MVP
Shows how the agent works without requiring user interaction
"""

from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from models import Goal, Reflection, FocusSession, FocusFlowSession
from logger import FocusLogger

console = Console()

def demo_session_creation():
    """Demonstrate how a session is created and structured"""
    
    console.print(Panel(
        "🎯 Focus Flow Agent - Demo Session",
        title="🚀 Demo Mode",
        border_style="green"
    ))
    
    # Create a sample session
    session = FocusFlowSession(
        session_id="demo_session_001",
        start_time=datetime.now(),
        available_time_minutes=120,
        total_focus_time=50,
        total_break_time=10,
        completed=True
    )
    
    # Add sample focus sessions
    goals = [
        "Study physics Chapter 4",
        "Write introduction for research paper",
        "Review and organize notes"
    ]
    
    reflections = [
        {
            "goal_achieved": True,
            "distractions": "Phone notifications",
            "what_worked": "Quiet environment, clear goal",
            "what_didnt_work": "Phone nearby",
            "next_time_improvements": "Put phone in another room"
        },
        {
            "goal_achieved": False,
            "distractions": "Email checking, social media",
            "what_worked": "Good writing flow once focused",
            "what_didnt_work": "Too many interruptions",
            "next_time_improvements": "Close email, use website blocker"
        },
        {
            "goal_achieved": True,
            "distractions": "None",
            "what_worked": "Clear structure, good momentum",
            "what_didnt_work": "Could have been more systematic",
            "next_time_improvements": "Use a checklist approach"
        }
    ]
    
    for i, (goal_desc, reflection_data) in enumerate(zip(goals, reflections), 1):
        goal = Goal(description=goal_desc)
        
        reflection = Reflection(
            session_id=f"demo_session_001_block_{i}",
            goal_achieved=reflection_data["goal_achieved"],
            distractions=reflection_data["distractions"],
            what_worked=reflection_data["what_worked"],
            what_didnt_work=reflection_data["what_didnt_work"],
            next_time_improvements=reflection_data["next_time_improvements"]
        )
        
        focus_session = FocusSession(
            session_id=f"demo_session_001_block_{i}",
            start_time=datetime.now(),
            end_time=datetime.now(),
            duration_minutes=25 if i < 3 else 20,  # Last session adapted to be shorter
            goal=goal,
            reflection=reflection,
            completed=True
        )
        
        session.focus_sessions.append(focus_session)
    
    return session

def demo_analytics(session):
    """Demonstrate analytics and insights"""
    
    console.print("\n[bold cyan]📊 Session Analytics[/bold cyan]")
    
    # Calculate statistics
    total_sessions = len(session.focus_sessions)
    completed_goals = sum(1 for s in session.focus_sessions 
                         if s.reflection and s.reflection.goal_achieved)
    success_rate = completed_goals / total_sessions if total_sessions > 0 else 0
    
    # Create analytics table
    table = Table(title="Session Performance")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total Focus Sessions", str(total_sessions))
    table.add_row("Goals Achieved", f"{completed_goals}/{total_sessions}")
    table.add_row("Success Rate", f"{success_rate:.1%}")
    table.add_row("Total Focus Time", f"{session.total_focus_time} minutes")
    table.add_row("Total Break Time", f"{session.total_break_time} minutes")
    table.add_row("Efficiency", f"{session.total_focus_time / session.available_time_minutes:.1%}")
    
    console.print(table)
    
    # Show insights
    console.print("\n[bold yellow]💡 Key Insights:[/bold yellow]")
    
    if success_rate >= 0.8:
        console.print("✅ Excellent focus performance! Keep up the great work.")
    elif success_rate >= 0.6:
        console.print("👍 Good progress! Consider the adaptation suggestions for even better results.")
    else:
        console.print("🔄 Room for improvement. Focus on reducing distractions and setting more achievable goals.")
    
    # Show common distractions
    distractions = [s.reflection.distractions for s in session.focus_sessions 
                   if s.reflection and s.reflection.distractions]
    
    if distractions:
        console.print(f"\n📱 Common distractions: {', '.join(set(distractions))}")
        console.print("💡 Tip: Try putting your phone in another room or using a website blocker.")

def demo_adaptation():
    """Demonstrate how the agent adapts"""
    
    console.print("\n[bold blue]🔄 Adaptation Examples[/bold blue]")
    
    adaptations = [
        {
            "scenario": "High success rate (80%+)",
            "adaptation": "Increase session duration to 30 minutes",
            "reason": "You're doing great! Let's challenge you with longer sessions."
        },
        {
            "scenario": "Low success rate (<50%)",
            "adaptation": "Reduce session duration to 15-20 minutes",
            "reason": "Let's build momentum with shorter, more achievable sessions."
        },
        {
            "scenario": "Phone distractions",
            "adaptation": "Suggest phone-free environment",
            "reason": "Physical separation from your phone can significantly improve focus."
        },
        {
            "scenario": "Email interruptions",
            "adaptation": "Recommend email blocking during sessions",
            "reason": "Batch email checking during breaks for better focus."
        }
    ]
    
    table = Table(title="Adaptation Strategies")
    table.add_column("Scenario", style="cyan")
    table.add_column("Adaptation", style="green")
    table.add_column("Reason", style="yellow")
    
    for adapt in adaptations:
        table.add_row(adapt["scenario"], adapt["adaptation"], adapt["reason"])
    
    console.print(table)

def main():
    """Run the demo"""
    
    console.print(Panel(
        "This demo shows how the Focus Flow Agent works:\n"
        "• Session creation and structure\n"
        "• Goal setting and reflection\n"
        "• Analytics and insights\n"
        "• Adaptation strategies",
        title="🎯 Focus Flow Agent Demo",
        border_style="blue"
    ))
    
    # Create demo session
    session = demo_session_creation()
    
    # Show session details
    console.print("\n[bold]📋 Sample Session Details:[/bold]")
    for i, focus_session in enumerate(session.focus_sessions, 1):
        status = "✅" if (focus_session.reflection and focus_session.reflection.goal_achieved) else "❌"
        console.print(f"  Block {i}: {status} {focus_session.goal.description}")
        if focus_session.reflection and focus_session.reflection.distractions:
            console.print(f"    Distractions: {focus_session.reflection.distractions}")
    
    # Show analytics
    demo_analytics(session)
    
    # Show adaptations
    demo_adaptation()
    
    # Save demo session
    logger = FocusLogger()
    logger.save_session(session)
    
    console.print(Panel(
        "🎉 Demo completed! The session has been saved to focus_flow_log.json\n\n"
        "To try the real agent, run: python3 main.py",
        title="✅ Demo Complete",
        border_style="green"
    ))

if __name__ == "__main__":
    main() 