from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from decimal import Decimal
from boto3.dynamodb.conditions import Key
from microservice.statistics.database import connect_db, get_or_create_table_post


db = connect_db()
table = get_or_create_table_post(db)


def create_page_statistics(page_id, user_id):
    try:
        response = table.put_item(
            Item={
                'page_id': page_id,
                'user_id': user_id,
                'posts_counter': 0,
                'likes_counter': 0,
                'followers_counter': 0
            })
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def update_posts_counter(page_id, user_id, counter):
    try:
        response = table.update_item(
            Key={
                "page_id": page_id,
                "user_id": user_id
            },
            UpdateExpression="SET posts_counter = posts_counter + :val",
            ExpressionAttributeValues={
                ":val": Decimal(counter)
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def update_like(post: dict, counter):
    try:
        response = table.update_item(
            Key={
                "page_id": post["page_id"],
            },
            UpdateExpression="SET likes_counter = likes_counter + :val",
            ExpressionAttributeValues={
                ":val": Decimal(counter),
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_page_statistics(page_id: str):
    try:
        response = table.query(
            KeyConditionExpression=Key("page_id").eq(page_id)
        )
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
