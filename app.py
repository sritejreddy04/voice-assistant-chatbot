import streamlit as st

# Configure the page
st.set_page_config(
    page_title="AI Voice Assistant",
    layout="wide"
)

# Libraries
import os
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv

# Detect cloud deployment
IS_CLOUD = os.getenv("STREAMLIT_SERVER_PORT") is not None

# Load API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("API key not found. Please configure the GROQ_API_KEY.")
    st.stop()

# Initialize LLM client
client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"

# Generate AI response
def get_ai_response(chat_messages):

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=chat_messages,
            temperature=0.7
        )

        result = response.choices[0].message.content

        return (
            result.strip()
            if result
            else "Sorry, I could not generate a response."
        )

    except Exception as e:

        return f"Error generating response: {e}"


# Initialize speech recognizer
recognizer = sr.Recognizer()


# Initialize Text-to-Speech engine
def get_tts_engine():

    if IS_CLOUD:
        return None

    try:

        import pyttsx3

        engine = pyttsx3.init()

        return engine

    except Exception as e:

        st.error(f"TTS initialization failed: {e}")

        return None


# Convert text to speech
def speak(text, voice_gender="girl"):

    # Disable TTS on cloud
    if IS_CLOUD:
        return

    try:

        engine = get_tts_engine()

        if engine is None:
            return

        voices = engine.getProperty("voices")

        if voices:

            if voice_gender == "boy":

                for voice in voices:

                    if "male" in voice.name.lower():

                        engine.setProperty(
                            "voice",
                            voice.id
                        )

                        break

            else:

                for voice in voices:

                    if (
                        "female" in voice.name.lower()
                        or "zira" in voice.name.lower()
                    ):

                        engine.setProperty(
                            "voice",
                            voice.id
                        )

                        break

        # Speech settings
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 0.8)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:

        st.error(f"TTS Error: {e}")


# Convert speech to text
def listen_to_speech():

    try:

        with sr.Microphone() as source:

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            audio = recognizer.listen(
                source,
                phrase_time_limit=10
            )

        text = recognizer.recognize_google(audio)

        return text.lower()

    except sr.UnknownValueError:

        return "Sorry, I could not understand your voice."

    except sr.RequestError:

        return "Speech recognition service is currently unavailable."

    except Exception:

        return "Voice input is unavailable in this deployment environment."


# Main application
def main():

    # App title
    st.title("AI Voice Assistant")

    st.caption(
        "Built using Python, Streamlit, and Groq LLM API"
    )

    st.markdown(
        "A real-time AI assistant with voice and text interaction powered by LLMs."
    )

    st.divider()

    # Initialize chat history
    if "chat_history" not in st.session_state:

        st.session_state.chat_history = [
            {
                "role": "system",
                "content": (
                    "You are a helpful voice assistant. "
                    "Keep responses concise."
                )
            }
        ]

    # Store displayed messages
    if "messages" not in st.session_state:

        st.session_state.messages = []

    # Sidebar
    with st.sidebar:

        st.header("Controls")

        # Voice response toggle
        tts_enable = st.checkbox(
            "Enable Voice Response",
            value=True
        )

        # Voice selection
        voice_gender = st.selectbox(
            "Voice Selection",
            options=["girl", "boy"],
            index=0,
            help="Select preferred voice type"
        )

        # Cloud deployment notice
        if IS_CLOUD:

            st.info(
                "Voice features work best in local environments."
            )

        else:

            # Voice input button
            if st.button(
                "Start Conversation",
                type="primary",
                use_container_width=True
            ):

                with st.spinner("Listening..."):

                    user_input = listen_to_speech()

                    if user_input and user_input not in [
                        "Sorry, I could not understand your voice.",
                        "Speech recognition service is currently unavailable."
                    ]:

                        st.session_state.messages.append({
                            "role": "user",
                            "content": user_input
                        })

                        st.session_state.chat_history.append({
                            "role": "user",
                            "content": user_input
                        })

                    # Generate AI response
                    with st.spinner("Thinking..."):

                        ai_response = get_ai_response(
                            st.session_state.chat_history
                        )

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": ai_response
                        })

                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": ai_response
                        })

                        if tts_enable:
                            speak(ai_response, voice_gender)

                        st.rerun()

        st.markdown("---")

        # Text Input
        st.subheader("Text Input")

        user_text = st.text_input(
            "Type your message",
            key="text_input"
        )

        # Send button
        if st.button(
            "Send",
            use_container_width=True
        ) and user_text:

            st.session_state.messages.append({
                "role": "user",
                "content": user_text
            })

            st.session_state.chat_history.append({
                "role": "user",
                "content": user_text
            })

            with st.spinner("Thinking..."):

                ai_response = get_ai_response(
                    st.session_state.chat_history
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response
                })

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": ai_response
                })

                if tts_enable:
                    speak(ai_response, voice_gender)

                st.rerun()

        st.markdown("---")

        # Clear chat
        if st.button(
            "Clear Chat",
            use_container_width=True
        ):

            st.session_state.messages = []

            st.session_state.chat_history = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful voice assistant. "
                        "Keep responses concise."
                    )
                }
            ]

            st.rerun()

    # Conversation section
    st.subheader("Conversation")

    for message in st.session_state.messages:

        if message["role"] == "user":

            with st.chat_message("user"):

                st.write(message["content"])

        else:

            with st.chat_message("assistant"):

                st.write(message["content"])

    # Welcome message
    if not st.session_state.messages:

        st.info(
            "Welcome! Start a conversation using voice or text input."
        )


# Run app
if __name__ == "__main__":

    main()