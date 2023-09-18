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

al_counter = client.cp_subsystem.get_atomic_long("counter").blocking()
al_counter.add_and_get(0)


# basic increment func
def increment_counter():
    for t in range(0, 10000):
        current = al_counter.increment_and_get()
        # print(current)


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

print(f'Final counter value: {al_counter.get()}')
print(f'Final execution time: {end_time- start_time: 0.2f} seconds')
