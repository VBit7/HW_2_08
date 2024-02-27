import json
from datetime import datetime
from mongoengine import connect
from models import Author, Quote


connect(
    'mydatabase',
    host="mongodb+srv://user:Example12345@cluster8.w3d66gu.mongodb.net/hw8?retryWrites=true&w=majority&appName=Cluster8"
)

with open('authors.json', 'r', encoding='utf-8') as f:
    authors_data = json.load(f)

with open('quotes.json', 'r', encoding='utf-8') as f:
    quotes_data = json.load(f)

for author_info in authors_data:
    born_date = datetime.strptime(author_info['born_date'], '%B %d, %Y')
    author = Author(
        fullname=author_info['fullname'],
        born_date=born_date,
        born_location=author_info['born_location'],
        description=author_info['description']
    )
    author.save()

for quote_info in quotes_data:
    author = Author.objects(fullname=quote_info['author']).first()
    quote = Quote(
        author=author,
        quote=quote_info['quote'],
        tags=quote_info['tags']
    )
    quote.save()
