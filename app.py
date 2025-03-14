import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Streamlit app title
st.title("Projectile Motion Simulation")

# Sidebar for user input
st.sidebar.header("Initial Conditions")
x_i = 0  # Initial X-position (fixed)
y_i = st.sidebar.slider("Initial Y-position (m)", 0, 100, 0)
V_i = st.sidebar.slider("Initial Velocity (m/s)", 0, 150, 100)
theta = st.sidebar.slider("Launch Angle (degrees)", 0, 90, 60)

# Air resistance
st.sidebar.header("Air Resistance")
air_resist_const = st.sidebar.slider("Air Resistance Constant", 0.0, 0.2, 0.0)
#air_resist_type = st.sidebar.radio("Resistance Type", [1, 2], index=0)
air_resist_type = 1

# Convert angle to radians
theta_rad = np.radians(theta)

# Define air resistance function
def air_resist_force(const, v, n):
    return const * (v ** n)

# Initial velocity components
if theta == 90:
    Vx_initial = 0
else:
    Vx_initial = V_i * np.cos(theta_rad)

Vy_initial = V_i * np.sin(theta_rad)

# Counteracting force due to air resistance
counterForce_i = air_resist_force(air_resist_const, V_i, air_resist_type)
if theta == 90:
    Ax_initial = 0
else:
    Ax_initial = counterForce_i * np.cos(theta_rad)

Ay_initial = counterForce_i * np.sin(theta_rad) + 9.81

# Data lists
x_data, y_data = [x_i], [y_i]
Vx_data, Vy_data = [Vx_initial], [Vy_initial]
Ax_data, Ay_data = [-Ax_initial], [-Ay_initial]
time_data = [0]

time_interval = 0.01  # Time step
i, new_y = 0, 1  # Iteration counter

# Simulation loop
while new_y >= 0:
    new_y = y_data[i] + Vy_data[i] * time_interval + 0.5 * Ay_data[i] * time_interval**2
    y_data.append(new_y)

    new_Vy = Vy_data[i] + Ay_data[i] * time_interval
    Vy_data.append(new_Vy)

    new_x = x_data[i] + Vx_data[i] * time_interval + 0.5 * Ax_data[i] * time_interval**2
    x_data.append(new_x)

    new_Vx = Vx_data[i] + Ax_data[i] * time_interval
    Vx_data.append(new_Vx)

    V_tot = np.sqrt(Vx_data[i]**2 + Vy_data[i]**2)
    counterForce = air_resist_force(air_resist_const, V_tot, air_resist_type)

    if new_Vx < 1e-6:
        if new_Vy > 0:
            new_theta = np.pi/2
        else:
            new_theta = -np.pi/2

    else:
        new_theta = np.arctan(new_Vy / new_Vx)
    new_Ay = -counterForce * np.sin(new_theta) - 9.81
    Ay_data.append(new_Ay)

    new_Ax = -counterForce * np.cos(new_theta)
    Ax_data.append(new_Ax)

    time_data.append((i + 1) * time_interval)

    i += 1

# Plot results using Streamlit

st.subheader("Y vs X (Projectile Path)")
fig1, ax1 = plt.subplots()
ax1.plot(x_data, y_data, label="Projectile Path", color="blue")
ax1.axhline(0, color="black")  # Ground level
if max(x_data) < 500:
    ax1.set_xlim(-20, 500)
    ax1.set_ylim(0, 600)

else:
    ax1.set_xlim(-100, 2500)
    ax1.set_ylim(0, 1600)
ax1.set_xlabel("X-axis (m)")
ax1.set_ylabel("Y-axis (m)")
ax1.legend()
st.pyplot(fig1)


st.subheader("Velocity vs Time")
fig2, ax2 = plt.subplots()
ax2.plot(time_data, Vx_data, label="Vx", color="blue")
ax2.plot(time_data, Vy_data, label="Vy", color="red")
ax2.axhline(0, color="black")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Velocity (m/s)")
ax2.legend()
st.pyplot(fig2)


st.subheader("Acceleration vs Time")
fig3, ax3 = plt.subplots()
ax3.plot(time_data, Ax_data, label="Ax", color="blue")
ax3.plot(time_data, Ay_data, label="Ay", color="red")
ax3.axhline(0, color="black")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Acceleration (m/s²)")
ax3.legend()
st.pyplot(fig3)


st.subheader("Position vs Time")
fig4, ax4 = plt.subplots()
ax4.plot(time_data, x_data, label="X Position", color="blue")
ax4.plot(time_data, y_data, label="Y Position", color="red")
ax4.axhline(0, color="black")
ax4.set_xlabel("Time (s)")
ax4.set_ylabel("Position (m)")
ax4.legend()
st.pyplot(fig4)
