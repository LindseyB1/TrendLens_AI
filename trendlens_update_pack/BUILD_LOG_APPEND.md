### 06JUN2026 - Welcome Video, Captions, Authentication, and Security Test Update

- Added a welcome video component for first-time users.
- Added `assets/welcome_captions.vtt` so subtitles display with the welcome video.
- Configured the video to autoplay muted because browsers commonly block autoplay with sound before user interaction.
- Added optional OIDC login gate in `auth.py`.
- Documented MFA as identity-provider-managed through Google, Microsoft, or another OIDC provider rather than custom-built inside the app.
- Added `security_utils.py` for public-input validation and high-risk content checks.
- Added tests in `Tests/test_security_and_ui.py` to verify caption creation, input normalization, and sensitive-pattern blocking.
- Added `.streamlit/secrets.example.toml` as a safe template while keeping real `.streamlit/secrets.toml` ignored.
- Updated documentation to explain the welcome video, captions, optional login, MFA-ready design, and public-information-only safety boundary.
