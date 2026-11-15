from app.storage import load_data, save_data


notifications = load_data("notifications.json")


def create_notifications(post, matched_agents):

    created = []

    for agent in matched_agents:

        next_id = max(
            [
                item["notification_id"]
                for item in notifications
            ],
            default=0
        ) + 1

        notification = {
            "notification_id": next_id,
            "agent_id": agent["agent_id"],
            "agent_name": agent["agent_name"],
            "company": agent["company"],
            "post_id": post["post_id"],
            "post_title": post["title"],
            "relevance_score": agent["relevance_score"],
            "matched_terms": agent["matched_terms"],
            "status": "New"
        }

        notifications.append(notification)
        created.append(notification)

    save_data("notifications.json", notifications)

    return created


def get_all_notifications():
    return notifications
