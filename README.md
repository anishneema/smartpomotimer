# 🎯 Focus Flow Agent - MVP

A smart Pomodoro timer with AI-powered goal-setting and reflection that adapts to your productivity patterns.

## 🚀 What It Does

The Focus Flow Agent is an intelligent productivity tool that:

- **Breaks your available time** into 25-minute focus blocks with 5-minute breaks
- **Helps you set specific goals** for each focus session using AI
- **Guides reflection** after each session to understand what worked and what didn't
- **Adapts session length** and strategies based on your performance
- **Tracks your progress** and provides insights for continuous improvement

## 🛠️ Features

### Core Features
- ⏰ **Smart Timer**: Visual countdown with progress tracking
- 🧠 **AI Goal Setting**: Nemotron-powered goal suggestions and refinement
- 🤔 **Guided Reflection**: Structured reflection prompts after each session
- 📊 **Adaptive Sessions**: Adjusts duration and strategies based on performance
- 💾 **Progress Tracking**: Saves all sessions, goals, and reflections
- 📈 **Analytics**: View success rates, focus time, and improvement trends
- 🌐 **Web Interface**: Beautiful Streamlit web app with real-time updates

### MVP User Flow
1. **Tell the agent your available time** (e.g., "I'm free from 2-4pm")
2. **Set specific goals** for each 25-minute block
3. **Focus with visual timer** and progress tracking
4. **Reflect on your session** - what worked, what didn't, what distracted you
5. **Get adaptive suggestions** for the next block
6. **Review your progress** and export data for analysis

## 🏗️ Architecture

```
Focus Flow Agent MVP
├── 🧠 Nemotron Agent (AI interactions)
├── ⏰ Timer Tool (session management)
├── 📒 Logger Tool (data persistence)
└── 🎯 Main Agent (orchestration)
```

### Components

| Component | Purpose |
|-----------|---------|
| **Nemotron Agent** | AI-powered goal-setting, reflection, and adaptation |
| **Timer Tool** | Visual countdown and session management |
| **Logger Tool** | Save sessions, goals, and reflections |
| **Main Agent** | Orchestrates the complete user experience |
| **Web App** | Beautiful Streamlit interface with real-time analytics |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Nemotron API key (optional, for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smartpomotimer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   ```bash
   # Create .env file
   echo "NEMOTRON_API_KEY=your_api_key_here" > .env
   ```

4. **Choose your interface:**

   **🌐 Web App (Recommended)**
   ```bash
   python3 run_web_app.py
   # or
   streamlit run streamlit_app.py
   ```

   **💻 Command Line**
   ```bash
   python3 main.py
   ```

## 📖 Usage

### Starting a Session

1. **Launch the app**: `python main.py`
2. **Choose option 1**: "Start a new focus session"
3. **Enter your available time**: e.g., 120 minutes (2 hours)
4. **Set goals**: The AI will help you set specific, achievable goals
5. **Focus**: Use the visual timer to stay on track
6. **Reflect**: Answer questions about your session
7. **Adapt**: Get suggestions for the next block

### Example Session

```
👤 You: I'm free 2-4pm (120 minutes)

🤖 Agent: Let's do 3 Pomodoros (25 min work, 5 min breaks)
        What's your goal for Block 1?

👤 You: Study physics Chapter 4

⏱️ [Timer starts: 25 minutes]

⏲️ [Timer ends]

🤖 Agent: Did you finish your goal? What distracted you?

👤 You: I got distracted by my phone.

🤖 Agent: Let's try a 20-min block next with no phone nearby.
        Goal for Block 2?
```

### Viewing Statistics

- **Option 2**: View overall statistics and success rates
- **Option 3**: Export your data for external analysis

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Nemotron API (optional)
NEMOTRON_API_KEY=your_api_key_here
NEMOTRON_API_URL=https://api.nemotron.ai/v1/chat/completions

# Timer settings (can be modified in config.py)
DEFAULT_FOCUS_DURATION=25
DEFAULT_BREAK_DURATION=5
```

### Customization

Edit `config.py` to modify:
- Default focus and break durations
- Log file location
- Agent personality settings

## 📊 Data Structure

The agent saves your sessions in `focus_flow_log.json`:

```json
{
  "session_id": "uuid",
  "start_time": "2024-01-15T14:00:00",
  "available_time_minutes": 120,
  "focus_sessions": [
    {
      "session_id": "uuid_block_1",
      "goal": {
        "description": "Study physics Chapter 4",
        "completed": true
      },
      "reflection": {
        "goal_achieved": true,
        "distractions": "Phone notifications",
        "what_worked": "Quiet environment",
        "next_time_improvements": "Put phone in another room"
      }
    }
  ]
}
```

## 🎯 Why It's a Real Agent

The Focus Flow Agent demonstrates true agent behavior:

- **Makes decisions** based on your input and performance
- **Uses memory** (logs previous sessions for context)
- **Takes multiple steps** (ask → wait → reflect → adapt)
- **Acts** (runs timers, stores data, provides suggestions)
- **Learns** (adapts strategies based on success patterns)

## 🚧 Future Enhancements

### Planned Features
- 📅 **Google Calendar Integration**: Schedule sessions automatically
- 🔔 **Push Notifications**: Reminders and session alerts
- 🌐 **Website Blockers**: Prevent distractions during focus time
- 📱 **Mobile App**: iOS/Android companion app
- 🤝 **Team Features**: Collaborative focus sessions
- 📊 **Advanced Analytics**: Detailed productivity insights

### Technical Improvements
- **Web Interface**: Beautiful web UI with real-time updates
- **API Endpoints**: RESTful API for integrations
- **Database**: PostgreSQL for better data management
- **Real-time Sync**: Cloud synchronization across devices

## 🤝 Contributing

This is an MVP version. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Pomodoro Technique**: Francesco Cirillo's time management method
- **Nemotron**: AI model for intelligent interactions
- **Rich**: Beautiful terminal interface library
- **Pydantic**: Data validation and settings management

---

**Ready to boost your productivity? Start your first focus session today!** 🚀 