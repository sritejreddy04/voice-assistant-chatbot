# 🎙️ AI Voice Assistant

A real-time AI voice assistant built using Python and Streamlit. The application supports both voice and text interaction powered by Large Language Models (LLMs).

---

## 🚀 Features

- Voice-to-text interaction
- Text-to-speech responses
- LLM-powered conversational responses
- Streamlit-based interactive UI
- Session-based chat history

---

## 🛠️ Tech Stack

- Python
- Streamlit
- SpeechRecognition
- pyttsx3
- Groq API
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

- Microphone access is required for voice interaction
- Voice input/output functionality works best in local environments due to cloud audio hardware limitations
- Ensure audio drivers are properly installed for local execution

---

## 📷 Demo

![AI Voice Assistant Demo](assets/demo.png)