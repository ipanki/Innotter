from fastapi import APIRouter
from microservice.statistics.models import Statistics
from microservice.statistics.service import create_page_statistics, update_posts_counter, get_page_statistics,\
    update_like

routes_user = APIRouter()


@routes_user.post("/create-post")
def create(page_id, user_id):
    return create_page_statistics(str(page_id), int(user_id))


@routes_user.post("/update-post")
def create(page_id):
    return update_posts_counter(str(page_id), 1)


@routes_user.post("/update-like")
def create(post: Statistics):
    return update_like(post.dict(), 1)


@routes_user.get("/statistics/{id}")
def get_by_id(page_id: str):
    return get_page_statistics(page_id)
