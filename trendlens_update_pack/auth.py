"""Optional authentication gate for TrendLens AI.

For a classroom/demo build, auth can remain OFF.
For a more professional build, turn it ON and use Streamlit OIDC login.
MFA is handled by the user's identity provider, such as Google or Microsoft.
"""

import os
from typing import Any


def _truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def auth_required() -> bool:
    """Return whether the app should require login."""
    try:
        import streamlit as st

        value = st.secrets.get("TRENDLENS_AUTH_REQUIRED", os.getenv("TRENDLENS_AUTH_REQUIRED", "false"))
    except Exception:
        value = os.getenv("TRENDLENS_AUTH_REQUIRED", "false")
    return _truthy(value)


def render_auth_gate() -> None:
    """Require OIDC login only when TRENDLENS_AUTH_REQUIRED is true.

    This avoids breaking the classroom demo while still documenting and supporting
    a stronger MFA-capable login option.
    """
    import streamlit as st

    with st.sidebar:
        st.markdown("### Security")

        if not auth_required():
            st.caption("Authentication: off for classroom/demo mode.")
            st.caption("Set TRENDLENS_AUTH_REQUIRED=true to require login.")
            return

        st.caption("Authentication: required. MFA is handled by your Google/Microsoft/OIDC account.")

        if not st.user.is_logged_in:
            st.info("Log in to use TrendLens AI.")
            st.button("Log in", on_click=st.login, use_container_width=True)
            st.stop()

        display_name = getattr(st.user, "name", None) or getattr(st.user, "email", None) or "authenticated user"
        st.success(f"Logged in as {display_name}")
        st.button("Log out", on_click=st.logout, use_container_width=True)
