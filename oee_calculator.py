"""
AURA - Step 2: The OEE Calculator
====================================================
This file reads the event_log produced by the digital twin (factory_twin.py)
and calculates OEE (Overall Equipment Effectiveness) for each machine.

Recap of the formula:
    OEE = Availability x Performance x Quality

    Availability = actual running time / planned production time
    Performance  = (ideal cycle time x total jobs made) / actual running time
    Quality      = good jobs / total jobs made
"""

from factory_twin import run_simulation, SIM_TIME, PROCESS_TIME_MEAN


def calculate_oee(event_log, machine_ids):
    """
    Reads through the event log and computes OEE per machine.
    Returns a dictionary: { machine_id: {availability, performance, quality, oee} }
    """
    results = {}

    for mid in machine_ids:
        # Filter only this machine's events
        machine_events = [e for e in event_log if e["machine_id"] == mid]

        # --- DOWNTIME: total minutes lost to breakdowns ---
        downtime = 0.0
        breakdown_start = None
        for e in machine_events:
            if e["event"] == "breakdown":
                breakdown_start = e["time"]
            elif e["event"] == "repaired" and breakdown_start is not None:
                downtime += (e["time"] - breakdown_start)
                breakdown_start = None

        # --- Availability ---
        planned_time = SIM_TIME
        run_time = planned_time - downtime
        availability = run_time / planned_time if planned_time > 0 else 0

        # --- Jobs completed & defective (count job_end events) ---
        job_end_events = [e for e in machine_events if e["event"] == "job_end"]
        total_jobs = len(job_end_events)
        defective_jobs = sum(1 for e in job_end_events if "defective=True" in e["details"])
        good_jobs = total_jobs - defective_jobs

        # --- Quality ---
        quality = good_jobs / total_jobs if total_jobs > 0 else 0

        # --- Performance ---
        # ideal time to make total_jobs, divided by the time it actually took to run
        ideal_time_needed = total_jobs * PROCESS_TIME_MEAN
        performance = ideal_time_needed / run_time if run_time > 0 else 0
        performance = min(performance, 1.0)  # cap at 100%, can't exceed ideal

        # --- Final OEE ---
        oee = availability * performance * quality

        results[mid] = {
            "availability": round(availability * 100, 1),
            "performance": round(performance * 100, 1),
            "quality": round(quality * 100, 1),
            "oee": round(oee * 100, 1),
            "total_jobs": total_jobs,
            "defective_jobs": defective_jobs,
            "downtime_minutes": round(downtime, 1),
        }

    return results


def print_oee_report(results):
    print("\n" + "=" * 60)
    print("OEE REPORT")
    print("=" * 60)
    for mid, r in results.items():
        print(f"\nMachine {mid}:")
        print(f"  Availability : {r['availability']}%")
        print(f"  Performance  : {r['performance']}%")
        print(f"  Quality      : {r['quality']}%")
        print(f"  --> OEE      : {r['oee']}%")
        print(f"  (jobs done: {r['total_jobs']}, defective: {r['defective_jobs']}, "
              f"downtime: {r['downtime_minutes']} min)")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    log, machines = run_simulation()
    machine_ids = [m.id for m in machines]
    results = calculate_oee(log, machine_ids)
    print_oee_report(results)