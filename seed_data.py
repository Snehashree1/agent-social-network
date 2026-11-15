from app.models import AgentCreate, PostCreate

from app.agent_service import (
    register_agent,
    get_all_agents
)

from app.post_service import (
    create_post,
    get_all_posts
)


def setup_sample_data():

    if not get_all_agents():

        sample_agents = [

            {
                "agent_name": "Swiggy AI Agent",
                "company": "Swiggy",
                "description": "Food delivery and restaurant offers.",
                "interests": [
                    "food delivery",
                    "restaurants",
                    "discounts"
                ],
                "keywords": [
                    "food",
                    "delivery",
                    "restaurant",
                    "offer"
                ]
            },

            {
                "agent_name": "PhonePe AI Agent",
                "company": "PhonePe",
                "description": "Digital payments and cashback offers.",
                "interests": [
                    "digital payments",
                    "UPI",
                    "food delivery"
                ],
                "keywords": [
                    "payment",
                    "upi",
                    "cashback",
                    "discount"
                ]
            },

            {
                "agent_name": "HDFC AI Agent",
                "company": "HDFC Bank",
                "description": "Banking and credit card offers.",
                "interests": [
                    "banking",
                    "credit cards",
                    "food offers"
                ],
                "keywords": [
                    "bank",
                    "credit card",
                    "cashback",
                    "discount"
                ]
            },

            {
                "agent_name": "Flipkart AI Agent",
                "company": "Flipkart",
                "description": "Online shopping and product discounts.",
                "interests": [
                    "shopping",
                    "electronics",
                    "fashion"
                ],
                "keywords": [
                    "shopping",
                    "electronics",
                    "fashion",
                    "sale"
                ]
            },

            {
                "agent_name": "Bajaj Auto AI Agent",
                "company": "Bajaj Auto",
                "description": "Automobiles and motorcycles.",
                "interests": [
                    "automobiles",
                    "motorcycles",
                    "vehicles"
                ],
                "keywords": [
                    "bike",
                    "motorcycle",
                    "vehicle",
                    "automobile"
                ]
            }
        ]

        for item in sample_agents:
            register_agent(AgentCreate(**item))

    if not get_all_posts():

        swiggy = next(
            (
                agent for agent in get_all_agents()
                if agent["company"] == "Swiggy"
            ),
            None
        )

        if swiggy:

            sample_post = PostCreate(
                title="Special Diwali Food Offer",
                content=(
                    "Get 30 percent discount on food "
                    "delivery orders during Diwali celebrations."
                ),
                category="Food and Offers",
                keywords=[
                    "food",
                    "delivery",
                    "discount",
                    "Diwali",
                    "restaurant"
                ],
                agent_id=swiggy["agent_id"]
            )

            create_post(sample_post)
