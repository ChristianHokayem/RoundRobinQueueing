from Event_Simulation.DTE_Simulator import run_sim


def generate_csv_line(input_list):
  return ",".join([str(i) for i in input_list]) + "\n"


output_str = generate_csv_line(["Lambda", "Packets", "Served Packets", "Served %", "Mismatched Packets", "Mismatch %",
                                "Blocked Packets", "Block %", "Throughput", "Average Wait Time"])

for LAMBDA in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]:
  number_of_packets, number_of_served_packets, number_of_mismatched_packets, number_of_blocked_packets, \
    throughput, avg_wait_time = run_sim(packet_arrival_rate_per_user=LAMBDA, packet_target_per_user=100000,
                                        number_of_users=15, number_of_servers=6, buffer_size=8 * 8e3,
                                        average_service_time=180, rate_of_high_priority=0.1, rate_of_medium_priority=0.1,
                                        rate_of_low_priority=0.8)
  served_percentage = 100 * number_of_served_packets / number_of_packets
  mismatched_percentage = 100 * number_of_mismatched_packets / number_of_packets
  blocked_percentage = 100 * number_of_blocked_packets / number_of_packets
  print("\n===========")
  print(f"Lambda = {LAMBDA}")
  print(f"Simulated Packets: {number_of_packets}")
  print("---")
  print(f"Served: {number_of_served_packets} ({round(served_percentage, 2)}%) ")
  print(f"\tThroughput: {throughput} bit/t.u.")
  print(f"\tAvg Wait Time: {avg_wait_time} t.u.")
  print(
    f"Mismatched: {number_of_mismatched_packets} ({round(mismatched_percentage, 2)}%)")
  print(f"Blocked: {number_of_blocked_packets} ({round(blocked_percentage, 2)}%)")
  print("===========\n")
  output_str += generate_csv_line([LAMBDA, number_of_packets, number_of_served_packets, served_percentage,
                                   number_of_mismatched_packets, mismatched_percentage, number_of_blocked_packets,
                                   blocked_percentage, throughput, avg_wait_time])

with open("rr_test.csv", "w+") as file:
  file.write(output_str)
