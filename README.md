# 🔥 Focus Flow Agent

An AI-powered productivity coach that adapts focus sessions based on your performance and preferences.

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

### Cloud Deployment

#### Option 1: Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy automatically

#### Option 2: NVIDIA Brev/Cloud Platforms
1. Upload your code to the cloud platform
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python run_app.py` or `streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0`

#### Option 3: Heroku
1. Ensure `Procfile` is in your repository
2. Deploy using Heroku CLI or GitHub integration

## 📁 Project Structure

```
smartpomotimer/
├── streamlit_app.py          # Main application
├── adaptive_agent.py         # AI agent for session optimization
├── config.py                 # Configuration settings
├── models.py                 # Data models
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment config
├── .streamlit/config.toml    # Streamlit configuration
└── run_app.py               # Deployment launcher
```

## 🎯 Features

- **Chatbot Interface**: Interactive session planning
- **Adaptive Timer**: AI-optimized session durations
- **Performance Tracking**: Session reflection and analytics
- **Smart Recommendations**: Personalized productivity insights
- **Modern Dashboard**: Progress visualization and stats

## 🔧 Configuration

Set up your environment variables in `.env`:
```
NEMOTRON_API_KEY=your_api_key_here
NEMOTRON_API_URL=https://api.nvcf.nvidia.com/v1/chat/completions
NEMOTRON_MODEL=nemotron-3-8b-chat-4k
```

## 🌐 Deployment Ports

The app is configured to run on port `8501` for cloud deployment. Make sure to:
- Set the port in your cloud platform configuration
- Configure any necessary firewall rules
- Set up environment variables for API keys

## 📊 Usage

1. **Start a Session**: Answer 3 simple questions about your task
2. **Focus**: Use the timer with AI-optimized duration
3. **Reflect**: Provide feedback on your session
4. **Adapt**: AI automatically adjusts for your next session
5. **Track**: View your progress in the dashboard

## 🛠️ Troubleshooting

- **Port Issues**: Ensure port 8501 is available and configured
- **API Errors**: Check your environment variables and API keys
- **Dependencies**: Run `pip install -r requirements.txt` to install all packages

## 📈 Performance

The app uses:
- **Streamlit** for the web interface
- **OpenAI/NVIDIA APIs** for AI recommendations
- **Local JSON storage** for session data
- **Adaptive algorithms** for session optimization

---

**Made with ❤️ for productive minds** 