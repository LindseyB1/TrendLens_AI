## Welcome Video, Captions, and Accessibility

TrendLens AI includes a short welcome video concept that introduces the site, explains the problem it solves, and gives users a simple step-by-step workflow. The video is designed to autoplay muted because browsers commonly block autoplay with sound before user interaction. Users can turn on the AI voice through the video controls.

The video also includes a WebVTT subtitle track at `assets/welcome_captions.vtt`. Captions support accessibility and make the introduction usable even when the video starts muted.

## Optional Login and MFA-Ready Authentication

TrendLens AI includes an optional authentication gate using Streamlit's OpenID Connect login workflow. For the classroom/demo version, authentication can remain disabled with `TRENDLENS_AUTH_REQUIRED=false`.

When authentication is enabled, login is handled through an external identity provider such as Google or Microsoft. Multi-factor authentication is not stored or managed inside TrendLens AI; it is handled by the user's identity provider account settings. This keeps the project safer than building a custom password and MFA database for a classroom prototype.

## Input Safety Controls

The app includes basic input validation to remind users to use only public or synthetic information. The validation helper flags common high-risk patterns such as possible SSNs, API keys, private keys, and classification markings before source text is sent to the model.

These checks do not replace human review, but they help reinforce the project boundary: do not paste classified, private, sensitive, restricted, protected, or personal information.
