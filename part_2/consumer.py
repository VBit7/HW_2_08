import pika
from models import Contact
from mongoengine import connect

# Підключення до MongoDB
connect('my_database', host='localhost', port=27017)

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='contact_queue')


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()

    if contact:
        # Імітація відправлення повідомлення по email (функція-заглушка)
        print(f"Відправлено email контакту: {contact.email}")

        # Оновлення поля message_sent
        contact.message_sent = True
        contact.save()
        print(f"Оновлено статус відправки повідомлення для контакту: {contact_id}")


# Підписка на чергу для отримання повідомлень
channel.basic_consume(queue='contact_queue', on_message_callback=callback, auto_ack=True)

print('Очікування повідомлень з черги RabbitMQ...')
channel.start_consuming()
