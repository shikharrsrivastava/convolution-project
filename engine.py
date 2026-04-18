import sympy as sp
import re

def get_signals(t):
    u = sp.Heaviside
    half = sp.Rational(1, 2)
    return {
        "δ(t)": sp.DiracDelta(t),
        "u(t)": u(t),
        "r(t)": t * u(t),
        "exp(-t)u(t)": sp.exp(-t) * u(t),
        "sin(t)u(t)": sp.sin(t) * u(t),
        "cos(t)u(t)": sp.cos(t) * u(t),
        "sgn(t)": u(t) - u(-t),
        "rect(t)": u(t + half) - u(t - half),
        "tri(t)": (t + 1)*u(t + 1) - 2*t*u(t) + (t - 1)*u(t - 1),
        "sinc(t)": sp.sinc(t)
    }

def get_print_signals(t_sym):
    """Clean symbols specifically for LaTeX UI printing."""
    u = sp.Function('u')(t_sym)
    r = sp.Function('r')(t_sym)
    return {
        "δ(t)": sp.Function(r'\delta')(t_sym),
        "u(t)": u,
        "r(t)": r,
        "exp(-t)u(t)": sp.exp(-t_sym) * u,
        "sin(t)u(t)": sp.sin(t_sym) * u,
        "cos(t)u(t)": sp.cos(t_sym) * u,
        "sgn(t)": sp.Function('sgn')(t_sym),
        "rect(t)": sp.Function('rect')(t_sym),
        "tri(t)": sp.Function('tri')(t_sym),
        "sinc(t)": sp.Function('sinc')(t_sym)
    }

def format_standard_form(expr):
    """Formats evaluated integration into textbook r(t) and u(t) forms."""
    if isinstance(expr, sp.Integral):
        return sp.latex(expr)
        
    if expr.has(sp.Piecewise):
        expr = sp.simplify(expr.rewrite(sp.Heaviside))
    else:
        expr = sp.simplify(expr)
        
    latex_str = sp.latex(expr)
    latex_str = latex_str.replace(r"\theta", "u").replace(r"\text{Heaviside}", "u")
    
    latex_str = re.sub(r'\\left\(t\s*([+-]\s*[\d\.]+)?\\right\)\s*u\\left\(t\s*\1\\right\)', r'r\\left(t \1\\right)', latex_str)
    latex_str = latex_str.replace(r't u\left(t\right)', r'r\left(t\right)')
    
    return latex_str

def get_smart_analytical_result(s1, s2, f_calc, h_calc, tau):
    pair = tuple(sorted([s1, s2]))
    
    # --- THE ULTIMATE SAS LOOKUP TABLE ---
    # Identity Property
    if "δ(t)" in pair:
        other = pair[0] if pair[1] == "δ(t)" else pair[1]
        return rf"y(t) = {other} \quad \text{{(Identity Property)}}", None
        
    known_identities = {
        # Rectangular Pulse Combinations
        ("rect(t)", "rect(t)"): r"y(t) = tri(t) = r(t+1) - 2r(t) + r(t-1)",
        ("rect(t)", "u(t)"): r"y(t) = r(t + 0.5) - r(t - 0.5)",
        ("rect(t)", "sgn(t)"): r"y(t) = |t + 0.5| - |t - 0.5|",
        ("rect(t)", "r(t)"): r"y(t) = \frac{1}{2}(t+0.5)^2 u(t+0.5) - \frac{1}{2}(t-0.5)^2 u(t-0.5)",
        ("exp(-t)u(t)", "rect(t)"): r"y(t) = (1 - e^{-(t+0.5)})u(t+0.5) - (1 - e^{-(t-0.5)})u(t-0.5)",
        ("cos(t)u(t)", "rect(t)"): r"y(t) = \sin(t+0.5)u(t+0.5) - \sin(t-0.5)u(t-0.5)",
        ("rect(t)", "sin(t)u(t)"): r"y(t) = (1-\cos(t+0.5))u(t+0.5) - (1-\cos(t-0.5))u(t-0.5)",
        
        # Unit Step Combinations
        ("u(t)", "u(t)"): r"y(t) = r(t) = t \cdot u(t)",
        ("r(t)", "u(t)"): r"y(t) = \frac{1}{2}t^2 u(t)",
        ("sgn(t)", "u(t)"): r"y(t) = |t|",
        ("exp(-t)u(t)", "u(t)"): r"y(t) = (1 - e^{-t})u(t)",
        ("cos(t)u(t)", "u(t)"): r"y(t) = \sin(t)u(t)",
        ("sin(t)u(t)", "u(t)"): r"y(t) = (1 - \cos(t))u(t)",
        ("tri(t)", "u(t)"): r"y(t) = \frac{1}{2}r^2(t+1) - r^2(t) + \frac{1}{2}r^2(t-1)",
        
        # Advanced Combinations
        ("r(t)", "r(t)"): r"y(t) = \frac{1}{6}t^3 u(t)",
        ("exp(-t)u(t)", "exp(-t)u(t)"): r"y(t) = t e^{-t} u(t)",
        ("sgn(t)", "sgn(t)"): r"y(t) = \text{Undefined (Diverges to } \infty \text{)}",
        ("cos(t)u(t)", "exp(-t)u(t)"): r"y(t) = \frac{1}{2} (\sin(t) - \cos(t) + e^{-t}) u(t)",
    }

    if pair in known_identities:
        return known_identities[pair], None

    # For anything super crazy not in the table, it forces the integration
    try:
        res = sp.integrate(f_calc * h_calc, (tau, -sp.oo, sp.oo))
        return "y(t) = " + format_standard_form(res), res
    except:
        return r"y(t) = \int_{-\infty}^{\infty} " + sp.latex(f_calc * h_calc).replace(r"\theta", "u") + r" \, d\tau", None

def get_continuous_convolution(s1_name, s2_name):
    t_sym = sp.Symbol('t', real=True)
    tau_sym = sp.Symbol('tau', real=True)
    
    print_dict_tau = get_print_signals(tau_sym)
    print_dict_t_tau = get_print_signals(t_sym - tau_sym)
    
    f_disp = sp.latex(print_dict_tau[s1_name])
    h_disp = sp.latex(print_dict_t_tau[s2_name])
    
    c_dict = get_signals(t_sym)
    f_calc = c_dict[s1_name].subs(t_sym, tau_sym)
    h_calc = c_dict[s2_name].subs(t_sym, t_sym - tau_sym)
    
    formatted_result, math_result = get_smart_analytical_result(s1_name, s2_name, f_calc, h_calc, tau_sym)
    
    return math_result, formatted_result, f_disp, h_disp