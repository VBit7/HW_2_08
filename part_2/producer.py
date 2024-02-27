import pika
from faker import Faker
from models import Contact
from mongoengine import connect

fake = Faker()

connect('my_database', host='localhost', port=27017)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='contact_queue')

for _ in range(10):
    full_name = fake.name()
    email = fake.email()
    contact = Contact(full_name=full_name, email=email)
    contact.save()

    channel.basic_publish(exchange='',
                          routing_key='contact_queue',
                          body=str(contact.id))

print("Contacts generated and sent to the RabbitMQ queue")

connection.close()
