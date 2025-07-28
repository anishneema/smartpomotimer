# 🚀 Quick Start Guide

Get the Focus Flow Agent running in 5 minutes!

## 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

## 2. (Optional) Set up Nemotron API

For AI-powered features, create a `.env` file:

```bash
echo "NEMOTRON_API_KEY=your_api_key_here" > .env
```

**Note**: The agent works without the API key, but AI features will be limited.

## 3. Test the Installation

```bash
python3 test_agent.py
```

You should see: `🎉 All tests passed!`

## 4. Try the Demo

```bash
python3 demo.py
```

This shows how the agent works without requiring user interaction.

## 5. Start Your First Session

**🌐 Web App (Recommended):**
```bash
python3 run_web_app.py
```

**💻 Command Line:**
```bash
python3 main.py
```

Then:
1. Enter your available time (e.g., 2pm-4pm or 120 minutes)
2. Set goals for each block
3. Focus with the visual timer
4. Reflect and track your progress!

## 🎯 Example Session

```
You: I'm free 2pm-4pm (120 minutes)

App: ✅ 4 Pomodoro blocks planned!

You: Goal: Study physics Chapter 4

⏱️ [Visual timer: 25:00 → 00:00]

App: ✅ Session Complete!

App: Did you complete your goal? What distracted you?

You: I got distracted by my phone.

App: 💡 Suggestion: Let's try a 20-min block next with no phone nearby.
```

## 📊 View Your Progress

- **Option 2**: View statistics and success rates
- **Option 3**: Export your data for analysis

## 🔧 Customization

Edit `config.py` to change:
- Default focus duration (25 minutes)
- Default break duration (5 minutes)
- Log file location

## 🆘 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Run `python3 test_agent.py` to verify everything works
- The agent saves all data in `focus_flow_log.json`

---

**Ready to boost your productivity? Start your first session now!** 🎯 