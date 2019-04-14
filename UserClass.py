from random import expovariate


class UserClass:
  def __init__(self, class_name, avg_deadline):
    self.name = class_name
    self.avg_deadline = avg_deadline

  def generate_deadline(self):
    return 1/expovariate(self.avg_deadline)
