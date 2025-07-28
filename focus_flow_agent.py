import uuid
from datetime import datetime
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

from config import Config
from models import FocusFlowSession, FocusSession, Goal, Reflection
from nemotron_agent import NemotronAgent
from timer import FocusTimer
from logger import FocusLogger

console = Console()

class FocusFlowAgent:
    """Main Focus Flow Agent that orchestrates the complete experience"""
    
    def __init__(self):
        self.nemotron = NemotronAgent()
        self.timer = FocusTimer()
        self.logger = FocusLogger()
        self.current_session: Optional[FocusFlowSession] = None
        
    def start_session(self, available_time_minutes: int) -> bool:
        """Start a new focus flow session"""
        session_id = str(uuid.uuid4())
        
        self.current_session = FocusFlowSession(
            session_id=session_id,
            start_time=datetime.now(),
            available_time_minutes=available_time_minutes
        )
        
        # Calculate number of possible Pomodoros
        total_pomodoro_time = Config.DEFAULT_FOCUS_DURATION + Config.DEFAULT_BREAK_DURATION
        max_pomodoros = available_time_minutes // total_pomodoro_time
        
        console.print(Panel(
            f"[bold green]🎯 Focus Flow Agent - MVP[/bold green]\n\n"
            f"Available time: {available_time_minutes} minutes\n"
            f"Maximum Pomodoros: {max_pomodoros}\n"
            f"Focus duration: {Config.DEFAULT_FOCUS_DURATION} minutes\n"
            f"Break duration: {Config.DEFAULT_BREAK_DURATION} minutes",
            title="🚀 Session Started",
            border_style="green"
        ))
        
        return self._run_focus_blocks(max_pomodoros)
    
    def _run_focus_blocks(self, max_blocks: int) -> bool:
        """Run the focus blocks for the session"""
        if not self.current_session:
            return False
            
        block_number = 1
        previous_sessions = []
        
        while block_number <= max_blocks and self._has_time_remaining():
            console.print(f"\n[bold blue]📋 Block {block_number}/{max_blocks}[/bold blue]")
            
            # Get adaptation suggestion
            adaptation = self.nemotron.suggest_adaptation(previous_sessions, "")
            duration = adaptation.get("duration", Config.DEFAULT_FOCUS_DURATION)
            
            if adaptation.get("suggestion"):
                console.print(Panel(
                    adaptation["suggestion"],
                    title="💡 Adaptation Suggestion",
                    border_style="blue"
                ))
            
            # Set goal for this block
            goal_description = self._get_goal_for_block(block_number, previous_sessions)
            if not goal_description:
                console.print("[yellow]Session cancelled by user[/yellow]")
                return False
            
            goal = Goal(description=goal_description)
            
            # Create focus session
            focus_session = FocusSession(
                session_id=f"{self.current_session.session_id}_block_{block_number}",
                start_time=datetime.now(),
                duration_minutes=duration,
                goal=goal
            )
            
            # Run the focus timer
            console.print(f"\n[bold green]🎯 Goal: {goal_description}[/bold green]")
            console.print(f"[cyan]Duration: {duration} minutes[/cyan]\n")
            
            if Confirm.ask("Ready to start the focus session?"):
                self.timer.countdown_display(3, "Starting focus session in")
                session_completed = self.timer.start_timer(duration, "Focus")
                
                focus_session.end_time = datetime.now()
                focus_session.completed = session_completed
                
                # Reflect on the session
                if session_completed:
                    reflection = self._reflect_on_session(focus_session)
                    focus_session.reflection = reflection
                
                # Add to current session
                self.current_session.focus_sessions.append(focus_session)
                self.current_session.total_focus_time += duration
                
                # Add to previous sessions for adaptation
                previous_sessions.append(focus_session)
                
                # Take a break (except after the last block)
                if block_number < max_blocks and self._has_time_remaining():
                    self._take_break()
                
                block_number += 1
            else:
                console.print("[yellow]Session cancelled[/yellow]")
                return False
        
        # Complete the session
        self.current_session.end_time = datetime.now()
        self.current_session.completed = True
        
        # Save session
        self.logger.save_session(self.current_session)
        
        # Show summary
        self._show_session_summary()
        
        return True
    
    def _get_goal_for_block(self, block_number: int, previous_sessions: list) -> Optional[str]:
        """Get goal for the current block"""
        # Get previous goals for context
        previous_goals = [s.goal for s in previous_sessions] if previous_sessions else None
        
        # Get suggestion from Nemotron
        suggestion = self.nemotron.suggest_goal(block_number, previous_goals)
        
        console.print(Panel(
            suggestion,
            title="🤖 Goal Setting",
            border_style="cyan"
        ))
        
        goal = Prompt.ask("What's your goal for this block")
        return goal.strip() if goal else None
    
    def _reflect_on_session(self, focus_session: FocusSession) -> Reflection:
        """Guide reflection on the completed session"""
        reflection_data = self.nemotron.reflect_on_session(
            focus_session.goal, 
            focus_session.duration_minutes
        )
        
        console.print(Panel(
            reflection_data["reflection_prompt"],
            title="🤔 Session Reflection",
            border_style="yellow"
        ))
        
        # Get user input
        goal_achieved = Confirm.ask("Did you achieve your goal?")
        distractions = Prompt.ask("What distracted you? (optional)", default="")
        what_worked = Prompt.ask("What worked well? (optional)", default="")
        what_didnt_work = Prompt.ask("What didn't work? (optional)", default="")
        improvements = Prompt.ask("What would you do differently next time? (optional)", default="")
        
        return Reflection(
            session_id=focus_session.session_id,
            goal_achieved=goal_achieved,
            distractions=distractions if distractions else None,
            what_worked=what_worked if what_worked else None,
            what_didnt_work=what_didnt_work if what_didnt_work else None,
            next_time_improvements=improvements if improvements else None
        )
    
    def _take_break(self):
        """Take a break between focus sessions"""
        console.print(Panel(
            "Time for a break! Take a moment to stretch, hydrate, or just relax.",
            title="☕ Break Time",
            border_style="green"
        ))
        
        if Confirm.ask("Start break timer?"):
            self.timer.countdown_display(3, "Starting break in")
            self.timer.start_timer(Config.DEFAULT_BREAK_DURATION, "Break")
            self.current_session.total_break_time += Config.DEFAULT_BREAK_DURATION
    
    def _has_time_remaining(self) -> bool:
        """Check if there's still time remaining in the session"""
        if not self.current_session:
            return False
            
        elapsed = (datetime.now() - self.current_session.start_time).total_seconds() / 60
        return elapsed < self.current_session.available_time_minutes
    
    def _show_session_summary(self):
        """Show a summary of the completed session"""
        if not self.current_session:
            return
            
        table = Table(title="📊 Session Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Focus Time", f"{self.current_session.total_focus_time} minutes")
        table.add_row("Total Break Time", f"{self.current_session.total_break_time} minutes")
        table.add_row("Focus Sessions", str(len(self.current_session.focus_sessions)))
        
        # Calculate success rate
        completed_goals = sum(1 for s in self.current_session.focus_sessions 
                            if s.reflection and s.reflection.goal_achieved)
        total_goals = len([s for s in self.current_session.focus_sessions if s.reflection])
        success_rate = completed_goals / total_goals if total_goals > 0 else 0
        
        table.add_row("Goals Achieved", f"{completed_goals}/{total_goals} ({success_rate:.1%})")
        
        console.print(table)
        
        # Show individual session details
        console.print("\n[bold]Session Details:[/bold]")
        for i, session in enumerate(self.current_session.focus_sessions, 1):
            status = "✅" if (session.reflection and session.reflection.goal_achieved) else "❌"
            console.print(f"  Block {i}: {status} {session.goal.description}")
    
    def show_stats(self):
        """Show overall statistics"""
        stats = self.logger.get_session_stats()
        
        table = Table(title="📈 Overall Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Sessions", str(stats["total_sessions"]))
        table.add_row("Total Focus Time", f"{stats['total_focus_time']} minutes")
        table.add_row("Success Rate", f"{stats['success_rate']:.1%}")
        table.add_row("Average Session Length", f"{stats['average_session_length']:.1f} minutes")
        table.add_row("Goals Completed", f"{stats['completed_goals']}/{stats['total_goals']}")
        
        console.print(table)
    
    def export_data(self):
        """Export session data"""
        filename = self.logger.export_summary()
        console.print(f"[green]Session summary exported to: {filename}[/green]") 