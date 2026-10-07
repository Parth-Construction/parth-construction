"""Generates the 30-day Parth Construction content plan (CSV + per-day meta.json)."""
import csv, json, os

CHANNEL = "Parth Construction"
BASE_TAGS = ["#construction", "#civilengineering", "#homeconstruction", "#buildingtips",
             "#shorts", "#reels", "#parthconstruction", "#india", "#civilengineer", "#house"]

# (topic, hook, [3 key points], extra tags)
DAYS = [
 ("5 mistakes while building a house", "Ghar banate waqt ye 5 galtiyan lakhon ka nuksan karti hain!", ["Skipping soil test", "No proper drawing before work", "Hiring the cheapest labour only"], ["#housebuilding", "#mistakes"]),
 ("How to estimate construction cost", "Apne ghar ka kharcha pehle se kaise nikaale?", ["Calculate built-up area in sq ft", "Multiply by local per-sq-ft rate", "Add 10% buffer for extras"], ["#costestimation", "#budget"]),
 ("Why cracks appear in walls", "Deewar mein crack kyun aate hain?", ["Poor curing and shrinkage", "Foundation settlement", "Temperature expansion without joints"], ["#wallcracks", "#repair"]),
 ("Test cement quality at site", "Cement asli hai ya nakli? 30 second mein check karo!", ["Check manufacturing date on bag", "No lumps, powder should be smooth", "Float test: a pinch should sink in water"], ["#cement", "#quality"]),
 ("Why curing concrete matters", "Slab dalke chhod diya? Ye galti mat karna!", ["Keep wet for at least 7 days", "Cover with wet gunny bags", "Never skip curing in summer"], ["#curing", "#concrete"]),
 ("Brick vs AAC block vs fly ash", "Kaunsi eent best hai - red brick, AAC ya fly ash?", ["Red brick: strong, heavier, costlier labour", "AAC block: light, good insulation", "Fly ash: budget friendly, uniform size"], ["#bricks", "#aacblock"]),
 ("How to check TMT steel quality", "TMT saria kharidne se pehle ye 3 cheezein dekho!", ["ISI mark and brand stamp on bar", "Uniform ribs, no rust flakes", "Check weight per metre as per size"], ["#tmt", "#steel"]),
 ("Types of foundation", "Ghar ki neev kaisi honi chahiye?", ["Isolated footing for firm soil", "Raft foundation for weak soil", "Pile foundation for very soft soil"], ["#foundation", "#civil"]),
 ("Terrace waterproofing", "Barish mein chhat tapakti hai? Ye karo!", ["Clean and repair cracks first", "Apply waterproofing coat in layers", "Finish with brickbat coba for slope"], ["#waterproofing", "#terrace"]),
 ("Column and beam basics", "Ghar ki haddi - column aur beam samjho!", ["Columns carry vertical load to foundation", "Beams carry slab load to columns", "Never cut reinforcement for pipes"], ["#column", "#beam"]),
 ("How to choose a contractor", "Contractor chunne se pehle ye 5 sawal zaroor poochho!", ["Ask for past project sites to visit", "Get a written agreement with stages", "Compare at least 3 quotations"], ["#contractor", "#tips"]),
 ("Plumbing mistakes to avoid", "Plumbing ki ye galti baad mein bahut mehngi padti hai!", ["Pressure test pipes before covering", "Keep proper slope in drain lines", "Provide inspection chambers"], ["#plumbing", "#bathroom"]),
 ("Electrical planning before slab", "Slab dalne se pehle electrical ka plan zaroor banao!", ["Fix conduit and boxes before casting", "Plan extra points for future", "Separate circuits for AC and kitchen"], ["#electrical", "#wiring"]),
 ("Choosing floor tiles", "Tiles kharidne se pehle ye dhyan rakho!", ["Vitrified for living areas", "Anti-skid tiles for bathrooms", "Buy 5-10% extra from the same batch"], ["#tiles", "#flooring"]),
 ("Slab shuttering process", "Slab ka shuttering kaise hota hai?", ["Level and prop the centring firmly", "Apply shuttering oil on plates", "Check levels before placing steel"], ["#shuttering", "#slab"]),
 ("Plastering tips", "Plaster fatne se kaise bachayein?", ["Wet the wall before plastering", "Use correct cement-sand ratio", "Cure plaster for 7 days"], ["#plaster", "#finishing"]),
 ("Save money on construction", "Quality se samjhauta kiye bina paise kaise bachayein?", ["Finalise design before starting", "Buy bulk material at the right season", "Avoid changes after casting"], ["#savemoney", "#budgethome"]),
 ("Importance of soil testing", "Soil test ke bina ghar banana = risk!", ["Tells safe bearing capacity", "Decides foundation type", "Costs little, saves lakhs"], ["#soiltest", "#geotechnical"]),
 ("Construction site safety", "Site par safety ignore mat karo!", ["Helmet and shoes are a must", "Check scaffolding before climbing", "Keep site clean of loose material"], ["#safety", "#sitelife"]),
 ("Bar bending schedule", "BBS kya hota hai aur kyun zaroori hai?", ["Lists bar size, shape and length", "Reduces steel wastage", "Makes billing accurate"], ["#bbs", "#reinforcement"]),
 ("M20 vs M25 concrete", "M20 aur M25 mein kya fark hai?", ["M20 mix is 1:1.5:3", "M25 mix is 1:1:2, stronger", "Use M25 for columns and heavy slabs"], ["#concretemix", "#m25"]),
 ("Kitchen layout planning", "Kitchen ka layout aise banao!", ["Follow work triangle: sink, stove, fridge", "Plan ventilation and chimney point", "Keep platform height comfortable"], ["#kitchen", "#design"]),
 ("Staircase design rules", "Seedhi banate waqt ye rule yaad rakho!", ["Riser about 150 mm", "Tread about 250-300 mm", "Same size for every step"], ["#staircase", "#homedesign"]),
 ("Treating dampness in walls", "Deewar mein seelan? Ye hai solution!", ["Find the source: leak or rising damp", "Fix plumbing leaks first", "Apply damp-proof treatment then repaint"], ["#dampness", "#seepage"]),
 ("Correct painting steps", "Paint karne ka sahi order kya hai?", ["Surface cleaning and putty", "Primer coat", "Two coats of paint"], ["#painting", "#homepaint"]),
 ("Home loan and stage payments", "Construction loan ka paisa kab milta hai?", ["Released in stages with progress", "Bank engineer inspects each stage", "Keep all bills and approvals ready"], ["#homeloan", "#finance"]),
 ("Site transformation timelapse", "Khali plot se ghar tak ka safar!", ["Excavation and foundation", "Structure and slab", "Finishing and handover"], ["#timelapse", "#beforeafter"]),
 ("A day at a construction site", "Ek civil engineer ka din kaisa hota hai?", ["Morning site inspection", "Material and labour planning", "Quality checks and reports"], ["#dayinthelife", "#civilengineerlife"]),
 ("Construction myths busted", "Construction ke ye 3 myths band karo maanna!", ["More cement does not mean stronger concrete", "Thicker wall is not always safer", "Cheap material is not always saving"], ["#myths", "#facts"]),
 ("Checklist before taking possession", "Ghar ka kabza lene se pehle ye checklist dekho!", ["Check wall and floor levels", "Test all taps, switches and doors", "Verify completion and occupancy papers"], ["#checklist", "#possession"]),
]

def build(i, d):
    topic, hook, pts, extra = d
    title = f"{hook.split('!')[0].split('?')[0]} | {CHANNEL}"[:95]
    tags = BASE_TAGS + extra
    desc = (f"{hook}\n\nIn this short:\n" + "\n".join(f"- {p}" for p in pts) +
            f"\n\nFollow {CHANNEL} for daily construction tips.\n\n" + " ".join(tags))
    script = (f"[0-3s] {hook}\n[3-9s] {pts[0]}.\n[9-15s] {pts[1]}.\n"
              f"[15-24s] {pts[2]}.\n[24-30s] Follow Parth Construction for daily tips!")
    veo = ("Vertical 9:16, realistic Indian construction site, natural daylight, cinematic. "
           f"Scene 1: {pts[0]}. Scene 2: {pts[1]}. Scene 3: {pts[2]}. "
           f"Voiceover in Hinglish, energetic male voice, saying: '{hook}'. No text overlays, no brand logos.")
    thumb = (f"YouTube thumbnail, 16:9, bold yellow and black, Indian civil engineer in safety helmet "
             f"pointing at {topic.lower()}, big readable text '{topic.upper()}', "
             "high contrast, clean, no watermark.")
    return {"day": i, "topic": topic, "hook": hook, "script_30s": script, "title": title,
            "description": desc, "hashtags": " ".join(tags), "gemini_video_prompt": veo,
            "chatgpt_thumbnail_prompt": thumb}

rows = [build(i, d) for i, d in enumerate(DAYS, 1)]
with open("content_plan.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
for r in rows:
    p = f"queue/day{r['day']:02d}"
    os.makedirs(p, exist_ok=True)
    json.dump({"title": r["title"], "description": r["description"], "tags": r["hashtags"].replace("#", "").split()},
              open(f"{p}/meta.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(rows), "days generated")
