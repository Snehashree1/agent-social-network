from pydantic import BaseModel, Field


class AgentCreate(BaseModel):
    agent_name: str = Field(min_length=2, max_length=80)
    company: str = Field(min_length=2, max_length=80)
    description: str = Field(min_length=5, max_length=500)
    interests: list[str] = Field(min_length=1)
    keywords: list[str] = Field(default_factory=list)


class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    content: str = Field(min_length=5, max_length=1000)
    category: str
    keywords: list[str] = Field(min_length=1)
    agent_id: int
