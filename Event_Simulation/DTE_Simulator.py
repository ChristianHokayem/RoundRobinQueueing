from heapq import heappop
from random import choice, expovariate

from Event_Simulation.Event import Event
from Packet.Packet import Packet
from Packet.PacketBuffer import FCFSPacketBuffer, InfiniteFCFSPacketBuffer
from Packet.TokenBucket import TokenBucket
from UserClass import UserClass
from Utils.generators import add_future_packet_arrival_events_to_heap


def run_sim(packet_arrival_rate_per_user, packet_target_per_user, number_of_users, number_of_servers, buffer_size,
            average_service_time):
  Packet.clear_packets()

  avg_inter_arrival_time = 1 / packet_arrival_rate_per_user

  max_sim_time = packet_target_per_user * avg_inter_arrival_time

  future_events = []

  user_classes = [UserClass("High", 15), UserClass("Medium", 30), UserClass("Low", 50)]
  user_packets = {i: InfiniteFCFSPacketBuffer() for i in range(number_of_users)}

  for user in user_packets.keys():
    add_future_packet_arrival_events_to_heap(future_events, max_sim_time, packet_arrival_rate_per_user,
                                             user, choice(user_classes))

  master_clock = 0

  buffer = FCFSPacketBuffer(buffer_size)
  bucket = TokenBucket(number_of_servers)
  current_user_service = 0

  while master_clock < max_sim_time:
    while future_events and future_events[0].time == master_clock:

      current_event = heappop(future_events)

      if current_event.type == Event.type_to_num['arrival']:
        user_packets[current_event.reference_packet.user].add_packet(current_event.reference_packet)

    # look for and read from a user which has a payload
    for i in range(number_of_users):
      if user_packets[current_user_service].queue:
        target_packet = user_packets[current_user_service].pop_packet()
        if buffer.add_packet(target_packet):
          target_packet.service_start_time = master_clock
        else:
          target_packet.blocked = True
        current_user_service = (current_user_service + 1) % number_of_users
        break

    buffer.drop_expired_packets(master_clock)

    for i in range(number_of_servers):
      if buffer.queue:
        popped_packet = buffer.pop_packet()
        popped_packet.serviced_amount += expovariate(1 / average_service_time)
        if popped_packet.serviced_amount > popped_packet.size:
          popped_packet.served = True
          popped_packet.service_end_time = master_clock + 1
        else:
          if not buffer.add_packet(popped_packet):
            popped_packet.blocked = True
          else:
            pass  # added back to queue

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

  print(f"Simulated Packets: {number_of_packets}")
  print("---")
  print(f"Served: {number_of_served_packets} ({round(100*number_of_served_packets / number_of_packets, 2)}%)")
  print(f"\tThroughput: {sum([i.size for i in served_packets])} bit/s")
  print(f"\tAvg Wait Time: {sum([i.wait for i in served_packets]) / number_of_served_packets} t.u.")
  print(f"Mismatched: {number_of_mismatched_packets} ({100*round(number_of_mismatched_packets / number_of_packets, 2)}%)")
  print(f"Blocked: {number_of_blocked_packets} ({100*round(number_of_blocked_packets / number_of_packets, 2)}%)")
  print("---")
  Packet.clear_packets()


for LAMBDA in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]:
  print("================")
  print(f"LAMBDA = {LAMBDA}")
  run_sim(packet_arrival_rate_per_user=LAMBDA, packet_target_per_user=10000,
          number_of_users=15, number_of_servers=6, buffer_size=8 * 8e3,
          average_service_time=180)
  print("================")
