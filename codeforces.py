import requests

STRUGGLE_VERDICTS = {
    "WRONG_ANSWER",
    "TIME_LIMIT_EXCEEDED",
    "MEMORY_LIMIT_EXCEEDED",
    "RUNTIME_ERROR",
    "COMPILATION_ERROR",
}


def get_recent_struggles(handle: str) -> list[dict] | str:
    """Fetch up to 10 unique problems the user recently got a non-AC verdict on."""
    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=40"

    try:
        response = requests.get(url, timeout=8)
        data = response.json()
    except requests.exceptions.Timeout:
        return "Request timed out. Codeforces may be slow right now."
    except Exception:
        return "Could not reach Codeforces. Check your internet connection."

    if data.get("status") != "OK":
        return f"Codeforces API error: {data.get('comment', 'Unknown error')}"

    seen    = set()
    results = []

    for submission in data["result"]:
        verdict = submission.get("verdict", "")
        if verdict not in STRUGGLE_VERDICTS:
            continue

        problem    = submission["problem"]
        contest_id = problem.get("contestId", "")
        index      = problem.get("index", "")
        key        = f"{contest_id}{index}"

        if key in seen:
            continue

        seen.add(key)
        results.append({
            "name":       problem["name"],
            "contest_id": contest_id,
            "index":      index,
            "url":        f"https://codeforces.com/contest/{contest_id}/problem/{index}",
            "verdict":    verdict.replace("_", " ").title(),
        })

        if len(results) == 10:
            break

    if not results:
        return "No recent struggles found — either this handle has no wrong submissions, or they're on a winning streak."

    return results
