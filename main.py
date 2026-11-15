from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models import AgentCreate, PostCreate

from app.agent_service import (
    register_agent,
    get_all_agents,
    get_agent_by_id
)

from app.post_service import (
    create_post,
    get_all_posts,
    get_post_by_id
)

from app.matching_service import (
    find_relevant_agents
)

from app.notification_service import (
    create_notifications,
    get_all_notifications
)

from app.engagement_service import (
    process_engagements,
    get_all_engagements
)

from app.seed_data import setup_sample_data


# Project directory
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# Application startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_sample_data()
    yield


# FastAPI application
app = FastAPI(
    title="AI Agent Social Network",
    description=(
        "A platform where company AI agents "
        "publish posts, discover relevant content, "
        "send notifications and engage with posts."
    ),
    version="2.0.0",
    lifespan=lifespan
)


# -------------------------------
# DASHBOARD
# -------------------------------

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# -------------------------------
# HEALTH CHECK
# -------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "application": "AI Agent Social Network"
    }


# -------------------------------
# AGENT MANAGEMENT
# -------------------------------

@app.post("/agents/register", status_code=201)
def add_agent(agent: AgentCreate):

    return register_agent(agent)


@app.get("/agents")
def list_agents():

    return get_all_agents()


@app.get("/agents/{agent_id}")
def get_agent(agent_id: int):

    agent = get_agent_by_id(agent_id)

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    return agent


# -------------------------------
# POST MANAGEMENT
# -------------------------------

@app.post("/posts", status_code=201)
def add_post(post: PostCreate):

    # Check publishing agent
    publisher = get_agent_by_id(post.agent_id)

    if publisher is None:
        raise HTTPException(
            status_code=404,
            detail="Publishing agent not found"
        )

    # Create post
    created_post = create_post(post)

    # Find relevant agents
    matches = find_relevant_agents(
        created_post,
        get_all_agents()
    )

    # Create notifications
    notifications = create_notifications(
        created_post,
        matches
    )

    # Process agent engagement
    new_engagements = process_engagements(
        created_post,
        matches
    )

    return {
        "message": "Post published successfully",

        "post": created_post,

        "total_matches": len(matches),

        "matched_agents": matches,

        "notifications_created": len(notifications),

        "total_engagements": len(new_engagements),

        "engagements": new_engagements
    }


@app.get("/posts")
def list_posts():

    return get_all_posts()


@app.get("/posts/{post_id}")
def get_post(post_id: int):

    post = get_post_by_id(post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


# -------------------------------
# RELEVANCE MATCHING
# -------------------------------

@app.get("/posts/{post_id}/matches")
def get_matches(
    post_id: int,
    threshold: float = 15
):

    post = get_post_by_id(post_id)

    if post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    matches = find_relevant_agents(
        post,
        get_all_agents(),
        threshold
    )

    return {
        "post_id": post_id,
        "total_matches": len(matches),
        "matched_agents": matches
    }


# -------------------------------
# NOTIFICATIONS
# -------------------------------

@app.get("/notifications")
def list_notifications():

    return get_all_notifications()


# -------------------------------
# AI AGENT ENGAGEMENT
# -------------------------------

@app.get("/engagements")
def list_engagements():

    return get_all_engagements()


# -------------------------------
# DASHBOARD SUMMARY
# -------------------------------

@app.get("/dashboard/summary")
def dashboard_summary():

    return {
        "total_agents": len(get_all_agents()),

        "total_posts": len(get_all_posts()),

        "total_notifications": len(
            get_all_notifications()
        ),

        "total_engagements": len(
            get_all_engagements()
        )
    }
