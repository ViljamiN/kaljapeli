from time import time
from game_logic import Timer
import constants


class Player:

    def __init__(self, id, name, gender, weight, drink_alc_perc=0.05):
        self.id = id
        self.name = name
        self.gender = gender
        self.weight = weight
        self.drink_alc_perc = drink_alc_perc
        self.color = (255, 255, 255)
        self.alcohol_consumed = 0
        self.bac = 0
        self.gender = gender
        self.gender_factor = constants.MALE_FACTOR if gender == 'male' else constants.FEMALE_FACTOR
        self.time_left_drunk = 0

    def drink(self):
        grams_of_alcohol = constants.SIP_SIZE*(self.drink_alc_perc*1000)
        self.alcohol_consumed += grams_of_alcohol
        self.calculate_bac()

    def calculate_bac(self):
        total_bac = self.alcohol_consumed / \
            (self.weight * self.gender_factor) * 100
        alcohol_burned = (time() - Timer.start_time) * \
            constants.BAC_REDUCTION_PER_SECOND
        real_bac = total_bac - alcohol_burned
        self.bac = real_bac if real_bac > 0 else 0

        self.time_left_drunk = self.bac / constants.BAC_REDUCTION_PER_SECOND / 3600
