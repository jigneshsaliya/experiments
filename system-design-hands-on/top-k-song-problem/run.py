from collections import defaultdict
import heapq

class TopKSongs:
        def __init__(self, k):
            self.k = k
            self.play_count = defaultdict(int)
            self.min_heap = []
            
        def play_sing(self, song_id):
            self.play_count[song_id] += 1
            
        def get_top_k(self):
            # Clear the min heap for fresh calculation
            self.min_heap = []
            
            # Build a min-heap of size k
            for song_id, count in self.play_count.items():
                if len(self.min_heap) < self.k:
                    # when the heap is not full, push the new song
                    heapq.heappush(self.min_heap, (count, song_id))
                else:
                    heapq.heappushpop(self.min_heap, (count, song_id))
            
            # Extract the top k songs from the min-heap
            return sorted(self.min_heap, key=lambda x: (-x[0], x[1]))
        
topk = TopKSongs(k=3)
# Simulate playing songs
topk.play_sing("song1")
topk.play_sing("song2")
topk.play_sing("song3")
topk.play_sing("song1")
topk.play_sing("song2")
topk.play_sing("song2")
topk.play_sing("song2")
topk.play_sing("song4")
print(topk.get_top_k())  # Should print the top 3 songs based on play count
# Example output: [(2, 'song1'), (2, 'song2'), (1, 'song3')]
# Example usage
# Note: The output format is (play_count, song_id) for clarity