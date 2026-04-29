import streamlit as st
import time
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("String Matching Visualizer (KMP vs Rabin-Karp)")

text = st.text_input("Text", "ABABDABACDABABCABAB")
pattern = st.text_input("Pattern", "ABABCABAB")
speed = st.slider("Speed", 0.01, 1.0, 0.1)

start = st.button("Start Comparison")

style = """
display:inline-block;
min-width:30px;
text-align:center;
margin:1px;
padding:6px;
border-radius:6px;
font-weight:bold;
"""

def compute_lps_visual(pattern, lps_box, speed):
    lps = [0]*len(pattern)
    length = 0
    i = 1

    while i < len(pattern):

        prev_length = length

        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length-1]
                continue
            else:
                lps[i] = 0
                i += 1

        pattern_html = ""
        lps_html = ""

        for idx, ch in enumerate(pattern):
            if idx == i-1:
                pattern_html += f'<span style="{style} background-color:orange;">{ch}</span>'
            elif idx == prev_length:   
                pattern_html += f'<span style="{style} background-color:green;">{ch}</span>'
            else:
                pattern_html += f'<span style="{style}">{ch}</span>'

        for idx, val in enumerate(lps):
            if idx == i-1:
                lps_html += f'<span style="{style} background-color:red;">{val}</span>'
            else:
                lps_html += f'<span style="{style}">{val}</span>'

        lps_box.markdown(
            "<h4>Building LPS Array</h4>" + pattern_html + "<br>" + lps_html,
            unsafe_allow_html=True
        )

        time.sleep(speed)

    return lps

def render_kmp(text, pattern, i, j, match):
    text_html = ""

    for idx, ch in enumerate(text):
        if idx == i:
            color = "green" if match else "red"
            text_html += f'<span style="{style} background-color:{color};">{ch}</span>'
        else:
            text_html += f'<span style="{style}">{ch}</span>'

    offset = i - j
    space = "".join([f'<span style="{style} visibility:hidden;">X</span>' for _ in range(offset)])

    pattern_html = "".join(
        [f'<span style="{style} background-color:blue;">{ch}</span>' for ch in pattern]
    )

    return text_html, space + pattern_html

def render_rk(text, pattern, start, m):
    text_html = ""

    for idx, ch in enumerate(text):
        if start <= idx < start + m:
            text_html += f'<span style="{style} background-color:red;">{ch}</span>'
        else:
            text_html += f'<span style="{style}">{ch}</span>'

    space = "".join([f'<span style="{style} visibility:hidden;">X</span>' for _ in range(start)])

    pattern_html = "".join(
        [f'<span style="{style} background-color:blue;">{ch}</span>' for ch in pattern]
    )

    return text_html, space + pattern_html

if start:

    col1, col2 = st.columns(2)

    kmp_steps = 0
    rk_steps = 0

    with col1:
        st.subheader("KMP")
        step_kmp_box = st.empty()
        lps_box = st.empty()
        st.markdown("---")
        kmp_box = st.empty()

    with col2:
        st.subheader("Rabin-Karp")
        step_rk_box = st.empty()
        rk_box = st.empty()

    progress = st.progress(0)

    lps = compute_lps_visual(pattern, lps_box, speed)
    time.sleep(0.3)

    i = j = 0

    d = 256
    q = 101
    m = len(pattern)
    n = len(text)

    p = t = 0
    h = 1

    for x in range(m-1):
        h = (h*d) % q

    for x in range(m):
        p = (d*p + ord(pattern[x])) % q
        t = (d*t + ord(text[x])) % q

    rk_i = 0

    while i < len(text) or rk_i <= n - m:

        if i < len(text):
            kmp_steps += 1
            step_kmp_box.markdown(f"**Steps:** {kmp_steps}")

            match = text[i] == pattern[j]
            text_html, pattern_html = render_kmp(text, pattern, i, j, match)

            kmp_box.markdown(text_html + "<br>" + pattern_html, unsafe_allow_html=True)

            if match:
                i += 1
                j += 1
            else:
                if j != 0:
                    j = lps[j-1]
                else:
                    i += 1

            if j == len(pattern):
                col1.success(f"Match at index {i - j}")
                j = lps[j-1]

        if rk_i <= n - m:
            rk_steps += 1
            step_rk_box.markdown(f"**Steps:** {rk_steps}")

            text_html, pattern_html = render_rk(text, pattern, rk_i, m)
            rk_box.markdown(text_html + "<br>" + pattern_html, unsafe_allow_html=True)

            if p == t:
                match = True
                for x in range(m):
                    if text[rk_i+x] != pattern[x]:
                        match = False
                        break
                if match:
                    col2.success(f"Match at index {rk_i}")

            if rk_i < n - m:
                t = (d*(t - ord(text[rk_i])*h) + ord(text[rk_i+m])) % q
                if t < 0:
                    t += q

            rk_i += 1

        progress.progress(min(i/len(text), 1.0))
        time.sleep(speed)

    st.markdown("## Performance Comparison")

    fig, ax = plt.subplots(figsize=(3, 2))  # smaller
    ax.bar(["KMP", "Rabin-Karp"], [kmp_steps, rk_steps])
    ax.set_title("Step Comparison", fontsize=10)
    ax.set_ylabel("Steps", fontsize=8)
    ax.tick_params(labelsize=8)

    plt.tight_layout()

    st.pyplot(fig, use_container_width=False)