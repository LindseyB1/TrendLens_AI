## Prompt / Design Iteration - Welcome Video and Security Polish

User goal: Add a short AI-voice welcome video that autoplays when users enter the site, explains the intent of TrendLens AI, explains the problem it solves, and gives simple steps for use.

Design decision:
- Video autoplays muted to comply with normal browser behavior.
- Users can manually enable sound through video controls.
- Subtitles are included by default through a WebVTT caption file.
- The video script uses an elevator-pitch structure: attention grabber, purpose, workflow, output value, safety boundary, and closing value statement.

Security iteration:
- Added optional OIDC login gate.
- MFA is handled by the identity provider instead of custom code.
- Added high-risk input checks for possible SSNs, API keys, private keys, and classification markings.
- Preserved classroom/demo usability by making authentication optional.
