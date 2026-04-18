import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sympy as sp
import os
from engine import get_continuous_convolution, get_signals

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SAS Convolution Project | Shikhar Srivastava", layout="wide", page_icon="📡", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR PREMIUM UI ---
st.markdown("""
    <style>
        /* Hide Streamlit default header and footer for a clean app feel */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Main background with gradient */
        .main { 
            background: linear-gradient(135deg, #0a0e1a 0%, #0f1419 50%, #0a0e1a 100%);
            background-attachment: fixed;
        }
        
        /* Logo header styling */
        .logo-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 25px;
            background: linear-gradient(135deg, rgba(0, 209, 255, 0.05) 0%, rgba(0, 145, 217, 0.03) 100%);
            padding: 20px 30px;
            border-radius: 14px;
            border: 1px solid rgba(0, 209, 255, 0.15);
            margin-bottom: 35px;
        }
        .logo-header img {
            max-width: 90px;
            height: auto;
            filter: drop-shadow(0 4px 8px rgba(0, 209, 255, 0.1));
            flex-shrink: 0;
        }
        .header-text h1 {
            margin: 0;
            color: #00d1ff;
            font-size: 1.6rem;
            font-weight: 800;
            letter-spacing: 0.3px;
            text-align: center;
        }
        .header-text p {
            margin: 5px 0 0 0;
            color: #58a6ff;
            font-size: 0.95rem;
            font-weight: 500;
            text-align: center;
        }
        
        /* Main Title Styling */
        .main-title {
            text-align: center;
            background: linear-gradient(135deg, #00d1ff 0%, #0091d9 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3.5rem;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 10px;
            text-shadow: 0 2px 20px rgba(0, 209, 255, 0.1);
        }
        
        .subtitle {
            text-align: center;
            color: #58a6ff;
            font-size: 1.3rem;
            font-weight: 500;
            margin-bottom: 30px;
            letter-spacing: 0.5px;
        }
        
        /* Institute Header Styling - Enhanced */
        .institute-header {
            background: linear-gradient(135deg, rgba(0, 209, 255, 0.08) 0%, rgba(0, 145, 217, 0.05) 100%);
            padding: 40px;
            border-radius: 18px;
            text-align: center;
            border: 2px solid rgba(0, 209, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 209, 255, 0.08), inset 0 1px 1px rgba(255, 255, 255, 0.05);
            margin-bottom: 40px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        .institute-header:hover {
            border-color: rgba(0, 209, 255, 0.4);
            box-shadow: 0 12px 48px rgba(0, 209, 255, 0.12), inset 0 1px 1px rgba(255, 255, 255, 0.05);
        }
        .institute-header h2 {
            margin: 0 0 12px 0;
            background: linear-gradient(135deg, #e5b300 0%, #ffd700 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            font-size: 2rem;
            letter-spacing: 0.5px;
        }
        .institute-header p {
            margin: 0;
            color: #8b949e;
            font-size: 1.1rem;
            font-weight: 500;
        }

        /* Custom Cards - Enhanced with modern design */
        .custom-card-blue {
            background: linear-gradient(135deg, rgba(22, 27, 34, 0.9) 0%, rgba(13, 17, 23, 0.9) 100%);
            padding: 32px;
            border-radius: 16px;
            border: 2px solid rgba(0, 209, 255, 0.15);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(0, 209, 255, 0.1);
            height: 100%;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border-left: 5px solid #00d1ff;
        }
        .custom-card-blue:hover {
            border-color: rgba(0, 209, 255, 0.3);
            box-shadow: 0 12px 32px rgba(0, 209, 255, 0.15), inset 0 1px 1px rgba(0, 209, 255, 0.1);
            transform: translateY(-4px);
        }
        
        .custom-card-green {
            background: linear-gradient(135deg, rgba(22, 27, 34, 0.9) 0%, rgba(13, 17, 23, 0.9) 100%);
            padding: 32px;
            border-radius: 16px;
            border: 2px solid rgba(46, 160, 67, 0.15);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(46, 160, 67, 0.1);
            height: 100%;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border-left: 5px solid #2ea043;
        }
        .custom-card-green:hover {
            border-color: rgba(46, 160, 67, 0.3);
            box-shadow: 0 12px 32px rgba(46, 160, 67, 0.15), inset 0 1px 1px rgba(46, 160, 67, 0.1);
            transform: translateY(-4px);
        }
        
        .card-title {
            color: #c9d1d9;
            font-size: 1.4rem;
            margin-bottom: 20px;
            font-weight: 700;
            border-bottom: 2px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 15px;
            letter-spacing: 0.3px;
        }
        .card-text {
            color: #8b949e;
            font-size: 1.05rem;
            line-height: 1.8;
        }
        
        .highlight { 
            color: #58a6ff; 
            font-weight: 700;
            display: inline-block;
        }
        
        /* About section styling */
        .about-section {
            background: linear-gradient(135deg, rgba(0, 209, 255, 0.05) 0%, rgba(46, 160, 67, 0.05) 100%);
            padding: 40px;
            border-radius: 16px;
            border: 2px solid rgba(200, 217, 255, 0.1);
            margin-top: 30px;
            backdrop-filter: blur(10px);
        }
        .about-section h3 {
            color: #58a6ff;
            font-size: 1.8rem;
            font-weight: 800;
            margin-bottom: 25px;
            letter-spacing: 0.5px;
        }
        .about-section p {
            color: #c9d1d9;
            font-size: 1.1rem;
            line-height: 1.8;
            margin-bottom: 20px;
        }
        .about-section ul li {
            color: #8b949e;
            font-size: 1.05rem;
            line-height: 2;
            margin-bottom: 12px;
        }
        .about-section ul li strong {
            color: #c9d1d9;
            font-weight: 700;
        }
        
        /* CTA text styling */
        .cta-section {
            background: linear-gradient(135deg, rgba(0, 209, 255, 0.1) 0%, rgba(0, 145, 217, 0.08) 100%);
            padding: 25px;
            border-radius: 12px;
            border-left: 4px solid #58a6ff;
            margin-top: 30px;
            color: #c9d1d9;
        }
        .cta-section strong {
            color: #00d1ff;
            font-weight: 700;
        }
        
        /* Section divider enhancement */
        hr {
            border-color: rgba(48, 54, 61, 0.5) !important;
            margin: 40px 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION WITH LOGO ---
# SIDEBAR HIDDEN - Signal selection moved to Calculator tab
st.sidebar.markdown("""
    <style>
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["🏠 Project Home", "🚀 Calculator & Visualizer", "📚 Full Theory & Properties"])

# ==========================================
# TAB 1: PREMIUM PROJECT HOMEPAGE
# ==========================================
with tab1:
    # Logo and College Name Header at the top
    col_logo, col_header = st.columns([0.12, 1], gap="medium")
    
    with col_logo:
        if os.path.exists("logo.png"):
            st.markdown("<div style='display: flex; align-items: center; height: 100%;'></div>", unsafe_allow_html=True)
            st.image("logo.png", width=85)
    
    with col_header:
        st.markdown("""
        <div style='display: flex; flex-direction: column; justify-content: center; height: 100%; padding: 10px 0;'>
            <h2 style='margin: 0 0 8px 0; color: #00d1ff; font-size: 1.5rem; font-weight: 800; line-height: 1.2;'>IIIT Naya Raipur</h2>
            <p style='margin: 0; color: #58a6ff; font-size: 0.9rem; font-weight: 500; line-height: 1.3;'>Dr. Shyama Prasad Mukherjee International Institute</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 25px 0; border-color: rgba(48, 54, 61, 0.5);'>", unsafe_allow_html=True)
    
    st.markdown("<div class='main-title'>Signals & Systems Convolution Project</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Interactive Convolution Visualizer & Advanced Calculator</div>", unsafe_allow_html=True)
    
    st.markdown("")
    
    # Premium Institute Header
    st.markdown("""
        <div class='institute-header'>
            <h2>Dr. Shyama Prasad Mukherjee International Institute of Information Technology</h2>
            <p>Naya Raipur (IIIT-NR) | A Centre of Excellence</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Custom HTML Cards for Credentials
    col_student, col_guide = st.columns(2)
    
    with col_student:
        st.markdown("""
        <div class='custom-card-blue'>
            <div class='card-title'>🎓 Submitted By</div>
            <div class='card-text'>
                <strong>Name:</strong> <span class='highlight'>Shikhar Srivastava</span><br><br>
                <strong>Branch:</strong> <span class='highlight'>Computer Science & Engineering</span><br><br>
                <strong>Roll Number:</strong> <span class='highlight'>251000081</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_guide:
        st.markdown("""
        <div class='custom-card-green'>
            <div class='card-title'>👨‍🏫 Under the Guidance Of</div>
            <div class='card-text'>
                <strong>Faculty:</strong> <span class='highlight'>Dr. Shrivishal Tripathi</span><br><br>
                <strong>Designation:</strong> Associate Professor<br><br>
                <strong>Department:</strong> Electronics & Communication Engineering
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='about-section'>
        <h3>✨ About This Project</h3>
        <p>
        Welcome to the Interactive Convolution Laboratory. This advanced computational tool bridges the critical gap between abstract mathematical theory and intuitive visual understanding in Signals and Systems analysis.
        </p>
        <ul>
            <li><strong>🧮 Automated Mathematical Solving:</strong> Precisely computes continuous convolution integrals with symbolic mathematics, formatting results into standard engineering notation using unit steps u(t) and linear ramps r(t).</li>
            <li><strong>📊 Discrete-Time Sequence Analysis:</strong> Dynamically generates step-by-step product sequences for y[n] with exact numerical indices and overlapping calculations.</li>
            <li><strong>🎬 Interactive Sliding Visualizer:</strong> Real-time interactive sliders demonstrating the mathematical "fold, shift, multiply, integrate/sum" process with instant visual feedback.</li>
            <li><strong>📈 Publication-Ready Graphing:</strong> Professional Plotly visualizations suitable for academic papers and presentations with customizable ranges and precision.</li>
        </ul>
    </div>
    
    <div class='cta-section'>
        <strong>🚀 Getting Started:</strong> Use the <strong>Configuration</strong> panel on the left sidebar to select your domain (continuous or discrete time) and choose your input and impulse response signals. Then navigate to the <strong>Calculator & Visualizer</strong> tab to explore the convolution operation interactively.
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# TAB 2: CALCULATOR & VISUALIZER
# ==========================================
with tab2:
    # Signal Configuration Section
    st.markdown("<h2 style='color: #00d1ff; font-weight: 800; font-size: 2rem; letter-spacing: 0.5px;'>⚙️ Configuration & Signal Selection</h2>", unsafe_allow_html=True)
    
    config_col1, config_col2 = st.columns([1, 2], gap="large")
    
    with config_col1:
        st.markdown("<h4 style='color: #58a6ff; font-weight: 700; margin-bottom: 15px;'>📊 Domain</h4>", unsafe_allow_html=True)
        domain = st.radio("", ["Continuous-Time (t)", "Discrete-Time [n]"], label_visibility="collapsed")
    
    with config_col2:
        st.markdown("<h4 style='color: #58a6ff; font-weight: 700; margin-bottom: 15px;'>📥 Select Signals</h4>", unsafe_allow_html=True)
        sig_col1, sig_col2 = st.columns(2, gap="medium")
        signals_list = list(get_signals(sp.symbols('t')).keys())
        
        with sig_col1:
            s1_select = st.selectbox("Input Signal f(t) / f[n]", signals_list, index=7)
        with sig_col2:
            s2_select = st.selectbox("Response h(t) / h[n]", signals_list, index=5)
    
    st.markdown("---")
    st.markdown("<h2 style='color: #00d1ff; font-weight: 800; font-size: 2rem; letter-spacing: 0.5px;'>🔍 Convolution Calculator & Visualizer</h2>", unsafe_allow_html=True)
    st.markdown("---")
    p1, p2 = st.columns(2)
    t_plot = np.linspace(-5, 5, 500)
    n_plot = np.arange(-5, 6)

    def plot_signal(name, domain_type, color, chart_id):
        fig = go.Figure()
        t_sym = sp.symbols('t', real=True)
        sig_expr = get_signals(t_sym)[name]
        
        func = sp.lambdify(t_sym, sig_expr, modules=['numpy', {'Heaviside': lambda x: np.where(x>=0,1,0), 'DiracDelta': lambda x: np.where(x==0, 5, 0)}])
        
        if domain_type == "Continuous-Time (t)":
            y = [float(func(val)) for val in t_plot]
            fig.add_trace(go.Scatter(x=t_plot, y=y, line=dict(color=color, width=3)))
        else:
            y = [float(func(val)) for val in n_plot]
            fig.add_trace(go.Scatter(x=n_plot, y=y, mode='markers', marker=dict(size=10, color=color)))
            for i, val in enumerate(n_plot):
                fig.add_shape(type='line', x0=val, y0=0, x1=val, y1=y[i], line=dict(color=color, width=2))
        
        fig.update_layout(height=250, template="plotly_dark", title=f"Signal: {name}", margin=dict(l=20,r=20,t=40,b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, key=chart_id)

    with p1: plot_signal(s1_select, domain, '#00d1ff', 'chart_f')
    with p2: plot_signal(s2_select, domain, '#ffcc00', 'chart_h')

    st.markdown("---")
    
    if domain == "Continuous-Time (t)":
        math_result, formatted_result, f_disp, h_disp = get_continuous_convolution(s1_select, s2_select)
        
        st.markdown("<h3 style='color: #c9d1d9; font-size: 1.4rem; font-weight: 700; margin-top: 25px;'>2. Mathematical Steps</h3>", unsafe_allow_html=True)
        st.markdown("**Step 1: Signal Definitions**")
        st.latex(rf"f(\tau) = {f_disp}")
        st.latex(rf"h(t-\tau) = {h_disp}")
        
        st.markdown("**Step 2: Convolution Integral**")
        st.latex(r"y(t) = \int_{-\infty}^{\infty} f(\tau)h(t-\tau)d\tau")
        
        st.markdown("**Step 3: Final Evaluated Equation**")
        st.latex(formatted_result)
        
        st.markdown("---")
        st.markdown("<h3 style='color: #c9d1d9; font-size: 1.4rem; font-weight: 700; margin-top: 25px;'>3. Interactive Sliding Visualizer</h3>", unsafe_allow_html=True)
        t_slide = st.slider("Shift value (t)", -5.0, 5.0, 0.0, 0.1)
        tau_range = np.linspace(-7, 7, 500)
        
        t_sym, tau_sym = sp.symbols('t tau', real=True)
        c_dict = get_signals(t_sym)
        f_calc = c_dict[s1_select].subs(t_sym, tau_sym)
        h_calc = c_dict[s2_select].subs(t_sym, t_sym - tau_sym)
        
        f_func = sp.lambdify(tau_sym, f_calc, modules=['numpy', {'Heaviside': lambda x: np.where(x>=0,1,0), 'DiracDelta': lambda x: np.where(x==0,1,0)}])
        h_func = sp.lambdify((t_sym, tau_sym), h_calc, modules=['numpy', {'Heaviside': lambda x: np.where(x>=0,1,0), 'DiracDelta': lambda x: np.where(x==0,1,0)}])
        
        f_vals = np.array([float(f_func(v)) for v in tau_range])
        h_vals = np.array([float(h_func(t_slide, v)) for v in tau_range])
        
        fig_slide = go.Figure()
        fig_slide.add_trace(go.Scatter(x=tau_range, y=f_vals, name="f(τ)", fill='tozeroy', line=dict(color='#00d1ff', width=2)))
        fig_slide.add_trace(go.Scatter(x=tau_range, y=h_vals, name=f"h({round(t_slide,1)}-τ)", fill='tozeroy', line=dict(color='#ffcc00', width=2)))
        
        overlap = np.minimum(f_vals, h_vals)
        fig_slide.add_trace(go.Scatter(x=tau_range, y=overlap, name="Overlap", fill='tozeroy', line=dict(color='rgba(255,0,0,0)'), fillcolor='rgba(255, 0, 0, 0.5)'))
        fig_slide.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_slide, use_container_width=True, key="slide_cont")

        st.markdown("---")
        st.markdown("<h3 style='color: #c9d1d9; font-size: 1.4rem; font-weight: 700; margin-top: 25px;'>4. Final Convolution Graph y(t)</h3>", unsafe_allow_html=True)
        t_vals_final = np.linspace(-6, 6, 400)
        
        dt = 12.0 / 400.0
        f_arr = np.array([float(f_func(v)) for v in t_vals_final])
        h_arr_t0 = np.array([float(h_func(0, v)) for v in t_vals_final])
        y_vals_final = np.convolve(f_arr, h_arr_t0, mode='same') * dt

        fig_final = go.Figure()
        fig_final.add_trace(go.Scatter(x=t_vals_final, y=y_vals_final, mode='lines', name='y(t)', line=dict(color='#ff007f', width=4)))
        fig_final.update_layout(template="plotly_dark", xaxis_title="t (Time)", yaxis_title="Amplitude y(t)", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_final, use_container_width=True, key="final_cont_graph")

    else:
        st.markdown("<h3 style='color: #c9d1d9; font-size: 1.4rem; font-weight: 700; margin-top: 25px;'>2. Discrete Convolution Textual Steps</h3>", unsafe_allow_html=True)
        n_slide = st.slider("Select current n to see step-by-step summation calculation", -10, 10, 0)
        n_indices = np.arange(-15, 16)
        
        t_sym = sp.symbols('t', real=True)
        f_expr = get_signals(t_sym)[s1_select]
        h_expr = get_signals(t_sym)[s2_select]
        
        f_np = sp.lambdify(t_sym, f_expr, modules=['numpy', {'Heaviside': lambda x: np.where(x>=0,1,0)}])
        h_np = sp.lambdify(t_sym, h_expr, modules=['numpy', {'Heaviside': lambda x: np.where(x>=0,1,0)}])
        
        x_vals = np.array([float(f_np(i)) for i in n_indices])
        h_flipped_shifted = np.array([float(h_np(n_slide - i)) for i in n_indices])
        
        symbolic_steps = []
        numeric_steps = []
        current_sum = 0
        
        for i, k in enumerate(n_indices):
            prod = x_vals[i] * h_flipped_shifted[i]
            if prod != 0:
                symbolic_steps.append(rf"x[{k}]h[{n_slide - k}]")
                numeric_steps.append(rf"({x_vals[i]:.2g})({h_flipped_shifted[i]:.2g})")
                current_sum += prod
        
        if not symbolic_steps:
            st.latex(rf"y[{n_slide}] = 0 \quad \text{{(No overlapping terms)}}")
        else:
            sym_str = " + ".join(symbolic_steps)
            num_str = " + ".join(numeric_steps)
            st.latex(rf"\begin{{aligned}} y[{n_slide}] &= \sum_{{k=-\infty}}^{{\infty}} x[k]h[{n_slide}-k] \\ &= {sym_str} \\ &= {num_str} \\ &= \mathbf{{{current_sum:.2g}}} \end{{aligned}}")
        
        fig_disc = go.Figure()
        fig_disc.add_trace(go.Scatter(x=n_indices, y=x_vals, mode='markers', name="x[k]", marker=dict(color='#00d1ff')))
        fig_disc.add_trace(go.Scatter(x=n_indices, y=h_flipped_shifted, mode='markers', name=f"h[{n_slide}-k]", marker=dict(color='#ffcc00')))
        
        for i, idx in enumerate(n_indices):
            fig_disc.add_shape(type='line', x0=idx, y0=0, x1=idx, y1=x_vals[i], line=dict(color='#00d1ff', width=1))
            fig_disc.add_shape(type='line', x0=idx, y0=0, x1=idx, y1=h_flipped_shifted[i], line=dict(color='#ffcc00', width=1))
            
        fig_disc.update_layout(template="plotly_dark", title=f"Visualizing Product Overlap at n={n_slide}", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_disc, use_container_width=True, key="slide_disc")
        
        st.markdown("---")
        st.markdown("<h3 style='color: #c9d1d9; font-size: 1.4rem; font-weight: 700; margin-top: 25px;'>3. Final Convolution Sequence y[n]</h3>", unsafe_allow_html=True)
        y_full_discrete = np.convolve([float(f_np(i)) for i in np.arange(-20, 20)], [float(h_np(i)) for i in np.arange(-20, 20)], mode='same')
        
        nz_indices = np.nonzero(y_full_discrete)[0]
        if len(nz_indices) > 0:
            start, end = nz_indices[0], nz_indices[-1]
            seq_vals = y_full_discrete[start:end+1]
            seq_n = np.arange(-20, 20)[start:end+1]
            seq_parts = []
            for val, n_val in zip(seq_vals, seq_n):
                if n_val == 0:
                    seq_parts.append(rf"\mathbf{{{val:.2g}}}_{{n=0}}")
                else:
                    seq_parts.append(f"{val:.2g}")
            st.latex(r"y[n] = \{ \dots, " + ", ".join(seq_parts) + r", \dots \}")
            
        fig_final_d = go.Figure()
        fig_final_d.add_trace(go.Scatter(x=np.arange(-20, 20), y=y_full_discrete, mode='markers', marker=dict(color='#ff007f', size=10)))
        for i, val in enumerate(y_full_discrete):
             fig_final_d.add_shape(type='line', x0=i-20, y0=0, x1=i-20, y1=val, line=dict(color='#ff007f', width=2))
        fig_final_d.update_layout(template="plotly_dark", xaxis_title="n", yaxis_title="y[n]", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_final_d, use_container_width=True, key="final_disc_graph")

# ==========================================
# TAB 3: MASSIVE THEORY EXPANSION (CTS & DTS)
# ==========================================
with tab3:
    st.markdown("<h2 style='color: #00d1ff; font-weight: 800; font-size: 2rem; letter-spacing: 0.5px;'>📚 Comprehensive Theory of Convolution</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h3 style='color: #58a6ff; font-size: 1.3rem; font-weight: 700;'>🎬 Recommended Video Tutorials</h3>", unsafe_allow_html=True)
    st.write("Visualizing convolution is often the hardest part. Check out these highly-rated conceptual explanations:")
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        st.video("https://www.youtube.com/watch?v=QmcoPYUfbJ8") 
        st.caption("*What is convolution? This is the easiest way to understand* (Discretised)")
    with v_col2:
        st.video("https://www.youtube.com/watch?v=x3Fdd6V_Hok") 
        st.caption("*How to Understand Convolution* (Iain Explains Signals & Systems)")

    st.markdown("---")
    
    st.markdown("<h3 style='color: #58a6ff; font-size: 1.3rem; font-weight: 700;'>🧠 What is Convolution?</h3>", unsafe_allow_html=True)
    st.write("""
    In Signals and Systems, **Convolution** is a mathematical operation that expresses how the shape of one signal is modified by another. 
    It is the fundamental equation for determining the output of a **Linear Time-Invariant (LTI)** system. 
    If you know a system's **Impulse Response ($h$)**, and you feed it an **Input Signal ($x$)**, convolution dictates the exact **Output Signal ($y$)**.
    """)

    st.markdown("#### The 4-Step Intuition (Fold, Shift, Multiply, Add)")
    
    step_col1, step_col2 = st.columns(2)
    with step_col1:
        st.info("**Continuous-Time (CTS)**")
        st.write("1. **Fold:** Reflect the impulse response $h(\\tau)$ across the y-axis to get $h(-\\tau)$.")
        st.write("2. **Shift:** Slide the flipped signal by time $t$ to get $h(t - \\tau)$.")
        st.write("3. **Multiply:** Take the product of the input $x(\\tau)$ and the shifted signal.")
        st.write("4. **Integrate:** Calculate the total overlapping area at that specific time $t$.")
        st.latex(r"y(t) = x(t) * h(t) = \int_{-\infty}^{\infty} x(\tau)h(t-\tau)d\tau")

    with step_col2:
        st.success("**Discrete-Time (DTS)**")
        st.write("1. **Fold:** Reflect the impulse sequence $h[k]$ across the y-axis to get $h[-k]$.")
        st.write("2. **Shift:** Slide the flipped sequence by index $n$ to get $h[n - k]$.")
        st.write("3. **Multiply:** Take the point-by-point product of $x[k]$ and the shifted sequence.")
        st.write("4. **Sum:** Add up all the overlapping points at that specific index $n$.")
        st.latex(r"y[n] = x[n] * h[n] = \sum_{k=-\infty}^{\infty} x[k]h[n-k]")

    st.markdown("---")
    st.markdown("<h3 style='color: #58a6ff; font-size: 1.3rem; font-weight: 700;'>🔑 Core Mathematical Properties</h3>", unsafe_allow_html=True)
    
    prop1, prop2, prop3 = st.columns([1, 2, 2])
    
    with prop1:
        st.write("**Property**")
        st.write("---")
        st.write("**Commutative**")
        st.write("")
        st.write("**Associative**")
        st.write("")
        st.write("**Distributive**")
        st.write("")
        st.write("**Identity Element**")
        st.write("")
        st.write("**Time-Shifting**")
        st.write("")
        st.write("**Differentiation / Difference**")

    with prop2:
        st.write("**Continuous-Time ($t$)**")
        st.write("---")
        st.latex(r"x(t) * h(t) = h(t) * x(t)")
        st.latex(r"x * (h_1 * h_2) = (x * h_1) * h_2")
        st.latex(r"x * (h_1 + h_2) = x * h_1 + x * h_2")
        st.latex(r"x(t) * \delta(t) = x(t)")
        st.latex(r"x(t-t_1) * h(t-t_2) = y(t - t_1 - t_2)")
        st.latex(r"\frac{d}{dt}[x*h] = \frac{dx}{dt}*h = x*\frac{dh}{dt}")

    with prop3:
        st.write("**Discrete-Time ($[n]$)**")
        st.write("---")
        st.latex(r"x[n] * h[n] = h[n] * x[n]")
        st.latex(r"x * (h_1 * h_2) = (x * h_1) * h_2")
        st.latex(r"x * (h_1 + h_2) = x * h_1 + x * h_2")
        st.latex(r"x[n] * \delta[n] = x[n]")
        st.latex(r"x[n-n_1] * h[n-n_2] = y[n - n_1 - n_2]")
        st.latex(r"y[n]-y[n-1] = x[n] * (h[n]-h[n-1])")
        
    st.markdown("---")
    st.markdown("#### ⚡ The Convolution Theorem (Frequency Domain)")
    st.write("""
    One of the most powerful concepts in electrical engineering is that **convolution in the time domain is equivalent to simple multiplication in the frequency domain**. This is heavily used to design filters.
    """)
    
    freq1, freq2 = st.columns(2)
    with freq1:
        st.info("**Continuous: Laplace & Fourier Transforms**")
        st.latex(r"x(t) * h(t) \quad \xleftrightarrow{\mathcal{F}} \quad X(\omega) \cdot H(\omega)")
        st.latex(r"x(t) * h(t) \quad \xleftrightarrow{\mathcal{S}} \quad X(s) \cdot H(s)")
    with freq2:
        st.success("**Discrete: DTFT & Z-Transforms**")
        st.latex(r"x[n] * h[n] \quad \xleftrightarrow{\mathcal{DTFT}} \quad X(e^{j\omega}) \cdot H(e^{j\omega})")
        st.latex(r"x[n] * h[n] \quad \xleftrightarrow{\mathcal{Z}} \quad X(z) \cdot H(z)")