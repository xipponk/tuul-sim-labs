import numpy as np
import matplotlib.pyplot as plt

# ตั้งค่าพารามิเตอร์เริ่มต้น
max_time = 50  # จำนวนรอบ (RTT)
cwnd = 1  # Congestion Window เริ่มต้น (MSS)
ssthresh = 16  # ค่า Slow Start Threshold
cwnd_list = []  # เก็บค่า CWND เพื่อ plot
phase_list = []  # บันทึกว่าอยู่ใน Slow Start หรือ AIMD

# จำลอง TCP Slow Start + AIMD
for t in range(max_time):
    cwnd_list.append(cwnd)

    if cwnd < ssthresh:  # ✅ Slow Start Phase
        phase_list.append("Slow Start")
        cwnd *= 2  # Exponential Growth (CWND x 2)
    else:  # ✅ AIMD Phase
        phase_list.append("Congestion Avoidance (AIMD)")
        if np.random.rand() < 0.1 and cwnd > 1:  # 10% โอกาสเกิด packet loss
            print(f"Packet loss at RTT {t+1}! Multiplicative Decrease.")
            ssthresh = max(cwnd // 2, 1)
            cwnd = max(cwnd // 2, 1)  # Multiplicative Decrease (MD)
        else:
            cwnd += 1  # Additive Increase (AI)
    
# วาดกราฟ
plt.figure(figsize=(10, 5))
plt.plot(range(1, max_time + 1), cwnd_list, marker='o', linestyle='-', color='b', label="CWND (Congestion Window)")
plt.xlabel("RTT (Time)")
plt.ylabel("Congestion Window (MSS)")
plt.title("TCP Slow Start + AIMD Simulation")

# แสดงจุดที่เปลี่ยนจาก Slow Start → AIMD
for i in range(len(phase_list)):
    if i > 0 and phase_list[i] != phase_list[i - 1]:  # จุดที่เปลี่ยน phase
        plt.axvline(x=i+1, color='r', linestyle='--', label="Slow Start → AIMD")

plt.legend()
plt.grid()
plt.show()