import pickle

from graph.state import GraphState  # Function to save the state as a serialized dump


def save_state(state: GraphState, step: str):
    with open(f'./states/state_after_{step}.pkl', 'wb') as f:
        pickle.dump(state, f)


# Function to load the state from a serialized dump
def load_state(step: str) -> GraphState:
    with open(f'./states/state_after_{step}.pkl', 'rb') as f:
        state = pickle.load(f)
    return state