## Projectile Motion Simulation using Cartesian coordinates

#Import python packages for extended functionality
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

#################################################################################################################
## Initial Conditions/Setup

# Streamlit app title
st.title("Projectile Motion Simulation")

# Sidebar for user input Initial Conditions
st.sidebar.header("Initial Conditions")
x_i = 0  # Initial X-position (fixed)
y_i = st.sidebar.slider("Initial Y-position (m)", 0, 100, 0)
V_i = st.sidebar.slider("Initial Velocity (m/s)", 0, 150, 100)
theta = st.sidebar.slider("Launch Angle (degrees)", 0, 90, 60)

# Air resistance
st.sidebar.header("Air Resistance")
air_resist_const = st.sidebar.slider("Air Resistance Constant", 0.0, 0.2, 0.0)
air_resist_type = 1

#################################################################################################################
## Calculating initial values

g = 9.81


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

Ay_initial = counterForce_i * np.sin(theta_rad) + g

#################################################################################################################

# Data lists
x_data, y_data = [x_i], [y_i]
Vx_data, Vy_data = [Vx_initial], [Vy_initial]
Ax_data, Ay_data = [-Ax_initial], [-Ay_initial]
time_data = [0]

time_interval = 0.01  # Time step
i, new_y = 0, 1  # Iteration counter


#################################################################################################################
# Simulation loop
while new_y >= 0:
    new_y = y_data[i] + Vy_data[i] * time_interval + 0.5 * Ay_data[i] * time_interval**2  #Y position
    y_data.append(new_y)

    new_Vy = Vy_data[i] + Ay_data[i] * time_interval     #Y component of Velocity
    Vy_data.append(new_Vy)

    new_x = x_data[i] + Vx_data[i] * time_interval + 0.5 * Ax_data[i] * time_interval**2   #X position
    x_data.append(new_x)

    new_Vx = Vx_data[i] + Ax_data[i] * time_interval     #X component of Velocity
    Vx_data.append(new_Vx)                                    

    V_tot = np.sqrt(Vx_data[i]**2 + Vy_data[i]**2)      #Total Speed
    counterForce = air_resist_force(air_resist_const, V_tot, air_resist_type)

    if new_Vx < 1e-6:      #Avoid Divide by zero error
        if new_Vy > 0:
            new_theta = np.pi/2
        else:
            new_theta = -np.pi/2

    else:
        new_theta = np.arctan(new_Vy / new_Vx)
    new_Ay = -counterForce * np.sin(new_theta) - g
    Ay_data.append(new_Ay)

    new_Ax = -counterForce * np.cos(new_theta)
    Ax_data.append(new_Ax)
    
    #Time data
    time_data.append((i + 1) * time_interval)

    i += 1 #Iteration counter


#################################################################################################################
# Plot results using Streamlit


# Trajectory Plot
st.subheader("Y vs X (Projectile Path)")
fig1, ax1 = plt.subplots()

# Toggle buttons for data elements in trajectory plot
if "plot_toggle" not in st.session_state:
    st.session_state.plot_toggle = True
if "scatter_toggle" not in st.session_state:
    st.session_state.scatter_toggle = False
if "vectors_toggle" not in st.session_state:
    st.session_state.vectors_toggle = False

if st.button("Toggle Trajectory"):
    st.session_state.plot_toggle = not st.session_state.plot_toggle

if st.button("Toggle Key Points"):
    st.session_state.scatter_toggle = not st.session_state.scatter_toggle

if st.button("Toggle Vectors"):
    st.session_state.vectors_toggle = not st.session_state.vectors_toggle



# Plot trajectory if toggled on
if st.session_state.plot_toggle:
    ax1.plot(x_data, y_data, label="Projectile Path", color="blue")

# Choose specific time steps for markers and vectors
time_steps = np.arange(0, max(time_data), 1.5)  # Every 0.75 seconds
indices = [np.argmin(np.abs(np.array(time_data) - t)) for t in time_steps]  # Find closest indices

# Plot key points if toggled on
if st.session_state.scatter_toggle:
    ax1.scatter([x_data[i] for i in indices], [y_data[i] for i in indices], color='black', label="Key Points")

# Plot velocity and acceleration vectors if toggled on

#Velocity Vector
if st.session_state.vectors_toggle:
    ax1.quiver(
        [x_data[i] for i in indices], [y_data[i] for i in indices],  # Starting points
        [10 * Vx_data[i] for i in indices], [10 * Vy_data[i] for i in indices],  # Vector components
        color="green", angles="xy", scale_units="xy", scale=10, width=0.005, label="Velocity"
    )
    
    #Accleleration vector
    ax1.quiver(
        [x_data[i] for i in indices], [y_data[i] for i in indices],  # Starting points
        [150 * Ax_data[i] for i in indices], [150 * Ay_data[i] for i in indices],  # Vector components
        color="red", angles="xy", scale_units="xy", scale=20, width=0.005, label="Acceleration"
    )



ax1.axhline(0, color="black")  # Ground level


#Axis Scaling
if max(x_data) < 500:
    ax1.set_xlim(-20, 500)
    ax1.set_ylim(0, 800)
elif max(x_data) < 1000:
    ax1.set_xlim(-100, 1000)
    ax1.set_ylim(0, 1000)
else:
    ax1.set_xlim(-100, 2500)
    ax1.set_ylim(0, 1600)

#Graph Labels
ax1.set_xlabel("X-axis (m)")
ax1.set_ylabel("Y-axis (m)")
ax1.legend()
st.pyplot(fig1)


#################################################################################################################
# Plot 2, Speed v Time

st.subheader("Velocity vs Time")
fig2, ax2 = plt.subplots()
ax2.plot(time_data, Vx_data, label="Vx", color="blue")
ax2.plot(time_data, Vy_data, label="Vy", color="red")

total_speed = []
for i in range(len(Vx_data)):
    total_speed.append(np.sqrt(Vx_data[i]**2 + Vy_data[i]**2))

ax2.plot(time_data, total_speed, label = "Total Speed")


ax2.axhline(0, color="black") #Ground level

#Graph Labels
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Velocity (m/s)")
ax2.legend()
st.pyplot(fig2)

#################################################################################################################
# Plot 3, Acceleration v Time

st.subheader("Acceleration vs Time")
fig3, ax3 = plt.subplots()
ax3.plot(time_data, Ax_data, label="Ax", color="blue")
ax3.plot(time_data, Ay_data, label="Ay", color="red")

ax3.axhline(0, color="black") #Ground level

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

ax4.axhline(0, color="black") #Ground level

#Graph Labels
ax4.set_xlabel("Time (s)")
ax4.set_ylabel("Position (m)")
ax4.legend()
st.pyplot(fig4)
