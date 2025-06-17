# Design top-k played song like Spotify.
- I want to design a system which can be something similar to Spotify Top K song.

## Functional requirement 
- Count the number of times each song is played
- Retrieve the Top-K most played songs in real time. 
- Scale to millions of user concurrently.
- Support play events from multiple devices/regions 
- Accuracy tradeoff (eventual vs strong consistency) is accepatable. 

## Non functional requirement 
- Highly scalable and distributed
- Low latency reads for Top K queries
- High write throughput for play requests
- Fault tolerent and cost-effective

