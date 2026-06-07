"""Optional authentication gate for TrendLens AI.

For a classroom/demo build, auth can remain OFF.
For a more professional build, turn it ON and use Streamlit OIDC login.
MFA is handled by the user's identity provider, such as Google or Microsoft.
"""

import os
from typing import Any
import logging


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

        required = auth_required()

        if not required:
            st.success("Demo mode: Authentication is OFF")
            st.caption("This app is configured for classroom/demo grading by default.")
            st.markdown(
                "Set the environment variable `TRENDLENS_AUTH_REQUIRED=true` or add it to Streamlit secrets to require login in production."
            )
            st.markdown(
                "**Production note:** Use Streamlit OIDC providers (Google, Microsoft, Okta, Auth0). Configure client IDs and secrets in `.streamlit/secrets.toml` or Streamlit Cloud secrets — do not commit these to GitHub."
            )
            st.caption("MFA is provider-managed by your identity provider.")
            return

        st.warning("Authentication: REQUIRED")
        st.markdown("MFA is handled by your identity provider (Google, Microsoft, Okta, Auth0). The app does not store passwords or MFA codes.")

        # Try to detect logged in user in a resilient way
        user_display = None

        try:
            user_obj = getattr(st, "user", None) or st.session_state.get("user")

            if user_obj:
                user_display = getattr(user_obj, "name", None) or getattr(user_obj, "email", None) or str(user_obj)
        except Exception as e:
            logging.debug(f"Auth: could not read user object: {e}")

        if user_display:
            st.success(f"Logged in as {user_display}")
            if hasattr(st, "logout"):
                st.button("Log out", on_click=st.logout, use_container_width=True)
        else:
            st.info("Log in to use TrendLens AI (production mode).")
            if hasattr(st, "login"):
                st.button("Log in", on_click=st.login, use_container_width=True)
            else:
                st.caption("Login button not available in this environment. Configure Streamlit OIDC or deploy on Streamlit Cloud/Enterprise to enable login buttons.")
