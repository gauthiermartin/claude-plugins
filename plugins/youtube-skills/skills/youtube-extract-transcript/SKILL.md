---
name: youtube-extract-transcript
description: Use when the user wants to pull the transcript or spoken-word text out of a YouTube video and save it as a standalone markdown file, given a video URL. Pairs with youtube-summarize-transcript, which condenses the resulting file. For research topics, pass the YouTube URL directly to /obsidian-skills:obsidian-research instead — it ingests transcripts itself.
---

1. **Get the URL.** Require a YouTube video URL from the user. If they gave an output path, use it; otherwise default to `~/Documents/Workspace/youtube-transcripts/` and create it with `mkdir -p` if missing.

2. **Confirm yt-dlp.** Run `which yt-dlp`. If missing, install with `uv tool install yt-dlp` — never `pip`/`pip3` for this.

3. **Fetch metadata.** `yt-dlp --skip-download --print "%(title)s|%(id)s|%(channel)s|%(upload_date)s" <url>` gives the title, video ID, channel, and upload date used for the filename and frontmatter.

4. **Download captions.** `yt-dlp --skip-download --write-subs --write-auto-subs --sub-format vtt --sub-langs "en.*,en" -o "<tmp>/%(id)s" <url>`. Manual subs win over auto-generated when both exist. If no English track exists, drop `--sub-langs` and take whatever track yt-dlp lists first.

5. **No captions at all?** Report to the user that this video has no caption track and stop. Do not fall back to audio transcription — out of scope for this skill.

6. **Convert to prose.** Run `uv run "${CLAUDE_PLUGIN_ROOT}/skills/youtube-extract-transcript/vtt_to_text.py" <downloaded.vtt>` to strip cue timing/markup and dedupe the rolling-caption repetition into clean paragraphs.

7. **Write the markdown file.** Frontmatter (`title`, `source_url`, `channel`, `upload_date`, `extracted_at` — today's date, via `date +%Y-%m-%d`) followed by the prose body. Filename: `<slug-of-title>-<video-id>.md`, saved to the resolved output directory.

8. **Done when** the file exists at the resolved path and its body is non-empty prose, not just frontmatter. Report the saved path to the user.

## Common mistakes

- Auto-generated VTT repeats lines across overlapping cues — always run it through `vtt_to_text.py`'s dedupe, never paste raw cue text into the file.
- Installing yt-dlp with `pip`/`pip3` violates this environment's Python tooling rules — use `uv tool install yt-dlp`.
