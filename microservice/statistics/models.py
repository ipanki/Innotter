from pydantic import BaseModel


class Statistics(BaseModel):
    page_id: str
    user_id: int
    posts_counter: int
    likes_counter: int
    followers_counter: int
