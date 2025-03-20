import re
import random
import string
import streamlit as st

# Page style 
st.set_page_config(page_title="Password Strength Checker", page_icon="🔐", layout="centered")

# Custom CSS for better styling
st.markdown("""
    <style>
        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        h1 {
            font-size: 26px;
            color: #333;
            font-weight: bold;
        }
        .stTextInput input {
            text-align: center;
        }
        .stButton button {
            width: 100%;
            background: linear-gradient(135deg, #007bff, #004085);
            color: white;
            font-size: 18px;
            border-radius: 5px;
            padding: 10px;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton button:hover {
            background: linear-gradient(135deg, #0056b3, #002752);
        }
        .strength-meter {
            width: 100%;
            height: 10px;
            background: #ddd;
            border-radius: 5px;
            margin-top: 10px;
            position: relative;
        }
        .strength-bar {
            height: 10px;
            border-radius: 5px;
            transition: width 0.3s ease-in-out;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.markdown("<h1>🔐 Password Strength Checker</h1>", unsafe_allow_html=True)
st.write("Enter your password below to check its security level. 🔍")

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1  
    else:
        feedback.append("❌ Password should be **at least 8 characters long**.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Password should contain **at least one uppercase (A-Z) and one lowercase (a-z) letter**.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Password should contain **at least one digit (0-9)**.")

    if re.search(r"[!@#$%^&*(),.?':{}|<>]", password):
        score += 1
    else:
        feedback.append("❌ Password should contain **at least one special character (!@#$%^&*(),.?':{}|<>)**.")

    # Ensure score does not exceed the index range
    score = min(score, 3)  # Prevents IndexError

    colors = ["red", "orange", "yellow", "green"]
    strength_text = ["Weak", "Moderate", "Good", "Strong"]

    st.markdown(f"""
        <div class='strength-meter'>
            <div class='strength-bar' style='width: {(score + 1) * 25}%; background: {colors[score]};'></div>
        </div>
        <p style='text-align: center; font-weight: bold; color: {colors[score]};'>{strength_text[score]} Password</p>
    """, unsafe_allow_html=True)

    if feedback:
        with st.expander("🔍 **Improve Your Password**"):
            for item in feedback:
                st.write(item)


# Initialize session state variables
if "generated_password" not in st.session_state:
    st.session_state.generated_password = ""
if "password_copied" not in st.session_state:
    st.session_state.password_copied = False

# Function to generate a strong password
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(12))

# Password input box
password = st.text_input("Enter your password:", type="password", help="Ensure your password is strong 🔐")

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Check Strength"):
        if password:
            check_password_strength(password)
        else:
            st.warning("⚠️ Please enter a password first!")

with col2:
    if st.button("Generate Strong Password"):
        st.session_state.generated_password = generate_password()
        st.success("🔑 Generated Password:")

# Display the generated password with a copy button
if st.session_state.generated_password:
    st.text_input("Generated Password", st.session_state.generated_password, key="password_display")

    # Copy Button (Manual Copy Required)
    if st.button("Copy Password"):
        st.session_state.password_copied = True

    if st.session_state.password_copied:
        st.success("✅ Password copied! (Manually copy it from above)")
st.markdown("</div>", unsafe_allow_html=True)
