# LEO Extended Kalman Filter Orbit Simulation (v2.0)

<p align="center">

![Domain](https://img.shields.io/badge/Domain-Guidance_Navigation_Control-red)
![System](https://img.shields.io/badge/System-Orbit_Determination-blueviolet)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![NumPy](https://img.shields.io/badge/NumPy-Linear_Algebra-013243?logo=numpy)
![SciPy](https://img.shields.io/badge/SciPy-ODE_Integration-8CAAE6?logo=scipy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?logo=matplotlib)

![Method](https://img.shields.io/badge/Method-Extended_Kalman_Filter-critical)
![Physics](https://img.shields.io/badge/Physics-Two_Body_Orbital_Dynamics-black)
![Validation](https://img.shields.io/badge/Validation-Monte_Carlo-orange)

![Status](https://img.shields.io/badge/Status-Validated-success)

</p>

## Overview
A high-fidelity framework for Low Earth Orbit (LEO) state determination. **Version 2.0** represents a professional-grade implementation of an Extended Kalman Filter (EKF), rigorously validated through Monte Carlo statistical analysis to ensure optimality and consistency for GNC applications.

## Visualization

<p align="center">
  <img src="output/LEO_EKF_MonteCarlo.gif" width="420"/>
</p>

---

## Engineering Upgrades (v2.0)
* **Joseph Covariance Update:** Implemented the Joseph form update to guarantee the covariance matrix remains symmetric and positive-definite, preventing numerical divergence.
* **Monte Carlo Validation:** Conducted 500-trial simulation batches to establish statistically significant performance metrics.
* **Optimal Residual Whitening:** Validated innovation sequences to prove filter optimality.
* **Precision Tuning:** Achieved steady-state sub-meter 95% radial tracking accuracy.

---

## Statistical Validation & Performance

The following results were derived from a 500-trial Monte Carlo analysis.

### 1. Filter Consistency (NEES & NIS)
The Normalized Estimation Error Squared (NEES) and Normalized Innovation Squared (NIS) plots verify that the filter is statistically consistent—meaning the filter's computed covariance correctly bounds the actual estimation error.

<p align="center">
  <img src="docs/figure_1.png" alt="NEES/NIS Consistency" width="700"/>
  <br><em>Fig 1: NEES (State Consistency) and NIS (Measurement Residual Consistency). The filter remains within theoretical 95% confidence bounds.</em>
</p>

### 2. Optimality (Whiteness Test)
The autocorrelation of the innovation sequence provides a "Whiteness Test." An optimal EKF extracts all available information from the measurements, leaving only white noise in the residuals. The sharp spike at zero lag followed by flat, low-magnitude correlation confirms that the filter has effectively "whitened" the innovation sequence.

<p align="center">
  <img src="docs/figure_2.png" alt="Whiteness Test" width="700"/>
  <br><em>Fig 2: Innovation autocorrelation (Whiteness Test) confirms filter optimality.</em>
</p>

### 3. Steady-State Tracking Performance
Final tracking precision is analyzed in the steady-state window (final 15 minutes of the orbit). The convergence indicates the filter successfully settled into an optimal tracking regime with sub-centimeter stability.

<p align="center">
  <img src="docs/figure_3.png" alt="RMSE Jitter" width="700"/>
  <br><em>Fig 3: RMSE Jitter Check (Final 15 Minutes) showing steady-state convergence.</em>
</p>

---

## Skills Demonstrated
* **Stochastic Estimation:** Implementation and tuning of Extended Kalman Filters.
* **Numerical Stability:** Matrix operations optimized for GNC (Joseph Form, `linalg.solve`).
* **V&V (Verification & Validation):** Statistical consistency analysis (NEES/NIS) and Monte Carlo simulation.
* **Orbital Mechanics:** High-fidelity propagation using RK45 numerical integration.
* **Software Engineering:** Version control, documentation, and technical reporting.

---

## Legacy Version
For the original prototype and basic EKF implementation, please refer to the [v1-legacy branch](https://github.com/NayStark/LEO-Extended-Kalman-Filter-Orbit-Simulation/tree/v1-legacy) or the [v1.0 Release](https://github.com/NayStark/LEO-Extended-Kalman-Filter-Orbit-Simulation/releases/tag/v1.0).
