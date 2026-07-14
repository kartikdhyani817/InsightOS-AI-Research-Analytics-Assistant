import hashlib


# ==========================================================
# DEFAULT USER
# ==========================================================

DEFAULT_USERNAME = "admin"

DEFAULT_PASSWORD = "insightos123"


# ==========================================================
# HASH PASSWORD
# ==========================================================

def hash_password(password):

    return hashlib.sha256(

        password.encode()

    ).hexdigest()


# ==========================================================
# STORED HASH
# ==========================================================

STORED_PASSWORD = hash_password(

    DEFAULT_PASSWORD

)


# ==========================================================
# LOGIN
# ==========================================================

def authenticate(

    username,

    password

):

    if username != DEFAULT_USERNAME:

        return False

    return (

        hash_password(password)

        ==

        STORED_PASSWORD

    )


# ==========================================================
# LOGIN STATUS
# ==========================================================

def is_logged_in(session_state):

    return session_state.get(

        "logged_in",

        False

    )


# ==========================================================
# LOGIN USER
# ==========================================================

def login(session_state):

    session_state.logged_in = True


# ==========================================================
# LOGOUT USER
# ==========================================================

def logout(session_state):

    session_state.logged_in = False


# ==========================================================
# CURRENT USER
# ==========================================================

def current_user(session_state):

    if session_state.get(

        "logged_in",

        False

    ):

        return DEFAULT_USERNAME

    return None