# Case Closed Files: episode playbook

Every scheduled run is a fresh cloud machine. It knows nothing except this repo and the
claude.ai project "Youtube Automation". Follow these steps in order.

## 0. Set up (5 min)
```
git clone https://github.com/henkobrandt-netizen/case-closed-files && cd case-closed-files
bash pipeline/setup.sh
```

## 1. Pick the case
- Take the top unclaimed topic in `episodes/BACKLOG.md`. Skip anything already in `episodes/`.
- Good topic: a true con, heist, forgery or swindle with a clear trick, a twist, and good sources.
  Advertiser-friendly: no gore, no sexual crimes, nothing about children, no living private people.
- Living public figures: stick to court records and major reporting. No new allegations.

## 2. Research (skills: deep-research or WebSearch, content-research-and-sourcing)
- At least 3 solid sources (museum, major paper, book, court record, Smithsonian, BBC...).
- Note every number, date and name with its source in `episodes/<id>/sources.md`.
- Where sources disagree, the script must say so ("accounts differ", "the story goes").

## 3. Write the script (skills: youtube-long-form, storytelling-and-narrative, hook-writer)
- Target 1,350-1,500 words: about 8-9 minutes at 180 wpm. 8 min+ lets YouTube run mid-roll ads.
- Structure: cold open (most tense moment, under 30 s, ends on a question) → title card →
  who → the setup → the trick (show HOW it worked, step by step) → the doubt → the save →
  the payoff → the twist / unravel → the ending → one-line "still standing" style close → outro.
- Re-hook every 60-90 s: a question, a reveal, or "but there was a problem".
- Write numbers and years as words in the spoken text. Short sentences. Present tense in the cold open.
- `SHORTS`: three parts, `{"a": [...], "b": [...], "c": [...]}`, each **60-100 s** (never under 60).
  Each part is its own mini story from a different stretch of the episode:
  a = cold open + who, b = the trick, c = the doubt / the test. Never give away the final twist.
  Each part: `("hook_x", [(spoken, "caption|split")])` → 2-3 long scenes as `(sid, None)` (reuses the
  LONG lines, so the animation stays in sync; to reword, keep the same number of lines) →
  `("cta_x", [(spoken, "caption")])`. CTA a/b: "Part two: ... Follow for part two."
  CTA c: "The full case is on the channel." Check lengths with `build.py <ep> plan`.
- Check names with `k.tokenizer.phonemize`; add fixes to `PHONEME_FIX`.

## 4. Animate (`episodes/<id>/scenes.py`)
- One function per scene, named `sc_<scene id>`. Shorts reuse these: `pipeline/shorts.py` frames each
  line in 9:16 automatically (follows what appears, never slices text, pulls wider when needed),
  and adds the CASE / PART header, progress bar and auto captions.
- Per part add `SCENES["hook_x"] = hook_card([2 big lines], stamp_text=..., prop=...)` and
  `SCENES["cta_x"] = cta_card("CASE 00N · NAME", "PART 2 NEXT" | "PART 3 NEXT" | "FULL CASE")`.
  A bad auto frame can be pinned with `SHORT_VIEW = {"sid": 0.4}` (x as a fraction of 1920).
- Reuse `pipeline/lib.py` pieces: figure, card/dossier, letter, newspaper, stamp, label, item
  checklist, route map, liner, two-person table, suspicion bar, chip, notes_pile, skylines...
- Look: dark navy, gold accents, red stamps, paper documents, silhouettes. Never a real photo,
  never a copyrighted artwork, logo or character. Real people only as silhouettes.
- Label invented documents "RECONSTRUCTION" or "ILLUSTRATION".
- Add `HITS` / `SHORT_HITS` for stamp thuds, `THUMB_WORDS` + `thumbnail()`.
- Check: `python3 pipeline/build.py episodes/<id> stills` then look at every contact sheet (long and short_a/b/c).
  Fix overlaps, text off screen, empty frames, anything unreadable. Repeat until clean.

## 5. Build
`python3 pipeline/build.py episodes/<id>` (tts → render → audio → final → thumbs → qa). ~30 min on 2 cores.
QA must show: long ≤ 90 MB, each short ≤ 40 MB and 60-100 s, loudness about -16 LUFS, long ≥ 8:00.
Use `--names short_a,short_b` to rebuild only some cuts.
Pull 6 frames from the final long.mp4 and look at them.

## 6. Thumbnail + metadata (skills: thumbnail-design, youtube-publishing-and-metadata)
- Thumbnail: one hero object + one silhouette + 0-3 bold outlined words that do NOT repeat the title.
  Must read in greyscale at 168 px wide (`work/thumb_check.png`). Make 3 variants for A/B.
- Title: under 60 characters, main keyword first, curiosity without lying.
- `description.txt`: 300-500 words. Line 1 = hook. Keyword in lines 2-3. Chapters from the qa
  output (first one 0:00). About-the-channel paragraph. Sources note + "synthetic voice" note.
- `meta.json`: title, tags (first = exact title keyword), categoryId 27, madeForKids false.

## 7. Publish
1. Copy description into `media/<id>/`, commit `episodes/<id>` (not work/) and `media/<id>/`, push.
2. vidIQ: `vidiq_video_upload` with `https://raw.githubusercontent.com/henkobrandt-netizen/case-closed-files/main/media/<id>/long.mp4`
   (and short_a/b/c.mp4). Thumbnail: `vidiq_upload_image` with the raw URL of thumb_1.jpg.
3. `vidiq_social_post_draft_create`. Long: Case Closed Files YouTube, public, 17:00 SAST on the next
   free day, thumbnailImageId. Each short part: ONE draft per part with three destinations, all at
   the same time: YouTube (public, title "... (Part N/3) #shorts"), Instagram, TikTok
   (PUBLIC_TO_EVERYONE, allowComment true, musicUsageConfirmed true: the user chose these 17 Nov 2026).
   Short slots: 12:00 and 19:00 SAST, the next free ones after the long, parts in order.
   Accounts: YouTube UCwu-WpflQQiUYFDwYOQxMug, Instagram 29969156796002355. NEVER Vice City Moments
   (_000uVwT74MhVnXlVEc3loFY7qs5fEQAOUfu) or The Build Bill.
   **TikTok: the user posts it by hand** (decided 17 Nov 2026). Do not add a TikTok destination.
3b. Hand-off (every run, the user asked for it): write `handoff/<date>.json` (copy the last one: title,
   posts = the 3 parts with the same times as YouTube, TikTok captions "hook + Part N/3 + Follow for Part
   N+1 + Full case on YouTube: Case Closed Files + 6 hashtags", todos = anything the user must do),
   run `python3 pipeline/handoff.py handoff/<date>.json`, publish the .html as an artifact (the TikTok
   posting kit) and send the .ics with SendUserFile (the user taps it on iPhone to add the reminders).
4. Send the user ONE message with the drafts, the kit link and the .ics. Publish only after they say yes.
5. Log the episode in `episodes/LOG.md` and mark the topic taken in BACKLOG.md. Commit + push.

## House rules
- Same voice every episode (config.py). Same look. Same "CASE CLOSED" outro.
- Never invent facts, quotes, or numbers. Hedge disputed claims on screen and in narration.
- No copyrighted music, art, footage, logos or characters.
- vidIQ credits are scarce (free plan): uploads and posting are free, scoring/generation is not.
