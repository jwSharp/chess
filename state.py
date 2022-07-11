
# State Class - Abstract based class for all the other state files
# Base/ Parent Class that all other states will inherit from
# Will need some sort of "time"
# Can be used as a template for Parent Class

class State:
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self, time, actions):
        pass

    def render(self, display):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()	

