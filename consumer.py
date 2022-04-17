import pika, json
from microservice.microservice.statistics import service, config

params = pika.URLParameters(config.rabbitmq_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='statistics')


def on_message_callback(ch, method, properties, body):
    payload = json.loads(body)
    page_id = str(payload['page_id'])
    user_id = int(payload['user_id'])

    if properties.content_type == 'page_created':
        service.create_page_statistics(page_id, user_id)

    elif properties.content_type == 'post_created':
        service.update_posts_counter(page_id, user_id, 1)

    elif properties.content_type == 'post_deleted':
        service.update_posts_counter(page_id, user_id, -1)

    elif properties.content_type == 'like_created':
        service.update_likes_counter(page_id, user_id, 1)

    elif properties.content_type == 'like_deleted':
        service.update_likes_counter(page_id, user_id, -1)

    elif properties.content_type == 'follower_created':
        service.update_followers_counter(page_id, user_id, 1)


channel.basic_consume(queue='statistics', on_message_callback=on_message_callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
