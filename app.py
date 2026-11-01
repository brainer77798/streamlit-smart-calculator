import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sympy as sp
import math
from decimal import Decimal, InvalidOperation

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OmniCalc | Ultimate Scientific & Graphing Calculator",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS for Sleek Catppuccin Mocha UI ──────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
  }
  code, pre, .mono-font {
    font-family: 'JetBrains Mono', monospace !important;
  }

  /* Main container adjustments */
  .block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1200px;
  }

  /* Top Navigation Bar Branding */
  .brand-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 24px;
    background: linear-gradient(90deg, #181825, #1e1e2e);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 24px;
  }
  .brand-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #cdd6f4;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .brand-title span {
    background: linear-gradient(135deg, #cba6f7, #89b4fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .brand-subtitle {
    font-size: 0.85rem;
    color: #a6adc8;
    background: rgba(203, 166, 247, 0.1);
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid rgba(203, 166, 247, 0.25);
  }

  /* Calculator Display Container */
  .calc-card {
    background: #181825;
    border-radius: 22px;
    padding: 22px;
    border: 1px solid rgba(255, 255, 255, 0.07);
    box-shadow: 0 16px 48px rgba(0,0,0,0.45);
  }
  .display-box {
    background: #11111b;
    border-radius: 14px;
    padding: 18px 22px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 18px;
    text-align: right;
  }
  .display-history {
    color: #6c7086;
    font-size: 0.95rem;
    min-height: 24px;
    font-family: 'JetBrains Mono', monospace;
  }
  .display-main {
    color: #cdd6f4;
    font-size: 2.3rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.5px;
    overflow-x: auto;
    white-space: nowrap;
  }

  /* History list styling */
  .history-card {
    background: #181825;
    border-radius: 16px;
    padding: 14px 18px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 10px;
    transition: all 0.2s ease;
  }
  .history-card:hover {
    border-color: rgba(203, 166, 247, 0.4);
    transform: translateY(-1px);
  }
  .hist-expr {
    color: #9399b2;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
  }
  .hist-res {
    color: #a6e3a1;
    font-size: 1.15rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
  }

  /* Feature callout panels */
  .callout-box {
    background: #1e1e2e;
    border-radius: 14px;
    padding: 18px;
    border-left: 4px solid #cba6f7;
    margin-bottom: 16px;
  }

  /* Button sizing and style overhaul */
  .stButton > button {
    height: 54px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    font-family: 'JetBrains Mono', sans-serif !important;
    transition: all 0.15s ease-in-out !important;
  }
  .stButton > button:active {
    transform: scale(0.96) !important;
  }
</style>
""", unsafe_allow_html=True)

# ─── App Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-header">
  <div class="brand-title">
    🧮 <span>OmniCalc Pro</span>
  </div>
  <div class="brand-subtitle">
    Standard • Scientific • Graphing • Programmer • Financial • Units
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Session State Initializer ─────────────────────────────────────────────────
def get_session():
    defaults = {
        "std_display": "0",
        "std_expr": "",
        "std_just_eval": False,
        "std_history": [],
        "sci_display": "0",
        "sci_expr": "",
        "sci_just_eval": False,
        "sci_angle_unit": "Rad",
        "sci_history": []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

get_session()

# ─── Navigation Tabs ───────────────────────────────────────────────────────────
tabs = st.tabs([
    "🧮 Standard",
    "🔬 Scientific & Calculus",
    "📈 Graphing Studio",
    "💻 Programmer",
    "💰 Financial & Loan",
    "📐 Unit Converter"
])

# ==============================================================================
# TAB 1: STANDARD CALCULATOR
# ==============================================================================
with tabs[0]:
    s_col, h_col = st.columns([2.5, 1.5], gap="large")

    def std_digit(char):
        s = st.session_state
        if s.std_just_eval:
            s.std_display = char
            s.std_expr = ""
            s.std_just_eval = False
        elif s.std_display == "0" and char != ".":
            s.std_display = char
        elif char == "." and "." in s.std_display:
            return
        else:
            s.std_display += char

    def std_op(op):
        s = st.session_state
        if s.std_just_eval:
            s.std_expr = s.std_display + " " + op + " "
            s.std_just_eval = False
        elif s.std_expr.endswith(("+ ", "- ", "* ", "/ ")):
            s.std_expr = s.std_expr[:-2] + op + " "
        else:
            s.std_expr += s.std_display + " " + op + " "
            s.std_display = "0"

    def std_equal():
        s = st.session_state
        if not s.std_expr:
            return
        full_expr = s.std_expr + s.std_display
        try:
            allowed = set("0123456789+-*/.() ")
            if not all(c in allowed for c in full_expr):
                raise ValueError("Invalid tokens")
            raw_res = eval(full_expr, {"__builtins__": {}})
            # Format nicely
            if isinstance(raw_res, float):
                dec = Decimal(str(raw_res))
                res_str = f"{dec:.10f}".rstrip('0').rstrip('.')
            else:
                res_str = str(raw_res)
            s.std_history.insert(0, {"expr": full_expr, "res": res_str})
            s.std_display = res_str
            s.std_expr = full_expr + " ="
            s.std_just_eval = True
        except ZeroDivisionError:
            s.std_display = "Cannot divide by 0"
            s.std_just_eval = True
        except Exception:
            s.std_display = "Error"
            s.std_just_eval = True

    def std_clear():
        s = st.session_state
        s.std_display = "0"
        s.std_expr = ""
        s.std_just_eval = False

    def std_backspace():
        s = st.session_state
        if s.std_just_eval or len(s.std_display) <= 1:
            s.std_display = "0"
            s.std_just_eval = False
        else:
            s.std_display = s.std_display[:-1]

    def std_percent():
        s = st.session_state
        try:
            val = float(s.std_display) / 100
            s.std_display = f"{Decimal(str(val)):.10f}".rstrip('0').rstrip('.')
        except Exception:
            pass

    def std_sign():
        s = st.session_state
        if s.std_display.startswith("-"):
            s.std_display = s.std_display[1:]
        elif s.std_display != "0":
            s.std_display = "-" + s.std_display

    with s_col:
        st.markdown(f"""
        <div class="calc-card">
          <div class="display-box">
            <div class="display-history">{st.session_state.std_expr}&nbsp;</div>
            <div class="display-main">{st.session_state.std_display}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        # Buttons Grid
        # Row 1
        b1, b2, b3, b4 = st.columns(4)
        if b1.button("AC", key="std_ac", use_container_width=True): std_clear(); st.rerun()
        if b2.button("+/-", key="std_sign", use_container_width=True): std_sign(); st.rerun()
        if b3.button("%", key="std_pct", use_container_width=True): std_percent(); st.rerun()
        if b4.button("÷", key="std_div", type="primary", use_container_width=True): std_op("/"); st.rerun()

        # Row 2
        b5, b6, b7, b8 = st.columns(4)
        if b5.button("7", key="std_7", use_container_width=True): std_digit("7"); st.rerun()
        if b6.button("8", key="std_8", use_container_width=True): std_digit("8"); st.rerun()
        if b7.button("9", key="std_9", use_container_width=True): std_digit("9"); st.rerun()
        if b8.button("×", key="std_mul", type="primary", use_container_width=True): std_op("*"); st.rerun()

        # Row 3
        b9, b10, b11, b12 = st.columns(4)
        if b9.button("4", key="std_4", use_container_width=True): std_digit("4"); st.rerun()
        if b10.button("5", key="std_5", use_container_width=True): std_digit("5"); st.rerun()
        if b11.button("6", key="std_6", use_container_width=True): std_digit("6"); st.rerun()
        if b12.button("−", key="std_sub", type="primary", use_container_width=True): std_op("-"); st.rerun()

        # Row 4
        b13, b14, b15, b16 = st.columns(4)
        if b13.button("1", key="std_1", use_container_width=True): std_digit("1"); st.rerun()
        if b14.button("2", key="std_2", use_container_width=True): std_digit("2"); st.rerun()
        if b15.button("3", key="std_3", use_container_width=True): std_digit("3"); st.rerun()
        if b16.button("+", key="std_add", type="primary", use_container_width=True): std_op("+"); st.rerun()

        # Row 5
        b17, b18, b19, b20 = st.columns([2, 1, 1, 1])
        if b17.button("0", key="std_0", use_container_width=True): std_digit("0"); st.rerun()
        if b18.button(".", key="std_dot", use_container_width=True): std_digit("."); st.rerun()
        if b19.button("⌫", key="std_bsp", use_container_width=True): std_backspace(); st.rerun()
        if b20.button("=", key="std_eq", type="primary", use_container_width=True): std_equal(); st.rerun()

    with h_col:
        st.subheader("📋 History Log")
        if st.session_state.std_history:
            if st.button("🗑️ Clear History", key="std_clr_hist", use_container_width=True):
                st.session_state.std_history = []
                st.rerun()
            for item in st.session_state.std_history[:15]:
                st.markdown(f"""
                <div class="history-card">
                  <div class="hist-expr">{item['expr']}</div>
                  <div class="hist-res">= {item['res']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No calculations yet. Enter operations to see history.")

# ==============================================================================
# TAB 2: SCIENTIFIC & CALCULUS
# ==============================================================================
with tabs[1]:
    sci_l, sci_r = st.columns([1.6, 1.4], gap="large")

    with sci_l:
        st.markdown("### 🔬 Scientific Formula Evaluator")
        
        angle_mode = st.radio("Angle Mode", ["Degrees", "Radians"], horizontal=True, key="sci_angle_select")

        expr_input = st.text_input(
            "Enter Mathematical Expression",
            value="sin(pi / 4) + sqrt(144) * log10(100)",
            help="Supports sin, cos, tan, sqrt, log, log10, exp, factorial, pi, e, powers (^ or **)"
        )

        col_fn1, col_fn2, col_fn3, col_fn4, col_fn5 = st.columns(5)
        with col_fn1:
            if st.button("sin(x)", key="btn_sin", use_container_width=True):
                st.info("Example: `sin(pi/2)` or `sin(90)` in Degrees")
            if st.button("x²", key="btn_sq", use_container_width=True):
                st.info("Example: `5**2` or `5^2`")
        with col_fn2:
            if st.button("cos(x)", key="btn_cos", use_container_width=True):
                st.info("Example: `cos(0)` or `cos(pi)`")
            if st.button("xʸ", key="btn_pow", use_container_width=True):
                st.info("Example: `2**8`")
        with col_fn3:
            if st.button("tan(x)", key="btn_tan", use_container_width=True):
                st.info("Example: `tan(pi/4)`")
            if st.button("√x", key="btn_sqrt", use_container_width=True):
                st.info("Example: `sqrt(16)`")
        with col_fn4:
            if st.button("ln(x)", key="btn_ln", use_container_width=True):
                st.info("Example: `log(e)` for natural log")
            if st.button("log₁₀(x)", key="btn_log10", use_container_width=True):
                st.info("Example: `log10(1000)`")
        with col_fn5:
            if st.button("x!", key="btn_fact", use_container_width=True):
                st.info("Example: `factorial(5)`")
            if st.button("π & e", key="btn_const", use_container_width=True):
                st.info("Constants: `pi`, `e`")

        eval_btn = st.button("🚀 Calculate Value", key="sci_eval_action", type="primary", use_container_width=True)

        if eval_btn or expr_input:
            clean_expr = expr_input.replace("^", "**")
            # Build safe math context
            is_deg = (angle_mode == "Degrees")
            ctx = {
                "pi": math.pi,
                "e": math.e,
                "sqrt": math.sqrt,
                "log": math.log,
                "log10": math.log10,
                "log2": math.log2,
                "exp": math.exp,
                "factorial": math.factorial,
                "abs": abs,
                "sin": (lambda x: math.sin(math.radians(x))) if is_deg else math.sin,
                "cos": (lambda x: math.cos(math.radians(x))) if is_deg else math.cos,
                "tan": (lambda x: math.tan(math.radians(x))) if is_deg else math.tan,
                "asin": (lambda x: math.degrees(math.asin(x))) if is_deg else math.asin,
                "acos": (lambda x: math.degrees(math.acos(x))) if is_deg else math.acos,
                "atan": (lambda x: math.degrees(math.atan(x))) if is_deg else math.atan,
                "sinh": math.sinh,
                "cosh": math.cosh,
                "tanh": math.tanh,
            }
            try:
                val = eval(clean_expr, {"__builtins__": {}}, ctx)
                st.markdown(f"""
                <div style="background:#11111b; border: 1px solid #a6e3a1; border-radius: 14px; padding: 18px 24px; margin-top: 15px;">
                  <div style="color: #6c7086; font-size: 0.85rem; font-family:'JetBrains Mono';">RESULT</div>
                  <div style="color: #a6e3a1; font-size: 2rem; font-weight: 700; font-family:'JetBrains Mono';">{val}</div>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Calculation Error: {e}")

    with sci_r:
        st.markdown("### 📐 Symbolic Calculus Engine (SymPy)")
        st.markdown("Perform exact derivatives, integrals, limits, and expansions symbolically.")

        sym_x = sp.Symbol('x')
        sym_input = st.text_input("Enter f(x):", value="x**3 * sin(x) - 4*x + 1", key="sym_expr_in")
        
        calc_mode = st.selectbox("Calculus Operation", [
            "Derivative: d/dx f(x)",
            "Second Derivative: d²/dx² f(x)",
            "Indefinite Integral: ∫ f(x) dx",
            "Definite Integral: ∫[a, b] f(x) dx",
            "Limit: lim_{x -> a} f(x)",
            "Taylor Series Expansion"
        ])

        try:
            parsed_sym = sp.sympify(sym_input.replace("^", "**"))
            st.latex(f"f(x) = {sp.latex(parsed_sym)}")

            if calc_mode == "Derivative: d/dx f(x)":
                diff_res = sp.diff(parsed_sym, sym_x)
                st.markdown("**First Derivative:**")
                st.latex(f"\\frac{{d}}{{dx}} f(x) = {sp.latex(diff_res)}")
                st.markdown(f"`Simplified:` `{sp.simplify(diff_res)}`")

            elif calc_mode == "Second Derivative: d²/dx² f(x)":
                diff2_res = sp.diff(parsed_sym, sym_x, 2)
                st.markdown("**Second Derivative:**")
                st.latex(f"\\frac{{d^2}}{{dx^2}} f(x) = {sp.latex(diff2_res)}")

            elif calc_mode == "Indefinite Integral: ∫ f(x) dx":
                int_res = sp.integrate(parsed_sym, sym_x)
                st.markdown("**Indefinite Integral:**")
                st.latex(f"\\int f(x) dx = {sp.latex(int_res)} + C")

            elif calc_mode == "Definite Integral: ∫[a, b] f(x) dx":
                c_a, c_b = st.columns(2)
                with c_a: a_val = st.number_input("Lower limit (a):", value=0.0)
                with c_b: b_val = st.number_input("Upper limit (b):", value=3.14159)
                def_res = sp.integrate(parsed_sym, (sym_x, a_val, b_val))
                st.markdown("**Definite Integral Result:**")
                st.latex(f"\\int_{{{a_val}}}^{{{b_val}}} f(x) dx = {float(def_res):.6f}")

            elif calc_mode == "Limit: lim_{x -> a} f(x)":
                lim_pt = st.number_input("Limit point (a):", value=0.0)
                lim_res = sp.limit(parsed_sym, sym_x, lim_pt)
                st.markdown(f"**Limit as x → {lim_pt}:**")
                st.latex(f"\\lim_{{x \\to {lim_pt}}} f(x) = {sp.latex(lim_res)}")

            elif calc_mode == "Taylor Series Expansion":
                order_n = st.slider("Expansion Order:", min_value=1, max_value=8, value=4)
                series_res = sp.series(parsed_sym, sym_x, 0, order_n)
                st.markdown(f"**Taylor Series around x=0 (O(x^{order_n})):**")
                st.latex(f"{sp.latex(series_res)}")

        except Exception as sym_err:
            st.warning(f"SymPy parser note: {sym_err}")

# ==============================================================================
# TAB 3: GRAPHING STUDIO
# ==============================================================================
with tabs[2]:
    st.markdown("### 📈 Interactive Function Grapher")

    graph_ctrl, graph_view = st.columns([1.1, 2.2], gap="large")

    with graph_ctrl:
        preset_choice = st.selectbox("Quick Function Presets", [
            "Custom Function",
            "Damped Harmonic: exp(-0.2*x) * sin(2*x)",
            "Cubic Polynomial: x**3 - 3*x**2 - x + 3",
            "Gaussian Distribution: exp(-x**2 / 2) / sqrt(2*pi)",
            "Wave Superposition: sin(x) + sin(2.5*x) + 0.5*cos(4*x)",
            "Rational Function: (x**2 - 1) / (x**2 + 1)",
            "Sigmoid Curve: 1 / (1 + exp(-x))"
        ])

        preset_defaults = {
            "Custom Function": "sin(x) * cos(0.5*x)",
            "Damped Harmonic: exp(-0.2*x) * sin(2*x)": "exp(-0.2*x) * sin(2*x)",
            "Cubic Polynomial: x**3 - 3*x**2 - x + 3": "x**3 - 3*x**2 - x + 3",
            "Gaussian Distribution: exp(-x**2 / 2) / sqrt(2*pi)": "exp(-x**2 / 2) / sqrt(2*pi)",
            "Wave Superposition: sin(x) + sin(2.5*x) + 0.5*cos(4*x)": "sin(x) + sin(2.5*x) + 0.5*cos(4*x)",
            "Rational Function: (x**2 - 1) / (x**2 + 1)": "(x**2 - 1) / (x**2 + 1)",
            "Sigmoid Curve: 1 / (1 + exp(-x))": "1 / (1 + exp(-x))"
        }

        default_f1 = preset_defaults[preset_choice]

        f1_str = st.text_input("f₁(x):", value=default_f1, key="graph_f1")
        enable_f2 = st.checkbox("Overlay second function f₂(x)", value=False)
        f2_str = st.text_input("f₂(x):", value="cos(x)", key="graph_f2") if enable_f2 else None

        show_derivative = st.checkbox("Plot numerical derivative f'₁(x)", value=False)
        fill_integral = st.checkbox("Highlight integral area under f₁(x)", value=False)

        st.markdown("---")
        x_min, x_max = st.slider("X-Axis Domain", min_value=-20.0, max_value=20.0, value=(-6.28, 6.28), step=0.1)
        points_count = st.select_slider("Resolution (Sampling Points)", options=[200, 500, 1000, 2000], value=500)

    with graph_view:
        # Generate plot data
        xs = np.linspace(x_min, x_max, points_count)
        
        # NumPy evaluation dictionary
        np_scope = {
            "x": xs,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "sqrt": np.sqrt,
            "exp": np.exp,
            "log": np.log,
            "log10": np.log10,
            "pi": np.pi,
            "e": np.e,
            "abs": np.abs,
        }

        fig = go.Figure()

        try:
            clean_f1 = f1_str.replace("^", "**")
            y1 = eval(clean_f1, {"__builtins__": {}}, np_scope)
            
            # Primary Curve
            fill_style = 'tozeroy' if fill_integral else None
            fill_color = 'rgba(203, 166, 247, 0.15)' if fill_integral else None
            
            fig.add_trace(go.Scatter(
                x=xs, y=y1,
                name="f₁(x)",
                mode="lines",
                line=dict(color="#cba6f7", width=3),
                fill=fill_style,
                fillcolor=fill_color,
                hovertemplate="x: %{x:.3f}<br>f₁(x): %{y:.3f}<extra></extra>"
            ))

            # Numerical Derivative
            if show_derivative:
                dy1 = np.gradient(y1, xs)
                fig.add_trace(go.Scatter(
                    x=xs, y=dy1,
                    name="f'₁(x) [Derivative]",
                    mode="lines",
                    line=dict(color="#f38ba8", width=2, dash="dash"),
                    hovertemplate="x: %{x:.3f}<br>f'₁(x): %{y:.3f}<extra></extra>"
                ))

            # Secondary Curve
            if enable_f2 and f2_str:
                clean_f2 = f2_str.replace("^", "**")
                y2 = eval(clean_f2, {"__builtins__": {}}, np_scope)
                fig.add_trace(go.Scatter(
                    x=xs, y=y2,
                    name="f₂(x)",
                    mode="lines",
                    line=dict(color="#89b4fa", width=2.5),
                    hovertemplate="x: %{x:.3f}<br>f₂(x): %{y:.3f}<extra></extra>"
                ))

            # Zero-crossing roots detection
            roots = []
            for i in range(len(y1) - 1):
                if np.isfinite(y1[i]) and np.isfinite(y1[i+1]):
                    if (y1[i] <= 0 and y1[i+1] >= 0) or (y1[i] >= 0 and y1[i+1] <= 0):
                        # Linear interpolation for zero
                        x_zero = xs[i] - y1[i] * (xs[i+1] - xs[i]) / (y1[i+1] - y1[i] + 1e-12)
                        roots.append(x_zero)

            if roots and len(roots) <= 15:
                fig.add_trace(go.Scatter(
                    x=roots, y=[0]*len(roots),
                    name="Roots (f(x)=0)",
                    mode="markers",
                    marker=dict(color="#a6e3a1", size=9, symbol="diamond"),
                    hovertemplate="Root at x = %{x:.4f}<extra></extra>"
                ))

            # Extrema detection
            valid_y = y1[np.isfinite(y1)]
            if len(valid_y) > 0:
                min_val, max_val = float(np.min(valid_y)), float(np.max(valid_y))
                st.caption(f"📊 **Domain Extremes on Range:** Min = `{min_val:.4f}` | Max = `{max_val:.4f}` | Detected Zeros = `{len(roots)}`")

        except Exception as plot_err:
            st.error(f"Function Plot Error: {plot_err}")

        # Modern Catppuccin Theme Styling for Plotly
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#181825",
            plot_bgcolor="#11111b",
            font=dict(family="Plus Jakarta Sans", color="#cdd6f4"),
            margin=dict(l=30, r=20, t=30, b=30),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor="rgba(24, 24, 37, 0.8)",
                bordercolor="rgba(255, 255, 255, 0.1)",
                borderwidth=1
            ),
            xaxis=dict(
                gridcolor="rgba(255, 255, 255, 0.08)",
                zerolinecolor="rgba(203, 166, 247, 0.4)",
                zerolinewidth=2
            ),
            yaxis=dict(
                gridcolor="rgba(255, 255, 255, 0.08)",
                zerolinecolor="rgba(203, 166, 247, 0.4)",
                zerolinewidth=2
            ),
            height=480
        )

        st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# TAB 4: PROGRAMMER CALCULATOR
# ==============================================================================
with tabs[3]:
    st.markdown("### 💻 Programmer & Base Conversion Matrix")

    prog_col1, prog_col2 = st.columns([1.2, 1.8], gap="large")

    with prog_col1:
        base_type = st.selectbox("Input Number Base", ["Decimal (DEC)", "Hexadecimal (HEX)", "Binary (BIN)", "Octal (OCT)"])
        prog_in = st.text_input("Enter Value", value="255", key="prog_val_in")
        word_size = st.selectbox("Word Size", ["64-bit (QWORD)", "32-bit (DWORD)", "16-bit (WORD)", "8-bit (BYTE)"])

        masks = {
            "64-bit (QWORD)": (1 << 64) - 1,
            "32-bit (DWORD)": (1 << 32) - 1,
            "16-bit (WORD)": (1 << 16) - 1,
            "8-bit (BYTE)": 0xFF
        }
        current_mask = masks[word_size]

        try:
            if "DEC" in base_type:
                parsed_int = int(prog_in, 10)
            elif "HEX" in base_type:
                parsed_int = int(prog_in, 16)
            elif "BIN" in base_type:
                parsed_int = int(prog_in.replace(" ", ""), 2)
            elif "OCT" in base_type:
                parsed_int = int(prog_in, 8)
            masked_int = parsed_int & current_mask
        except Exception:
            masked_int = 0
            st.error("Invalid number for selected base")

    with prog_col2:
        st.markdown("#### Multi-Base Representations")
        dec_str = f"{masked_int}"
        hex_str = f"0x{masked_int:X}"
        oct_str = f"0o{masked_int:o}"
        raw_bin = f"{masked_int:b}"
        # Group binary digits by nibbles (4 bits)
        padded_len = ((len(raw_bin) + 3) // 4) * 4
        padded_bin = raw_bin.zfill(padded_len)
        formatted_bin = " ".join([padded_bin[i:i+4] for i in range(0, len(padded_bin), 4)])

        st.markdown(f"""
        <div style="background:#181825; border-radius:14px; padding:18px; border:1px solid rgba(255,255,255,0.08);">
          <div style="margin-bottom:12px;">
            <span style="color:#f38ba8; font-weight:700; width:60px; display:inline-block;">HEX</span>
            <span style="color:#cdd6f4; font-family:'JetBrains Mono'; font-size:1.15rem;">{hex_str}</span>
          </div>
          <div style="margin-bottom:12px;">
            <span style="color:#89b4fa; font-weight:700; width:60px; display:inline-block;">DEC</span>
            <span style="color:#cdd6f4; font-family:'JetBrains Mono'; font-size:1.15rem;">{dec_str}</span>
          </div>
          <div style="margin-bottom:12px;">
            <span style="color:#f9e2af; font-weight:700; width:60px; display:inline-block;">OCT</span>
            <span style="color:#cdd6f4; font-family:'JetBrains Mono'; font-size:1.15rem;">{oct_str}</span>
          </div>
          <div>
            <span style="color:#a6e3a1; font-weight:700; width:60px; display:inline-block;">BIN</span>
            <span style="color:#a6e3a1; font-family:'JetBrains Mono'; font-size:1.1rem; word-break:break-all;">{formatted_bin}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Bitwise Operations")
        b_op = st.selectbox("Operator", ["AND (&)", "OR (|)", "XOR (^)", "NOT (~)", "Shift Left (<<)", "Shift Right (>>)"])
        operand2 = st.number_input("Second Operand", value=1, step=1) if "NOT" not in b_op else None

        if "AND" in b_op:
            res_bit = (masked_int & int(operand2)) & current_mask
        elif "OR" in b_op:
            res_bit = (masked_int | int(operand2)) & current_mask
        elif "XOR" in b_op:
            res_bit = (masked_int ^ int(operand2)) & current_mask
        elif "NOT" in b_op:
            res_bit = (~masked_int) & current_mask
        elif "Left" in b_op:
            res_bit = (masked_int << int(operand2)) & current_mask
        elif "Right" in b_op:
            res_bit = (masked_int >> int(operand2)) & current_mask

        st.info(f"Bitwise Result: **DEC** = `{res_bit}` | **HEX** = `0x{res_bit:X}` | **BIN** = `0b{res_bit:b}`")

# ==============================================================================
# TAB 5: FINANCIAL & LOAN
# ==============================================================================
with tabs[4]:
    st.markdown("### 💰 Financial Calculators")

    fin_mode = st.radio("Financial Tool", ["Loan / Mortgage EMI", "Compound Interest & Investment Growth"], horizontal=True)

    if fin_mode == "Loan / Mortgage EMI":
        l_col, r_col = st.columns([1.2, 1.8], gap="large")

        with l_col:
            principal = st.number_input("Loan Amount ($)", min_value=100.0, value=250000.0, step=5000.0)
            annual_rate = st.number_input("Annual Interest Rate (%)", min_value=0.1, value=6.5, step=0.1)
            tenure_years = st.slider("Loan Term (Years)", min_value=1, max_value=40, value=30)

            # EMI Calculation
            monthly_rate = (annual_rate / 100) / 12
            total_months = tenure_years * 12
            emi = principal * monthly_rate * ((1 + monthly_rate) ** total_months) / (((1 + monthly_rate) ** total_months) - 1)
            total_payment = emi * total_months
            total_interest = total_payment - principal

            st.markdown(f"""
            <div style="background:#181825; border-radius:14px; padding:20px; border-left:4px solid #a6e3a1; margin-top:20px;">
              <div style="color:#6c7086; font-size:0.85rem;">MONTHLY PAYMENT (EMI)</div>
              <div style="color:#a6e3a1; font-size:2rem; font-weight:700;">${emi:,.2f}</div>
              <hr style="border-color:rgba(255,255,255,0.08); margin:12px 0;">
              <div style="font-size:0.9rem; color:#cdd6f4;">Total Principal: <b>${principal:,.2f}</b></div>
              <div style="font-size:0.9rem; color:#f38ba8;">Total Interest: <b>${total_interest:,.2f}</b></div>
              <div style="font-size:0.9rem; color:#89b4fa;">Total Repayment: <b>${total_payment:,.2f}</b></div>
            </div>
            """, unsafe_allow_html=True)

        with r_col:
            st.markdown("#### Payment Breakdown")
            pie_fig = go.Figure(data=[go.Pie(
                labels=['Principal Amount', 'Total Interest'],
                values=[principal, total_interest],
                hole=0.55,
                marker=dict(colors=['#89b4fa', '#f38ba8']),
                textinfo='label+percent'
            )])
            pie_fig.update_layout(
                paper_bgcolor="#181825",
                font=dict(family="Plus Jakarta Sans", color="#cdd6f4"),
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=340
            )
            st.plotly_chart(pie_fig, use_container_width=True)

    else:
        # Compound Interest
        ci_l, ci_r = st.columns([1.2, 1.8], gap="large")

        with ci_l:
            init_inv = st.number_input("Initial Deposit ($)", value=10000.0, step=1000.0)
            monthly_contrib = st.number_input("Monthly Contribution ($)", value=500.0, step=50.0)
            ci_rate = st.slider("Estimated Annual Return (%)", min_value=1.0, max_value=25.0, value=8.0, step=0.5)
            inv_years = st.slider("Investment Horizon (Years)", min_value=1, max_value=45, value=20)

            # Year by year breakdown
            year_arr = list(range(0, inv_years + 1))
            balance_arr = []
            contrib_arr = []
            r = (ci_rate / 100) / 12

            for y in year_arr:
                m = y * 12
                if r > 0:
                    val = init_inv * ((1 + r) ** m) + monthly_contrib * (((1 + r) ** m - 1) / r)
                else:
                    val = init_inv + monthly_contrib * m
                balance_arr.append(val)
                contrib_arr.append(init_inv + monthly_contrib * m)

            final_bal = balance_arr[-1]
            final_contrib = contrib_arr[-1]
            final_gain = final_bal - final_contrib

            st.markdown(f"""
            <div style="background:#181825; border-radius:14px; padding:20px; border-left:4px solid #89b4fa; margin-top:20px;">
              <div style="color:#6c7086; font-size:0.85rem;">PROJECTED BALANCE</div>
              <div style="color:#89b4fa; font-size:2rem; font-weight:700;">${final_bal:,.2f}</div>
              <div style="color:#a6e3a1; font-size:0.95rem; margin-top:4px;">+${final_gain:,.2f} Total Interest Earned</div>
            </div>
            """, unsafe_allow_html=True)

        with ci_r:
            st.markdown("#### Growth Trajectory")
            growth_fig = go.Figure()
            growth_fig.add_trace(go.Scatter(
                x=year_arr, y=balance_arr,
                name="Total Value",
                fill='tozeroy',
                line=dict(color="#a6e3a1", width=3)
            ))
            growth_fig.add_trace(go.Scatter(
                x=year_arr, y=contrib_arr,
                name="Principal Invested",
                line=dict(color="#89b4fa", width=2, dash="dash")
            ))
            growth_fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#181825",
                plot_bgcolor="#11111b",
                font=dict(family="Plus Jakarta Sans", color="#cdd6f4"),
                margin=dict(t=20, b=20, l=30, r=20),
                height=340
            )
            st.plotly_chart(growth_fig, use_container_width=True)

# ==============================================================================
# TAB 6: UNIT CONVERTER
# ==============================================================================
with tabs[5]:
    st.markdown("### 📐 Comprehensive Unit Converter")

    unit_category = st.selectbox("Category", [
        "Length & Distance",
        "Weight & Mass",
        "Temperature",
        "Speed",
        "Digital Storage",
        "Time"
    ])

    uc_col1, uc_col2, uc_col3 = st.columns([1.5, 1.5, 1.5], gap="medium")

    # Unit conversion factors relative to standard base units
    conversions = {
        "Length & Distance": {
            "Meters (m)": 1.0,
            "Kilometers (km)": 1000.0,
            "Centimeters (cm)": 0.01,
            "Millimeters (mm)": 0.001,
            "Miles (mi)": 1609.344,
            "Yards (yd)": 0.9144,
            "Feet (ft)": 0.3048,
            "Inches (in)": 0.0254,
            "Nautical Miles (nmi)": 1852.0
        },
        "Weight & Mass": {
            "Kilograms (kg)": 1.0,
            "Grams (g)": 0.001,
            "Milligrams (mg)": 0.000001,
            "Pounds (lb)": 0.45359237,
            "Ounces (oz)": 0.028349523125,
            "Metric Tons (t)": 1000.0,
            "Stones (st)": 6.35029
        },
        "Speed": {
            "Meters / second (m/s)": 1.0,
            "Kilometers / hour (km/h)": 0.277778,
            "Miles / hour (mph)": 0.44704,
            "Knots (kn)": 0.514444,
            "Mach (at sea level)": 340.29
        },
        "Digital Storage": {
            "Bytes (B)": 1.0,
            "Kilobytes (KB)": 1024.0,
            "Megabytes (MB)": 1024.0 ** 2,
            "Gigabytes (GB)": 1024.0 ** 3,
            "Terabytes (TB)": 1024.0 ** 4,
            "Petabytes (PB)": 1024.0 ** 5
        },
        "Time": {
            "Seconds (s)": 1.0,
            "Minutes (min)": 60.0,
            "Hours (hr)": 3600.0,
            "Days (d)": 86400.0,
            "Weeks (wk)": 604800.0,
            "Years (365d)": 31536000.0
        }
    }

    if unit_category == "Temperature":
        with uc_col1:
            temp_in = st.number_input("Value", value=100.0, step=1.0)
        with uc_col2:
            from_t = st.selectbox("From", ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"])
        with uc_col3:
            to_t = st.selectbox("To", ["Fahrenheit (°F)", "Celsius (°C)", "Kelvin (K)"])

        # Convert to Celsius first
        if from_t == "Celsius (°C)": c = temp_in
        elif from_t == "Fahrenheit (°F)": c = (temp_in - 32) * 5/9
        else: c = temp_in - 273.15

        # Convert from Celsius to target
        if to_t == "Celsius (°C)": out_temp = c
        elif to_t == "Fahrenheit (°F)": out_temp = (c * 9/5) + 32
        else: out_temp = c + 273.15

        st.markdown(f"""
        <div style="background:#181825; border-radius:14px; padding:20px; border-left:4px solid #cba6f7; margin-top:20px;">
          <div style="color:#6c7086; font-size:0.85rem;">CONVERTED VALUE</div>
          <div style="color:#cba6f7; font-size:2.2rem; font-weight:700; font-family:'JetBrains Mono';">{out_temp:.4f} {to_t}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        unit_dict = conversions[unit_category]
        unit_names = list(unit_dict.keys())

        with uc_col1:
            val_in = st.number_input("Quantity", value=1.0, step=1.0)
        with uc_col2:
            from_u = st.selectbox("From Unit", unit_names, index=0)
        with uc_col3:
            to_u = st.selectbox("To Unit", unit_names, index=min(1, len(unit_names)-1))

        # Base unit conversion
        base_val = val_in * unit_dict[from_u]
        converted_val = base_val / unit_dict[to_u]

        st.markdown(f"""
        <div style="background:#181825; border-radius:14px; padding:20px; border-left:4px solid #cba6f7; margin-top:20px;">
          <div style="color:#6c7086; font-size:0.85rem;">CONVERTED VALUE</div>
          <div style="color:#cba6f7; font-size:2.2rem; font-weight:700; font-family:'JetBrains Mono';">{converted_val:,.6g} {to_u}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #6c7086; font-size: 0.82rem;">OmniCalc Pro • Built with Streamlit, Plotly & SymPy</p>',
    unsafe_allow_html=True
)
