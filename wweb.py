import streamlit as st
import openai
import pyttsx3

# === 🔐 Setup your API Key ===
client = openai.OpenAI(api_key="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")  # Replace with your real key

# === 🔊 Text-to-Speech Function ===
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# === 🎯 Streamlit App ===
st.set_page_config(page_title="AI Voice Assistant", page_icon="🗣️")
st.title("🗣️ AI Voice Assistant")

# === 💬 Chat History using session_state ===
if "history" not in st.session_state:
    st.session_state.history = []

# === 📝 User Input ===
text_input = st.text_input("Type your question or message:")

# === 🤖 Handle Input and AI Response ===
if text_input:
    # Add user message to history
    st.session_state.history.append({"role": "user", "content": text_input})

    # Send to OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.history
    )

    # Extract response
    answer = response.choices[0].message.content

    # Add AI response to history
    st.session_state.history.append({"role": "assistant", "content": answer})

    # Show AI response
    st.success(f"🤖 AI says: {answer}")

    # Speak it
    speak_text(answer)

# === 📜 Display Full Chat History ===
if st.session_state.history:
    st.markdown("### 💬 Chat History")
    for msg in st.session_state.history:
        role = "👤 You" if msg["role"] == "user" else "🤖 AI"
        st.markdown(f"**{role}:** {msg['content']}")


