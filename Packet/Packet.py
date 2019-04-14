class Packet:
  packets_tracker = []

  def __init__(self, arrival_time, deadline, user_id, size):
    self.arrival_time = arrival_time
    self.service_start_time = None
    self.deadline = deadline
    self.service_end_time = None
    self.wait = None
    self.user = user_id
    self.size = size
    self.serviced_amount = 0
    self.blocked = False
    self.mismatched = False
    self.served = False
    Packet.packets_tracker.append(self)

  @staticmethod
  def clear_packets():
    Packet.packets_tracker.clear()

  def __lt__(self, other):
    return self.arrival_time < other.arrival_time
