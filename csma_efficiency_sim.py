import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("CSMA/CD Efficiency Simulator")

# User input sliders
T_trans = st.slider("Transmission time (µs)", 10, 200, 50)
T_prop_min = st.slider("Minimum T_prop (µs)", 0, 50, 1)
T_prop_max = st.slider("Maximum T_prop (µs)", 50, 500, 100)

T_prop_range = np.linspace(T_prop_min, T_prop_max, 100)

# Efficiency formula
def csma_cd_efficiency(T_prop, T_trans):
    return 1 / (1 + 5 * (T_prop / T_trans))

eff_values = csma_cd_efficiency(T_prop_range, T_trans)

# Plot
fig, ax = plt.subplots()
ax.plot(T_prop_range, eff_values, label="Efficiency", color='blue')
ax.set_xlabel("Propagation Delay (T_prop) [µs]")
ax.set_ylabel("Efficiency")
ax.set_title("CSMA/CD Efficiency vs Propagation Delay")
ax.grid(True)
ax.legend()

st.pyplot(fig)