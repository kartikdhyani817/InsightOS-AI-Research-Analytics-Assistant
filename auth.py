import hashlib
from typing import Any


# ==========================================================
# DEFAULT USER
# ==========================================================

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "insightos123"


# ==========================================================
# HASH PASSWORD
# ==========================================================

def hash_password(password: str) -> str:
    """Return the SHA-256 hash of a password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ==========================================================
# STORED HASH
# ==========================================================

STORED_PASSWORD = hash_password(DEFAULT_PASSWORD)


# ==========================================================
# AUTHENTICATE
# ==========================================================

def authenticate(username: str, password: str) -> bool:
    """Validate the supplied username and password."""
    if not isinstance(username, str) or not isinstance(password, str):
        return False

    return (
        username.strip() == DEFAULT_USERNAME
        and hash_password(password) == STORED_PASSWORD
    )


# ==========================================================
# LOGIN STATUS
# ==========================================================

def is_logged_in(session_state: Any) -> bool:
    """Return True when the current Streamlit session is logged in."""
    return bool(session_state.get("logged_in", False))


# ==========================================================
# LOGIN
# ==========================================================

def login(*args: Any) -> bool:
    """
    Backward-compatible login helper.

    Supported usage:

    auth.login(username, password)
        Validates credentials and returns True or False.

    auth.login(session_state)
        Marks an already-authenticated session as logged in.

    auth.login(username, password, session_state)
        Validates credentials and updates the session automatically.
    """

    # Used by app.py as: auth.login(username, password)
    if len(args) == 2:
        username, password = args
        return authenticate(username, password)

    # Used as: auth.login(session_state)
    if len(args) == 1:
        session_state = args[0]
        session_state["logged_in"] = True
        session_state["username"] = DEFAULT_USERNAME
        return True

    # Optional combined usage:
    # auth.login(username, password, st.session_state)
    if len(args) == 3:
        username, password, session_state = args

        if authenticate(username, password):
            session_state["logged_in"] = True
            session_state["username"] = DEFAULT_USERNAME
            return True

        session_state["logged_in"] = False
        return False

    raise TypeError(
        "login() expects (username, password), "
        "(session_state), or (username, password, session_state)"
    )


# ==========================================================
# LOGOUT USER
# ==========================================================

def logout(session_state: Any) -> None:
    """Log the current user out and clear stored username information."""
    session_state["logged_in"] = False
    session_state["username"] = ""


# ==========================================================
# CURRENT USER
# ==========================================================

def current_user(session_state: Any) -> str | None:
    """Return the logged-in username, otherwise None."""
    if is_logged_in(session_state):
        return session_state.get("username") or DEFAULT_USERNAME

    return None