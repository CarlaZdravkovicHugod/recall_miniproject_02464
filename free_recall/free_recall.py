import random
import time
import os
import pandas as pd

text_path = r"C:\Users\alexa\Documents\GitHub\recall_miniproject_02464\free_recall\words.txt"
num_words = 10
num_runs = 1
show_time = 8.0

word_pool = open(text_path, "r").read().replace("\n", "").replace(" ", "").split(",")

results = []

for run in range(1, num_runs + 1):
    word_list = random.sample(word_pool, num_words)
    
    print(f"Run {run}/{num_runs}")
    print(word_list)
    time.sleep(show_time)

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

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

name = r"\free_recall_runs{runs}_words{words}_".format(runs=num_runs, words=num_words)
save_path = r"C:\Users\alexa\Documents\GitHub\recall_miniproject_02464\free_recall" + name + r"{i}.csv"

i = 0
while os.path.exists(save_path.format(i = i)):
    i += 1

df.to_csv(save_path.format(i = i), index=False)

print(f"\nAll runs complete. Results saved to {save_path.format(i = i)}")
