import streamlit as st


# ==========================================================
# DEFAULT THEME
# ==========================================================

def initialize_theme():

    if "theme" not in st.session_state:

        st.session_state.theme = "Light"


# ==========================================================
# CURRENT THEME
# ==========================================================

def current_theme():

    return st.session_state.theme


# ==========================================================
# TOGGLE THEME
# ==========================================================

def toggle_theme():

    if st.session_state.theme == "Light":

        st.session_state.theme = "Dark"

    else:

        st.session_state.theme = "Light"


# ==========================================================
# LIGHT THEME CSS
# ==========================================================

LIGHT_THEME = """
<style>

body{

    background:#FFFFFF;

    color:#111827;

}

.block-container{

    background:#FFFFFF;

}

div[data-testid="stMetric"]{

    border-radius:12px;

    padding:10px;

}

</style>
"""


# ==========================================================
# DARK THEME CSS
# ==========================================================

DARK_THEME = """
<style>

body{

    background:#0E1117;

    color:#FAFAFA;

}

.block-container{

    background:#0E1117;

}

div[data-testid="stMetric"]{

    border-radius:12px;

    padding:10px;

}

</style>
"""


# ==========================================================
# APPLY THEME
# ==========================================================

def apply_theme():

    initialize_theme()

    if current_theme() == "Dark":

        st.markdown(

            DARK_THEME,

            unsafe_allow_html=True

        )

    else:

        st.markdown(

            LIGHT_THEME,

            unsafe_allow_html=True

        )


# ==========================================================
# THEME SWITCH
# ==========================================================

def theme_switch():

    initialize_theme()

    if st.button(

        f"🌙 Switch to {'Dark' if current_theme() == 'Light' else 'Light'} Mode",

        use_container_width=True

    ):

        toggle_theme()

        st.rerun()