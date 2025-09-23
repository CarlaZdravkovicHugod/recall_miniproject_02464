import random
import time
import csv
import os
from datetime import datetime
from collections import Counter

# Function to generate a sequence of digits
def generate_sequence(length, allow_repeats=True):
    if allow_repeats:
        return [str(random.randint(0, 9)) for _ in range(length)]
    else:
        digits = list('0123456789')
        random.shuffle(digits)
        return digits[:length] if length <= 10 else digits * (length // 10 + 1)[:length]  # Repeat if >10

# Function to present sequence
def present_sequence(sequence, rate):
    for item in sequence:
        print(item, end='', flush=True)  # Print without newline for serial feel, but wait
        time.sleep(rate)
        print('\r   ', end='', flush=True)  # Clear the line after display
        time.sleep(0.1)  # Brief clear
    print("\nSequence presented.")

# Function for pause
def do_pause(duration):
    print(f"Pausing for {duration} seconds...")
    time.sleep(duration)

# Function for working memory task (e.g., count backwards)
def do_working_memory_task(duration):
    print("Perform this task: Count backwards from 100 by 3s out loud for the next few seconds.")
    time.sleep(duration)
    print("Task over.")

# Function for free recall
def free_recall(trial_num, seq_length, rate, with_pause=False, pause_duration=10, with_wm_task=False, wm_task_duration=10, allow_repeats=True):
    sequence = generate_sequence(seq_length, allow_repeats)
    present_sequence(sequence, rate)
    
    if with_pause:
        do_pause(pause_duration)
    if with_wm_task:
        do_working_memory_task(wm_task_duration)
    
    print("Recall as many digits as you can, in any order. Enter them separated by spaces:")
    response = input().strip().split()
    
    recalled_count = Counter(response)
    original_count = Counter(sequence)
    correct = sum(min(recalled_count.get(item, 0), count) for item, count in original_count.items())
    
    # For position analysis
    positions = []
    for pos, item in enumerate(sequence):
        if recalled_count[item] > 0:
            positions.append((pos, item))
            recalled_count[item] -= 1  # To handle multiples, but this is approximate for positions
    
    return {
        'trial': trial_num,
        'sequence': sequence,
        'response': response,
        'correct': correct,
        'total': seq_length,
        'proportion': correct / seq_length,
        'positions_recalled': positions
    }

# Function for serial recall
def serial_recall(trial_num, seq_length, rate, chunk_size=1, retention_duration=5, allow_repeats=False):
    sequence = generate_sequence(seq_length, allow_repeats)
    
    # For chunking
    if chunk_size > 1:
        chunks = [''.join(sequence[i:i+chunk_size]) for i in range(0, len(sequence), chunk_size)]
        present_sequence(chunks, rate)
    else:
        present_sequence(sequence, rate)
    
    time.sleep(retention_duration)
    
    print("Recall the digits in the order presented. Enter them separated by spaces:")
    response = input().strip().split()
    
    # Truncate response if longer than sequence
    response = response[:seq_length]
    
    correct = sum(1 for a, b in zip(sequence, response) if a == b)
    errors = [(i, sequence[i], response[i]) for i in range(len(response)) if sequence[i] != response[i]]
    
    return {
        'trial': trial_num,
        'sequence': sequence,
        'response': response,
        'correct': correct,
        'total': seq_length,
        'proportion': correct / seq_length,
        'errors': errors
    }

# Function to run an experiment and save data
def run_experiment(exp_type, num_trials, **kwargs):
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{exp_type}_{timestamp}.csv"
    
    for trial in range(1, num_trials + 1):
        print(f"\nTrial {trial}/{num_trials}")
        if exp_type == 'free_recall':
            result = free_recall(trial, **kwargs)
        elif exp_type == 'serial_recall':
            result = serial_recall(trial, **kwargs)
        else:
            raise ValueError("Unknown experiment type")
        results.append(result)
    
    # Save to CSV
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['trial', 'sequence', 'response', 'correct', 'total', 'proportion', 'extra'])
        for res in results:
            extra = res.get('positions_recalled') if 'positions_recalled' in res else res.get('errors', '')
            writer.writerow([res['trial'], ','.join(res['sequence']), ','.join(res['response']), res['correct'], res['total'], res['proportion'], str(extra)])
    
    print(f"Experiment complete. Data saved to {filename}")
    return results

# Main application
def main():
    print("Welcome to Memory Experiment App")
    while True:
        print("\nChoose experiment:")
        print("1: Free Recall")
        print("2: Serial Recall")
        print("3: Quit")
        choice = input("Enter choice: ").strip()
        
        if choice == '3':
            break
        elif choice not in ['1', '2']:
            continue
        
        exp_type = 'free_recall' if choice == '1' else 'serial_recall'
        
        num_trials = 20#int(input("Number of trials (at least 20): ") or 20)
        seq_length = 8#int(input("Sequence length: ") or (15 if exp_type == 'free_recall' else 7))
        rate = float(input("Presentation rate (seconds per item): ") or 1.0)
        allow_repeats = "y"#input("Allow repeats in sequence? (y/n): ").lower() == 'y'
        
        kwargs = {
            'seq_length': seq_length,
            'rate': rate,
            'allow_repeats': allow_repeats
        }
        
        if exp_type == 'free_recall':
            with_pause = input("Add pause after sequence? (y/n): ").lower() == 'y'
            if with_pause:
                pause_duration = float(input("Pause duration (seconds): ") or 10)
                kwargs['with_pause'] = True
                kwargs['pause_duration'] = pause_duration
            
            with_wm_task = input("Add working memory task after sequence? (y/n): ").lower() == 'y'
            if with_wm_task:
                wm_task_duration = float(input("WM task duration (seconds): ") or 10)
                kwargs['with_wm_task'] = True
                kwargs['wm_task_duration'] = wm_task_duration
        
        elif exp_type == 'serial_recall':
            chunk_size = int(input("Chunk size (1 for no chunking): ") or 1)
            kwargs['chunk_size'] = chunk_size
            
            retention_duration = float(input("Retention duration (seconds): ") or 5)
            kwargs['retention_duration'] = retention_duration
        
        run_experiment(exp_type, num_trials, **kwargs)

if __name__ == "__main__":
    main()