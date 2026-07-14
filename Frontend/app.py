import streamlit as st
import requests
import json


# ------------------------
# CSS (Sticky Header)
# ------------------------

st.markdown("""
<style>
.sticky-header {
    position: sticky;
    top: 0;
    background-color: #0e1117;
    padding: 10px;
    z-index: 999;
    border-bottom: 1px solid #444;
}
</style>
""", unsafe_allow_html=True)

# ------------------------
# DB
# ------------------------
USER_DB = "users.json"

def load_users():
    try:
        with open(USER_DB, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# ------------------------
# Auth
# ------------------------
def signup(username, password):
    users = load_users()
    if username in users:
        return False, "User already exists"
    users[username] = password2
    save_users(users)
    return True, "Signup successful"

def login(username, password):
    users = load_users()
    return username in users and users[username] == password

# ------------------------
# Backend API
# ------------------------
def get_response(query):
    try:
        res = requests.post("http://ai_app:8000/chat", json={"query": query})
        return res.json().get("response", "No response")
    except:
        return "⚠️ Backend not connected"


# ------------------------
# Session State
# ------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "chat" not in st.session_state:
    st.session_state.chat = []


# ------------------------
# LOGIN / SIGNUP
# ------------------------
if not st.session_state.logged_in:
    st.title("🔐 Chat Assistant")

    option = st.radio("Choose", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        if st.button("Signup"):
            success, msg = signup(username, password)
            st.success(msg) if success else st.error(msg)

    else:
        if st.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")

# ------------------------
# MAIN CHAT
# ------------------------
else:
    st.title(f"🤖 Chat Assistant (Hi {st.session_state.username})")

    # ------------------------
    # Sticky Header
    # ------------------------
    st.markdown('<div class="sticky-header">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.chat = []
            st.rerun()
            
    with col2:
        st.write("Welcome to the AI Assistant! Ask me anything. ")

    st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------
    # Chat Display
    # ------------------------
    for sender, msg in st.session_state.chat:
        if sender == "You":
            st.chat_message("user").write(msg)
        else:
            st.chat_message("assistant").write(msg)
            


   
    # ------------------------
    # Text Input
    # ------------------------
    query = st.chat_input("Type your message...")

    if query:
        st.session_state.chat.append(("You", query))

        response = get_response(query)
        st.session_state.chat.append(("Bot", response))



        st.rerun()