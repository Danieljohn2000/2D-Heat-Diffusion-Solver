import numpy as np
import matplotlib.pyplot as plt

# 1. CREATE THE COMPUTATIONAL GRID

nx = 50
ny = 50

width = 1.0
height = 1.0

dx = width / (nx - 1)
dy = height / (ny - 1)

# 2. PHYSICAL PARAMETERS

alpha = 0.01  # Thermal diffusivity
total_time = 2.0  # Total simulation time
dt = 0.001  # Time step

num_steps = int(total_time / dt)

# 3. CREATE TEMPERATURE FIELD

temperature = np.zeros((ny, nx))

# 4. INITIAL CONDITIONS

# Create a hot region in the center
temperature[20:30, 20:30] = 100.0

# 5. APPLY BOUNDARY CONDITIONS

temperature[:, 0] = 0
temperature[:, -1] = 0
temperature[0, :] = 0
temperature[-1, :] = 0

# 6. CHECK STABILITY

stability_limit = dx**2 * dy**2 / (2 * alpha * (dx**2 + dy**2))

if dt > stability_limit:
    raise ValueError(f"Time step is too large. " f"Use dt <= {stability_limit:.6f}")


# 7. TIME LOOP

for step in range(num_steps):

    new_temperature = temperature.copy()

    for j in range(1, ny - 1):

        for i in range(1, nx - 1):

            d2T_dx2 = (
                temperature[j, i + 1] - 2 * temperature[j, i] + temperature[j, i - 1]
            ) / dx**2

            d2T_dy2 = (
                temperature[j + 1, i] - 2 * temperature[j, i] + temperature[j - 1, i]
            ) / dy**2

            new_temperature[j, i] = temperature[j, i] + alpha * dt * (d2T_dx2 + d2T_dy2)

    temperature = new_temperature


# 8. DISPLAY FINAL TEMPERATURE FIELD

plt.figure(figsize=(8, 6))

plt.imshow(temperature, origin="lower", extent=[0, width, 0, height], cmap="hot")

plt.colorbar(label="Temperature")

plt.xlabel("x position")
plt.ylabel("y position")

plt.title("2D Heat Diffusion Simulation")

plt.tight_layout()

plt.savefig("temperature_distribution.png", dpi=300)

plt.show()
