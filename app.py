import streamlit as st
import math
from decimal import Decimal, InvalidOperation

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="✨ Smart Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Google Font ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 520px; }

  /* ── Calculator card ── */
  .calc-card {
    background: linear-gradient(145deg, #1e1e2e, #181825);
    border-radius: 24px;
    padding: 28px 28px 20px 28px;
    box-shadow: 0 24px 64px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.06);
  }

  /* ── Display area ── */
  .display-wrapper {
    background: rgba(0,0,0,0.35);
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.07);
    min-height: 90px;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-end;
    word-break: break-all;
  }
  .display-expr {
    color: #6c7086;
    font-size: 0.9rem;
    margin-bottom: 4px;
    min-height: 20px;
    word-break: break-all;
    text-align: right;
  }
  .display-val {
    color: #cdd6f4;
    font-size: 2.2rem;
    font-weight: 700;
    text-align: right;
    letter-spacing: -1px;
  }

  /* ── Button grid ── */
  .stButton > button {
    width: 100% !important;
    height: 64px !important;
    border-radius: 14px !important;
    border: none !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    cursor: pointer !important;
    transition: all 0.12s ease !important;
    letter-spacing: 0.3px !important;
  }
  .stButton > button:active {
    transform: scale(0.94) !important;
  }

  /* Number buttons */
  div[data-testid="column"]:has(button[kind="secondary"]) .stButton > button {
    background: #313244 !important;
    color: #cdd6f4 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
  }
  div[data-testid="column"]:has(button[kind="secondary"]) .stButton > button:hover {
    background: #45475a !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.4) !important;
  }

  /* Operator buttons */
  div[data-testid="column"]:has(button[kind="primary"]) .stButton > button {
    background: linear-gradient(135deg, #cba6f7, #b4befe) !important;
    color: #1e1e2e !important;
    box-shadow: 0 4px 16px rgba(203,166,247,0.35) !important;
  }
  div[data-testid="column"]:has(button[kind="primary"]) .stButton > button:hover {
    background: linear-gradient(135deg, #d4b2ff, #c5cafe) !important;
    box-shadow: 0 6px 24px rgba(203,166,247,0.5) !important;
  }

  /* Equals button */
  .eq-btn .stButton > button {
    background: linear-gradient(135deg, #a6e3a1, #94e2d5) !important;
    color: #1e1e2e !important;
    font-size: 1.4rem !important;
    box-shadow: 0 4px 18px rgba(166,227,161,0.4) !important;
  }
  .eq-btn .stButton > button:hover {
    background: linear-gradient(135deg, #b8f0b3, #a6ede4) !important;
    box-shadow: 0 6px 26px rgba(166,227,161,0.55) !important;
  }

  /* Clear button */
  .clear-btn .stButton > button {
    background: linear-gradient(135deg, #f38ba8, #eba0ac) !important;
    color: #1e1e2e !important;
    box-shadow: 0 4px 16px rgba(243,139,168,0.35) !important;
  }
  .clear-btn .stButton > button:hover {
    background: linear-gradient(135deg, #f7a3bc, #f0b3bc) !important;
    box-shadow: 0 6px 24px rgba(243,139,168,0.5) !important;
  }

  /* Backspace / util buttons */
  .util-btn .stButton > button {
    background: #45475a !important;
    color: #f5c2e7 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
  }
  .util-btn .stButton > button:hover {
    background: #585b70 !important;
  }

  /* History sidebar */
  .history-item {
    background: rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 8px;
    border-left: 3px solid #cba6f7;
    font-size: 0.88rem;
    color: #a6adc8;
  }
  .history-expr { color: #6c7086; font-size: 0.8rem; }
  .history-result { color: #cdd6f4; font-weight: 600; font-size: 1rem; }

  /* Title */
  .calc-title {
    text-align: center;
    color: #cdd6f4;
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin-bottom: 20px;
  }
  .calc-title span { color: #cba6f7; }
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ─────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "display":     "0",
        "expression":  "",
        "history":     [],
        "just_equal":  False,
        "error":       False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─── Core Logic ────────────────────────────────────────────────────────────────
def safe_eval(expr: str):
    """Evaluate arithmetic expression safely."""
    try:
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expr):
            return None, "Invalid characters"
        result = eval(expr, {"__builtins__": {}})  # nosec
        return result, None
    except ZeroDivisionError:
        return None, "Division by zero!"
    except Exception:
        return None, "Invalid expression"


def fmt(value) -> str:
    """Format number: strip unnecessary decimals, handle large nums."""
    if isinstance(value, float):
        if value != value:      # NaN
            return "Error"
        if abs(value) == float('inf'):
            return "∞"
        # Use Decimal for clean formatting
        try:
            d = Decimal(str(value))
            formatted = f"{d:.10f}".rstrip('0').rstrip('.')
            return formatted
        except InvalidOperation:
            return str(value)
    return str(value)


def on_digit(char: str):
    s = st.session_state
    if s.error or s.just_equal:
        s.display = char
        s.expression = ""
        s.error = False
        s.just_equal = False
    elif s.display == "0" and char != ".":
        s.display = char
    elif char == "." and "." in s.display:
        return
    else:
        s.display += char


def on_operator(op: str):
    s = st.session_state
    s.error = False
    # Append current display value + operator to expression
    if s.just_equal:
        # continue chaining from result
        s.expression = s.display + " " + op + " "
        s.just_equal = False
    elif s.expression.endswith(("+ ", "- ", "* ", "/ ")):
        # Replace last operator
        s.expression = s.expression[:-2] + op + " "
    else:
        s.expression += s.display + " " + op + " "
        s.display = "0"


def on_equal():
    s = st.session_state
    if not s.expression:
        return
    full_expr = s.expression + s.display
    # Build display-friendly expression
    disp_expr = full_expr
    result, err = safe_eval(full_expr.replace(" ", ""))
    if err:
        s.history.insert(0, {"expr": disp_expr, "result": err})
        s.display = err
        s.expression = ""
        s.error = True
    else:
        formatted = fmt(result)
        s.history.insert(0, {"expr": disp_expr, "result": formatted})
        if len(s.history) > 20:
            s.history = s.history[:20]
        s.display = formatted
        s.expression = disp_expr + " ="
        s.just_equal = True


def on_clear():
    s = st.session_state
    s.display = "0"
    s.expression = ""
    s.error = False
    s.just_equal = False


def on_backspace():
    s = st.session_state
    if s.error or s.just_equal:
        on_clear()
        return
    if len(s.display) > 1:
        s.display = s.display[:-1]
    else:
        s.display = "0"


def on_percent():
    s = st.session_state
    try:
        val = float(s.display) / 100
        s.display = fmt(val)
    except Exception:
        pass


def on_sign():
    s = st.session_state
    if s.display.startswith("-"):
        s.display = s.display[1:]
    elif s.display != "0":
        s.display = "-" + s.display


# ─── Layout ────────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([3, 1.2])

with left_col:
    # Title
    st.markdown('<div class="calc-title">🧮 <span>Smart</span> Calculator</div>', unsafe_allow_html=True)

    # Display
    expr_text = st.session_state.expression or ""
    disp_text = st.session_state.display
    st.markdown(f"""
    <div class="calc-card">
      <div class="display-wrapper">
        <div class="display-expr">{expr_text}&nbsp;</div>
        <div class="display-val">{disp_text}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")  # spacer

    # ── Button Grid ──────────────────────────────────────────────────────────
    # Row 1: AC  +/-  %  ÷
    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    with r1c1:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("AC", key="ac", use_container_width=True):
            on_clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with r1c2:
        st.markdown('<div class="util-btn">', unsafe_allow_html=True)
        if st.button("+/-", key="sign", use_container_width=True):
            on_sign()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with r1c3:
        st.markdown('<div class="util-btn">', unsafe_allow_html=True)
        if st.button("%", key="pct", use_container_width=True):
            on_percent()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with r1c4:
        if st.button("÷", key="div", type="primary", use_container_width=True):
            on_operator("/")
            st.rerun()

    # Row 2: 7  8  9  ×
    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    with r2c1:
        if st.button("7", key="7", use_container_width=True):
            on_digit("7"); st.rerun()
    with r2c2:
        if st.button("8", key="8", use_container_width=True):
            on_digit("8"); st.rerun()
    with r2c3:
        if st.button("9", key="9", use_container_width=True):
            on_digit("9"); st.rerun()
    with r2c4:
        if st.button("×", key="mul", type="primary", use_container_width=True):
            on_operator("*"); st.rerun()

    # Row 3: 4  5  6  −
    r3c1, r3c2, r3c3, r3c4 = st.columns(4)
    with r3c1:
        if st.button("4", key="4", use_container_width=True):
            on_digit("4"); st.rerun()
    with r3c2:
        if st.button("5", key="5", use_container_width=True):
            on_digit("5"); st.rerun()
    with r3c3:
        if st.button("6", key="6", use_container_width=True):
            on_digit("6"); st.rerun()
    with r3c4:
        if st.button("−", key="sub", type="primary", use_container_width=True):
            on_operator("-"); st.rerun()

    # Row 4: 1  2  3  +
    r4c1, r4c2, r4c3, r4c4 = st.columns(4)
    with r4c1:
        if st.button("1", key="1", use_container_width=True):
            on_digit("1"); st.rerun()
    with r4c2:
        if st.button("2", key="2", use_container_width=True):
            on_digit("2"); st.rerun()
    with r4c3:
        if st.button("3", key="3", use_container_width=True):
            on_digit("3"); st.rerun()
    with r4c4:
        if st.button("+", key="add", type="primary", use_container_width=True):
            on_operator("+"); st.rerun()

    # Row 5: 0 (wide)  .  ⌫  =
    r5c1, r5c2, r5c3, r5c4 = st.columns([2, 1, 1, 1])
    with r5c1:
        if st.button("0", key="0", use_container_width=True):
            on_digit("0"); st.rerun()
    with r5c2:
        if st.button(".", key="dot", use_container_width=True):
            on_digit("."); st.rerun()
    with r5c3:
        st.markdown('<div class="util-btn">', unsafe_allow_html=True)
        if st.button("⌫", key="bsp", use_container_width=True):
            on_backspace(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with r5c4:
        st.markdown('<div class="eq-btn">', unsafe_allow_html=True)
        if st.button("=", key="eq", use_container_width=True):
            on_equal(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── History panel ─────────────────────────────────────────────────────────────
with right_col:
    st.markdown("### 📋 History")
    if not st.session_state.history:
        st.markdown('<p style="color:#585b70;font-size:0.85rem;">No calculations yet.</p>', unsafe_allow_html=True)
    else:
        if st.button("🗑️ Clear", key="clrhist", use_container_width=True):
            st.session_state.history = []
            st.rerun()
        for item in st.session_state.history:
            st.markdown(f"""
            <div class="history-item">
              <div class="history-expr">{item['expr']}</div>
              <div class="history-result">= {item['result']}</div>
            </div>
            """, unsafe_allow_html=True)
