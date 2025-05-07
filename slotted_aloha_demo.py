import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📡 Slotted ALOHA Simulation")

num_nodes = st.slider("Number of nodes", 2, 10, 4)
num_slots = st.slider("Number of time slots", 5, 30, 10)
prob_send = st.slider("Probability p (retransmission after collision)", 0.0, 1.0, 0.5)

node_next_attempt = [0] * num_nodes
node_waiting = [True] * num_nodes

slot_status = []
slot_senders = [[] for _ in range(num_slots)]

for t in range(num_slots):
    transmitters = []
    for i in range(num_nodes):
        if node_waiting[i] and node_next_attempt[i] <= t:
            if np.random.rand() < prob_send:
                transmitters.append(i)
                slot_senders[t].append(i)

    if len(transmitters) == 0:
        slot_status.append("E")
    elif len(transmitters) == 1:
        slot_status.append("S")
        node_waiting[transmitters[0]] = False
    else:
        slot_status.append("C")
        for i in transmitters:
            node_next_attempt[i] = t + 1

fig, ax = plt.subplots(figsize=(12, 2))
colors = {"C": "red", "S": "green", "E": "gray"}
for t in range(num_slots):
    ax.add_patch(plt.Rectangle((t, 0), 1, 1, color=colors[slot_status[t]]))
    ax.text(t + 0.5, 0.5, slot_status[t], va="center", ha="center", color="white", fontsize=12)
ax.set_xlim(0, num_slots)
ax.set_ylim(0, 1)
ax.axis("off")
st.pyplot(fig)

for t in range(num_slots):
    if slot_status[t] == "C":
        st.write(f"🔴 Slot {t}: Collision - nodes {slot_senders[t]}")
    elif slot_status[t] == "S":
        st.write(f"🟢 Slot {t}: Success - node {slot_senders[t][0]}")
    else:
        st.write(f"⚪ Slot {t}: Empty")