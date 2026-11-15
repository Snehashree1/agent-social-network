from app.storage import load_data, save_data


agents = load_data("agents.json")


def get_next_agent_id():
    return max(
        [agent["agent_id"] for agent in agents],
        default=0
    ) + 1


def register_agent(agent_data):
    agent = agent_data.model_dump()
    agent["agent_id"] = get_next_agent_id()

    agents.append(agent)

    save_data("agents.json", agents)

    return agent


def get_all_agents():
    return agents


def get_agent_by_id(agent_id):
    return next(
        (
            agent for agent in agents
            if agent["agent_id"] == agent_id
        ),
        None
    )
