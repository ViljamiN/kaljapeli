from time import time

MINUTE_BEER_LEHTISAARI = 0
MINUTE_BEER = 1
OPTIMIZED_BAC = 2


class Timer:
    start_time = 1
    round_time = 1
    game_time = 60

    def reset_clock():
        Timer.start_time = time()

    def round_time_left():
        return Timer.round_time - ((time() - Timer.start_time) % Timer.round_time)

    def get_elapsed_time():
        return time() - Timer.start_time


class BasicLogic:
    def __init__(self, players):
        self.counter_text = ""
        self.players = players
        self.some_drinking_to_do = True

    def get_counter_value(self, round_left):
        return int(round_left) + 1

    def players_drink(self, drinkers):
        for p in drinkers:
            p.drink()
        self.players.sort(key=lambda x: x.bac, reverse=True)
        self.some_drinking_to_do = False

    def get_counter_text(self):
        return self.counter_text

    def update_counter(self, round_left):
        self.counter_text = str(self.get_counter_value(round_left))
        self.some_drinking_to_do = True


class ClassicMinuteBeerMode(BasicLogic):
    # This class is a subclass of BasicLogic
    # each minute every players drink 1 shot of beer.
    # when drinking is done, the bac is calculated and the players are sorted by bac

    def __init__(self, session_code, players):
        super().__init__(players)
        self.game_id = session_code
        self.game_message_text = ""
        self.game_over = False

    # This method updates the game state based on the time left in the round

    def update_game(self):
        round_left = Timer.round_time_left()

        if (round_left <= 5):
            # if there is less than 5 seconds left in the round, update the counter
            self.update_counter(round_left)
            self.game_message_text = ""
        elif (round_left >= Timer.round_time - 5):
            # if there is more than 55 seconds left in the round, drink
            self.counter_text = ""
            self.game_message_text = "Juokaa prkl"
            if self.some_drinking_to_do:
                # if there is still drinking to do, drink
                self.players_drink(self.players)
                # also return a message to the host with the current minute count and the players sorted by bac
                self.game_message_text = f"Minuutti {int((Timer.round_time - round_left) / 60) + 1}:\n" + "\n".join(
                    [f"{p.name}: {p.bac:.2f}" for p in self.players])
                return self.game_message_text
        else:
            self.game_message_text = ""


class OptimizedBACMode(BasicLogic):

    def __init__(self, session_code, players):
        super().__init__(players)
        self.game_id = session_code
        self.drinkers = []
        self.show_drinkers = False

    def update_game(self):
        round_left = Timer.round_time_left()
        if (round_left <= 5):
            self.update_counter(round_left)

        elif (round_left >= Timer.round_time - 5):
            if self.some_drinking_to_do:
                self.counter_text = ""
                self.drinkers = self.get_drinkers()
                self.players_drink(self.drinkers)
        if (round_left >= Timer.round_time - 5):
            self.show_drinkers = True
        else:
            self.show_drinkers = False

    def get_drinkers(self):
        average_bac = self.get_average_bac()
        return [p for p in self.players if p.bac <= average_bac]

    def get_average_bac(self):
        sum = 0.0
        for p in self.players:
            sum += p.bac

        return sum / len(self.players)
