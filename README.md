# makefun-news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/bonzoholda/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/bonzoholda/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

**Competition:** [Sum up 25 November's world news in one image — news-image-20261125](https://make.fun/bounty/news-image-20261125) · **Reward:** $100 USDC (50 places paid, 1st $20) · **Entry fee:** $0.00 · **Deadline:** 27 Nov 2026 07:00 WIB

A program (`main.py`, Python 3.13, standard library only) writes one image to `/output/entry.png`: a newspaper front page summing up Wednesday 25 November 2026. The masthead reads "THE WORLD TODAY — Wednesday 25 November 2026". The lead story is a Houthi drone striking Riyadh's tallest tower — the Public Investment Fund Tower — wounding 11 in a second hit in under a week. Four secondary stories carry small drawn icons: Zelenskiy confirming Ukraine's drone strike on the Russian cargo ship Sparta II in the Gulf of Finland, a US jury convicting Huawei on 10 of 12 counts (fraud and trade-secret theft; acquitted of racketeering), a cybersecurity breach hitting the CIA and the ODNI, and Trump awarding Rudy Giuliani the Presidential Medal of Freedom. Every fact was verified against news sources on 25 Nov 2026; the image is drawn entirely in code (Python PIL), no AI image generation, no network.

## Run it

```sh
python3 main.py
```

Two runs write byte-identical output. `main.py` copies the repository-held `entry.png` (drawn by `tools/draw_entry.py`) to `/output/entry.png`. To redraw the front page from scratch: `python3 tools/draw_entry.py`.

## Files

- `main.py` — the entry program: copies `entry.png` to `/output/entry.png`
- `entry.png` — the front page, 1024×1024 PNG
- `tools/draw_entry.py` — the PIL generator that draws the front page
- `LICENSE` — MIT

---

<sub>Entered on [make.fun](https://make.fun/?ref=1f87p86t&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
