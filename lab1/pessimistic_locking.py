import hazelcast
from threading import Thread
import logging
from time import perf_counter

logging.basicConfig(level=logging.INFO)

client = hazelcast.HazelcastClient(
    cluster_name="lab1",
    cluster_members=[
        "192.168.1.23:5701",
        "192.168.1.23:5702",
        "192.168.1.23:5703"
    ])

my_map = client.get_map("basic").blocking()
my_map.put("counter", 0)


# pessimistic locking - https://docs.hazelcast.com/hazelcast/5.3/data-structures/locking-maps
def increment_counter():
    my_map.lock("counter")
    for t in range(0, 10000):
        my_map.replace("counter", my_map.get("counter")+1)
        # print("New current: ", my_map.get("counter"))
    my_map.unlock("counter")


# configure 10 threads
threads = [Thread(target=increment_counter)
           for t in range(0, 10)]

# start performance check
start_time = perf_counter()

# do our stuff
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

end_time = perf_counter()

print(f'Final counter value: {my_map.get("counter")}')
print(f'Final execution time: {end_time- start_time: 0.2f} seconds')
