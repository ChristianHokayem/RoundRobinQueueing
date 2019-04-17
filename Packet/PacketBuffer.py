from heapq import heappush, heappop, heapify


class FCFSPacketBuffer:
  def __init__(self, capacity):
    self.queue = []
    self.capacity = capacity

  def add_packet(self, packet, current_time):
    if (self.capacity - packet.size) >= 0:
      heappush(self.queue, (current_time, packet))
      self.capacity -= packet.size
      return True
    else:
      return False

  def pop_packet(self):
    if self.queue:
      self.capacity += self.queue[0][1].size
      return heappop(self.queue)[1]
    else:
      return None

  def drop_expired_packets(self, current_time):
    packets_for_removal = []
    for packet in self.queue:
      if packet[1].deadline < current_time:
        packets_for_removal.append(packet)
    for packet in packets_for_removal:
      self.queue.remove(packet)
      self.capacity += packet[1].size
      packet[1].mismatched = True
    heapify(self.queue)


class InfiniteFCFSPacketBuffer:
  def __init__(self):
    self.queue = []

  def add_packet(self, packet, current_time):
    heappush(self.queue, (current_time, packet))
    return True

  def pop_packet(self):
    if self.queue:
      return heappop(self.queue)[1]
    else:
      return None

  def read_top_element(self):
    return self.queue[0][1]
