# 📔 Memoir

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![MiMo v2.5](https://img.shields.io/badge/MiMo-v2.5-orange.svg)](https://mimo.xiaomi.com)

> **AI-powered journal with sentiment tracking, mood analysis, and weekly insights — powered by Xiaomi MiMo v2.5.**

Write your thoughts. Memoir analyzes each entry for sentiment, mood score, key themes, emotions, and provides actionable insights. Track your emotional patterns over time with beautiful visualizations.

**[Live Demo](https://memoir-demo.trycloudflare.com)** · **[Report Bug](../../issues)** · **[Request Feature](../../issues)**

---

## 📸 Screenshots

| Dashboard | Entry Detail | Journal History |
|-----------|-------------|-----------------|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Entry](docs/screenshots/entry.png) | ![History](docs/screenshots/history.png) |

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────┐
│                   Memoir                            │
│             (Tornado + Chart.js)                     │
├────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  Write   │    │  MiMo    │    │  Visualize│      │
│  │  Entry   │───►│  Analyze │───►│  (Charts) │      │
│  └──────────┘    └────┬─────┘    └──────────┘      │
│                        │                             │
│              ┌─────────┼─────────┐                  │
│              ▼         ▼         ▼                  │
│        Sentiment   Mood Score  Themes               │
│        + Emotions  + Insights  + Patterns            │
│                        │                             │
│                  ┌─────▼─────┐                      │
│                  │  SQLite   │                      │
│                  └───────────┘                      │
└────────────────────────────────────────────────────┘
```

---

## ✨ Features

- 💭 **Sentiment Analysis** — Positive, negative, or neutral classification
- 📊 **Mood Tracking** — 1-10 scale with Chart.js visualization over time
- 🏷️ **Theme Extraction** — Key topics and themes identified per entry
- 💡 **AI Insights** — Actionable feedback on your writing patterns
- 📅 **Weekly Summary** — AI-generated weekly mood and theme report
- 🔍 **Search & Filter** — Find entries by content, tags, or mood
- 📈 **Token Usage** — Track MiMo API consumption

---

## 🔥 Token Economics

| Action | Tokens | Daily (1 entry) | Monthly |
|--------|--------|-----------------|---------|
| Entry Analysis | ~3K | ~3K | ~90K |
| Weekly Summary | ~5K | — | ~20K |
| Monthly Review | ~10K | — | ~10K |
| **Total** | | **~3K** | **~120K** |

---

## 🚀 Quick Start

```bash
git clone https://github.com/ricobudipad2-droid/memoir.git
cd memoir
pip install -r requirements.txt
cp .env.example .env
# Edit .env — set MIMO_API_KEY
python app.py
```

Open [http://localhost:8888](http://localhost:8888)

### Docker

```bash
docker compose up --build
```

---

## 📖 API

```bash
# Create entry
curl -X POST http://localhost:8888/api/entries -H "Content-Type: application/json" -d '{"content":"Today was amazing...","title":"Great Day","tags":"personal,happy"}'

# Get entries
curl http://localhost:8888/api/entries

# Mood history
curl http://localhost:8888/api/mood-history
```

---

## 🤝 Contributing · 📄 License (MIT)
