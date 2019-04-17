from heapq import heappop
from random import expovariate, random

from Event_Simulation.Event import Event
from Packet.Packet import Packet
from Packet.PacketBuffer import FCFSPacketBuffer, InfiniteFCFSPacketBuffer
from UserClass import UserClass
from Utils.generators import add_future_packet_arrival_events_to_heap


def run_sim(packet_arrival_rate_per_user, packet_target_per_user, number_of_users, number_of_servers, buffer_size,
            average_service_time, rate_of_high_priority, rate_of_medium_priority, rate_of_low_priority):
  Packet.clear_packets()

  if round(rate_of_high_priority + rate_of_medium_priority + rate_of_low_priority, 3) != 1:
    raise ValueError("Sum of rate of priorities does not match 1")

  avg_inter_arrival_time = 1 / packet_arrival_rate_per_user

  max_sim_time = packet_target_per_user * avg_inter_arrival_time

  future_events = []

  high_priority_class = UserClass("High", 15)
  medium_priority_class = UserClass("Medium", 30)
  low_priority_class = UserClass("Low", 50)

  user_packets = {i: InfiniteFCFSPacketBuffer() for i in range(number_of_users)}

  for user in user_packets.keys():
    rand_num = random()
    if rand_num < rate_of_high_priority:
      add_future_packet_arrival_events_to_heap(future_events, max_sim_time, packet_arrival_rate_per_user,
                                               user, high_priority_class)
    elif rand_num < rate_of_high_priority + rate_of_medium_priority:
      add_future_packet_arrival_events_to_heap(future_events, max_sim_time, packet_arrival_rate_per_user,
                                               user, medium_priority_class)
    else:
      add_future_packet_arrival_events_to_heap(future_events, max_sim_time, packet_arrival_rate_per_user,
                                               user, low_priority_class)

  master_clock = 0

  buffer = FCFSPacketBuffer(buffer_size)
  current_user_service = 0

  while master_clock < max_sim_time:
    serviced_packet = False

    while future_events and future_events[0].time == master_clock:

      current_event = heappop(future_events)

      if current_event.type == Event.type_to_num['arrival']:
        user_packets[current_event.reference_packet.user].add_packet(current_event.reference_packet, master_clock)

    # look for and read from a user which has a payload
    for i in range(number_of_users):
      if user_packets[current_user_service].queue:
        target_packet = user_packets[current_user_service].pop_packet()
        if buffer.add_packet(target_packet, master_clock):
          target_packet.service_start_time = master_clock
        else:
          target_packet.blocked = True
        current_user_service = (current_user_service + 1) % number_of_users
        break

    buffer.drop_expired_packets(master_clock)

    for i in range(number_of_servers):
      if buffer.queue:
        serviced_packet = True
        popped_packet = buffer.pop_packet()
        popped_packet.serviced_amount += expovariate(1 / average_service_time)
        if popped_packet.serviced_amount > popped_packet.size:
          popped_packet.served = True
          popped_packet.service_end_time = master_clock + 1
        else:
          if not buffer.add_packet(popped_packet, master_clock):
            popped_packet.blocked = True
          else:
            pass  # added back to queue

    if not serviced_packet and not buffer.queue:
      master_clock = future_events[0].time
      continue

    master_clock += 1

  served_packets = [i for i in Packet.packets_tracker if i.served is True]
  mismatched_packets = [i for i in Packet.packets_tracker if i.mismatched is True]
  blocked_packets = [i for i in Packet.packets_tracker if i.blocked is True]
  all_packets = served_packets + mismatched_packets + blocked_packets

  number_of_served_packets = len(served_packets)
  number_of_mismatched_packets = len(mismatched_packets)
  number_of_blocked_packets = len(blocked_packets)
  number_of_packets = len(all_packets)

  for packet in served_packets:
    packet.wait = packet.service_end_time - packet.service_start_time

  throughput = sum([i.size for i in served_packets]) / master_clock
  avg_wait_time = sum([i.wait for i in served_packets]) / number_of_served_packets

  Packet.clear_packets()

  return number_of_packets, number_of_served_packets, number_of_mismatched_packets, number_of_blocked_packets, \
         throughput, avg_wait_time
