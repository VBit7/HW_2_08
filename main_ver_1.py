from mongoengine import connect
from models import Author, Quote

# Підключення до бази даних MongoDB Atlas
connect(
    'mydatabase',
    # host='mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/<database-name>?retryWrites=true&w=majority'
    host="mongodb+srv://user:Example12345@cluster8.w3d66gu.mongodb.net/hw8?retryWrites=true&w=majority&appName=Cluster8"
)


def search_quotes(query):
    if query.startswith('name:'):
        author_name = query.split(':')[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote.quote)
        else:
            print("Author not found.")
    elif query.startswith('tag:'):
        tag = query.split(':')[1].strip()
        quotes = Quote.objects(tags=tag)
        for quote in quotes:
            print(quote.quote)
    elif query.startswith('tags:'):
        tags = query.split(':')[1].strip().split(',')
        quotes = Quote.objects(tags__in=tags)
        for quote in quotes:
            print(quote.quote)
    elif query == 'exit':
        exit()
    else:
        print("Invalid query.")

# Головний цикл для пошуку
while True:
    user_input = input("Enter your search query: ")
    search_quotes(user_input)
