import json
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python policy.py <q_json> [start_state]")
        sys.exit(1)

    q_file = sys.argv[1]
    start_state = sys.argv[2] if len(sys.argv) > 2 else 'A'  # Default start state 'A'

    # Load Q-values
    with open(q_file, 'r') as f:
        Q = json.load(f)

    # Derive a greedy policy from Q-values
    # Policy: pi(v) = argmin_{u} Q(v,u)
    # We'll start from start_state and move until we find no actions.
    current_state = start_state
    path = [current_state]

    while True:
        # If current state not in Q or no actions available, we've reached a terminal state or no known actions
        if current_state not in Q or len(Q[current_state]) == 0:
            break

        # Pick the action with minimal Q-value
        actions = Q[current_state]
        best_action = min(actions, key=actions.get)

        # Append the chosen action (which doubles as next_state in this environment)
        path.append(best_action)

        # Move to next_state
        current_state = best_action

    # Print the sequence of chosen actions (path)
    print(f"Greedy minimal-Q path from node {start_state}:")
    print(" -> ".join(path))

if __name__ == "__main__":
    main()
