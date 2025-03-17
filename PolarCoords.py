import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Streamlit app title
st.title("Projectile Motion using A_Parallel and A_Perpendicular")

# Sidebar for user input
st.sidebar.header("Initial Conditions")
x_i = 0  # Initial X-position (fixed)
y_i = st.sidebar.slider("Initial Y-position (m)", 0, 100, 0)
V_i = st.sidebar.slider("Initial Velocity (m/s)", 10, 150, 100)
theta = st.sidebar.slider("Launch Angle (degrees)", 0, 90, 45)

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


# Counteracting force due to air resistance
counterForce_i = air_resist_force(air_resist_const, V_i, air_resist_type)


g = 9.81

Ai_perp = -g * np.cos(theta_rad)
Ai_para = -counterForce_i - (g * np.sin(theta_rad))


# Data lists
x_data, y_data = [x_i], [y_i]
V_data = [V_i]
A_perp_data, A_para_data = [Ai_perp], [Ai_para]
theta_data = [theta_rad]



circle_radius_i = V_i**2 / Ai_perp
circle_radius_data = [circle_radius_i]


circle_position_Xi = x_i + circle_radius_i * np.sin(theta_rad)
circle_position_Yi = y_i - circle_radius_i * np.cos(theta_rad)
circle_position_x_data = [circle_position_Xi]
circle_position_y_data = [circle_position_Yi]


time_data = [0]

time_interval = 0.01  # Time step*
i, y_new = 0, 1  # Iteration counter

# Simulation loop
while y_new >= 0:

    #Velocity and Acceleration Calculations
    V_new = V_data[i] + A_para_data[i] * time_interval
    V_data.append(V_new)

    A_para_new = -1 * air_resist_force(air_resist_const, V_new, air_resist_type) - g * np.sin(theta_data[i])
    A_para_data.append(A_para_new)

    A_perp_new = -g * np.cos(theta_data[i])
    A_perp_data.append(A_perp_new)


    #Inscribed Circle Data/Calculations
    delta_S_new = V_data[i] * time_interval + 0.5 * A_para_data[i] * time_interval ** 2

    epsilon = 1e-6
    circle_radius_new = V_data[i] ** 2 / (abs(A_perp_data[i]) + epsilon)
    circle_radius_data.append(circle_radius_new)


    circle_position_x_new = x_data[i] + circle_radius_new * np.sin(theta_data[i])
    circle_position_y_new = y_data[i] - circle_radius_new * np.cos(theta_data[i])

    circle_position_x_data.append(circle_position_x_new)
    circle_position_y_data.append(circle_position_y_new)


    delta_a_new = delta_S_new / circle_radius_new


    #Theta Data
    theta_new = theta_data[i] - delta_a_new
    theta_data.append(theta_new)


    #Position Data
    x_new = x_data[i] + delta_S_new * np.cos(theta_new)
    y_new = y_data[i] + delta_S_new * np.sin(theta_new)

    x_data.append(x_new)
    y_data.append(y_new)

    if i % 10 == 0:  # Print every 10 iterations
        print(f"Iteration {i}: x={x_new}, y={y_new}, V={V_new}, theta={theta_new*180/np.pi}, delta_a={delta_a_new}")

    time_data.append((i + 1) * time_interval)

    i += 1

# Plot results using Streamlit

st.subheader("Y vs X (Projectile Path)")
fig1, ax1 = plt.subplots()
ax1.plot(x_data, y_data, label="Projectile Path", color="blue")


ax1.axhline(0, color="black")  # Ground level
if max(x_data) < 800:
    ax1.set_xlim(-20, 800)
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
ax2.plot(time_data, V_data, label="Velocity", color="blue")
ax2.axhline(0, color="black")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Velocity (m/s)")
ax2.legend()
st.pyplot(fig2)


st.subheader("Acceleration vs Time")
fig3, ax3 = plt.subplots()
ax3.plot(time_data, A_perp_data, label="A_perp", color="blue")
ax3.plot(time_data, A_para_data, label="A_para", color="red")
ax3.plot(time_data, np.sqrt(A_perp_data**2 + A_para_data**2), label="sqrt(A_perp^2 + A_para^2)", color="purple")
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
