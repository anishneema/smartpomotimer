import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from config import Config
from models import FocusFlowSession, FocusSession, Goal, Reflection

class FocusLogger:
    """Logger for saving focus session data and reflections"""
    
    def __init__(self, log_file: str = None):
        self.log_file = log_file or Config.LOG_FILE
        
    def save_session(self, session: FocusFlowSession) -> bool:
        """Save a complete focus flow session"""
        try:
            # Load existing sessions
            sessions = self.load_all_sessions()
            
            # Add new session
            sessions.append(session.dict())
            
            # Save back to file
            with open(self.log_file, 'w') as f:
                json.dump(sessions, f, indent=2, default=str)
                
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False
    
    def load_all_sessions(self) -> List[Dict[str, Any]]:
        """Load all saved sessions"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading sessions: {e}")
            return []
    
    def get_recent_sessions(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get sessions from the last N days"""
        sessions = self.load_all_sessions()
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_sessions = []
        for session in sessions:
            session_date = datetime.fromisoformat(session['start_time'].replace('Z', '+00:00'))
            if session_date >= cutoff_date:
                recent_sessions.append(session)
                
        return recent_sessions
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics from all sessions"""
        sessions = self.load_all_sessions()
        
        if not sessions:
            return {
                "total_sessions": 0,
                "total_focus_time": 0,
                "success_rate": 0,
                "average_session_length": 0
            }
        
        total_sessions = len(sessions)
        total_focus_time = sum(s.get('total_focus_time', 0) for s in sessions)
        
        # Calculate success rate
        completed_goals = 0
        total_goals = 0
        
        for session in sessions:
            for focus_session in session.get('focus_sessions', []):
                if focus_session.get('reflection'):
                    total_goals += 1
                    if focus_session['reflection'].get('goal_achieved', False):
                        completed_goals += 1
        
        success_rate = completed_goals / total_goals if total_goals > 0 else 0
        avg_session_length = total_focus_time / total_sessions if total_sessions > 0 else 0
        
        return {
            "total_sessions": total_sessions,
            "total_focus_time": total_focus_time,
            "success_rate": success_rate,
            "average_session_length": avg_session_length,
            "total_goals": total_goals,
            "completed_goals": completed_goals
        }
    
    def export_summary(self, filename: str = None) -> str:
        """Export a summary of all sessions"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"focus_flow_summary_{timestamp}.txt"
        
        stats = self.get_session_stats()
        sessions = self.load_all_sessions()
        
        with open(filename, 'w') as f:
            f.write("=== Focus Flow Agent Session Summary ===\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Overall stats
            f.write("📊 OVERALL STATISTICS\n")
            f.write("=" * 30 + "\n")
            f.write(f"Total Sessions: {stats['total_sessions']}\n")
            f.write(f"Total Focus Time: {stats['total_focus_time']} minutes\n")
            f.write(f"Success Rate: {stats['success_rate']:.1%}\n")
            f.write(f"Average Session Length: {stats['average_session_length']:.1f} minutes\n\n")
            
            # Recent sessions
            f.write("📅 RECENT SESSIONS\n")
            f.write("=" * 30 + "\n")
            
            for session in sessions[-5:]:  # Last 5 sessions
                start_time = datetime.fromisoformat(session['start_time'].replace('Z', '+00:00'))
                f.write(f"\nSession: {start_time.strftime('%Y-%m-%d %H:%M')}\n")
                f.write(f"Duration: {session.get('total_focus_time', 0)} minutes\n")
                
                for i, focus_session in enumerate(session.get('focus_sessions', []), 1):
                    goal = focus_session.get('goal', {})
                    reflection = focus_session.get('reflection', {})
                    
                    f.write(f"  Block {i}: {goal.get('description', 'No goal')}\n")
                    if reflection:
                        achieved = "✅" if reflection.get('goal_achieved') else "❌"
                        f.write(f"    {achieved} Goal achieved: {reflection.get('goal_achieved', False)}\n")
                        if reflection.get('distractions'):
                            f.write(f"    Distractions: {reflection['distractions']}\n")
        
        return filename 