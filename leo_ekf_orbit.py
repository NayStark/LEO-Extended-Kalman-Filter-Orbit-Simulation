from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import scipy.stats as stats
from tqdm import tqdm

sigma_meas = 0.1
R = np.eye(3) * sigma_meas**2
Q = np.eye(6) * 8.75e-14

mu = 398600.0
R_earth = 6378.0
h = 500.0
r0 = R_earth + h
v0 = np.sqrt(mu / r0)
incl = np.deg2rad(45)

N_TRIALS = 500
T_orbit = 2 * np.pi * np.sqrt(r0**3 / mu)
t_eval = np.linspace(0, T_orbit, 200)
dt_array = np.diff(t_eval)

def two_body(t, x):
    r = np.linalg.norm(x[:3])
    ax, ay, az = -mu*x[0]/r**3, -mu*x[1]/r**3, -mu*x[2]/r**3
    return [x[3], x[4], x[5], ax, ay, az]

def fx_jacobian(x, dt):
    r = np.linalg.norm(x[:3])
    Fx = np.eye(6)
    Fx[0:3, 3:6] = np.eye(3) * dt
    mu_r5 = mu / r**5
    Fx[3:6,0:3] = dt * np.array([
        [3*x[0]**2 - r**2, 3*x[0]*x[1], 3*x[0]*x[2]],
        [3*x[1]*x[0], 3*x[1]**2 - r**2, 3*x[1]*x[2]],
        [3*x[2]*x[0], 3*x[2]*x[1], 3*x[2]**2 - r**2]
    ]) * mu_r5
    return Fx

def run_trial():
    # True State Init
    X0 = [r0, 0, 0, 0, v0*np.cos(incl), v0*np.sin(incl)]
    sol = solve_ivp(two_body, (0, T_orbit), X0, t_eval=t_eval, rtol=1e-9, atol=1e-12)
    X_true = sol.y
    Z = X_true[:3, :] + np.random.randn(3, X_true.shape[1]) * sigma_meas

    # EKF Init
    X_est = np.zeros_like(X_true)
    X_est[:, 0] = X_true[:, 0] + np.random.randn(6) * 5.0
    P = np.eye(6) * (5.0**2)
    
    errors, nees_vals, nis_vals = np.zeros((6, len(t_eval))), np.zeros(len(t_eval)), np.zeros(len(t_eval))
    H = np.hstack((np.eye(3), np.zeros((3,3))))
    
    for k in range(1, len(t_eval)):
        dt = dt_array[k-1]
        
        # Predict
        sol_pred = solve_ivp(two_body, [0, dt], X_est[:, k-1], t_eval=[dt], rtol=1e-9, atol=1e-12)
        x_pred = sol_pred.y[:, -1]
        Fx = fx_jacobian(X_est[:, k-1], dt)
        P = Fx @ P @ Fx.T + Q
        
        # Update
        y = Z[:, k] - H @ x_pred
        S = H @ P @ H.T + R
        K = P @ H.T @ np.linalg.inv(S)
        
        X_est[:, k] = x_pred + K @ y
        
        # Joseph Form Update
        I_KH = np.eye(6) - K @ H
        P = I_KH @ P @ I_KH.T + K @ R @ K.T
        P = (P + P.T) / 2
        
        # Metrics
        err = X_true[:, k] - X_est[:, k]
        errors[:, k] = err
        nees_vals[k] = err.T @ np.linalg.solve(P, err)
        nis_vals[k] = y.T @ np.linalg.inv(S) @ y
        
    return X_true, X_est, errors, nees_vals, nis_vals

all_errors, all_nees, all_nis = [], [], []
final_X_true = None
final_X_est = None
print(f"Running Monte Carlo...")
for _ in tqdm(range(N_TRIALS)):
    X_true, X_est,err, nees, nis = run_trial()
    final_X_true = X_true
    final_X_est = X_est
    all_errors.append(err)
    all_nees.append(nees)
    all_nis.append(nis)

y_flat = np.array(all_nis).flatten() # Use the 'y' values from the run_trial
plt.figure(figsize=(8, 4))
plt.acorr(y_flat - np.mean(y_flat), maxlags=50)
plt.title("Innovation Autocorrelation (Whitening Test)")
plt.xlabel("Lag"); plt.ylabel("Correlation")
plt.grid(True)
plt.show()

# Aggregation
avg_errors = np.mean(np.array(all_errors)**2, axis=0)
rmse = np.sqrt(np.sum(avg_errors[:3, :], axis=0))
mean_nees = np.mean(np.array(all_nees), axis=0)
mean_nis = np.mean(np.array(all_nis), axis=0)

# Confidence Bounds
alpha = 0.05
lower_nees = stats.chi2.ppf(alpha/2, N_TRIALS * 6) / N_TRIALS
upper_nees = stats.chi2.ppf(1 - alpha/2, N_TRIALS * 6) / N_TRIALS
lower_nis = stats.chi2.ppf(alpha/2, N_TRIALS * 3) / N_TRIALS
upper_nis = stats.chi2.ppf(1 - alpha/2, N_TRIALS * 3) / N_TRIALS

all_errors_m = np.array(all_errors) * 1000

avg_errors_m = np.mean(all_errors_m**2, axis=0)
rmse_m = np.sqrt(np.sum(avg_errors_m[:3, :], axis=0))

final_errors_norm_m = np.linalg.norm(all_errors_m[:3, -1, :], axis=0)
sep_50_m = np.percentile(final_errors_norm_m, 50)
sep_95_m = np.percentile(final_errors_norm_m, 95)

print(f"--- Accuracy Metrics ---")
print(f"50% of trials are within: {sep_50_m:.3f} m")
print(f"95% of trials are within: {sep_95_m:.3f} m")

def get_convergence_time(rmse_array, t_array, threshold_m=30.0, buffer=5):
    """
    Finds the first time step where RMSE drops below threshold and stays there.
    threshold_m: Convergence limit in meters (e.g., 30 meters)
    buffer: Number of consecutive steps to ensure stability
    """
    # Find all indices where rmse is below threshold
    below_thresh = np.where(rmse_m < threshold_m)[0]
    
    if len(below_thresh) == 0:
        return None
        
    # Check for consecutive stability
    for idx in below_thresh:
        if np.all(rmse_m[idx : idx + buffer] < threshold_m):
            return t_array[idx] / 60 # Return in minutes
            
    return None

conv_time = get_convergence_time(rmse_m, t_eval)
print(f"Filter converged (to < 30m) at: {conv_time:.2f} minutes")

# Plotting
fig, axes = plt.subplots(3, 1, figsize=(10, 12))
axes[0].plot(t_eval/60, rmse, 'k'); axes[0].set_title("Position RMSE"); axes[0].set_ylabel("km")
axes[1].plot(t_eval/60, mean_nees, 'b', label='Mean NEES'); axes[1].axhline(6, color='k', linestyle='-'); axes[1].axhline(upper_nees, color='r', linestyle='--'); axes[1].axhline(lower_nees, color='r', linestyle='--'); axes[1].set_title("NEES (Consistency)"); axes[1].set_ylabel("NEES")
axes[2].plot(t_eval/60, mean_nis, 'g', label='Mean NIS'); axes[2].axhline(3, color='k', linestyle='-'); axes[2].axhline(upper_nis, color='r', linestyle='--'); axes[2].axhline(lower_nis, color='r', linestyle='--'); axes[2].set_title("NIS (Residuals)"); axes[2].set_ylabel("NIS"); axes[2].set_xlabel("Time [min]")
for ax in axes: ax.grid(True, alpha=0.5)
plt.tight_layout();plt.show()

# Animation of the last trial
print("Generating Animation...")

fig_ani = plt.figure(figsize=(6,6))
ax_ani = fig_ani.add_subplot(111, projection='3d')

def update(i):
    ax_ani.clear()
    ax_ani.plot(final_X_true[0,:i], final_X_true[1,:i], final_X_true[2,:i], 'b-', label='True Orbit')
    ax_ani.plot(final_X_est[0,:i], final_X_est[1,:i], final_X_est[2,:i], 'r--', label='EKF Estimate')
    
    ax_ani.scatter(0, 0, 0, color='k', s=40)
    
    ax_ani.set_xlabel('x [km]'); ax_ani.set_ylabel('y [km]'); ax_ani.set_zlabel('z [km]')
    ax_ani.set_title(f'LEO Orbit Estimation')
    ax_ani.legend(loc='upper right')
    
    ax_ani.view_init(30, i/2)
    ax_ani.set_box_aspect([1,1,1])
    
    max_val = np.max(np.abs(final_X_true[:3,:]))
    ax_ani.set_xlim([-max_val, max_val])
    ax_ani.set_ylim([-max_val, max_val])
    ax_ani.set_zlim([-max_val, max_val])

ani = FuncAnimation(fig_ani, update, frames=final_X_true.shape[1], interval=20)

ani.save("output/LEO_EKF_MonteCarlo.gif", writer=PillowWriter(fps=20))

# plt.show()

ss_start_idx = 178 

all_errors_ss = np.array(all_errors)[:, :, ss_start_idx:] 
all_errors_m_ss = all_errors_ss * 1000
radial_errors_ss = np.linalg.norm(all_errors_m_ss[:, :3, :], axis=1).flatten()

sep_50 = np.percentile(radial_errors_ss, 50)
sep_95 = np.percentile(radial_errors_ss, 95)

print(f"--- Refined Steady-State Performance (Final 10 min) ---")
print(f"95% of steady-state samples are within: {sep_95:.3f} m")

final_slice = slice(-33, None) 

plt.figure(figsize=(8, 4))
plt.plot(t_eval[final_slice]/60, rmse[final_slice], 'k')
plt.title("RMSE Jitter Check (Final 15 Minutes)")
plt.ylabel("RMSE [m]")
plt.grid(True)
plt.show()