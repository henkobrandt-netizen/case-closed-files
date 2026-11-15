"""House style for Case Closed Files. Change here, every episode follows."""
VOICE = "am_michael"      # Kokoro voice. Same voice every episode.
SPEED = 1.12              # ~180 words/min
SENT_PAUSE = 0.13         # silence between sentences (s)
LONG_PAD = dict(lead=.25, gap=.2, tail=.35)
SHORT_PAD = dict(lead=.08, gap=.12, tail=.2)
FIXED = {"title": 3.2, "outro": 4.0}  # scenes with no narration
BPM = 104
LONG_MAX_MB = 90          # GitHub raw limit is 100 MB per file
SHORT_MAX_MB = 40
KOKORO_DIR = "/home/claude/.cache/kokoro"
