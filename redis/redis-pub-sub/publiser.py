import redis
import time

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

channel = "news"

while True:
    message = input("Enter a message to publish (or 'exit' to quit): ")
    if message.lower() == 'exit':
        break
    redis_client.publish(channel, message)
    print(f"Published: {message}")

print("Publisher exited.")
