import subprocess
import time

# Range of task numbers to run (inclusive)
start = 0
end = 29

for task_num in range(start, end + 1):
    print(f"\n=== Running task_num {task_num} ===")
    cmd = [
        "poetry", "run", "python", "manual_crew.py",
        f"--task_nums", str(task_num)
    ]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"Task {task_num} failed with exit code {result.returncode}")
    # Optional: sleep between runs to avoid overloading resources
    time.sleep(2)
print("\nAll tasks completed.")
