import streamlit as st
import openai
import speech_recognition as sr
import streamlit.components.v1 as components

# ========== API Key ==========
openai.api_key = "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"  # ⚠️ Replace with a new secure API key

# ========== Streamlit Setup ==========
st.set_page_config(page_title="AI Voice Assistant", layout="centered")
st.title("🗣️ AI Voice Assistant")
st.markdown("Talk or type to your assistant and get spoken responses!")

# ========== Session State for Chat History ==========
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ========== Function to Speak Text in Browser ==========
def speak_text(text):
    escaped = text.replace('"', '\\"')
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{escaped}");
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# ========== Function to Get Response from OpenAI ==========
def get_response(prompt):
    st.session_state.chat_history.append(("🧑 You", prompt))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response['choices'][0]['message']['content']
    st.session_state.chat_history.append(("🤖 AI", answer))
    return answer

# ========== Voice Input ==========
if st.button("🎤 Click to Speak"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = r.listen(source)

    try:
        user_input = r.recognize_google(audio)
        st.success(f"You said: {user_input}")
        ai_response = get_response(user_input)
        st.write("🤖 AI says:", ai_response)
        speak_text(ai_response)

    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand what you said.")
    except Exception as e:
        st.error(f"Error: {e}")

# ========== Text Input ==========
text_input = st.text_input("💬 Or type your question here:")
if text_input:
    try:
        ai_response = get_response(text_input)
        st.write("🤖 AI says:", ai_response)
        speak_text(ai_response)
    except Exception as e:
        st.error(f"Error: {e}")

# ========== Display Chat History ==========
with st.expander("🗂️ Chat History", expanded=True):
    for role, message in st.session_state.chat_history:
        if role == "🧑 You":
            st.markdown(f"**{role}:** {message}")
        else:
            st.markdown(f"**{role}:** {message}")

# ========== Clear Chat History ==========
if st.button("🧹 Clear Chat History"):
    st.session_state.chat_history = []
    st.success("Chat history cleared.")
