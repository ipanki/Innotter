import pika, json


params = pika.URLParameters('amqps://ygktmlix:cVwf88X44xiW8_37lqbWYQ6Zh0gfLujT@baboon.rmq.cloudamqp.com/ygktmlix')
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish_create_page_event(page):
    body = {'page_id': page.id, 'user_id': page.owner.id}
    channel.basic_publish(exchange='', routing_key='create_page', body=json.dumps(body))


def publish_update_posts_counter_event(page):
    body = {'page_id': page.id, 'user_id': page.owner.id}
    channel.basic_publish(exchange='', routing_key='update_posts_counter', body=json.dumps(body))
