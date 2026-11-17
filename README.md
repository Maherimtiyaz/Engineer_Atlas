# Engineer's Atlas

A self-study path from how computers work to launching your own AI product: backend engineering, machine learning, LLMs, AI engineering, deployment, MLOps/LLMOps/AIOps, distribution and scaling.

- **10 phases in order**, plus optional research electives
- Every topic: key ideas, lectures, original papers and sources, in-depth articles, projects and GitHub repos
- **Milestone projects** at the end of each phase
- **Topic map** with a study-path panel: click any topic to see exactly what to learn first
- **Focus mode** that hides everything except your current phase
- **Three reading modes** (Light, Paper, Night) and adjustable text size
- **Daily drop** of new AI research, tagged to the topic to study first

It is one static file (`index.html`) with no build step, no server and no accounts. Your progress is saved in your browser.

## Run it

**On your computer:** open `index.html` in any browser. Everything works offline except the daily drop.

**Online with GitHub Pages (free):**
1. In the repo: *Settings → Pages → Build and deployment → Source:* choose **GitHub Actions**.
2. Open the *Actions* tab and run **Deploy site** once (or push any change).
3. Your site is at `https://<your-username>.github.io/<repo-name>/`.

After that, every push and every daily update redeploys the site on its own.

## Daily drop

`.github/workflows/daily.yml` runs every day at 06:40 IST. It runs `scripts/update_daily.py`, which reads the public Hugging Face Daily Papers API (no API key needed), takes the 8 most-upvoted papers, tags each with an Atlas topic using keyword rules, and commits `daily.json`. Pages then redeploys on its own.

Run it by hand any time from the *Actions* tab (*Daily drop → Run workflow*), or locally:

```bash
python3 scripts/update_daily.py
```

To change the tagging, edit the `RULES` list at the top of the script.

## Your progress

"Mark as done", focus mode, reading mode and text size are stored in your browser's local storage. They stay on that browser and device. Clearing site data resets them.
