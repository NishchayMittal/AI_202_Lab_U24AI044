import random

class Env:
    def __init__(self):
        self.rooms = {
            'A': 'Dirt',
            'B': 'Dirt',
            'C': 'Dirt'
        }

    def stat(self, loc):
        return self.rooms[loc]

    def clean(self, loc):
        self.rooms[loc] = 'No Dirt'


class Agent:
    def __init__(self, envi):
        self.env = envi
        self.loc = 'A'
        self.tc = 0

        self.rule = {
            ('A', 'Dirt'): ['Remove'],
            ('A', 'No Dirt'): ['Move Right'],
            ('B', 'Dirt'): ['Remove'],
            ('B', 'No Dirt'): ['Move Left', 'Move Right'],
            ('C', 'Dirt'): ['Remove'],
            ('C', 'No Dirt'): ['Move Left']
        }

    def move(self, action):
        if self.loc == 'A' and action == 'Move Right':
            self.loc = 'B'
        elif self.loc == 'B' and action == 'Move Left':
            self.loc = 'A'
        elif self.loc == 'B' and action == 'Move Right':
            self.loc = 'C'
        elif self.loc == 'C' and action == 'Move Left':
            self.loc = 'B'

        self.tc += 1  

    def act(self):
        status = self.env.stat(self.loc)
        action = random.choice(self.rule[(self.loc, status)])

        print(f"({self.loc},{status})\t{action}\t\tCost:{self.tc}")

        if action == 'Remove':
            self.env.clean(self.loc)
            self.tc += 5 
        else:
            self.move(action)


env = Env()
agent = Agent(env)

print("Percept\t\tAction\t\tPerformance")

for _ in range(20):
    agent.act()

print("\nTotal Performance Cost:", agent.tc)
