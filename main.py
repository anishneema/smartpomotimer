#!/usr/bin/env python3
"""
Focus Flow Agent - MVP
A smart Pomodoro timer with AI-powered goal-setting and reflection
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.text import Text

from focus_flow_agent import FocusFlowAgent

console = Console()

def show_welcome():
    """Show welcome message and instructions"""
    welcome_text = """
    🎯 Focus Flow Agent - MVP Version
    
    This agent helps you make the most of your available time by:
    • Breaking it into focused 25-minute blocks with 5-minute breaks
    • Helping you set specific, achievable goals for each block
    • Guiding reflection after each session to improve future focus
    • Adapting session length and strategies based on your performance
    • Saving your progress for future analysis
    
    Ready to boost your productivity? Let's get started!
    """
    
    console.print(Panel(
        welcome_text,
        title="🚀 Welcome to Focus Flow Agent",
        border_style="green"
    ))

def show_menu():
    """Show the main menu"""
    menu_text = """
    What would you like to do?
    
    1. 🎯 Start a new focus session
    2. 📊 View your statistics
    3. 📤 Export your data
    4. ℹ️  About
    5. 🚪 Exit
    """
    
    console.print(Panel(
        menu_text,
        title="📋 Main Menu",
        border_style="blue"
    ))

def get_available_time() -> int:
    """Get the user's available time"""
    console.print("\n[bold cyan]How much time do you have available?[/bold cyan]")
    console.print("Examples: 60 minutes (1 hour), 120 minutes (2 hours), etc.")
    
    while True:
        try:
            minutes = IntPrompt.ask("Enter available time in minutes", default=60)
            if minutes < 30:
                console.print("[yellow]That's quite short! Consider at least 30 minutes for a meaningful session.[/yellow]")
                if not Confirm.ask("Continue anyway?"):
                    continue
            elif minutes > 480:  # 8 hours
                console.print("[yellow]That's a long session! Consider breaking it into smaller chunks.[/yellow]")
                if not Confirm.ask("Continue anyway?"):
                    continue
            
            return minutes
        except ValueError:
            console.print("[red]Please enter a valid number of minutes.[/red]")

def start_focus_session():
    """Start a new focus session"""
    available_time = get_available_time()
    
    agent = FocusFlowAgent()
    success = agent.start_session(available_time)
    
    if success:
        console.print("\n[bold green]🎉 Session completed successfully![/bold green]")
    else:
        console.print("\n[yellow]Session was interrupted or cancelled.[/yellow]")

def view_statistics():
    """View user statistics"""
    agent = FocusFlowAgent()
    agent.show_stats()

def export_data():
    """Export user data"""
    agent = FocusFlowAgent()
    agent.export_data()

def show_about():
    """Show information about the Focus Flow Agent"""
    about_text = """
    🎯 Focus Flow Agent - MVP Version 1.0
    
    This is an intelligent productivity tool that combines:
    • Pomodoro Technique (25-min focus, 5-min breaks)
    • AI-powered goal-setting and reflection
    • Adaptive session management
    • Progress tracking and analytics
    
    Built with:
    • Python 3.8+
    • Rich (for beautiful CLI interface)
    • Nemotron API (for AI interactions)
    • Pydantic (for data validation)
    
    The agent learns from your sessions and adapts to help you
    improve your focus and productivity over time.
    """
    
    console.print(Panel(
        about_text,
        title="ℹ️ About Focus Flow Agent",
        border_style="cyan"
    ))

def main():
    """Main application loop"""
    show_welcome()
    
    while True:
        show_menu()
        
        try:
            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                start_focus_session()
            elif choice == "2":
                view_statistics()
            elif choice == "3":
                export_data()
            elif choice == "4":
                show_about()
            elif choice == "5":
                console.print("\n[bold green]Thanks for using Focus Flow Agent![/bold green]")
                console.print("Keep focusing, keep growing! 🌱")
                break
                
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Session interrupted. Thanks for using Focus Flow Agent![/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]An error occurred: {e}[/red]")
            console.print("Please try again.")

if __name__ == "__main__":
    main() 