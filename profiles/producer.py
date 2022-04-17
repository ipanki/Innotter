import pika, json


params = pika.URLParameters('amqps://ygktmlix:cVwf88X44xiW8_37lqbWYQ6Zh0gfLujT@baboon.rmq.cloudamqp.com/ygktmlix')
connection = pika.BlockingConnection(params)
channel = connection.channel()


def _publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='statistics', body=json.dumps(body), properties=properties)


def publish_page_created_event(page):
    body = {'page_id': page.id, 'user_id': page.owner.id}
    _publish('page_created', body)


def publish_post_created_event(page):
    body = {'page_id': page.id, 'user_id': page.owner.id}
    _publish('post_created', body)


def publish_post_deleted_event(page):
    body = {'page_id': page.id, 'user_id': page.owner.id}
    _publish('post_deleted', body)


def publish_like_created_event(page):
    body = {'page_id': page.id, 'user_id': page.owner.id}
    _publish('like_created', body)


def publish_like_deleted_event(page):
    body = {'page_id': page.id, 'user_id': page.owner.id}
    _publish('post_deleted', body)


def publish_follower_created_event(page):
    body = {'page_id': page.id, 'user_id': page.owner.id}
    _publish('follower_created', body)
