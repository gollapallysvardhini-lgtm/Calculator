import streamlit as st
import math

st.set_page_config(page_title="Calculator", layout="centered")

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {display: none !important;}
    section[data-testid="stToolbar"] {display: none !important;}
    button[title="Deploy"], button[title="Share"], button[title="Settings"], button[aria-label="Deploy"], button[aria-label="Share"], button[aria-label="Settings"] {display: none !important;}
    div[title="Open navigation"] {display: none !important;}
    .stMainBlockContainer.block-container {width: 500px !important; max-width: 500px !important;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#session state
if "expression" not in st.session_state:
    st.session_state.expression = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "show_history" not in st.session_state:
    st.session_state.show_history = False

if "memory" not in st.session_state:
    st.session_state.memory = 0

#functions used in calculator
def update_expression(value):
    st.session_state.expression += str(value)

def clear():
    st.session_state.expression = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def calculate():
    try:
        exp = st.session_state.expression
        result = eval(exp)
        st.session_state.history.append(f"{exp} = {result}")
        st.session_state.expression = str(result)
    except:
        st.session_state.expression = "Error"

def square():
    try:
        val = float(st.session_state.expression)
        res = val ** 2
        st.session_state.history.append(f"{val}² = {res}")
        st.session_state.expression = str(res)
    except:
        st.session_state.expression = "Error"

def sqrt():
    try:
        val = float(st.session_state.expression)
        if val < 0:
            raise
        res = math.sqrt(val)
        st.session_state.history.append(f"√{val} = {res}")
        st.session_state.expression = str(res)
    except:
        st.session_state.expression = "Error"


def reciprocal():
    try:
        val = float(st.session_state.expression)
        if val == 0:
            raise
        res = 1 / val
        st.session_state.history.append(f"1/{val} = {res}")
        st.session_state.expression = str(res)
    except:
        st.session_state.expression = "Error"


def percent():
    try:
        val = float(st.session_state.expression)
        res = val / 100
        st.session_state.history.append(f"{val}% = {res}")
        st.session_state.expression = str(res)
    except:
        st.session_state.expression = "Error"


def clear_entry():
    st.session_state.expression = ""


def plus_minus():
    try:
        val = float(st.session_state.expression)
        if val == 0:
            st.session_state.expression = "0"
        else:
            st.session_state.expression = str(-val)
    except:
        st.session_state.expression = "Error"


def memory_clear():
    st.session_state.memory = 0


def memory_recall():
    st.session_state.expression = str(st.session_state.memory)


def memory_add():
    try:
        st.session_state.memory += float(st.session_state.expression)
    except:
        pass


def memory_subtract():
    try:
        st.session_state.memory -= float(st.session_state.expression)
    except:
        pass

#display calculator UI
st.markdown("""
<style>
.stMainBlockContainer.block-container {
    width: 500px !important;
    max-width: 500px !important;
    margin: 20px auto !important;
    padding: 20px 20px 10px 30px !important;
    background: #ffffff !important;
    border: 1px solid #959595 !important;
    border-radius: 36px !important;
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08) !important;
    box-sizing: border-box !important;
}

.display-wrapper {
    width: 100%;
    margin-bottom: 16px;
}

.display {
    background: #f8f8f8;
    color: #111;
    padding: 18px 18px;
    font-size: 28px;
    border-radius: 18px;
    text-align: right;
    height: 70px;
    border: 1px solid #8a7d7dc2;
    width: 100%;
    box-sizing: border-box;
}

.button-grid {
    width: 92%;
    margin-left: auto;
    margin-right: 0;
    padding-left: 0;
}

button {
    width: 100%;
    aspect-ratio: 1 / 1;
    font-size: 18px !important;
    margin: 0px;
    border: none !important;
    box-shadow: none !important;
    background: #d2d2d2a3 !important;
    color: #333 !important;
    border-radius: 12px !important;
}

button:hover {
    background: #b0b0b0 !important;
}

button:focus {
    outline: none !important;
}

button[title="⋯"], button[aria-label="⋯"] {
    border-radius: 12px !important;
    background: #c0c0c0 !important;
    color: #333 !important;
    font-size: 20px !important;
}

.stButton button {
    min-height: 60px !important;
}

</style>
""", unsafe_allow_html=True)

#Display and history button
cols = st.columns([0.7, 5], gap="small")
if cols[0].button("⋯", key="history_btn"):
    st.session_state.show_history = not st.session_state.show_history
cols[1].markdown(f'<div class="display">{st.session_state.expression}</div>', unsafe_allow_html=True)

#Sidebar history
if st.session_state.show_history:
    if st.session_state.history:
        for item in reversed(st.session_state.history[-10:]):
            st.sidebar.write(item)
    else:
        st.sidebar.write("No history yet.")

#Buttons
st.markdown('<div class="button-grid">', unsafe_allow_html=True)

#Memory Row
cols = st.columns(4, gap="xsmall")
cols[0].button("MC", on_click=memory_clear)
cols[1].button("MR", on_click=memory_recall)
cols[2].button("M+", on_click=memory_add)
cols[3].button("M-", on_click=memory_subtract)

#Row 1
cols = st.columns(4, gap="xsmall")
cols[0].button("%", on_click=percent)
cols[1].button("CE", on_click=clear_entry)
cols[2].button("C", on_click=clear)
cols[3].button("⌫", on_click=backspace)

#Row 2
cols = st.columns(4, gap="xsmall")
cols[0].button("1/x", on_click=reciprocal)
cols[1].button("x²", on_click=square)
cols[2].button("√", on_click=sqrt)
cols[3].button("/", on_click=lambda: update_expression("/"))

#Row 3
cols = st.columns(4, gap="xsmall")
cols[0].button("1", on_click=lambda: update_expression("1"))
cols[1].button("2", on_click=lambda: update_expression("2"))
cols[2].button("3", on_click=lambda: update_expression("3"))
cols[3].button("x", on_click=lambda: update_expression("*"))

#Row 4
cols = st.columns(4, gap="xsmall")
cols[0].button("4", on_click=lambda: update_expression("4"))
cols[1].button("5", on_click=lambda: update_expression("5"))
cols[2].button("6", on_click=lambda: update_expression("6"))
cols[3].button("-", on_click=lambda: update_expression("-"))

#Row 5
cols = st.columns(4, gap="xsmall")
cols[0].button("7", on_click=lambda: update_expression("7"))
cols[1].button("8", on_click=lambda: update_expression("8"))
cols[2].button("9", on_click=lambda: update_expression("9"))
cols[3].button("+", on_click=lambda: update_expression("+"))

#Row 6
cols = st.columns(4, gap="xsmall")
cols[0].button("+/-", on_click=plus_minus)
cols[1].button("0", on_click=lambda: update_expression("0"))
cols[2].button(".", on_click=lambda: update_expression("."))
cols[3].button("=", on_click=calculate)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.show_history:
    st.sidebar.header("History")
    for item in reversed(st.session_state.history):
        st.sidebar.write(item)