# M3akKoura — Automated Football Content Research Pipeline

An automated pipeline that picks a trending football player, researches their career, finds and downloads relevant highlight footage, and uses AI vision to identify the best goal/celebration moments worth turning into short-form video content.

This is a personal learning project focused on **API integration, LLM orchestration, and pipeline automation** — built to strengthen backend and automation skills, not a production content system.

> **Status**: Research pipeline complete and working end-to-end. Video rendering, QA scoring, and workflow orchestration (n8n) are in progress. See [Roadmap](#roadmap) below.

## What it does

1. **Topic discovery** — pulls Google Trends data for a list of football keywords, scores them, and picks the most "hot" one right now
2. **Career research** — fetches the player's Wikipedia page and uses an LLM to extract their real senior clubs (filtering out youth academies and one-off appearances)
3. **Video sourcing** — searches YouTube per club + player combo, ranks results by view count
4. **Smart downloading** — downloads videos in ranked order until a disk-space budget (~1GB) is reached, with automatic retry on failure
5. **Vision analysis** — extracts frames every few seconds from each video, describes each frame using a vision-language model, then has a second LLM read the full sequence and pick out the actual goal/celebration moments with timestamps and reasoning

## Architecture

```
main.py                          # orchestrator — runs the full pipeline
pipeline/
  research/
    topic.py                     # Google Trends scoring
    football_api.py              # Wikipedia + LLM career extraction
    popularity.py                # YouTube search + ranking
    downloader.py                # yt-dlp video downloading
    vision.py                    # ffmpeg frame extraction + vision LLM + decision LLM
  planner/                       # (in progress) AI edit planning
  qa/                            # (in progress) automated quality scoring
  video/                         # (in progress) rendering engine
config/
  keywords.txt                   # trending topic candidates
```

## Tech stack

| Tool | Role |
|---|---|
| Python | Core pipeline logic |
| Google Trends (`pytrends`) | Topic/trend discovery |
| Wikipedia API | Player career data |
| NVIDIA-hosted LLMs (Kimi K3, Llama 3.2 Vision) | Career extraction, frame description, moment selection |
| YouTube Data API v3 | Video search and metadata |
| `yt-dlp` | Video downloading |
| `ffmpeg` | Frame extraction |

## Challenges & how they were solved

A few of the real problems hit while building this, since debugging real APIs is most of the actual work:

- **A silent logic bug that looked like it worked.** An early version of the team-confirmation step accidentally sent a team *name* where the football API expected a numeric team *id*. It didn't error — it just returned inconsistent, sometimes-wrong results, which is far more dangerous than a crash. Traced it by printing the raw variable inside the loop instead of assuming its type, which exposed the mismatch immediately.

- **A "working" result that was actually a false positive.** After fixing the bug above, results still looked plausible but were inconsistent between runs for the same input. Digging into the raw API responses revealed the football stats API's player-search endpoint depends on season context — a player no longer active at a club (e.g. searching a retired stint) can legitimately return zero results even though the request itself is correct. Solved by dropping the external verification step entirely and replacing it with a tightly-scoped LLM prompt (explicit exclusion rules + "do not fabricate numbers") — simpler, more reliable, and removed a fragile third-party dependency.

- **Chasing a moving target across model deprecations.** Multiple LLM model identifiers returned 404 or 410 (end-of-life) errors mid-project as the provider's catalog changed. Solved by verifying exact model strings directly against the provider's live model pages instead of reusing remembered names, and building small isolated test scripts to confirm a model actually works before wiring it into the main pipeline.

- **A download that "succeeded" but returned the wrong data.** After a video download completed successfully, extracting the final file path crashed with a `KeyError`. The library merges separate video/audio streams into one file, and the expected key didn't reflect the post-merge path. Solved by printing all available keys on the result object and finding the correct nested field (`requested_downloads`) instead of guessing.

- **Designing around a hard resource constraint.** With limited disk space, the pipeline couldn't just download every candidate video. Solved by ranking candidates by popularity and downloading in order while tracking cumulative file size, stopping once a fixed budget is hit — a simple greedy algorithm that keeps the system usable on modest hardware.

- **Handling AI output that doesn't always come back clean.** LLM responses are expected to be structured JSON, but real API calls can fail (rate limits) or occasionally return malformed output. Solved with defensive error handling that lets the pipeline continue processing other videos in a batch instead of crashing entirely on one bad response.

## Roadmap

- [ ] Django API layer wrapping each pipeline stage
- [ ] n8n workflow orchestration (visual pipeline, retries, scheduling)
- [ ] AI edit planner (timestamp-level clip selection and sequencing)
- [ ] Automated QA scoring system
- [ ] Video rendering engine (ffmpeg-based cutting, transitions, audio sync)

## Notes

This project downloads publicly available footage for personal research and portfolio/learning purposes only — it is not intended for public redistribution or commercial use.
