import pika
from faker import Faker
from models import Contact
from mongoengine import connect

fake = Faker()

# Підключення до MongoDB
connect('my_database', host='localhost', port=27017)

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='contact_queue')

# Генерація фейкових контактів та запис у базу даних
for _ in range(10):  # Згенеруємо 10 контактів, ви можете змінити цю кількість за потребою
    full_name = fake.name()
    email = fake.email()
    contact = Contact(full_name=full_name, email=email)
    contact.save()

    # Надсилаємо ID створеного контакту у чергу RabbitMQ
    channel.basic_publish(exchange='',
                          routing_key='contact_queue',
                          body=str(contact.id))

print("Сгенеровано та відправлено контакти до черги RabbitMQ")

connection.close()
