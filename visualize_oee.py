"""
AURA - Step 3: Visualize OEE as a bar chart
"""

import matplotlib.pyplot as plt
from factory_twin import run_simulation
from oee_calculator import calculate_oee

log, machines = run_simulation()
machine_ids = [m.id for m in machines]
results = calculate_oee(log, machine_ids)

# Prepare data for plotting
labels = [f"Machine {mid}" for mid in machine_ids]
availability = [results[mid]["availability"] for mid in machine_ids]
performance = [results[mid]["performance"] for mid in machine_ids]
quality = [results[mid]["quality"] for mid in machine_ids]
oee = [results[mid]["oee"] for mid in machine_ids]

x = range(len(labels))
width = 0.2

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar([i - 1.5*width for i in x], availability, width, label="Availability")
ax.bar([i - 0.5*width for i in x], performance, width, label="Performance")
ax.bar([i + 0.5*width for i in x], quality, width, label="Quality")
ax.bar([i + 1.5*width for i in x], oee, width, label="OEE", color="black")

ax.set_ylabel("Percentage (%)")
ax.set_title("OEE Breakdown per Machine")
ax.set_xticks(list(x))
ax.set_xticklabels(labels)
ax.legend()
ax.set_ylim(0, 110)

plt.tight_layout()
plt.savefig("oee_chart.png")
print("Chart saved as oee_chart.png — open it from the file explorer!")
plt.show()