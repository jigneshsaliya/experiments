import redis

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

channel = "news"

# Create a pub/sub object
pubsub = redis_client.pubsub()
pubsub.subscribe(channel)

print(f"Subscribed to channel: {channel}")

# Listen for messages
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Received: {message['data']}")
