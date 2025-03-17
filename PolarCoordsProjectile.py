import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

# Streamlit app title
st.title("Projectile Motion using A_Parallel and A_Perpendicular")

# Sidebar for user input
st.sidebar.header("Initial Conditions")
x_i = 0  # Initial X-position (fixed)
y_i = st.sidebar.slider("Initial Y-position (m)", 0, 100, 0)
V_i = st.sidebar.slider("Initial Velocity (m/s)", 10, 150, 100)
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

    if theta != 90:
        A_perp_new = -g * np.cos(theta_data[i])
    else:
        A_perp_new = 0

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
    if theta != 90:
        x_new = x_data[i] + delta_S_new * np.cos(theta_new)
    else:
        x_new = 0
    y_new = y_data[i] + delta_S_new * np.sin(theta_new)

    x_data.append(x_new)
    y_data.append(y_new)

    #if i % 10 ==0:
        #print(f"Iteration {i}: x={x_new}")

    time_data.append((i + 1) * time_interval)

    i += 1

# Plot results using Streamlit

st.subheader("Y vs X (Projectile Path)")
fig1, ax1 = plt.subplots()

# Initialize session state variables if they don’t exist
if "plot_toggle" not in st.session_state:
    st.session_state.plot_toggle = True
if "scatter_toggle" not in st.session_state:
    st.session_state.scatter_toggle = False
if "circles_toggle" not in st.session_state:
    st.session_state.circles_toggle = False

# Define button logic to toggle states
if st.button("Toggle Trajectory"):
    st.session_state.plot_toggle = not st.session_state.plot_toggle

if st.button("Toggle Key Points"):
    st.session_state.scatter_toggle = not st.session_state.scatter_toggle

if st.button("Toggle Circles"):
    st.session_state.circles_toggle = not st.session_state.circles_toggle

if st.session_state.plot_toggle:
    ax1.plot(x_data, y_data, label="Projectile Path", color="blue")

# Choose specific time steps for markers and circles
time_steps = np.arange(0, max(time_data), 3)  # Every 1.5 seconds
indices = [np.argmin(np.abs(np.array(time_data) - t)) for t in time_steps]  # Find the closest indices
indices[0] = 1
# Plot key points if toggled on
if st.session_state.scatter_toggle:
    ax1.scatter([x_data[i] for i in indices], [y_data[i] for i in indices], color='black', label="Key Points")

# Plot circles if toggled on
if st.session_state.circles_toggle:
    for i in indices:
        circle_data = Circle((circle_position_x_data[i], circle_position_y_data[i]), circle_radius_data[i], fill = False, edgecolor = 'red', linewidth = 2, alpha = 0.5)
        ax1.add_patch(circle_data)

    ax1.set_aspect('equal', adjustable='datalim')  # Prevents circles from being distorted

ax1.axhline(0, color="black")  # Ground level


if max(x_data) < 500:
    ax1.set_xlim(-20, 500)
    ax1.set_ylim(0, 800)

elif max(x_data) < 1000:
    ax1.set_xlim(-100, 1000)
    ax1.set_ylim(0, 1000)
else:
    ax1.set_xlim(-100, 2500)
    ax1.set_ylim(0, 1600)


ax1.set_xlabel("X-axis (m)")
ax1.set_ylabel("Y-axis (m)")
ax1.legend()
st.pyplot(fig1)


st.subheader("Velocity vs Time")
fig2, ax2 = plt.subplots()
ax2.plot(time_data, V_data, label="Total Speed", color="purple")
#ax2.plot(time_data, V_data*np.sin(theta_data), label="Y Velocity", color="blue")
#ax2.plot(time_data, V_data*np.cos(theta_data), label="X Velocity", color="red")
ax2.axhline(0, color="black")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Velocity (m/s)")
ax2.legend()
st.pyplot(fig2)


st.subheader("Acceleration vs Time")
fig3, ax3 = plt.subplots()
ax3.plot(time_data, A_perp_data, label="A_perp", color="blue")
ax3.plot(time_data, A_para_data, label="A_para", color="red")

#combine_acceleration = []
#for i in range(len(A_para_data)):
    #ombine_acceleration.append(np.sqrt(A_para_data[i]**2 + A_perp_data[i]**2))

#ax3.plot(time_data, combine_acceleration, label="Combined", color="purple")

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
