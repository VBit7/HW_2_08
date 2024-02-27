import json
from datetime import datetime
from mongoengine import connect
from models import Author, Quote

# Підключення до бази даних MongoDB
# connect('mydatabase', host='mongodb://localhost:27017/mydatabase')

# Підключення до бази даних MongoDB Atlas
connect(
    'mydatabase',
    # host='mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/<database-name>?retryWrites=true&w=majority'
    host="mongodb+srv://user:Example12345@cluster8.w3d66gu.mongodb.net/hw8?retryWrites=true&w=majority&appName=Cluster8"
)

# Завантаження авторів з файлу authors.json
with open('authors.json', 'r', encoding='utf-8') as f:
    authors_data = json.load(f)

# Завантаження цитат з файлу quotes.json
with open('quotes.json', 'r', encoding='utf-8') as f:
    quotes_data = json.load(f)

# Завантаження авторів
for author_info in authors_data:
    born_date = datetime.strptime(author_info['born_date'], '%B %d, %Y')
    author = Author(
        fullname=author_info['fullname'],
        born_date=born_date,
        born_location=author_info['born_location'],
        description=author_info['description']
    )
    author.save()

# Завантаження цитат
for quote_info in quotes_data:
    author = Author.objects(fullname=quote_info['author']).first()
    quote = Quote(
        author=author,
        quote=quote_info['quote'],
        tags=quote_info['tags']
    )
    quote.save()
