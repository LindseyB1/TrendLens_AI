## Test Case 7: Welcome Video, Subtitles, and User Onboarding

### Input / Setup
- Add `assets/welcome_captions.vtt`.
- Add or simulate `assets/welcome_video.mp4`.
- Open the Streamlit app landing page.

### Expected Behavior
The app should display a welcome video section near the top of the site. If the MP4 exists, the video should autoplay muted, display subtitles by default, and allow the user to turn on sound with the video controls. If the MP4 does not exist, the app should show a useful placeholder and the voiceover script.

### Actual Output
Pending local app test.

### Pass or Needs Improvement
Pending.

### Notes for Improvement
This strengthens user onboarding, accessibility, and professional presentation.

---

## Test Case 8: Optional OIDC Login and MFA-Ready Design

### Input / Setup
- Keep `TRENDLENS_AUTH_REQUIRED=false` for classroom/demo mode.
- Confirm app loads without requiring login.
- Later set `TRENDLENS_AUTH_REQUIRED=true` after configuring OIDC secrets.

### Expected Behavior
When authentication is disabled, the app should continue to work for classroom testing. When authentication is enabled and OIDC is configured, the app should require login before the user can access the reporting workflow. MFA should be handled by the external identity provider, not by custom app code.

### Actual Output
Pending local app test.

### Pass or Needs Improvement
Pending.

### Notes for Improvement
This improves security while avoiding unnecessary custom password storage for the project prototype.

---

## Test Case 9: Source Input Safety Validation

### Input / Setup
Paste a source containing a fake high-risk pattern such as `123-45-6789` or `OPENAI_API_KEY`.

### Expected Behavior
The app should block report generation and tell the user to remove high-risk content before generating the report.

### Actual Output
Pending local app test.

### Pass or Needs Improvement
Pending.

### Notes for Improvement
This reinforces the public-information-only boundary and lowers the chance of accidental sensitive data entry.
