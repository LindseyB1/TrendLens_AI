# TrendLens AI Update Patch Instructions

This update adds:

1. Welcome video support with subtitles.
2. Optional OIDC login/MFA-ready authentication gate.
3. Public-input safety checks.
4. Additional pytest smoke tests.
5. Documentation update text.

## 1. Add these new files to the project root

Copy these files/folders into the TrendLens_AI repo:

```text
ui_components.py
auth.py
security_utils.py
assets/welcome_captions.vtt
scripts/generate_welcome_voice.py
Tests/test_security_and_ui.py
.streamlit/secrets.example.toml
```

## 2. Update requirements.txt

Add any missing lines from `requirements_patch.txt`.

## 3. Update app.py imports

Near the top of `app.py`, add:

```python
from auth import render_auth_gate
from security_utils import PUBLIC_ONLY_WARNING, validate_public_sources
from ui_components import render_welcome_video
```

## 4. Add auth gate after st.set_page_config(...)

Immediately after `st.set_page_config(...)`, add:

```python
render_auth_gate()
```

Keep `TRENDLENS_AUTH_REQUIRED=false` until your OIDC secrets are configured.

## 5. Add the welcome video after your header/banner loads

Inside `render_header()`, after the title/caption/intro paragraph, add:

```python
render_welcome_video()
```

The app will show a placeholder until you add:

```text
assets/welcome_video.mp4
```

The captions file already exists:

```text
assets/welcome_captions.vtt
```

## 6. Add source validation before report generation

After you build `sources` and `valid_source_count`, add:

```python
source_errors, source_warnings = validate_public_sources(sources)

for warning in source_warnings:
    st.warning(warning)

for error in source_errors:
    st.error(error)
```

Then inside the Generate button logic, add this check before calling the model:

```python
elif source_errors:
    st.error("Fix the source input issues before generating a report.")
```

## 7. Create the voiceover and video

Generate the AI voiceover:

```powershell
python scripts/generate_welcome_voice.py
```

This creates:

```text
assets/welcome_voice.mp3
```

Then create the final MP4 in Canva, Clipchamp, CapCut, or another editor:

```text
assets/welcome_video.mp4
```

Use the MP3 voiceover, short visuals, a soft fade-in/fade-out, and the caption text from `assets/welcome_captions.vtt`.

## 8. Test locally

```powershell
python -m pytest Tests/test_security_and_ui.py -v
python -m streamlit run app.py
```

## 9. Commit and push

```powershell
git status
git add app.py auth.py security_utils.py ui_components.py assets/welcome_captions.vtt scripts/generate_welcome_voice.py Tests/test_security_and_ui.py .streamlit/secrets.example.toml requirements.txt README.md BUILD_LOG.md Tests/eval_results.md AI_PROMPT_LOG.md
git commit -m "Add welcome video, captions, auth gate, and security tests"
git push
```
