"""Add today's top AI papers to daily.json. Runs in GitHub Actions; no API keys needed.

Source: the public Hugging Face Daily Papers API. Each paper is tagged with the
Atlas topic it most relates to, using simple keyword rules below.
"""
import datetime as dt
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "daily.json"
KEEP_DAYS = 45
PER_DAY = 8

# (keywords, topic id, level) — first match wins, so put specific rules first.
RULES = [
    (["prompt injection", "jailbreak", "red team", "alignment", "safety", "deceptive"], "safety", "Advanced"),
    (["interpretab", "sparse autoencoder", "circuit", "probing"], "mechinterp", "Advanced"),
    (["agent", "tool use", "tool-use", "function calling", "mcp", "computer use", "web navigation"], "agents", "Intermediate"),
    (["retrieval", "rag", "memory"], "rag", "Intermediate"),
    (["benchmark", "evaluation", "evaluating", "leaderboard", "llm-as-a-judge"], "evals", "Intermediate"),
    (["reasoning", "chain-of-thought", "test-time", "math", "theorem"], "reason", "Advanced"),
    (["reinforcement learning", "grpo", "ppo", "reward", "rlhf", "preference", "dpo"], "posttrain", "Advanced"),
    (["speculative decoding", "kv cache", "quantiz", "inference", "serving", "throughput", "latency"], "serve", "Advanced"),
    (["lora", "fine-tun", "finetun", "adapter", "distill"], "peft", "Advanced"),
    (["mixture of experts", "mixture-of-experts", "moe"], "moe", "Advanced"),
    (["attention", "long context", "long-context", "state space", "mamba", "linear-time"], "effattn", "Advanced"),
    (["diffusion", "flow matching", "image generation", "video generation", "text-to-image", "text-to-video"], "diffusion", "Advanced"),
    (["speech", "audio", "tts", "asr", "voice"], "speech", "Advanced"),
    (["vision-language", "multimodal", "vlm", "video understanding", "image understanding"], "multimodal", "Advanced"),
    (["robot", "embodied", "vision-language-action"], "rlbasics", "Advanced"),
    (["scaling law", "pretrain", "pre-train", "language model", "llm", "foundation model"], "pretrain", "Intermediate"),
    (["transformer"], "tf", "Intermediate"),
]


def fetch(date: str):
    url = f"https://huggingface.co/api/daily_papers?date={date}&limit=50"
    req = urllib.request.Request(url, headers={"User-Agent": "engineers-atlas-daily"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def tag(title: str, summary: str):
    # Titles are the strongest signal; fall back to the summary.
    for text in (title.lower(), summary.lower()):
        for words, topic, level in RULES:
            if any(w in text for w in words):
                return topic, level
    return None, "Intermediate"


def main():
    today = dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30))).date()
    data = json.loads(OUT.read_text()) if OUT.exists() else {"days": []}
    if any(d["date"] == today.isoformat() for d in data["days"]):
        print("already updated today")
        return
    papers = []
    for back in (0, 1):
        papers = fetch((today - dt.timedelta(days=back)).isoformat())
        if papers:
            break
    papers.sort(key=lambda x: -x.get("paper", {}).get("upvotes", 0))
    items = []
    for x in papers[:PER_DAY]:
        p = x["paper"]
        summary = (p.get("ai_summary") or p.get("summary") or "").strip().replace("\n", " ")
        topic, level = tag(p["title"], summary)
        items.append({
            "kind": "paper", "title": p["title"], "url": f"https://huggingface.co/papers/{p['id']}",
            "source": "Hugging Face Papers", "level": level, "topic": topic,
            "note": (summary[:260] + "…") if len(summary) > 260 else summary,
        })
    if not items:
        print("no papers found")
        return
    data["days"].insert(0, {"date": today.isoformat(), "summary": "Most-upvoted papers on Hugging Face Daily Papers.", "items": items})
    cutoff = (today - dt.timedelta(days=KEEP_DAYS)).isoformat()
    data["days"] = [d for d in data["days"] if d["date"] >= cutoff]
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print(f"added {len(items)} items for {today}")


if __name__ == "__main__":
    main()
