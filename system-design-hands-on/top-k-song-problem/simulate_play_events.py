import time
import random
from collections import defaultdict
from faker import Faker
from datetime import datetime

fak = Faker()

# sample data
SONGS = [f"song_{i}" for i in range(1, 21)]
USERS = [f"user_{i}" for i in range(1 ,11)]

# In-memory play count store
play_count = defaultdict(int)

def generate_play_event():
    return {
        "user_id": random.choice(USERS),
        "song_id": random.choice(SONGS),
        "timestamp": datetime.now().isoformat() + "Z"
    }
    
def process_event(event): 
    song_id = event["song_id"]
    play_count[song_id]+= 1  # Increment play count for the song
    
def get_top_k(k=5):
    # Sort songs by play count and return the top k
    sorted_songs = sorted(play_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_songs[:k]

def run_simulation(num_events=100, delay=0.1):
    for _ in range(num_events):
        event = generate_play_event()
        process_event(event)
        print(f"Processed event: {event}")
        time.sleep(delay)  # Simulate delay between events

    print("\nTop K Songs:")
    for rank, (song_id, count) in enumerate(get_top_k(), start=1):
        print(f"{rank}. {song_id} - {count} plays")

if __name__ == "__main__":
    run_simulation()