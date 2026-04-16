# LEO Extended Kalman Filter Orbit Simulation
<p align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![NumPy](https://img.shields.io/badge/NumPy-linear%20algebra-013243?logo=numpy)
![SciPy](https://img.shields.io/badge/SciPy-ODE%20solver-8CAAE6?logo=scipy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-visualization-11557C?logo=matplotlib)
![GNC](https://img.shields.io/badge/GNC-Orbit%20Estimation-orange)
![EKF](https://img.shields.io/badge/Algorithm-Extended%20Kalman%20Filter-red)
![Orbit%20Dynamics](https://img.shields.io/badge/Physics-Two%20Body%20Problem-blueviolet)
![Status](https://img.shields.io/badge/Status-Completed-success)

</p>

Python script that showcases an EKF filter for a LEO orbit, with simulated sensor data, compared to the "actual" calculated orbit.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/NayStark/LEO-Extended-Kalman-Filter-Orbit-Simulation/main/output/LEO_EKF_RK45_Orbit-ezgif.com-optimize.gif" alt="LEO Orbit EKF" width="400"/>
</p>

## 🛰 Overview
- Simulates full 3D two-body orbital motion using **RK45 numerical integration**
- Generates **noisy sensor data** to mimic imperfect satellite measurements
- Implements an **Extended Kalman Filter (EKF)** for orbit estimation
- Visualizes **true vs. estimated orbit** in an animated 3D plot

---

## 📈 Results
- EKF successfully tracks the satellite orbit
- Position estimation error converges within a few kilometers
- Includes 3D orbit visualization (gif)

<p align="center">
  <img src="https://github.com/user-attachments/assets/30215de5-8837-4be7-94e9-d3e8f042c8f5" alt="LEO Orbit EKF" width="700"/>
</p>
---

The animation will be saved automatically to your Desktop.

---

## 🎯 Skills Demonstrated
- Orbital Mechanics & Propagation (Two-body dynamics, RK45)
- State Estimation (Extended Kalman Filter)
- Python for Simulation & Visualization
- Guidance, Navigation, and Control (GNC)
