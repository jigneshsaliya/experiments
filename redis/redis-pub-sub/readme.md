# Redis Pub/Sub with Docker and Python

This guide will help you set up a **Redis** server using Docker, create a **Publisher** and **Subscriber** in Python, and run a demo to test the setup.

---

## **1. Running Redis Locally using Docker Compose**

### **Prerequisites**
- Docker installed ([Download Docker](https://www.docker.com/get-started))
- Python installed ([Download Python](https://www.python.org/downloads/))
- `redis-py` library installed
  ```bash
  pip install redis
  ```

### **Setup Redis with Docker Compose**
1. Create a file named `docker-compose.yml` and add the following content:

    ```yaml
    version: '3.8'
    
    services:
      redis:
        image: redis:latest
        container_name: redis_local
        ports:
          - "6379:6379"
        volumes:
          - redis_data:/data
        command: ["redis-server", "--appendonly", "yes"]
    
    volumes:
      redis_data:
        driver: local
    ```

2. Run the following command to start the Redis container:
    ```bash
    docker-compose up -d
    ```
3. Verify Redis is running:
    ```bash
    docker ps
    ```
    You should see a container named `redis_local` running.

---

## **2. Validate the Docker Container**
To confirm that Redis is running correctly inside the container, follow these steps:

1. **SSH into the Redis container:**
    ```bash
    docker exec -it redis_local sh
    ```
2. **Run Redis CLI inside the container:**
    ```bash
    redis-cli
    ```
3. **Test Redis with the PING command:**
    ```bash
    PING
    ```
    You should see the response:
    ```
    PONG
    ```
4. Exit the Redis CLI and the container:
    ```bash
    exit
    exit
    ```

---

## **3. Set Up the Subscriber**
Create a Python script named `sub.py` to subscribe to a Redis channel:

```python
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
```

Run the script:
```bash
python sub.py
```

---

## **4. Set Up the Publisher**
Create a Python script named `pub.py` to publish messages to the Redis channel:

```python
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
```

Run the script:
```bash
python pub.py
```

---

## **5. Demo: Running the Publisher and Subscriber**
1. Open **two terminal windows**.
2. In the first terminal, start the **subscriber**:
    ```bash
    python sub.py
    ```
3. In the second terminal, start the **publisher**:
    ```bash
    python pub.py
    ```
4. Type messages in the **publisher** script, and you should see them appear in the **subscriber** output.
5. When done, type `exit` in the **publisher** to stop publishing messages.
6. Stop the subscriber using `CTRL + C`.

---

### **Stopping and Cleaning Up**
- To stop the Redis container:
  ```bash
  docker-compose down
  ```
- To remove the container and Redis data:
  ```bash
  docker-compose down -v
  ```

---

### **Conclusion**
You have successfully set up a **Redis Pub/Sub** system using Docker and Python. 🎉 You can now use this setup for real-time messaging applications!

