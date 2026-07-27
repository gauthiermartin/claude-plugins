# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Convert a WebVTT caption file into deduplicated plain-text prose."""
import re
import sys
from pathlib import Path

TAG_RE = re.compile(r"<[^>]+>")
TIMESTAMP_LINE_RE = re.compile(r"-->")
WORD_TAG_RE = re.compile(r"<c>|</c>|<\d{2}:\d{2}:\d{2}\.\d{3}>")


def parse_cues(vtt_text: str) -> list[tuple[list[str], bool]]:
    """The file header (WEBVTT line plus Kind:/Language: metadata) ends at
    the first cue timing line — skip everything before that unconditionally.
    Each cue is returned with whether it carried word-level karaoke tags
    (the mark of an auto-caption 'growing' cue, vs. a plain echo cue)."""
    cues: list[tuple[list[str], bool]] = []
    current: list[str] = []
    tagged = False
    header_done = False
    for raw_line in vtt_text.splitlines():
        line = raw_line.strip()
        if not header_done:
            if TIMESTAMP_LINE_RE.search(line):
                header_done = True
            continue
        if not line:
            if current:
                cues.append((current, tagged))
                current = []
                tagged = False
            continue
        if line.startswith(("NOTE", "STYLE", "REGION")) or TIMESTAMP_LINE_RE.search(line):
            continue
        if line.isdigit():
            continue
        if WORD_TAG_RE.search(line):
            tagged = True
        clean = TAG_RE.sub("", line).strip()
        if clean:
            current.append(clean)
    if current:
        cues.append((current, tagged))
    return cues


def extract_lines(cues: list[tuple[list[str], bool]]) -> list[str]:
    """Auto-captions render a rolling 2-line window: a 'growing' cue (tagged,
    word-by-word) is followed by a brief untagged 'settle' cue that just
    re-flashes the newest line. Only a growing cue's last line is new content
    — its earlier line(s) and every settle cue are echoes to discard.

    Manual/plain subtitles carry no tags at all; there every cue is new
    content, so nothing gets discarded."""
    if not any(is_tagged for _, is_tagged in cues):
        return [line for lines, _ in cues for line in lines]
    return [lines[-1] for lines, is_tagged in cues if is_tagged and lines]


def to_prose(lines: list[str]) -> str:
    text = re.sub(r"\s+", " ", " ".join(lines)).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    paragraphs = [" ".join(sentences[i : i + 4]) for i in range(0, len(sentences), 4)]
    return "\n\n".join(paragraphs)


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: vtt_to_text.py <captions.vtt>", file=sys.stderr)
        raise SystemExit(1)
    vtt_path = Path(sys.argv[1])
    cues = parse_cues(vtt_path.read_text(encoding="utf-8"))
    print(to_prose(extract_lines(cues)))


if __name__ == "__main__":
    main()
