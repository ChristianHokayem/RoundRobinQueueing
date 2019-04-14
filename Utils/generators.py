from heapq import heappush
from random import expovariate, uniform

from Event_Simulation.Event import Event
from Packet.Packet import Packet


def add_future_packet_arrival_events_to_heap(events_heap, max_time, arrival_rate,
                                             user_id, user_class, current_time=0):
  while current_time < max_time:
    arrival_time = current_time + round(expovariate(arrival_rate))
    current_time = arrival_time

    deadline = current_time + user_class.generate_deadline()

    new_packet = Packet(arrival_time, deadline, user_id, 8*uniform(64, 1500))
    heappush(events_heap, Event(arrival_time, Event.type_to_num['arrival'], new_packet))

  return events_heap
