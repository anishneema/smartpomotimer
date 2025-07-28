from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class Goal(BaseModel):
    """Represents a goal for a focus session"""
    description: str
    created_at: datetime = Field(default_factory=datetime.now)
    completed: bool = False
    notes: Optional[str] = None

class Reflection(BaseModel):
    """Represents a reflection after a focus session"""
    session_id: str
    goal_achieved: bool
    distractions: Optional[str] = None
    what_worked: Optional[str] = None
    what_didnt_work: Optional[str] = None
    next_time_improvements: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class FocusSession(BaseModel):
    """Represents a single focus session"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: int
    goal: Goal
    reflection: Optional[Reflection] = None
    completed: bool = False

class FocusFlowSession(BaseModel):
    """Represents a complete focus flow session with multiple blocks"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    available_time_minutes: int
    focus_sessions: List[FocusSession] = []
    total_focus_time: int = 0
    total_break_time: int = 0
    completed: bool = False 