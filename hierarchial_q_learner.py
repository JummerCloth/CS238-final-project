import csv
import sys
import json
from collections import defaultdict

def main():
    if len(sys.argv) < 2:
        print("Usage: python hierarchical_q_learner.py <input_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]

    # Q-learning parameters
    alpha = 0.1  # learning rate
    gamma = 0.9  # discount factor

    # Initialize Q-values: Q[state][action] = q_value
    Q = defaultdict(lambda: defaultdict(float))

    # We'll store transitions in memory and then process them.
    # Each row in CSV: episode,state,action,next_state,cost
    transitions = []
    states = set()
    actions_per_state = defaultdict(set)

    # Read the CSV
    with open(input_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            s = row['state']
            a = row['action']
            s_next = row['next_state']
            c = float(row['cost'])
            transitions.append((s, a, s_next, c))
            states.add(s)
            states.add(s_next)
            actions_per_state[s].add(a)

    # Identify terminal states:
    # If a state does not appear as a 'state' with any outgoing action, 
    # it could be terminal. Alternatively, we can guess terminal states 
    # by the data pattern. We'll consider states with no outgoing actions as terminal.
    non_terminal = set(actions_per_state.keys())
    terminal_states = {st for st in states if st not in non_terminal}

    # Q-learning update:
    # For each transition (s,a,s_next,c):
    # Q(s,a) <- Q(s,a) + alpha * [ c + gamma*min_{a'}Q(s_next,a') - Q(s,a) ]
    # If s_next is terminal: min_{a'}Q(s_next,a') = 0
    for (s, a, s_next, c) in transitions:
        current_q = Q[s][a]

        if s_next in terminal_states:
            next_val = 0.0
        else:
            # pick min Q-value among all actions in s_next
            if Q[s_next]:
                next_val = min(Q[s_next][a2] for a2 in Q[s_next])
            else:
                # If no action known for s_next yet, assume 0
                next_val = 0.0

        new_q = current_q + alpha * (c + gamma * next_val - current_q)
        Q[s][a] = new_q

    # Convert Q-values to a normal dictionary for JSON
    Q_dict = {}
    for s in Q:
        Q_dict[s] = dict(Q[s])

    # Save to q.json
    with open('q.json', 'w') as f:
        json.dump(Q_dict, f, indent=2)

    print("Q-values have been saved to q.json")

if __name__ == "__main__":
    main()
