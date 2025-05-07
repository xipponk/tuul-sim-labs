import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Initial Parameters
max_time = 50  # Round Trip Time (RTT)
cwnd = 1  # Initial Congestion Window (cwnd = 1 MSS)
ssthresh = 16  # Slow Start Threshold value
timeout_probability = 0.05  # Probability for Timeout (My default is 5%)
packet_loss_probability = 0.03  # Probability for Packet Loss (My default is 3%)
severe_loss_probability = 0.01  # Probability for severe Packet Loss until Reset congestion window (My default is 1%)

data = []  # collect data for table

# Start Simulation
print(f"{'RTT':<5} {'CWND (MSS)':<12} {'SSTHRESH':<12} {'Phase'}")
print("-" * 50)

for t in range(1, max_time + 1):
    phase = "Slow Start" if cwnd < ssthresh else "Congestion Avoidance (AIMD)"

    # Show RTT round on terminal screen
    print(f"{t:<5} {cwnd:<12} {ssthresh:<12} {phase}")

    # Collect data in DataFrame
    data.append([t, cwnd, ssthresh, phase])

    # Timeout check (RTO Expiry)
    if np.random.rand() < timeout_probability:
        print(f"\u23F3 Timeout at RTT {t}! Reset to Slow Start.")
        ssthresh = max(cwnd // 2, 1)
        cwnd = 1  # Reset CWND back to Slow Start phase
        continue  # skip to next RTT

    # Packet Loss checking
    if np.random.rand() < packet_loss_probability and cwnd > 1:
        if np.random.rand() < severe_loss_probability:  # Check for severe Loss
            print(f"\u26A0\uFE0F Severe Packet Loss at RTT {t}! Reset to Slow Start.")
            ssthresh = max(cwnd // 2, 1)
            cwnd = 1  # Reset CWND to Slow Start phase
        else:  # If it is a normal Loss (utilized Multiplicative Decrease (MD))
            print(f"\u26A0\uFE0F Packet loss at RTT {t}! Multiplicative Decrease.")
            ssthresh = max(cwnd // 2, 1)
            cwnd = max(cwnd // 2, 1)  # Multiplicative Decrease (MD)
        continue  # skip to next RTT

    # Slow Start Phase
    if cwnd < ssthresh:
        cwnd *= 2  # Exponential Growth (CWND x 2)
    else:  # AIMD Phase
        cwnd += 1  # Additive Increase (AI)

# Create a DataFrame
df = pd.DataFrame(data, columns=["RTT", "CWND (MSS)", "SSTHRESH", "Phase"])

# Show table in Console
print("\nFinal Table of CWND Values:")
print(df.to_string(index=False))

# Draw a graph :)
plt.figure(figsize=(10, 5))
plt.plot(df["RTT"], df["CWND (MSS)"], marker='o', linestyle='-', color='b', label="CWND (Congestion Window)")
plt.xlabel("RTT (Time)")
plt.ylabel("Congestion Window (MSS)")
plt.title("TCP Slow Start + AIMD with Timeout Reset Simulation")

# Mark point that change from Slow Start phase → AIMD phase
for i in range(len(df)):
    if i > 0 and df["Phase"][i] != df["Phase"][i - 1]:  # point that phase has been changed
        plt.axvline(x=df["RTT"][i], color='r', linestyle='--', label="Slow Start → AIMD")

plt.legend()
plt.grid()
plt.show()