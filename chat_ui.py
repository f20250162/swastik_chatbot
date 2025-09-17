import streamlit as st
import os
import google.generativeai as genai
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI

if "conversation" not in st.session_state:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=st.secrets["GOOGLE_API_KEY"]
# <-- safer than hardcoding
    )
    st.session_state.conversation = ConversationChain(
        llm=llm,
        memory=ConversationBufferMemory()
    )


GEMINI_API_KEY = os.getenv("AIzaSyDpLztPNrU346jGvjQA5YoIcZZ1KbFJrbI")



# Personalities
PERSONALITIES = {
    "Roast 🔥": "You are a savage roasting assistant who makes fun of the user playfully.",
    "Cool City Guy 😎": "You are a chill, high-tech city guy who talks casually and uses modern slang.",
    "Shakespeare 🎭": "You speak like Shakespeare, full of dramatic flair and old English style.",
    "Normal 🤖": "You are a helpful and friendly assistant who provides clear and concise answers."
}




def query_gemini(prompt, personality):
    # full prompt that includes the personality
    full_prompt = f"{personality}\nUser: {prompt}\nAssistant:"

    try:
        
        reply = st.session_state.conversation.run(full_prompt)
        return reply
    except Exception as e:
        return f"⚠️ Could not get a reply from Gemini via LangChain. Error: {str(e)}"

    


# Streamlit UI
st.title("⚡Swastik's Multi-Personality Chatbot ")

# Select personality
selected_personality = st.selectbox("Choose a personality:", list(PERSONALITIES.keys()))

# Reset history button
if "history" not in st.session_state:
    st.session_state.history = []
if st.button("Reset Chat"):
    st.session_state.history = []


# Display full chat history every rerun
for speaker, msg in st.session_state.history:
    with st.chat_message("user" if speaker == "You" else "ai"):
        st.markdown(msg)

# Input box at bottom
user_input = st.chat_input("Type your message...")

if user_input:
    # Run through LangChain ConversationChain (has memory)
    reply = query_gemini(user_input, PERSONALITIES[selected_personality])


    # Add user message immediately to chat
    st.session_state.history.append(("You", user_input))
    st.chat_message("user").markdown(user_input)

    # Show bot reply
    with st.chat_message("ai"):
        st.markdown(reply)

    # Save bot reply to history
    st.session_state.history.append(("Bot", reply))

