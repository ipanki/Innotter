import pika, json
from microservice.statistics.service import create_page_statistics, update_posts_counter

params = pika.URLParameters('amqps://ygktmlix:cVwf88X44xiW8_37lqbWYQ6Zh0gfLujT@baboon.rmq.cloudamqp.com/ygktmlix')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='create_page')
channel.queue_declare(queue='update_posts_counter')
channel.queue_declare(queue='update_likes_counter')
channel.queue_declare(queue='update_followers_counter')


def callback_on_page_created(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    page_id = data['page_id']
    user_id = data['user_id']
    print(data)
    create_page_statistics(str(page_id), int(user_id))


channel.basic_consume(queue='create_page', on_message_callback=callback_on_page_created, auto_ack=True)


def callback_on_posts_counter(ch, method, properties, body):
    print('Received in update_posts_counter')
    data = json.loads(body)
    page_id = data['page_id']
    user_id = data['user_id']
    print(data)
    update_posts_counter(str(page_id), int(user_id), 1)


channel.basic_consume(queue='update_posts_counter', on_message_callback=callback_on_posts_counter, auto_ack=True)


print('Started Consuming')

channel.start_consuming()

channel.close()
