import random
import time
import os
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent

text_path = base_dir / "words.txt"
num_words = 8
num_runs = 20
show_time = 2.0

word_pool = open(text_path, "r").read().replace("\n", "").replace(" ", "").split(",")

results = []

def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

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

name = f"free_recall_runs{num_runs}_words{num_words}_"
save_path = base_dir / f"{name}{{i}}.csv"

i = 0
while os.path.exists(save_path.format(i = i)):
    i += 1

df.to_csv(save_path.format(i = i), index=False)

print(f"\nAll runs complete. Results saved to {save_path.format(i = i)}")
