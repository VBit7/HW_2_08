import pika
from models import Contact
from mongoengine import connect


connect('my_database', host='localhost', port=27017)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='contact_queue')


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()

    if contact:
        print(f"Email sent to contact: {contact.email}")

        contact.message_sent = True
        contact.save()
        print(f"Updated message delivery status for contact: {contact_id}")


channel.basic_consume(queue='contact_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages from the RabbitMQ queue...')
channel.start_consuming()
