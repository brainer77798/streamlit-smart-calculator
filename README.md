# 🧮 OmniCalc Pro — Scientific, Graphing & Financial Suite

[![Deploy with Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=brainer77798/streamlit-smart-calculator&branch=main&mainModule=app.py)

A comprehensive, responsive, high-performance calculator suite built with **Python**, **Streamlit**, **Plotly**, and **SymPy**, styled in the modern dark **Catppuccin Mocha** design system.

---

## 🚀 Live 1-Click Streamlit.io Deployment

Deploy to Streamlit Community Cloud with pre-configured settings:

👉 **[Launch on Streamlit Community Cloud](https://share.streamlit.io/deploy?repository=brainer77798/streamlit-smart-calculator&branch=main&mainModule=app.py)**

---

## ✨ Features & Modules

### 1. 🧮 Standard Calculator
- Modern keypad layout with zero-division protection and graceful error recovery.
- Operations: `+`, `−`, `×`, `÷`, `%`, sign toggling `+/-`, and backspace `⌫`.
- Calculation history with quick clearing and expression replay.

### 2. 🔬 Scientific & Calculus Engine
- **Trigonometric & Hyperbolic**: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh`.
- **Angle Modes**: Degrees and Radians.
- **Logarithms & Powers**: `ln`, `log10`, `log2`, `e^x`, `10^x`, square roots, and factorials.
- **Symbolic Calculus (Powered by SymPy)**:
  - Exact 1st and 2nd derivatives $\frac{d}{dx} f(x)$, $\frac{d^2}{dx^2} f(x)$
  - Indefinite integrals $\int f(x) dx + C$
  - Definite integrals with custom $[a, b]$ bounds
  - Calculus limits $\lim_{x \to a} f(x)$
  - Taylor Series expansions up to 8th order

### 3. 📈 Interactive Graphing Studio
- Interactive graphing powered by **Plotly** (pan, zoom, hover crosshairs, and box select).
- Multi-function overlay (plot $f_1(x)$ and $f_2(x)$ side-by-side).
- Instant presets: *Damped Harmonics, Cubic Polynomials, Gaussian Bell Curves, Wave Superpositions, Sigmoid Curves*.
- Numerical derivative overlays ($f'_1(x)$) and shaded area under curve ($\int f_1(x) dx$).
- Automatic roots detection (zero-crossings) and domain extreme calculation.

### 4. 💻 Programmer Matrix
- Instant synchronization across **HEX**, **DEC**, **OCT**, and formatted **BIN** (grouped nibbles).
- Configurable word sizing: 64-bit (QWORD), 32-bit (DWORD), 16-bit (WORD), and 8-bit (BYTE).
- Bitwise operations: `AND (&)`, `OR (|)`, `XOR (^)`, `NOT (~)`, `Shift Left (<<)`, `Shift Right (>>)`.

### 5. 💰 Financial Calculators
- **Loan & Mortgage EMI**:
  - Amortization calculation with dynamic principal vs. interest breakdown charts.
- **Compound Interest & Wealth Growth**:
  - Future value projections with recurring monthly contributions and interactive growth curves.

### 6. 📐 Unit Converter
- Real-time conversion across 6 categories:
  - **Length & Distance** (meters, km, miles, feet, inches, yards, nautical miles)
  - **Weight & Mass** (kg, grams, mg, pounds, ounces, tons, stones)
  - **Temperature** (Celsius, Fahrenheit, Kelvin)
  - **Speed** (m/s, km/h, mph, knots, Mach)
  - **Digital Storage** (Bytes, KB, MB, GB, TB, PB)
  - **Time** (seconds, minutes, hours, days, weeks, years)

---

## 💻 Local Setup & Execution

1. **Clone the repository**:
   ```bash
   git clone https://github.com/brainer77798/streamlit-smart-calculator.git
   cd streamlit-smart-calculator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application**:
   ```bash
   streamlit run app.py
   ```
