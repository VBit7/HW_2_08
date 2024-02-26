import redis
import regex as re
from mongoengine import connect
from models import Author, Quote

# Підключення до бази даних MongoDB Atlas
connect(
    'mydatabase',
    host="mongodb+srv://user:Example12345@cluster8.w3d66gu.mongodb.net/hw8?retryWrites=true&w=majority&appName=Cluster8"
)

# Підключення до Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def search_quotes(query):
    # Перевірка, чи результат запиту є в кеші Redis
    cached_result = redis_client.get(query)
    if cached_result:
        print("Result from cache:")
        print(cached_result.decode())
        return

    # Регулярний вираз для скороченого запису
    short_query_regex = re.compile(r'^(name|tag):(.+)$')

    match = short_query_regex.match(query)
    if match:
        command, value = match.groups()
        if command == 'name':
            query = f'name:{value}'
        elif command == 'tag':
            query = f'tag:{value}'

    if query.startswith('name:'):
        author_name = query.split(':')[1].strip()
        # Застосовуємо регулярний вираз для пошуку часткового співпадіння
        regex_pattern = f'^{author_name}'
        authors = Author.objects(fullname__regex=regex_pattern, fullname__iregex=regex_pattern)
        if authors:
            for author in authors:
                quotes = Quote.objects(author=author)
                result = "\n".join(quote.quote for quote in quotes)
                print(result)
                # Збереження результату у кеші Redis
                redis_client.set(query, result)
        else:
            print("Author not found.")
    elif query.startswith('tag:'):
        tag = query.split(':')[1].strip()
        quotes = Quote.objects(tags__icontains=tag)
        result = "\n".join(quote.quote for quote in quotes)
        print(result)
        # Збереження результату у кеші Redis
        redis_client.set(query, result)
    elif query.startswith('tags:'):
        tags = query.split(':')[1].strip().split(',')
        quotes = Quote.objects(tags__icontains=tags[0])
        for tag in tags[1:]:
            quotes = quotes.filter(tags__icontains=tag)
        result = "\n".join(quote.quote for quote in quotes)
        print(result)
        # Збереження результату у кеші Redis
        redis_client.set(query, result)
    elif query == 'exit':
        exit()
    else:
        print("Invalid query.")

# Головний цикл для пошуку
while True:
    user_input = input("Enter your search query: ")
    search_quotes(user_input)
