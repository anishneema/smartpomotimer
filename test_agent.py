#!/usr/bin/env python3
"""
Test script for Focus Flow Agent MVP
"""

import sys
from datetime import datetime

def test_imports():
    """Test that all modules can be imported"""
    try:
        from config import Config
        from models import Goal, Reflection, FocusSession, FocusFlowSession
        from nemotron_agent import NemotronAgent
        from timer import FocusTimer
        from logger import FocusLogger
        from focus_flow_agent import FocusFlowAgent
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_models():
    """Test data models"""
    try:
        from models import Goal, Reflection, FocusSession, FocusFlowSession
        
        # Test Goal creation
        goal = Goal(description="Test goal")
        assert goal.description == "Test goal"
        assert goal.completed == False
        
        # Test Reflection creation
        reflection = Reflection(
            session_id="test_session",
            goal_achieved=True,
            distractions="Phone"
        )
        assert reflection.goal_achieved == True
        assert reflection.distractions == "Phone"
        
        # Test FocusSession creation
        session = FocusSession(
            session_id="test_session",
            start_time=datetime.now(),
            duration_minutes=25,
            goal=goal
        )
        assert session.duration_minutes == 25
        
        print("✅ Data models work correctly")
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_config():
    """Test configuration"""
    try:
        from config import Config
        
        assert Config.DEFAULT_FOCUS_DURATION == 25
        assert Config.DEFAULT_BREAK_DURATION == 5
        assert Config.AGENT_NAME == "Focus Flow Agent"
        
        print("✅ Configuration loaded correctly")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_agent_creation():
    """Test agent creation"""
    try:
        from focus_flow_agent import FocusFlowAgent
        
        agent = FocusFlowAgent()
        assert agent.nemotron is not None
        assert agent.timer is not None
        assert agent.logger is not None
        
        print("✅ Agent created successfully")
        return True
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Focus Flow Agent MVP...\n")
    
    tests = [
        test_imports,
        test_config,
        test_models,
        test_agent_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Focus Flow Agent is ready to use.")
        print("\nTo start using it, run: python3 main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 