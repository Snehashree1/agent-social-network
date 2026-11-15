from app.storage import load_data, save_data


engagements = load_data("engagements.json")


def generate_comment(post, agent):
    company = agent["company"]
    category = post.get("category", "").lower()

    if "food" in category:
        return (
            f"{company} is interested in this offer! "
            "This could be useful for customers looking for great deals."
        )

    if "payment" in category or "finance" in category:
        return (
            f"{company} finds this offer relevant. "
            "Digital payment benefits can provide extra value to customers."
        )

    return (
        f"{company} finds this update interesting. "
        "Thanks for sharing this information!"
    )


def process_engagements(post, matched_agents):

    created = []

    for agent in matched_agents:

        score = agent["relevance_score"]

        # Agent decides whether to engage
        should_engage = score >= 25

        if not should_engage:
            continue

        engagement = {
            "engagement_id": max(
                [item["engagement_id"] for item in engagements],
                default=0
            ) + 1,

            "post_id": post["post_id"],
            "post_title": post["title"],
            "agent_id": agent["agent_id"],
            "agent_name": agent["agent_name"],
            "company": agent["company"],
            "relevance_score": score,
            "decision": "Engaged",
            "comment": generate_comment(post, agent)
        }

        engagements.append(engagement)
        created.append(engagement)

    save_data("engagements.json", engagements)

    return created


def get_all_engagements():
    return engagements
