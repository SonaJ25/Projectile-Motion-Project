## Project 1, projectile motion simulation

#Install packages
import matplotlib.pyplot as plt  #Graph Plotting
import numpy as np               #Python Math (Trig)
import vpython as vp             #Simulation

########################################################################################################################

# Initial data values
x_i = 0          #Initial X-position
y_i = 0          #Initial Y-position
if y_i < 0:
    print('Initial Y position must be positive or zero')
    exit()

V_i = 150       #Initial Velocity
theta = 80      #Initial Launch Angle (0 to 90 deg)
if theta < 0 or theta > 90:
    print('choose a theta value between 0 and 90')
    exit()
theta_rad = theta * (np.pi / 180)   #Convert deg to radians for calculations

########################################################################################################################

#Optional Air Resistance

air_resist_const = 0.2          #Define the air resistance constant

air_resist_type = 1              #Linear (1) or Quadratic (2) wind resistance


def air_resist_force(const, v, n):
    return const * (v**n)

########################################################################################################################


#Initial Velocity/Acceleration Calculations
Vx_initial = float(V_i * np.cos(theta_rad))
Vy_initial = float(V_i * np.sin(theta_rad))

counterForce = float(air_resist_force(air_resist_const, V_i, air_resist_type))
Ax_initial = float(counterForce * np.cos(theta_rad))
Ay_initial = float(counterForce * np.sin(theta_rad))


#Setting up data arrays and variables for the projectile motion simulation
x_data = list([x_i])
y_data = list([y_i])
V_tot_data = list([V_i])
Vx_data = list([Vx_initial])
Vy_data = list([Vy_initial])
Ax_data = list([-1 * Ax_initial])
Ay_data = list([-1 * Ay_initial - 9.81])
time_data = list([0])

time_interval = 0.01     #Time interval between iterations (delta-T)



########################################################################################################################

i = 0                    #Iteration Counter

new_y = 1                #Allows for while loop condition to start
while new_y >= 0:        #Loop will continue until a "New-y" value falls below ground level (y=0)

    new_y = float(y_data[i] + (Vy_data[i] * time_interval) + (0.5 * Ay_data[i] * time_interval**2))
    y_data.append(new_y)

    new_Vy = float(Vy_data[i] + (Ay_data[i] * time_interval))
    Vy_data.append(new_Vy)


    new_x = float(x_data[i] + (Vx_data[i] * time_interval) + (0.5 * Ax_data[i]) * time_interval**2)
    x_data.append(new_x)

    new_Vx = float(Vx_data[i] + (Ax_data[i] * time_interval))
    Vx_data.append(new_Vx)


    V_tot = np.sqrt(Vx_data[i]**2 + Vy_data[i]**2)
    V_tot_data.append(V_tot)
    counterForce = float(air_resist_force(air_resist_const, V_tot, air_resist_type))

    new_theta = np.arctan(new_Vy/new_Vx)


    new_Ay = (-1 * counterForce * np.sin(new_theta)) - 9.81
    Ay_data.append(new_Ay)

    new_Ax = -1 * counterForce * np.cos(new_theta)
    Ax_data.append(new_Ax)


    time_data.append((i + 1)*time_interval)

    i += 1

########################################################################################################################

# Create the 3D scene
scene = vp.canvas(title="Projectile Motion Simulation")
scene.width = 800
scene.height = 600

z_data = [0] * len(x_data)
scene.camera.pos = vp.vector(max(x_data)/2, max(y_data)/2, 1250)  # Position the camera
scene.camera.axis = vp.vector(0, 0, -1250)



#Creating the moving cyan sphere
moving_sphere = vp.sphere(pos=vp.vector(x_data[0], y_data[0], z_data[0]), radius=10, color=vp.color.cyan)


#Animating the cyan sphere, and leaving a trail of red dots
for i in range(len(x_data)):
    vp.rate(120)

    moving_sphere.pos = vp.vector(x_data[i], y_data[i], z_data[i])           #Updating the cyan sphere position

    if i % 100 == 0:                        #Creating a red sphere every "second" of the simulation
        trail_sphere = vp.sphere(pos=moving_sphere.pos, radius=6, color=vp.color.red)

        velocity_vector = vp.vector(Vx_data[i], Vy_data[i], 0)
        velocity_arrow = vp.arrow(pos=moving_sphere.pos, axis=velocity_vector*0.5, color=vp.color.green)

        acceleration_vector = vp.vector(Ax_data[i], Ay_data[i], 0)
        acceleration_arrow = vp.arrow(pos=moving_sphere.pos, axis=acceleration_vector*5, color=vp.color.yellow)
########################################################################################################################
#Additional Data Plots


#Y vs X plot
plt.plot(x_data, y_data, label='Y vs X', color='blue')
plt.axhline(0, color='black')  # Horizontal line
plt.axvline(0, color='black')  # Vertical line

plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Y vs X")
plt.legend()

plt.show()


#Acceleration vs Time plots
plt.plot(time_data, Ax_data, label='Ax data', color='blue')
plt.plot(time_data, Ay_data, label='Ay data', color='red')
plt.axhline(0, color='black')  # Horizontal line
plt.axvline(0, color='black')  # Vertical line

plt.xlabel("Time")
plt.ylabel("Acceleration")
plt.title("Acceleration vs Time")
plt.legend()

plt.show()

#Veloctiy vs Time plots
plt.plot(time_data, Vx_data, label='Vx data', color='blue')
plt.plot(time_data, Vy_data, label='Vy data', color='red')
plt.axhline(0, color='black')  # Horizontal line
plt.axvline(0, color='black')  # Vertical line

plt.xlabel("Time")
plt.ylabel("Velocity")
plt.title("Velocity vs Time")
plt.legend()

plt.show()


#Position vs time plots
plt.plot(time_data, x_data, label='x data', color='blue')
plt.plot(time_data, y_data, label='y data', color='red')
plt.axhline(0, color='black')  # Horizontal line
plt.axvline(0, color='black')  # Vertical line

plt.xlabel("Time")
plt.ylabel("Position")
plt.title("Position vs Time")
plt.legend()

plt.show()

