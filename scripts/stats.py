#!/usr/bin/env python3
"""Render the profile stats card (light + dark SVG) from the GitHub GraphQL API.

Stdlib only, so the workflow needs no install step. Reads GITHUB_TOKEN and
optionally GH_LOGIN (defaults to LeenHawk). Writes assets/stats-{light,dark}.svg.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import urllib.request
from html import escape
from pathlib import Path

LOGIN = os.environ.get("GH_LOGIN", "LeenHawk")
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = Path(__file__).resolve().parent.parent / "assets"


def gql(query: str, **variables) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.load(r)
    if body.get("errors"):
        raise SystemExit(f"GraphQL error: {body['errors']}")
    return body["data"]


def repos() -> list[dict]:
    out, cursor = [], None
    q = """query($login:String!,$cursor:String){user(login:$login){repositories(
      first:100, after:$cursor, ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC){
      pageInfo{hasNextPage endCursor}
      nodes{stargazerCount languages(first:10, orderBy:{field:SIZE,direction:DESC}){
        edges{size node{name color}}}}}}}"""
    while True:
        page = gql(q, login=LOGIN, cursor=cursor)["user"]["repositories"]
        out += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            return out
        cursor = page["pageInfo"]["endCursor"]


def contributions() -> tuple[int, int, int, int, list[tuple[str, int]]]:
    """Commits this year, commits all time, PRs all time, created year, daily calendar."""
    created = gql("query($login:String!){user(login:$login){createdAt}}", login=LOGIN)["user"]["createdAt"]
    first_year = int(created[:4])
    now = dt.datetime.now(dt.timezone.utc)
    q = """query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){
      contributionsCollection(from:$from,to:$to){totalCommitContributions
        restrictedContributionsCount totalPullRequestContributions
        contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
    commits_all = prs_all = commits_year = 0
    days: list[tuple[str, int]] = []
    for year in range(first_year, now.year + 1):
        start = dt.datetime(year, 1, 1, tzinfo=dt.timezone.utc)
        end = min(dt.datetime(year, 12, 31, 23, 59, 59, tzinfo=dt.timezone.utc), now)
        c = gql(q, login=LOGIN, **{"from": start.isoformat(), "to": end.isoformat()})["user"]["contributionsCollection"]
        commits_all += c["totalCommitContributions"]
        prs_all += c["totalPullRequestContributions"]
        if year == now.year:
            commits_year = c["totalCommitContributions"]
        for w in c["contributionCalendar"]["weeks"]:
            days += [(d["date"], d["contributionCount"]) for d in w["contributionDays"]]
    days.sort()
    return commits_year, commits_all, prs_all, first_year, days


def streaks(days: list[tuple[str, int]]) -> tuple[int, int]:
    today = dt.date.today().isoformat()
    days = [d for d in days if d[0] <= today]
    longest = run = 0
    for _, n in days:
        run = run + 1 if n > 0 else 0
        longest = max(longest, run)
    current = 0
    # Today without contributions yet doesn't break the streak.
    tail = days[:-1] if days and days[-1][1] == 0 else days
    for _, n in reversed(tail):
        if n == 0:
            break
        current += 1
    return current, longest


def merged_upstream() -> int:
    q = 'query($q:String!){search(query:$q,type:ISSUE,first:1){issueCount}}'
    return gql(q, q=f"author:{LOGIN} is:pr is:merged -user:{LOGIN}")["search"]["issueCount"]


def fmt(n: int) -> str:
    return f"{n/1000:.1f}k".replace(".0k", "k") if n >= 10000 else f"{n:,}"


def render(theme: dict, stats: list[tuple[str, str]], langs: list[tuple[str, str, float]], foot: str) -> str:
    W, H = 1200, 236
    pad = 40
    col = (W - 2 * pad) / len(stats)
    cells = []
    for i, (value, label) in enumerate(stats):
        x = pad + i * col
        cells.append(
            f'<g class="c" style="animation-delay:{0.08 * i:.2f}s">'
            f'<text x="{x:.1f}" y="92" class="v">{escape(value)}</text>'
            f'<text x="{x:.1f}" y="120" class="l">{escape(label)}</text></g>'
        )
    # language bar
    bar_y, bar_h, bar_w = 152, 8, W - 2 * pad
    x, segs, keys = pad, [], []
    for i, (name, color, share) in enumerate(langs):
        w = bar_w * share
        segs.append(f'<rect x="{x:.2f}" y="{bar_y}" width="{max(w - 2, 1):.2f}" height="{bar_h}" rx="1.5" fill="{color}"/>')
        x += w
    kx = pad
    for name, color, share in langs:
        label = f"{name} {share * 100:.0f}%"
        keys.append(
            f'<circle cx="{kx + 4}" cy="{bar_y + 33}" r="4" fill="{color}"/>'
            f'<text x="{kx + 14}" y="{bar_y + 37.5}" class="k">{escape(label)}</text>'
        )
        kx += 24 + 6.7 * len(label)
    t = theme
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(", ".join(f"{v} {l}" for v, l in stats))}">
<style>
text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif}}
.v{{font-size:40px;font-weight:650;letter-spacing:-1.2px;fill:{t["ink"]}}}
.l{{font-size:15px;fill:{t["muted"]}}}
.k{{font-size:13px;fill:{t["muted"]}}}
.f{{font-size:12px;fill:{t["faint"]}}}
.c{{opacity:0;animation:in .5s ease-out forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
@media (prefers-reduced-motion:reduce){{.c{{animation:none;opacity:1}}}}
</style>
<rect width="{W}" height="{H}" rx="6" fill="{t["bg"]}" stroke="{t["rule"]}"/>
{"".join(cells)}
{"".join(segs)}
{"".join(keys)}
<text x="{W - pad}" y="{H - 16}" text-anchor="end" class="f">{escape(foot)}</text>
</svg>
'''


def main() -> None:
    rs = repos()
    stars = sum(r["stargazerCount"] for r in rs)
    sizes: dict[str, list] = {}
    for r in rs:
        for e in r["languages"]["edges"]:
            n = e["node"]
            sizes.setdefault(n["name"], [0, n["color"] or "#8b949e"])[0] += e["size"]
    total = sum(v[0] for v in sizes.values()) or 1
    top = sorted(sizes.items(), key=lambda kv: -kv[1][0])[:6]
    langs = [(k, v[1], v[0] / total) for k, v in top]
    rest = 1 - sum(s for _, _, s in langs)
    if rest > 0.005:
        langs.append(("Other", "#8b949e", rest))

    commits_year, commits_all, prs_all, since, days = contributions()
    current, longest = streaks(days)
    upstream = merged_upstream()
    year = dt.date.today().year

    stats = [
        (fmt(stars), "stars earned"),
        (fmt(commits_year), f"commits in {year}"),
        (fmt(commits_all), f"commits since {since}"),
        (fmt(prs_all), "pull requests"),
        (fmt(upstream), "merged upstream"),
        (f"{current}d", f"streak · best {longest}d"),
    ]
    foot = f"public activity · updated {dt.date.today().isoformat()}"
    themes = {
        "light": dict(bg="#ffffff", rule="#d0d7de", ink="#1f2328", muted="#59636e", faint="#818b98"),
        "dark": dict(bg="#0d1117", rule="#30363d", ink="#e6edf3", muted="#9198a1", faint="#6e7681"),
    }
    OUT.mkdir(exist_ok=True)
    for name, t in themes.items():
        (OUT / f"stats-{name}.svg").write_text(render(t, stats, langs, foot))
    print(json.dumps({"stats": stats, "langs": [(n, round(s, 3)) for n, _, s in langs]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
