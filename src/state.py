import os
import pickle

class State():
    def __init__(self):
        self.state = self.load_state()

    def load_state(self):
        if not os.path.exists('src/tmp/state.pickle'):
            return {}
        
        with open('src/tmp/state.pickle', 'rb') as f:
            return pickle.load(f)
        
appState = State()
