class Game:
    def __init__(self) -> None:
        self.running = False
        self.players = []
        self.active_player = -1

    def start(self) -> None:
        self.running = True

    def stop(self) -> None:
        self.running = False

    def add_player(self, player: object) -> None:
        self.players.append(player)
        player.set_idx(self.players.index(player))

    def remove_player(self, idx: int) -> None:
        if len(self.players) > 0:
            self.players.pop(idx)
            for player in self.players:
                player.set_idx(self.players.index(player))
            return True

    def next_player(self) -> object:
        if self.active_player < len(self.players)-1:
            self.active_player += 1
        else:
            self.active_player = 0
        return self.players[self.active_player]

    def reset_players(self) -> None:
        for player in self.players:
            player.init()

class Player:
    def __init__(self, name: str, gender: str, age: int) -> None:
        self.name = name
        self.gender = gender
        self.age = age
        self.idx = -1
        self.init()

    # Values that can be reset so player's objects don't need to be
    # completely re-instanciated if same players want to play again.
    def init(self) -> None:
        self.health = 100
        self.weapons = []
        self.max_weapons = 2
        self.dropped_weapon = None  

    def set_idx(self, idx: int) -> None:
        self.idx = idx

    def pickup_weapon(self, weapon: object) -> bool:
        if len(self.weapons) < self.max_weapons:
            self.weapons.append(weapon)
            return True

    def drop_weapon(self, idx: int) -> bool:
        if len(self.weapons) > 0:
            self.dropped_weapon = self.weapons[idx].name
            self.weapons.pop(idx)
            return True

    def throw_weapon(self, idx: int) -> None:
        self.weapons.pop(idx)

class Weapon:
    health = 100

class Newspaper(Weapon):
    def __init__(self) -> None:
        self.name = 'Newspaper'
        self.damage = .1
        self.wield_durability = 0.2
        self.throw_durability = 0.1

class Towel(Weapon):
    def __init__(self) -> None:
        self.name = 'Towel'
        self.damage = 3
        self.melee_durability = 1
        self.throw_durability = 1

class Bear(Weapon):
    def __init__(self) -> None:
        self.name = 'Stuffed bear'
        self.damage = .1
        self.melee_durability = 0.4
        self.throw_durability = 1

# Function that doesnt yet have anywhere to "live"
def pick_opponant(active_player: object) -> int:
    print(f'{active_player.name.split()[0]}, choose an opponant:')
    valid_indexes = []
    for player in game.players:
        if player.idx != active_player.idx: 
            print(f'  {player.idx+1}: {player.name}')
            valid_indexes.append(player.idx)
    choice = -1   # Temp value
    return choice

# Namespace only...
class setup:
    @staticmethod
    def add_player(player):
        game.add_player(player)
        print(f'Welcome {player.name.split()[0]}')

    @staticmethod
    def remove_player(idx: int):
        if game.remove_player(idx):
            print('Player removed')
        else:
            print('No players to remove')

    @staticmethod
    def display_players() -> None:
        print('Players:')
        for player in game.players:
            print(f'  {player.idx+1}: {player.name}')

# Namespace only...
class weapon_actions:
    @staticmethod   
    def pickup(player: object, weapon: object) -> None:
        if player.pickup_weapon(weapon):
            print(f'{player.name} has picked up a {weapon.name.lower()}')
        else:
            print(f'{player.name} cannot carry any more weapons (current max: {player.max_weapons})')

    @staticmethod
    def drop(player: object, idx: int) -> None:
        if player.drop_weapon(idx):
            print(f'{player.name} dropped a {player.dropped_weapon.lower()}')
        else:
            print(f'{player.name} has no more weapons to drop')

    @staticmethod
    def display(player: object) -> None:
        if player.weapons:
            print(f'{player.name} is carrying:')
            for idx, weapon in enumerate(player.weapons):
                print(f'  {idx+1}: {weapon.name}')
        else:
            print(f'{player.name} has no weapons')

if __name__ == '__main__':
 
   # Main game object...
    game = Game()

    # Manually set up some players...
    player = Player('Peter Smith','male',28)
    setup.add_player(player)
    player = Player('Robyn Bates','female',25)
    setup.add_player(player)

    setup.display_players()

    # Simulate some typical game loop actions...
    active_player = game.next_player()
    weapon_actions.pickup(active_player,Towel())

    active_player = game.next_player()
    weapon_actions.pickup(active_player,Newspaper())

    active_player = game.next_player()
    weapon_actions.pickup(active_player,Bear())

    active_player = game.next_player()
    weapon_actions.display(active_player)
    weapon_actions.drop(active_player,0)
    weapon_actions.drop(active_player,0)            # Test of player having zero weapons

    active_player = game.next_player()
    weapon_actions.display(active_player)
    weapon_actions.pickup(active_player,Newspaper()) # Test of player having max weapons

    choice = pick_opponant(active_player)
