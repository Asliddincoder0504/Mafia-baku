import random

ROLES = ["Mafia", "Doctor", "Detective", "Civilian"]

def assign_roles(players):
    shuffled_roles = random.sample(ROLES * (len(players) // len(ROLES) + 1), len(players))
    return {player: shuffled_roles[i] for i, player in enumerate(players)}
