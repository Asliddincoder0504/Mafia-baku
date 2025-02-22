from roles import assign_roles

class MafiaGame:
    def __init__(self):
        self.players = []
        self.roles = {}

    def add_player(self, player_id):
        if player_id not in self.players:
            self.players.append(player_id)

    def start_game(self):
        self.roles = assign_roles(self.players)
        return self.roles

game = MafiaGame()
