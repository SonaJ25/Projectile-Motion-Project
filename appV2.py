import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time  # To control animation speed

# Streamlit app title
st.title("Real-Time Projectile Motion Simulation")

# Sidebar for user input
st.sidebar.header("Initial Conditions")
x_i = 0  # Initial X-position (fixed)
y_i = st.sidebar.slider("Initial Y-position (m)", 0, 100, 0)
V_i = st.sidebar.slider("Initial Velocity (m/s)", 0, 150, 100)
theta = st.sidebar.slider("Launch Angle (degrees)", 0, 90, 60)

# Air resistance settings
st.sidebar.header("Air Resistance")
air_resist_const = st.sidebar.slider("Air Resistance Constant", 0.0, 0.2, 0.0)

# Convert angle to radians
theta_rad = np.radians(theta)

# Define air resistance function
def air_resist_force(const, v):
    return const * v  # Assuming linear air resistance

# Initial velocity components
Vx, Vy = V_i * np.cos(theta_rad), V_i * np.sin(theta_rad)
Ax, Ay = -air_resist_force(air_resist_const, V_i) * np.cos(theta_rad), -9.81 - air_resist_force(air_resist_const, V_i) * np.sin(theta_rad)

# Time step
time_interval = 0.01
x, y, t = x_i, y_i, 0

# Create an empty plot container
plot_container = st.empty()

# **Real-Time Simulation Loop**
trajectory_x, trajectory_y = [], []  # To store path

while y >= 0:
    # Update position using kinematic equations
    x += Vx * time_interval + 0.5 * Ax * time_interval**2
    y += Vy * time_interval + 0.5 * Ay * time_interval**2

    # Update velocity
    Vx += Ax * time_interval
    Vy += Ay * time_interval

    # Update air resistance force
    V_tot = np.sqrt(Vx**2 + Vy**2)
    counterForce = air_resist_force(air_resist_const, V_tot)
    Ax = -counterForce * np.cos(theta_rad)
    Ay = -9.81 - counterForce * np.sin(theta_rad)

    # Store trajectory for plotting
    trajectory_x.append(x)
    trajectory_y.append(y)

    # **Real-time update of 3D plot**
    fig = go.Figure()

    # Plot full trajectory
    fig.add_trace(go.Scatter3d(x=trajectory_x, y=trajectory_y, z=[0] * len(trajectory_x),
                                mode="lines", line=dict(color="blue"), name="Path"))

    # Plot moving projectile
    fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[0], mode="markers",
                                marker=dict(color="red", size=6), name="Projectile"))

    # Set plot layout
    fig.update_layout(title="Real-Time 3D Projectile Motion",
                      scene=dict(xaxis_title="X Position (m)",
                                 yaxis_title="Y Position (m)",
                                 zaxis_title="Z Position (m)"),
                      margin=dict(l=0, r=0, b=0, t=40))

    # Update the Streamlit container
    plot_container.plotly_chart(fig)

    # Slow down the loop for real-time effect
    time.sleep(0.0001)

st.success("Simulation complete! 🎯")
