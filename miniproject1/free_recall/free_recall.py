import random
import time
import os
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent

text_path = base_dir / "words.txt"
num_words = 8
num_runs = 20
show_time = 2

# Working memory task options
use_working_memory_task_input = input("Add working memory task between presentation and recall? (y/n): ").lower().strip()
use_working_memory_task = use_working_memory_task_input == 'y'
wm_task_duration = 10  # Duration of working memory task in seconds

if use_working_memory_task:
    wm_duration_input = input(f"Working memory task duration in seconds (default {wm_task_duration}): ").strip()
    if wm_duration_input:
        wm_task_duration = float(wm_duration_input)

word_pool = open(text_path, "r").read().replace("\n", "").replace(" ", "").split(",")

results = []

def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def do_working_memory_task(duration):
    """Working memory task: Count backwards from a random number by 3s"""
    start_number = random.randint(150, 250)
    print(f"Working memory task:")
    print(f"Count backwards from {start_number} by 3s out loud.")
    print(f"Continue counting for {duration} seconds...")
    
    start_time = time.time()
    while time.time() - start_time < duration:
        time.sleep(0.1)
    
    print("Time's up!")
    time.sleep(1)  # Brief pause to show "Time's up!" message
    clr()

for run in range(1, num_runs + 1):
    random.shuffle(word_pool)
    word_list = word_pool[:num_words]
    
    for word in word_list:
        clr()
        print(f"Run {run}/{num_runs}")
        print(word, end="", flush=True)
        time.sleep(show_time)

    clr()
    print(f"Run {run}/{num_runs}")
    
    # Add working memory task if enabled
    if use_working_memory_task:
        do_working_memory_task(wm_task_duration)
        print(f"Run {run}/{num_runs}")
    
    recalled = input("Type all the words you remember, separated by spaces:\n").lower().split()

    correct = [w for w in recalled if w in word_list]
    missed = [w for w in word_list if w not in recalled]

    print(f"\nYou recalled {len(set(correct))} out of {len(word_list)} words correctly.")
    print("Correct words:", set(correct))
    print("Missed words:", missed)
    print("-" * 50)

    results.append({
        "run": run,
        "shown_words": ",".join(word_list),
        "recalled_words": ",".join(recalled),
        "correct_count": len(set(correct)),
        "missed_count": len(missed)
    })
    
    time.sleep(2.0)

df = pd.DataFrame(results)

# Create filename that indicates if working memory task was used
wm_suffix = f"_wm{int(wm_task_duration)}s" if use_working_memory_task else "_nowm"
name = f"free_recall_runs{num_runs}_words{num_words}{wm_suffix}_"

i = 0
save_path = base_dir / f"{name}{i}.csv"
while os.path.exists(save_path):
    i += 1
    save_path = base_dir / f"{name}{i}.csv"

df.to_csv(save_path, index=False)

print(f"\nAll runs complete. Results saved to {save_path}")
