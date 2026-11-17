"""Hand-off for the user: a TikTok posting kit (HTML page) and an iCloud-ready reminders file (.ics).

usage: python3 pipeline/handoff.py handoff/<name>.json
The JSON holds {"title", "posts": [{when, case, part, title, video, caption}],
"todos": [{when, title, notes, minutes?, rrule?}]}. `when` is local SAST "YYYY-MM-DD HH:MM".
Writes handoff/<name>.html and handoff/<name>.ics. Every post also becomes a reminder.
Also rebuilds calendar/ccf-tiktok.ics from every handoff/*.json: the user's iPhone subscribes to
https://raw.githubusercontent.com/henkobrandt-netizen/case-closed-files/main/calendar/ccf-tiktok.ics
so commit and push after running this, and new reminders show up on their phone by themselves.
"""
import sys, json, html, datetime as dt, os, uuid

SAST = dt.timezone(dt.timedelta(hours=2))
def parse(s): return dt.datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=SAST)
def z(d): return d.astimezone(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def ics_text(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")

def fold(line):
    b = line.encode(); out = []
    while len(b) > 74:
        cut = 74
        while (b[cut] & 0xC0) == 0x80: cut -= 1   # never split a UTF-8 character
        out.append(b[:cut].decode()); b = b" " + b[cut:]
    out.append(b.decode()); return "\r\n".join(out)

def ics(items, cal):
    L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Case Closed Files//Handoff//EN", "CALSCALE:GREGORIAN",
         "METHOD:PUBLISH", f"X-WR-CALNAME:{ics_text(cal)}", "X-WR-TIMEZONE:Africa/Johannesburg",
         "REFRESH-INTERVAL;VALUE=DURATION:PT6H", "X-PUBLISHED-TTL:PT6H"]
    stamp = z(dt.datetime.now(SAST))
    for it in items:
        start = parse(it["when"]); end = start + dt.timedelta(minutes=it.get("minutes", 15))
        L += ["BEGIN:VEVENT", f"UID:{uuid.uuid5(uuid.NAMESPACE_URL, it['title'] + it['when'])}@caseclosedfiles",
              f"DTSTAMP:{stamp}", f"DTSTART:{z(start)}", f"DTEND:{z(end)}",
              f"SUMMARY:{ics_text(it['title'])}", f"DESCRIPTION:{ics_text(it.get('notes', ''))}"]
        if it.get("url"): L.append(f"URL:{it['url']}")
        if it.get("rrule"): L.append(f"RRULE:{it['rrule']}")
        for m in (10, 0):
            L += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{ics_text(it['title'])}", f"TRIGGER:-PT{m}M", "END:VALARM"]
        L.append("END:VEVENT")
    L.append("END:VCALENDAR")
    return "\r\n".join(fold(l) for l in L) + "\r\n"

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Special+Elite&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
/* VOICE: a field agent's job sheet, plain and quick to act on.
   IDEA: a manila case folder with dated orders clipped inside.
   PICTURE: the stack of order slips itself, each stamped when posted.
   COLOUR and TYPE: white paper, folder tan, stamp red; Special Elite titles, Inter text.
   LAYOUT: one column of slips with big hanging times, settings card on top. */
:root{color-scheme:light dark;--bg:light-dark(#ffffff,#121316);--paper:light-dark(#ffffff,#1b1d22);--ink:light-dark(#16181d,#eceae4);
--mute:light-dark(#5b5f69,#a3a6ad);--tan:light-dark(#d9b77e,#8a6a35);--tanbg:light-dark(#f3e6cc,#2a2419);--red:light-dark(#c8312b,#ff6b5f);--line:light-dark(#e3ddd0,#2f3138)}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Inter,system-ui,sans-serif;overflow-x:clip}
.band{padding:clamp(24px,4vw,56px) max(5vw,16px);max-width:820px;margin:0 auto}
.folder{background:var(--tanbg);border-top:14px solid var(--tan);border-radius:4px 18px 4px 4px;padding:22px 22px 18px}
h1{font:400 clamp(32px,6vw,48px)/1.05 'Special Elite',monospace;margin:0 0 8px;text-wrap:balance}
h2{font:400 26px/1.1 'Special Elite',monospace;margin:34px 0 12px}
.sub{color:var(--mute);margin:0}
.rules{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px;margin-top:16px;padding:0;list-style:none}
.rules li{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:10px 12px;font-weight:600}
.rules b{color:var(--red)}
.slip{position:relative;display:grid;grid-template-columns:110px minmax(0,1fr);gap:16px;background:var(--paper);border:1px solid var(--line);
border-radius:12px;padding:18px;margin:12px 0;box-shadow:0 2px 0 var(--line)}
.when{font:800 26px/1 Inter,sans-serif;white-space:nowrap}.day{color:var(--mute);font-size:14px;margin-top:6px}
.tag{font-size:14px;color:var(--mute);font-weight:600}.ttl{font:800 19px/1.25 Inter,sans-serif;margin:2px 0 10px}
textarea{width:100%;min-height:118px;font:16px/1.45 Inter,sans-serif;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px;resize:vertical}
.row{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px;align-items:center}
.btn{min-height:44px;padding:0 16px;border-radius:10px;border:1px solid var(--ink);background:var(--ink);color:var(--bg);font:600 15px Inter,sans-serif;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center}
.btn.alt{background:transparent;color:var(--ink)}
.btn:focus-visible,textarea:focus-visible,input:focus-visible{outline:3px solid var(--red);outline-offset:2px}
label.done{display:inline-flex;gap:8px;align-items:center;min-height:44px;font-weight:600}
input[type=checkbox]{width:22px;height:22px;accent-color:var(--red)}
.stamp{position:absolute;right:16px;top:14px;border:3px solid var(--red);color:var(--red);font:400 18px 'Special Elite',monospace;padding:2px 10px;transform:rotate(-8deg);opacity:0;transition:opacity .25s}
.slip.posted .stamp{opacity:.9}.slip.posted{opacity:.72}
.todo{display:grid;grid-template-columns:110px minmax(0,1fr);gap:16px;padding:12px 0;border-top:1px solid var(--line)}
.ok{color:var(--red);font-weight:600;min-height:20px}
@media(max-width:600px){.slip,.todo{grid-template-columns:1fr;gap:6px}.when{font-size:22px}}
@media(prefers-reduced-motion:reduce){.stamp{transition:none}}
</style></head><body><main class="band">
<header class="folder"><h1>__TITLE__</h1><p class="sub">Post each video on TikTok at its time. Tap Get video, save it, then paste the caption.</p>
<ul class="rules"><li>Who can watch: <b>Everyone</b></li><li>Comments: <b>On</b></li><li>AI-generated content label: <b>On</b> (AI voice)</li><li>Sound: keep the video's own sound</li></ul></header>
<h2>Posts</h2><div id="posts"></div>
<h2>Also on your list</h2><div id="todos"></div>
<p class="sub" style="margin-top:28px">Tick a post when it's up. Ticks are saved in this browser only.</p>
</main><script>{
const D=__DATA__;
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt=w=>{const[d,t]=w.split(' ');const x=new Date(d+'T12:00:00');return{t,d:x.toLocaleDateString('en-GB',{weekday:'short',day:'numeric',month:'short'})}};
let saved={};try{saved=JSON.parse(localStorage.getItem('ccf-tt')||'{}')}catch(e){}
document.getElementById('posts').innerHTML=D.posts.map((p,i)=>{const f=fmt(p.when);return `<article class="slip${saved[p.id]?' posted':''}" id="s${i}">
<div><div class="when">${f.t}</div><div class="day">${f.d}</div></div><div><div class="tag">${esc(p.case)} · Part ${p.part} of 3</div><div class="ttl">${esc(p.title)}</div>
<textarea id="c${i}" aria-label="Caption">${esc(p.caption)}</textarea>
<div class="row"><a class="btn" href="${esc(p.video)}">Get video</a><button class="btn alt" data-i="${i}">Copy caption</button>
<label class="done"><input type="checkbox" data-id="${esc(p.id)}" data-s="s${i}"${saved[p.id]?' checked':''}> Posted</label></div><div class="ok" id="k${i}"></div></div>
<div class="stamp">POSTED</div></article>`}).join('');
document.getElementById('todos').innerHTML=D.todos.map(t=>{const f=fmt(t.when);return `<div class="todo"><div><div class="when" style="font-size:20px">${f.t}</div><div class="day">${f.d}</div></div><div><div class="ttl" style="margin:0">${esc(t.title)}</div><div class="sub">${esc(t.notes||'')}</div></div></div>`}).join('');
document.addEventListener('click',async e=>{const b=e.target.closest('button[data-i]');if(!b)return;const i=b.dataset.i,ta=document.getElementById('c'+i),k=document.getElementById('k'+i);
try{await navigator.clipboard.writeText(ta.value);k.textContent='Caption copied.'}catch(err){ta.select();k.textContent='Select all and copy.'}});
document.addEventListener('change',e=>{const c=e.target;if(!c.dataset.id)return;saved[c.dataset.id]=c.checked;document.getElementById(c.dataset.s).classList.toggle('posted',c.checked);
try{localStorage.setItem('ccf-tt',JSON.stringify(saved))}catch(err){}});
}</script></body></html>"""

if __name__ == "__main__":
    src = sys.argv[1]; spec = json.load(open(src)); base = os.path.splitext(src)[0]
    for p in spec["posts"]: p.setdefault("id", f"{p['case']}-{p['part']}-{p['when']}")
    data = json.dumps({"posts": spec["posts"], "todos": spec["todos"]}, ensure_ascii=False).replace("</", "<\\/")
    open(base + ".html", "w").write(PAGE.replace("__TITLE__", html.escape(spec["title"])).replace("__DATA__", data))
    def reminders(spec):
        return [{"when": p["when"], "title": f"Post on TikTok: {p['case']} Part {p['part']}/3", "url": p["video"],
                 "notes": f"{p['title']}\nVideo: {p['video']}\nCaption:\n{p['caption']}\nSettings: Everyone, comments on, AI label on."}
                for p in spec["posts"]] + spec["todos"]
    rem = reminders(spec)
    open(base + ".ics", "w", newline="").write(ics(rem, spec.get("calendar", "Case Closed Files")))
    import glob
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); allr, seen = [], set()
    for f in sorted(glob.glob(os.path.join(root, "handoff", "*.json"))):
        for r in reminders(json.load(open(f))):
            k = (r["title"], r["when"])
            if k not in seen: seen.add(k); allr.append(r)
    os.makedirs(os.path.join(root, "calendar"), exist_ok=True)
    feed = os.path.join(root, "calendar", "ccf-tiktok.ics")
    open(feed, "w", newline="").write(ics(allr, "CCF TikTok posts"))
    print("wrote", base + ".html", base + ".ics", len(rem), "reminders; feed", feed, len(allr), "events")
