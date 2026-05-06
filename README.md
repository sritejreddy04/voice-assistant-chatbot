# 🎙️ AI Voice Assistant

A real-time AI voice and text assistant built using Python and Streamlit.  
The application integrates Large Language Models (LLMs) through the Groq API to provide conversational AI capabilities with both voice and text interaction.

---

## 🚀 Features

- Voice-to-text interaction
- Text-to-speech responses
- LLM-powered conversational AI
- Real-time text chat interface
- Session-based conversation history
- Streamlit interactive UI
- Cloud deployment support with local voice fallback handling

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Groq API
- SpeechRecognition
- pyttsx3
- python-dotenv

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/voice-assistant-chatbot.git
cd voice-assistant-chatbot
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### Run the application

```bash
streamlit run app.py
```

---

## 📌 Notes

- Microphone access is required for full voice interaction
- Voice input/output functionality works best in local environments due to cloud audio hardware limitations
- Cloud deployment supports text-based interaction with LLM responses
- API keys should never be committed to GitHub repositories

---

## 📷 Demo

![AI Voice Assistant Demo](assets/demo.png)