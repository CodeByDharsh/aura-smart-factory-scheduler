# AURA — Self-Healing Production Scheduler

A software-only Industry 4.0 project combining a factory digital twin, 
real-time OEE (Overall Equipment Effectiveness) tracking, and an AI-driven 
scheduler that automatically reacts to disruptions like machine breakdowns.

## What it does
- Simulates a virtual factory with multiple machines, random job arrivals, 
  and random breakdowns (digital twin)
- Calculates OEE (Availability × Performance × Quality) in real time from 
  the simulation
- Visualizes machine efficiency with charts
- (Coming) Uses AI to automatically reschedule jobs when disruptions happen, 
  validated against the digital twin before being applied

## Tech stack
Python, SimPy (simulation), Matplotlib (visualization) — more coming: 
FastAPI, React, reinforcement learning

## Progress
- ✅ Digital twin (virtual factory simulation)
- ✅ OEE calculation engine
- ✅ OEE visualization
- ⬜ Live web dashboard
- ⬜ AI scheduler
- ⬜ What-if simulation + explainability

## Author
Dharshini — BE CSE, Sathyabama University
