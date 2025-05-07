import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("📡 CSMA Collision from Propagation Delay")

# Parameters
num_nodes = st.slider("Number of nodes", 2, 6, 4)
distance_between_nodes = st.slider("Distance between nodes (arbitrary units)", 1, 10, 3)
packet_duration = st.slider("Packet duration (in time units)", 5, 20, 10)

# Choose two transmitters
tx_node1 = st.selectbox("Transmitting Node A", list(range(num_nodes)), index=0)
tx_node2 = st.selectbox("Transmitting Node B", list(range(num_nodes)), index=num_nodes - 1)
tx_start1 = st.slider(f"Start time of Node A", 0, 50, 5)
tx_start2 = st.slider(f"Start time of Node B", 0, 50, 10)

# Positions of nodes
positions = np.arange(num_nodes) * distance_between_nodes

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot propagation from Node A
for t in range(packet_duration):
    arrival = [tx_start1 + t + abs(pos - positions[tx_node1]) for pos in positions]
    ax.plot(arrival, positions, 'y.', alpha=0.4)

# Plot propagation from Node B
for t in range(packet_duration):
    arrival = [tx_start2 + t + abs(pos - positions[tx_node2]) for pos in positions]
    ax.plot(arrival, positions, 'r.', alpha=0.4)

# Mark transmission bars
ax.plot([tx_start1, tx_start1 + packet_duration], [positions[tx_node1]]*2, 'y-', linewidth=4, label=f'Node A (#{tx_node1})')
ax.plot([tx_start2, tx_start2 + packet_duration], [positions[tx_node2]]*2, 'r-', linewidth=4, label=f'Node B (#{tx_node2})')

ax.set_xlabel("Time")
ax.set_ylabel("Node Position")
ax.set_title("Signal Propagation and Possible Collision Zone")
ax.legend()
st.pyplot(fig)

# Midpoint collision detection
mid_pos = (positions[tx_node1] + positions[tx_node2]) // 2
arrival1 = tx_start1 + abs(mid_pos - positions[tx_node1])
arrival2 = tx_start2 + abs(mid_pos - positions[tx_node2])
collided = abs(arrival1 - arrival2) < packet_duration

if collided:
    st.error("⚠️ Collision is likely due to overlapping signals at midpoint!")
else:
    st.success("✅ No collision detected at midpoint.")