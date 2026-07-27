---
name: youtube-summarize-transcript
description: Use when the user wants to summarize a YouTube transcript markdown file, such as one produced by youtube-extract-transcript.
---

1. **Get the transcript file.** Require a path to an existing transcript markdown file. If it doesn't exist, stop and ask the user for a valid path — don't guess one.

2. **Read the whole body.** Separate the frontmatter (`title`, `source_url`, `channel`, `upload_date`) from the prose body. For a long transcript, read it in full before writing anything — a summary drafted from only the opening section silently drops the video's later topics.

3. **Write the TL;DR.** A 2-3 sentence paragraph capturing what the video is about and its main conclusion. Keep supporting detail out of it — that belongs in Key Points.

4. **Write the Key Points.** A bulleted list of the video's distinct topics, claims, and takeaways, in the order they occur. One bullet per distinct point — every topic the transcript covers should be represented by at least one bullet, not just the first few.

5. **Assemble the summary file.** Frontmatter: the transcript's `title`, `source_url`, `channel`, `upload_date`, plus `summarized_at` (today's date, via `date +%Y-%m-%d`) and `source_transcript` (the transcript file's path). Body, in order: a `[Full transcript](<relative-or-absolute-path>)` markdown link to the source file, the TL;DR paragraph, then a `## Key Points` heading with the bullets. The link makes the source reachable by clicking, not just by reading frontmatter.

6. **Save.** Same filename as the source transcript (for traceability between the two), written to `~/Documents/Workspace/youtube-transcript-summaries/` — create it with `mkdir -p` if missing.

7. **Done when** the summary file exists, its TL;DR is non-empty, and every distinct topic in the transcript is represented in Key Points. Report the saved path to the user.

## Common mistakes

- Truncating the read partway through a long transcript — Key Points then only covers the beginning of the video.
- Letting the TL;DR balloon into a second Key Points list instead of staying to 2-3 sentences.
- Dropping the transcript's frontmatter instead of carrying it into the summary — that's what keeps the summary traceable to its source video.
