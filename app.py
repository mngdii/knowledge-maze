import streamlit as st
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Pre-Calc 12 Mastery Maze", page_icon="📐", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #4CAF50; color: white; font-weight: bold; }
    .report-card { background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 20px; }
    .user-ans { color: #e74c3c; font-weight: bold; } /* 红色 - 用户答案 */
    .correct-ans { color: #2e86c1; font-weight: bold; } /* 蓝色 - 正确答案 */
    .explanation { background-color: #fdf2e9; padding: 10px; border-left: 5px solid #e67e22; margin-top: 10px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# --- QUESTION DATABASE (Added Explanations) ---
DB = {
    "Logarithms & Exponentials": [
        {
            "topic": "Basic Logarithms",
            "q": "Simplify: log(1000)",
            "a": "3",
            "exp": "Since the base is 10, log(1000) = log(10³). By the power rule, it equals 3."
        },
        {
            "topic": "Negative Exponents",
            "q": "Simplify: log_x(1/x^3)",
            "a": "-3",
            "exp": "1/x³ can be written as x⁻³. Therefore, log_x(x⁻³) = -3."
        },
        {
            "topic": "Changing Bases",
            "q": "Simplify: log_8(32)",
            "a": "5/3",
            "exp": "Using change of base: log(32)/log(8) = log(2⁵)/log(2³) = 5/3."
        },
        {
            "topic": "Exponential Equations",
            "q": "Solve: 4^(x^2 - 2x) = 8^(1 - x)",
            "a": "3/2, -1",
            "exp": "Set bases to 2: 2^(2(x²-2x)) = 2^(3(1-x)). Solving 2x²-4x = 3-3x leads to (2x-3)(x+1)=0."
        },
        {
            "topic": "Logarithmic Identity",
            "q": "Solve for x: 9^(log_3(6)) = x",
            "a": "36",
            "exp": "Rewrite 9 as 3². So (3²)^(log_3(6)) = 3^(2*log_3(6)) = 3^(log_3(6²)) = 6² = 36."
        },
        {
            "topic": "Compound Interest",
            "q": "Years for $1250 to become $7000 at 6.75% quarterly? (Round to 1 decimal)",
            "a": "25.7",
            "exp": "Use A = P(1 + r/n)^(nt). 7000 = 1250(1 + 0.0675/4)^(4t). Solving with logs gives t ≈ 25.7."
        },
        {
            "topic": "Log Expressions",
            "q": "If log 5 = a and log 36 = b, express log(6/25) in terms of a and b",
            "a": "1/2b-2a",
            "exp": "log(6/25) = log(6) - log(25) = log(36^0.5) - log(5²) = 1/2*log(36) - 2*log(5) = 1/2b - 2a."
        }
    ]
}

# --- INITIALIZATION ---
if 'menu' not in st.session_state: st.session_state.menu = True
if 'curr' not in st.session_state: st.session_state.curr = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'report' not in st.session_state: st.session_state.report = []
if 'done' not in st.session_state: st.session_state.done = False

# --- UI: MAIN MENU ---
if st.session_state.menu:
    st.title("🎓 Pre-Calculus 12 Mastery Maze")
    st.write("Welcome to the diagnostic learning system. Select your unit:")
    for unit in DB.keys():
        if st.button(f"Begin {unit} Adventure"):
            st.session_state.questions = DB[unit]
            random.shuffle(st.session_state.questions)
            st.session_state.menu = False
            st.rerun()

# --- UI: MAZE INTERFACE ---
elif not st.session_state.done:
    q_list = st.session_state.questions
    idx = st.session_state.curr
    q_item = q_list[idx]

    st.progress(idx / len(q_list), text=f"Question {idx+1} of {len(q_list)}")
    st.subheader(q_item['q'])
    user_input = st.text_input("Answer:", key=f"input_{idx}")

    if st.button("Submit Answer"):
        is_correct = user_input.replace(" ","").lower() == q_item['a'].replace(" ","").lower()
        if is_correct: st.session_state.score += 1
        
        # 记录详细报告：原题、用户答案、正确答案、解析
        st.session_state.report.append({
            "question": q_item['q'],
            "user_ans": user_input if user_input else "(Empty)",
            "correct_ans": q_item['a'],
            "is_correct": is_correct,
            "explanation": q_item['exp']
        })

        if idx + 1 < len(q_list):
            st.session_state.curr += 1
        else:
            st.session_state.done = True
        st.rerun()

# --- UI: ENHANCED DIAGNOSTIC REPORT ---
else:
    st.balloons()
    st.header("📊 Final Diagnostic Report")
    st.metric("Final Score", f"{st.session_state.score}/{len(st.session_state.questions)}")
    
    st.markdown("---")
    
    for i, item in enumerate(st.session_state.report):
        with st.container():
            # 使用 Markdown 渲染自定义颜色的报告卡
            status_icon = "✅" if item['is_correct'] else "❌"
            st.markdown(f"""
            <div class="report-card">
                <h4>Question {i+1}: {item['question']}</h4>
                <p><b>Your Answer:</b> <span class="user-ans">{item['user_ans']}</span> {status_icon}</p>
                <p><b>Correct Answer:</b> <span class="correct-ans">{item['correct_ans']}</span></p>
                <div class="explanation">
                    <b>Tutor's Explanation:</b><br>{item['explanation']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    if st.button("Return to Main Menu"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
