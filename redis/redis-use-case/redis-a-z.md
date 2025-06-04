# Redis
- Redis just not being used for cache but its versatile. it handles the diverse use cases such as rate limiting, session management, leaderboard etc. 
- Since redis is in memory it is so fast and it is built and using common data strcture which is making ita blazin fast.
- it support various data strctures like strins, hashes, lists, Hash map, sets and sorted set and that one is making ideal to use redis for cases such as `Caching`, `rate limiting`, `pub/sub messaging` and even designing `social media feeds`. 

## why redis is so fast?
- its in memory data storage. And this makes it so fast compares to other data base which store data on hard disk etc. 
- Single threaded architecture: Redis process all request on a single threaded and no context switching. 
- Non blocking I/O: An event loop and asynchronous request handling ensure low latency and high throughput.
- Optimized data strcutures 

## Understand redis data strctures with example
- `Strings`
    - its being used to store user session data
    - cahing frequently access api responses.
- `Lists` 
    - to implement message queue for asyncronous task.
    - Storing timeline in social media applications.
- `Sets`
    - To track unique visitors. 
    - Maintain unique hastag for posts
- `Sorted Sets`
    - this data strcture combines hash table and sorted sets. Each entry has a string `member`(the key) and a double `score` (sorted value). this allows you to access entries directly by a member or score, and retrieve members in order based on thier score.
    - creating leaderboard in online game.
    - top k most played songs. 
    - ranking search results based on the number likes for a keyword.
- `Hash Maps`
    - commonly used of storing strctures data like objects. 
    - stroing user profile field like name, email, and age. 
    - caching database query results in strctured format.

## List of basic redis command
- Basic redis SET, GET and INCR command
```text
SET foo 1 # it set 1 for key
GET foo # returns 1 for foo if it set or return nil
INCR foo # returns 2 here since foo value was already set as one integer. if foo value is not integer then it returns error like **(error) ERR value is not an integer or out of range**

SET user_session_123 "active" EX 10   # expires in 10 seconds. EX <seconds> or PX <milliseconds> can be used with SET.
```
- `LPUSH and RPUSH`: using that command you can create kind of list as well, and this one can act as kind of queue as well
```text
127.0.0.1:6379> LPUSH queue one
(integer) 1
127.0.0.1:6379> LPUSH queue two
(integer) 2
127.0.0.1:6379> LPUSH queue three
(integer) 3

["three", "two", "one"] <-- Head (Left)

- if you need to set TTL for queue
EXPIRE queue 600   # expires in 10 minutes

127.0.0.1:6379> LRANGE queue 0 -1 # use this command to display all the value in queue
1) "three"
2) "two"
3) "one"

# RPUSH: push from the right
127.0.0.1:6379> RPUSH r_queue one
(integer) 1
127.0.0.1:6379> RPUSH r_queue two
(integer) 2
127.0.0.1:6379> RPUSH r_queue three
(integer) 3

["One", "two", "three"] <-- Tail (Right)

- LRANGE r_queue 0 -1 shows the list from left (head) to right (tail).
127.0.0.1:6379> LRANGE r_queue 0 -1
1) "one"
2) "two"
3) "three"
```
- `LPOP or RPOP` is being used to consume the value from this queue
```text
127.0.0.1:6379> LPOP r_queue ## pop value from left
"one"
```
- 🧠 Pro Tips
```text
LPUSH = Add to left (start) 
RPUSH = Add to right (end) 
LPOP = Remove from left (start), 
RPOP = Remove from right (end), 
Use RPUSH + LPOP OR LPUSH + RPOP for queues -> you can make queue
Use LPUSH + LPOP for stacks -> you can make stack
BLPOP : when you have to wait until item gets available in your queue blocking pop
```

- Sorted Set command of Redis ZADD, ZRANGE, ZREVRANG
- Below using ZADD command you can create sorted hash map with name of hasmap as `ipl_leader_board_2025` and then you can add key as `team name` and value as their `points` in 2025 tournament. 
- Redis internally creates sorted set based on score(value) you have provided.
```text
127.0.0.1:6379> ZADD ipl_leader_board_2025 15 rcb
(integer) 1
127.0.0.1:6379> ZADD ipl_leader_board_2025 12 MI
(integer) 1
127.0.0.1:6379> ZADD ipl_leader_board_2025 10 SRH
(integer) 1
127.0.0.1:6379> ZADD ipl_leader_board_2025 14 GT
(integer) 1
127.0.0.1:6379> ZADD ipl_leader_board_2025 8 DC
(integer) 1
```
- `ZRANGE` command returns key and value from that sorted hash map.
- if you need value in ascending/ increasing order then use `ZRANGE`. 
```text
127.0.0.1:6379> ZRANGE ipl_leader_board_2025 0 5
1) "DC"
2) "SRH"
3) "MI"
4) "GT"
5) "rcb"
```
- if you need value with score then use `WITHSCORE` parameter
```text
127.0.0.1:6379> ZRANGE ipl_leader_board_2025 0 5 WITHSCORES
 1) "DC"
 2) "8"
 3) "SRH"
 4) "10"
 5) "MI"
 6) "12"
 7) "GT"
 8) "14"
 9) "rcb"
10) "15"
```
- `ZREVRANGE`: if you need value in descending/ decreasing order then use this command. 
```text
127.0.0.1:6379> ZREVRANGE ipl_leader_board_2025 0 5
1) "rcb"
2) "GT"
3) "MI"
4) "SRH"
5) "DC"
```
- if you need value with score then use `WITHSCORE` parameter
```text
127.0.0.1:6379> ZREVRANGE ipl_leader_board_2025 0 5 WITHSCORES
 1) "rcb"
 2) "15"
 3) "GT"
 4) "14"
 5) "MI"
 6) "12"
 7) "SRH"
 8) "10"
 9) "DC"
10) "8"
```

- `SADD`: to create just set you can use this command, as it will create set with name which will always have unique value, NOTE: here there is no score
```text
127.0.0.1:6379> SADD users user1 # Added user1 in to users set
(integer) 1
127.0.0.1:6379> SADD users user2 # Added user2 in to users set
(integer) 1
127.0.0.1:6379> SADD users user2 # tried to add already existing user in to set and then it return 0 means it is already existing in set
(integer) 0
```

- `SMEMBERS` : to list down all value in has set
```text
127.0.0.1:6379> SMEMBERS users
1) "user1"
2) "user2"
```
- `HSET`: it is kind of like hasmap(in JAVA) or dictionary (in python) DSA.
```text
127.0.0.1:6379> HSET user:1 name "John Smith" age 25 email "johnsmith@gmail.com"
(integer) 3 ## here HSET creates this hashmap with name user:1 and it can hold this key and value
```
- to get specific value for key or get all key value then use below command
```text
127.0.0.1:6379> HGETALL user:1 # gives all key and value
1) "name"
2) "John Smith"
3) "age"
4) "25"
5) "email"
6) "johnsmith@gmail.com"
127.0.0.1:6379> HGET user:1 email # since you specified which key value you need it will return that only if it exist
"johnsmith@gmail.com"
```
- `XADD`: To create kind of like Append only file steam in redis
- This adds a new entry with auto-generated ID (*) to the stream mystream
```text
127.0.0.1:6379> XADD mystream * name Sara surname OConnor
"1748033411485-0"
```
- using this `XADD` you can create steam and producer can put event in this stream (Append only, durable) and other side consumer can consume this event from stream and then ack as well after processing.

- most of the time you can use `EXPIRE` command to set expire for given key. which is being called as TTL.
```text
ZADD ipl_leader_board_2025 15 rcb
EXPIRE ipl_leader_board_2025 86400  # expires in 1 day 86400 is total seconds in one day
```

# Top redis use cases in system design
## Redis as cache

## Redis as a distributed lock: Ensuring data consistency in System Design

## Redis as Leaderboard in Gaming applications

## Redis as a Rate Limiter: Best Practices for High Traffic Systems

## Locating nearby drivers with Redis Geohashes in ride-hailing apps

## Redis for async communication: Message Queues

## Storing and analyzing time series data in Redis

## Managing user sessions with Redis

## Redis for top posts in Social Media: Real-Time ranking and engagement optimization

## Other use cases of Redis:
- Real-time messaging using Pub-Sub (Figure 10)
- Approximate the cardinality of a large set using HyperLogLog
- Full-text search using the RedisSearch module
- Storing nested JSON without re-serialization costs using RedisJSON
