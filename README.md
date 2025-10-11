# LEO Extended Kalman Filter Orbit Simulation
Python script that showcases an EKF filter for a LEO orbit, with simulated sensor data, compared to the "actual" calculated orbit.
---

## 🛰 Overview
- Simulates full 3D two-body orbital motion using **RK45 numerical integration**
- Generates **noisy sensor data** to mimic imperfect satellite measurements
- Implements an **Extended Kalman Filter (EKF)** for orbit estimation
- Visualizes **true vs. estimated orbit** in an animated 3D plot

---

## 📈 Results
- EKF successfully tracks the satellite orbit
- Position estimation error converges within a few kilometers
- Includes 3D orbit visualization (`LEO_EKF_RK45_Orbit.gif`)

---

The animation and plots will be saved automatically to your Desktop.

---

## 🎯 Skills Demonstrated
- Orbital Mechanics & Propagation (Two-body dynamics, RK45)
- State Estimation (Extended Kalman Filter)
- Python for Simulation & Visualization
- Guidance, Navigation, and Control (GNC)
