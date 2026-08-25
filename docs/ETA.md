# CityBus Enterprise Platform - Dynamic ETA Calculation Engine

## 1. Dynamic ETA Math Model
The ETA calculation incorporates real-time vehicle kinematics, stop dwell times, route corridor geometry, and peak-hour traffic multipliers:

$$\text{ETA} = \left( \frac{d_{\text{remaining}}}{v_{\text{effective}}} \times 60 \times \mu_{\text{traffic}} \right) + (N_{\text{stops}} \times t_{\text{dwell}})$$

Where:
- $d_{\text{remaining}}$: Great-Circle Haversine distance along route corridor waypoints to target stop (km).
- $v_{\text{effective}}$: Smoothed velocity ($v_{\text{current}}$ if $>8\text{ km/h}$, else baseline $28\text{ km/h}$).
- $\mu_{\text{traffic}}$: Peak congestion multiplier ($1.25\times$ between 08:00-10:00 and 17:00-20:00 IST).
- $N_{\text{stops}}$: Count of intermediate stops remaining before arrival.
- $t_{\text{dwell}}$: Typical dwell duration (0.75 minutes / 45 seconds per stop).

## 2. Confidence Scoring
Confidence index is computed from sensor status:
- Moving vehicle ($v > 5\text{ km/h}$): 92% base confidence.
- Stationary/dwelling vehicle ($v \le 5\text{ km/h}$): 75% confidence.
- Delayed status: $-15\%$ penalty.
