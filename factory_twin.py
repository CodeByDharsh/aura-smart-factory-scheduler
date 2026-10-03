"""
AURA - Step 1: The Digital Twin (Virtual Factory)
====================================================
This file creates a PRETEND factory that behaves like a real one.
"""

import simpy
import random

# ---------------------------------------------------------
# CONFIGURATION - easy to tweak later
# ---------------------------------------------------------
NUM_MACHINES = 3          # how many machines our virtual factory has
SIM_TIME = 8 * 60         # simulate an 8-hour shift, in minutes
JOB_ARRIVAL_INTERVAL = 12 # a new job arrives roughly every 12 minutes
PROCESS_TIME_MEAN = 10    # a job takes ~10 minutes to process on average
BREAKDOWN_CHANCE_PER_MIN = 0.003  # small chance each minute a machine breaks down
REPAIR_TIME_MEAN = 20     # if broken, machine takes ~20 minutes to fix
DEFECT_CHANCE = 0.05      # 5% chance a finished job is defective (bad quality)

random.seed(42)  # so results are repeatable while we're testing

# ---------------------------------------------------------
# EVENT LOG - this is our "black box recorder"
# ---------------------------------------------------------
event_log = []

def log_event(time, machine_id, event_type, details=""):
    event_log.append({
        "time": round(time, 2),
        "machine_id": machine_id,
        "event": event_type,
        "details": details
    })


# ---------------------------------------------------------
# MACHINE - represents one physical machine in the factory
# ---------------------------------------------------------
class Machine:
    def __init__(self, env, machine_id):
        self.env = env
        self.id = machine_id
        self.resource = simpy.Resource(env, capacity=1)
        self.is_broken = False
        self.jobs_completed = 0
        self.jobs_defective = 0
        env.process(self.breakdown_watcher())

    def breakdown_watcher(self):
        while True:
            yield self.env.timeout(1)
            if not self.is_broken and random.random() < BREAKDOWN_CHANCE_PER_MIN:
                self.env.process(self.break_down())

    def break_down(self):
        self.is_broken = True
        log_event(self.env.now, self.id, "breakdown")
        repair_time = random.expovariate(1 / REPAIR_TIME_MEAN)
        yield self.env.timeout(repair_time)
        self.is_broken = False
        log_event(self.env.now, self.id, "repaired", f"downtime={round(repair_time,1)}min")

    def process_job(self, job_id):
        with self.resource.request() as req:
            yield req

            while self.is_broken:
                yield self.env.timeout(1)

            log_event(self.env.now, self.id, "job_start", f"job={job_id}")
            process_time = random.expovariate(1 / PROCESS_TIME_MEAN)
            yield self.env.timeout(process_time)

            is_defective = random.random() < DEFECT_CHANCE
            self.jobs_completed += 1
            if is_defective:
                self.jobs_defective += 1

            log_event(
                self.env.now, self.id, "job_end",
                f"job={job_id} duration={round(process_time,1)}min defective={is_defective}"
            )


# ---------------------------------------------------------
# JOB GENERATOR - creates new jobs (orders) arriving over time
# ---------------------------------------------------------
def job_generator(env, machines):
    job_id = 0
    while True:
        yield env.timeout(random.expovariate(1 / JOB_ARRIVAL_INTERVAL))
        job_id += 1
        chosen_machine = random.choice(machines)
        log_event(env.now, chosen_machine.id, "job_arrived", f"job={job_id}")
        env.process(chosen_machine.process_job(job_id))


# ---------------------------------------------------------
# RUN THE SIMULATION
# ---------------------------------------------------------
def run_simulation():
    event_log.clear()
    env = simpy.Environment()
    machines = [Machine(env, machine_id=i) for i in range(1, NUM_MACHINES + 1)]
    env.process(job_generator(env, machines))
    env.run(until=SIM_TIME)
    return event_log, machines


if __name__ == "__main__":
    log, machines = run_simulation()

    print(f"\n--- Simulation finished: {SIM_TIME} minutes ({SIM_TIME/60:.0f}-hour shift) ---\n")
    for m in machines:
        print(f"Machine {m.id}: {m.jobs_completed} jobs completed, {m.jobs_defective} defective")

    print(f"\nTotal events logged: {len(log)}")
    print("\nFirst 10 events:")
    for e in log[:10]:
        print(e)