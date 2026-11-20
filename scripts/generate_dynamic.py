"""Regenerates the data-driven SVGs (tiger contribution graph + stats card).

Runs in GitHub Actions (see .github/workflows/update-profile.yml) but also works locally:

    GH_TOKEN=ghp_xxx GH_USER=Muhtasim-Masum-Hasnayen python scripts/generate_dynamic.py

Without a token (or with --demo) it writes sample data. If the API call fails with a token
present, the script exits with an error so existing real-data files are never overwritten.
Only the Python standard library is used.
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stats as stats_mod  # noqa: E402
import tiger as tiger_mod  # noqa: E402
from common import write  # noqa: E402

LOGIN = os.environ.get("GH_USER", "Muhtasim-Masum-Hasnayen")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

QUERY = """
query($login:String!){
  user(login:$login){
    followers{totalCount}
    following{totalCount}
    repositories(ownerAffiliation:OWNER, isFork:false, first:100){
      totalCount
      nodes{ stargazerCount languages(first:8, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name color } } } }
    }
    contributionsCollection{
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ contributionCount date weekday contributionLevel } }
      }
    }
  }
}
"""
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def gql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json", "User-Agent": "profile-assets"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]


def main():
    if "--demo" in sys.argv or not TOKEN:
        print("Writing sample-data assets (no token or --demo).")
        write("tiger-contribution.svg", tiger_mod.build(tiger_mod.demo_weeks(), demo=True, login=LOGIN))
        write("stats.svg", stats_mod.build(demo=True, login=LOGIN))
        return

    u = gql(QUERY, {"login": LOGIN})
    cc = u["contributionsCollection"]
    weeks = [
        [dict(date=d["date"], count=d["contributionCount"], level=LEVELS.get(d["contributionLevel"], 0), weekday=d["weekday"]) for d in w["contributionDays"]]
        for w in cc["contributionCalendar"]["weeks"]
    ]
    write("tiger-contribution.svg", tiger_mod.build(weeks, demo=False, login=LOGIN))

    nodes = u["repositories"]["nodes"]
    totals, colors = {}, {}
    for n in nodes:
        for e in n["languages"]["edges"]:
            totals[e["node"]["name"]] = totals.get(e["node"]["name"], 0) + e["size"]
            colors[e["node"]["name"]] = e["node"]["color"] or "#8B949E"
    grand = sum(totals.values()) or 1
    langs = sorted(((k, colors[k], v * 100 / grand) for k, v in totals.items()), key=lambda t: -t[2])[:6]
    data = dict(
        followers=u["followers"]["totalCount"],
        following=u["following"]["totalCount"],
        repos=u["repositories"]["totalCount"],
        stars=sum(n["stargazerCount"] for n in nodes),
        commits=cc["totalCommitContributions"],
        prs=cc["totalPullRequestContributions"],
        issues=cc["totalIssueContributions"],
        contributions=cc["contributionCalendar"]["totalContributions"],
        langs=langs or stats_mod.DEMO["langs"],
    )
    write("stats.svg", stats_mod.build(data, demo=False, login=LOGIN))


if __name__ == "__main__":
    main()
