import streamlit as st
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Knowledge Maze", page_icon="🔑", layout="centered")

# --- CUSTOM CSS FOR BETTER LOOKS ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- QUESTION BANK (From your screenshots) ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"topic": "Basic Logarithms", "q": "Simplify: log(1000)", "a": "3"},
        {"topic": "Negative Exponents", "q": "Simplify: log_x(1/x^3)", "a": "-3"},
        {"topic": "Changing Bases", "q": "Simplify: log_8(32)", "a": "5/3"},
        {"topic": "Exponential Equations", "q": "Solve: 4^(x^2 - 2x) = 8^(1 - x) (Separate answers with comma, e.g., 1, 2)", "a": "3/2, -1"},
        {"topic": "Logarithmic Identity", "q": "Solve: 9^(log_3(6)) = x", "a": "36"},
        {"topic": "Compound Interest", "q": "Years needed for $1250 to become $7000 at 6.75% quarterly? (Round to 1 decimal)", "a": "25.7"},
        {"topic": "Log Expressions", "q": "If log 5 = a and log 36 = b, express log(6/25) in terms of a and b", "a": "1/2b-2a"}
    ]
    random.shuffle(st.session_state.questions)

# --- SESSION STATE INITIALIZATION ---
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.report = []
    st.session_state.game_over = False

# --- UI LAYOUT ---
st.title("🛡️ Knowledge Maze: The Logarithm Quest")
st.write("Solve the problem to advance through the maze and find the treasure!")

if not st.session_state.game_over:
    # Progress bar
    current_q = st.session_state.current_idx
    total_q = len(st.session_state.questions)
    progress = current_q / total_q
    st.progress(progress)
    st.write(f"**Current Progress: Room {current_q + 1} of {total_q}**")

    # Question Display
    q_data = st.session_state.questions[current_q]
    with st.expander("📍 Current Location Hint", expanded=True):
        st.write(f"**Knowledge Point:** {q_data['topic']}")
    
    st.subheader(q_data['q'])
    user_ans = st.text_input("Enter your answer:", placeholder="Type here...", key=f"input_{current_q}")

    if st.button("Submit & Move Forward 🏃"):
        # Clean input for comparison
        clean_user = user_ans.replace(" ", "").lower()
        clean_correct = q_data['a'].replace(" ", "").lower()
        
        if clean_user == clean_correct:
            st.session_state.score += 1
            st.session_state.report.append((q_data['topic'], "Mastered ✅"))
            st.toast("Correct! You moved forward.", icon="✅")
        else:
            st.session_state.report.append((q_data['topic'], f"Review Needed 🚩 (Ans: {q_data['a']})"))
            st.toast("Wrong! You hit a trap.", icon="❌")
        
        # Advance to next question
        if st.session_state.current_idx + 1 < total_q:
            st.session_state.current_idx += 1
            st.rerun()
        else:
            st.session_state.game_over = True
            st.rerun()

else:
    # --- END SCREEN ---
    st.balloons()
    st.success("🏁 You've reached the end of the maze!")
    
    col1, col2 = st.columns(2)
    col1.metric("Final Score", f"{st.session_state.score}/{len(st.session_state.questions)}")
    
    if st.session_state.score == len(st.session_state.questions):
        st.write("🎁 **Incredible! You opened the Golden Chest!**")
    else:
        st.write("🗝️ **You escaped, but some treasures remain hidden.**")

    st.markdown("### 📊 Diagnostic Report")
    st.write("Share this with your tutor to focus on your weak points:")
    for topic, status in st.session_state.report:
        st.write(f"- **{topic}**: {status}")

    if st.button("Restart Adventure 🔄"):
        st.session_state.current_idx = 0
        st.session_state.score = 0
        st.session_state.report = []
        st.session_state.game_over = False
        random.shuffle(st.session_state.questions)
        st.rerun()