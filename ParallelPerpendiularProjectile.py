## Projectile Motion Simulation using Polar coordinates

#Import python packages for extended functionality
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

#################################################################################################################
## Initial Conditions/Setup

# Streamlit app title
st.title("Projectile Motion using A_Parallel and A_Perpendicular")

# Sidebar for user input Initial Conditions
st.sidebar.header("Initial Conditions")
x_i = 0  # Initial X-position (fixed)
y_i = st.sidebar.slider("Initial Y-position (m)", 0, 100, 0)
V_i = st.sidebar.slider("Initial Velocity (m/s)", 10, 150, 100)
theta = st.sidebar.slider("Launch Angle (degrees)", 10, 80, 45)

# Air resistance
st.sidebar.header("Air Resistance")
air_resist_const = st.sidebar.slider("Air Resistance Constant", 0.0, 0.2, 0.0)
air_resist_type = 1
#################################################################################################################
## Calculating initial values

# Convert angle to radians
theta_rad = np.radians(theta)


# Define air resistance function
def air_resist_force(const, v, n):
    return const * (v ** n)
    
# Counteracting force due to air resistance
counterForce_i = air_resist_force(air_resist_const, V_i, air_resist_type)


#Initial acceleration values
g = 9.81

Ai_perp = -g * np.cos(theta_rad)
Ai_para = -counterForce_i - (g * np.sin(theta_rad))

#################################################################################################################
## Initializing data arrays and values for simulation

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



#################################################################################################################
## Simulation loop
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

    epsilon = 1e-6 #Avoid divide by zero error
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


    #Projectile position Data
    if theta != 90:
        x_new = x_data[i] + delta_S_new * np.cos(theta_new)
    else:
        x_new = 0
    y_new = y_data[i] + delta_S_new * np.sin(theta_new)

    x_data.append(x_new)
    y_data.append(y_new)
    
    #Time data
    time_data.append((i + 1) * time_interval)

    i += 1


#################################################################################################################
## Plot results using Streamlit

# Trajectory Plot
st.subheader("Y vs X (Projectile Path)")
fig1, ax1 = plt.subplots()

# Toggle buttons for data elements in trajectory plot
if "plot_toggle" not in st.session_state:
    st.session_state.plot_toggle = True
if "scatter_toggle" not in st.session_state:
    st.session_state.scatter_toggle = False
if "circles_toggle" not in st.session_state:
    st.session_state.circles_toggle = False
if "single_point_toggle" not in st.session_state:
    st.session_state.single_point_toggle = False


if st.button("Toggle Trajectory"):
    st.session_state.plot_toggle = not st.session_state.plot_toggle

if st.button("Toggle Key Points"):
    st.session_state.scatter_toggle = not st.session_state.scatter_toggle

if st.button("Toggle Circles"):
    st.session_state.circles_toggle = not st.session_state.circles_toggle

if st.button("Toggle Single Point Data and Circle"):
    st.session_state.single_point_toggle = not st.session_state.single_point_toggle



if st.session_state.plot_toggle:
    ax1.plot(x_data, y_data, label="Projectile Path", color="blue")

# Choose specific time steps for markers and circles
time_steps = np.arange(0, max(time_data), 2)  # Every 2 seconds
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


#Plot single point inscribed circle w/ acceleration and velocity
if st.session_state.single_point_toggle:
    if len(indices) < 6:
        point = indices[len(indices) // 2 - 1]
    else:
        point = indices[len(indices) // 2 - 2]

    #Velocity Vector
    ax1.quiver(
        [x_data[point]], [y_data[point]],  # Starting points
        [25*V_data[point]*np.cos(theta_data[point])], [25*V_data[point]*np.sin(theta_data[point])],  # Vector components
        color="green", angles="xy", scale_units="xy", scale=10, width=0.005, label="Velocity"
    )

    #A_perpendicular vector
    ax1.quiver(
        [x_data[point]], [y_data[point]],  # Starting points
        [250*A_perp_data[point]*np.sin(-theta_data[point])], [250*A_perp_data[point]*np.cos(-theta_data[point])],  # Vector components
        color="red", angles="xy", scale_units="xy", scale=20, width=0.005, label="A_Perpendicular"
    )

    #A_parallel vector
    ax1.quiver(
        [x_data[point]], [y_data[point]],  # Starting points
        [200*A_para_data[point]*np.cos(theta_data[point])], [200*A_para_data[point]*np.sin(theta_data[point])],  # Vector components
        color="blue", angles="xy", scale_units="xy", scale=20, width=0.005, label="A_Parallel"
    )

    #Plot Single circle
    ax1.add_patch(Circle((circle_position_x_data[point], circle_position_y_data[point]), circle_radius_data[point], fill=False,
        edgecolor='red', linewidth=2, alpha=0.5))

    ax1.set_aspect('equal', adjustable='datalim')  # Prevents circles from being distorted


ax1.axhline(0, color="black")  # Ground level

#Axis Scaling
if max(x_data) < 500:
    ax1.set_xlim(-20, 500)
    ax1.set_ylim(0, 500)

elif max(x_data) < 800:
    ax1.set_xlim(-100, 800)
    ax1.set_ylim(0, 600)
else:
    ax1.set_xlim(-300, 2500)
    ax1.set_ylim(0, 1600)

#Graph Labels
ax1.set_xlabel("X-axis (m)")
ax1.set_ylabel("Y-axis (m)")
ax1.legend()
st.pyplot(fig1)


#################################################################################################################
# Plot 2, Speed v Time

st.subheader("Speed vs Time")
fig2, ax2 = plt.subplots()
ax2.plot(time_data, V_data, label="Total Speed", color="purple")
ax2.axhline(0, color="black")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Speed (m/s)")
ax2.legend()
st.pyplot(fig2)

#################################################################################################################
# Plot 3, Acceleration v Time
st.subheader("Acceleration vs Time")
fig3, ax3 = plt.subplots()
ax3.plot(time_data, A_perp_data, label="A_perp", color="blue")
ax3.plot(time_data, A_para_data, label="A_para", color="red")


ax3.axhline(0, color="black") # Ground level

#Graph Labels
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Acceleration (m/s²)")
ax3.legend()
st.pyplot(fig3)

#################################################################################################################
#Plot 4, Position vs Time
st.subheader("Position vs Time")
fig4, ax4 = plt.subplots()
ax4.plot(time_data, x_data, label="X Position", color="blue")
ax4.plot(time_data, y_data, label="Y Position", color="red")
ax4.axhline(0, color="black")
ax4.set_xlabel("Time (s)")
ax4.set_ylabel("Position (m)")
ax4.legend()
st.pyplot(fig4)
