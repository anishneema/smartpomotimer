import time
import threading
from datetime import datetime, timedelta
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text

console = Console()

class FocusTimer:
    """Timer for focus and break sessions"""
    
    def __init__(self):
        self.is_running = False
        self.current_task = None
        
    def start_timer(self, duration_minutes: int, session_type: str = "Focus") -> bool:
        """Start a timer for the specified duration"""
        duration_seconds = duration_minutes * 60
        self.is_running = True
        
        # Create progress display
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task(
                f"[cyan]{session_type} Session", 
                total=duration_seconds
            )
            
            start_time = datetime.now()
            end_time = start_time + timedelta(seconds=duration_seconds)
            
            # Display session info
            console.print(Panel(
                f"[bold green]{session_type} Session Started![/bold green]\n"
                f"Duration: {duration_minutes} minutes\n"
                f"Ends at: {end_time.strftime('%H:%M:%S')}",
                title=f"⏰ {session_type} Timer",
                border_style="green"
            ))
            
            # Update progress
            while not progress.finished and self.is_running:
                elapsed = (datetime.now() - start_time).total_seconds()
                progress.update(task, completed=elapsed)
                time.sleep(1)
                
                # Check if timer should be stopped
                if elapsed >= duration_seconds:
                    break
            
            if self.is_running:
                # Timer completed naturally
                console.print(Panel(
                    f"[bold yellow]{session_type} Session Complete![/bold yellow]\n"
                    f"Time to take a break and reflect!",
                    title="✅ Session Finished",
                    border_style="yellow"
                ))
                return True
            else:
                # Timer was stopped manually
                console.print(Panel(
                    f"[bold red]{session_type} Session Interrupted[/bold red]",
                    title="⏹️ Timer Stopped",
                    border_style="red"
                ))
                return False
    
    def stop_timer(self):
        """Stop the current timer"""
        self.is_running = False
        
    def countdown_display(self, seconds: int, message: str = "Starting in"):
        """Display a countdown before starting a session"""
        console.print(f"\n[bold blue]{message}:[/bold blue]")
        
        for i in range(seconds, 0, -1):
            console.print(f"[yellow]{i}[/yellow]", end=" ", flush=True)
            time.sleep(1)
        console.print("\n[bold green]Go![/bold green]\n") 