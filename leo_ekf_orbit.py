import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.integrate import solve_ivp


mu = 398600.0      # gravitational parameter (km^3/s^2)
R_earth = 6378.0   # Earth radius (km)
h = 500.0          # altitude (km)
r0 = R_earth + h
v0 = np.sqrt(mu / r0)
incl = np.deg2rad(45)

# Initial 3D state [x, y, z, vx, vy, vz]
X0 = [r0, 0, 0, 0, v0*np.cos(incl), v0*np.sin(incl)]

# Two-body Dynamics Function
def two_body(t, x):
    r = np.linalg.norm(x[:3])
    ax, ay, az = -mu*x[0]/r**3, -mu*x[1]/r**3, -mu*x[2]/r**3
    return [x[3], x[4], x[5], ax, ay, az]

# True Orbit with RK45
T_orbit = 2*np.pi*np.sqrt(r0**3/mu)
t_span = (0, T_orbit)
n_steps = 1000
t_eval = np.linspace(0, T_orbit, n_steps)

sol = solve_ivp(two_body, t_span, X0, method='RK45', t_eval=t_eval, rtol=1e-9, atol=1e-12)
X_true = sol.y  # shape: (6, n_steps)

# Generating Simulated Noisy Measurements
sigma_meas = 10.0
Z = X_true[:3, :] + np.random.randn(3, X_true.shape[1]) * sigma_meas

# EKF Stuff + Loop
X_est = np.zeros_like(X_true)
X_est[:,0] = X_true[:,0] + np.random.randn(6)*5.0
P = np.eye(6) * 1e2
Q = np.eye(6) * 1e-3
R = np.eye(3) * sigma_meas**2
dt_array = np.diff(t_eval)

def fx_jacobian(x, dt):
    r = np.linalg.norm(x[:3])
    Fx = np.eye(6)
    Fx[0:3, 3:6] = np.eye(3) * dt
    mu_r5 = mu / r**5
    Fx[3:6,0:3] = dt * np.array([
        [3*x[0]**2 - r**2, 3*x[0]*x[1], 3*x[0]*x[2]],
        [3*x[1]*x[0], 3*x[1]**2 - r**2, 3*x[1]*x[2]],
        [3*x[2]*x[0], 3*x[2]*x[1], 3*x[2]**2 - r**2]
    ]) * -mu_r5
    return Fx

for k in range(1, X_true.shape[1]):
    dt = dt_array[k-1]
    
    # RK45 prediction
    sol_pred = solve_ivp(two_body, [0, dt], X_est[:,k-1], method='RK45', rtol=1e-9, atol=1e-12)
    x_pred = sol_pred.y[:, -1]
    
    # Covariance Propagation
    Fx = fx_jacobian(X_est[:, k-1], dt)
    P = Fx @ P @ Fx.T + Q
    
    # Measurement Update
    z = Z[:, k]
    H = np.hstack((np.eye(3), np.zeros((3,3))))
    y = z - H @ x_pred
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)
    X_est[:, k] = x_pred + K @ y
    P = (np.eye(6) - K @ H) @ P


# Plots
fig = plt.figure(figsize=(12,5))

# 3D Orbit Plot
ax1 = fig.add_subplot(121, projection='3d')
ax1.plot(X_true[0], X_true[1], X_true[2], 'b', label='True Orbit')
ax1.plot(X_est[0], X_est[1], X_est[2], 'r--', label='EKF Estimate')
ax1.scatter(0,0,0,c='k',s=40,label='Earth Center')
ax1.set_title("True vs EKF Orbit")
ax1.set_box_aspect([1,1,1])
ax1.set_xlabel("x [km]"); ax1.set_ylabel("y [km]"); ax1.set_zlabel("z [km]")
ax1.legend(); ax1.grid(True)

# Error Plot
ax2 = fig.add_subplot(122)
err = np.linalg.norm(X_true[:3] - X_est[:3], axis=0)
ax2.plot(t_eval/60, err, 'k')
ax2.set_title("EKF Position Error Over Time")
ax2.set_xlabel("Time [min]"); ax2.set_ylabel("Error [km]")
ax2.grid(True)
plt.tight_layout()
plt.show()


# 3D Animation GIF

# desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# GIF ,path
# gif_path = os.path.join(desktop_path, "LEO_EKF_RK45_Orbit.gif")
# fig2 = plt.figure(figsize=(6,6))
# ax3 = fig2.add_subplot(111, projection='3d')

# line_true, = ax3.plot([], [], [], 'b-', label='True Orbit')
# line_ekf, = ax3.plot([], [], [], 'r--', label='EKF Estimate')
# earth_marker = ax3.scatter(0, 0, 0, color='k', s=30)

# ax3.legend(loc='upper right')  # always visible

# def update(i):
    # ax3.clear()
    # ax3.plot(X_true[0,:i], X_true[1,:i], X_true[2,:i], 'b-', label='True Orbit')
    # ax3.plot(X_est[0,:i], X_est[1,:i], X_est[2,:i], 'r--', label='EKF Estimate')
    # ax3.scatter(0,0,0, color='k', s=40)
    # ax3.legend(loc='upper right')
    # ax3.set_xlabel('x [km]'); ax3.set_ylabel('y [km]'); ax3.set_zlabel('z [km]')
    # ax3.set_title('LEO Orbit Estimation (Full Orbit)')
    # ax3.view_init(30, i/2)
    # ax3.set_box_aspect([1,1,1])
    # return ax3

# ani = FuncAnimation(fig2, update, frames=X_true.shape[1], interval=20)
# ani.save(gif_path, writer=PillowWriter(fps=20))
# print("✅ Saved full closed orbit animation as LEO_EKF_RK45_Orbit.gif")
