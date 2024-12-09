import csv
import random
import numpy as np

# Fixed nodes:
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Define edges (actions) and their mean traversal times
# We'll represent the playground as a graph: state -> possible actions (next states)
# With a mean traversal time associated with each edge.
# For simplicity, let's use this simple structure
# A -> B or C
# B -> D or E
# C -> E or F
# D -> G
# E -> G
# F -> G
#
# We'll store a dictionary of the form:
# times_mean[(s,u)] = mean_time

times_mean = {
    ('A', 'B'): 1.2,
    ('A', 'C'): 10.0,
    ('B', 'D'): 1.5,
    ('B', 'E'): 2.7,
    ('C', 'E'): 2.4,
    ('C', 'F'): 2.0,
    ('D', 'G'): 13.0,
    ('E', 'G'): 0.3,
    ('F', 'G'): 2.9
}

# The standard deviation for the Gaussian noise
std_dev = 0.3

# We'll run a certain number of episodes:
num_episodes = 200

# In each episode, we start at A and attempt to reach G.
# The agent will pick random feasible paths. For demonstration, we will choose actions uniformly at random.
# In a real scenario, you might have a learned policy or an exploration strategy.

def get_actions(state):
    """Return possible actions (next states) from the current state."""
    # actions are the keys for which (state, next) in times_mean exists.
    return [u for (s,u) in times_mean.keys() if s == state]

# CSV file name
csv_filename = 'pupper_random_dataset.csv'

with open(csv_filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['episode','state','action','next_state','cost'])

    for ep in range(num_episodes):
        current_state = 'A'
        while current_state != 'G':
            actions = get_actions(current_state)
            if not actions:
                # No actions available, we are stuck (shouldn't happen in this setup)
                break
            # Choose an action at random
            action = random.choice(actions)
            # next_state is just action in this graph
            next_state = action

            mean_time = times_mean[(current_state, next_state)]
            # Sample a cost from a Gaussian around the mean_time
            cost = np.random.normal(loc=mean_time, scale=std_dev)

            # Record the step
            writer.writerow([ep, current_state, next_state, next_state, cost])

            current_state = next_state

# Print the generated CSV content
with open(csv_filename, 'r') as f:
    content = f.read()
    print("Generated CSV:\n")
    print(content)
