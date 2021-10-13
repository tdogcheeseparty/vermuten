import logging
import random


class RiddleException(Exception):
    pass


class Riddle(object):

    def __init__(self, riddle, answer, hint, image_name, correct_responses, incorrect_responses, completion_messsage):
        self.riddle = riddle
        self.image_name = image_name
        self.answer = answer
        self.hint = hint
        self.attempts = 0
        self.correct_responses = correct_responses
        self.incorrect_responses = incorrect_responses
        self.completion_message = completion_messsage

    def get_riddle(self):
        return self.riddle

    def get_hint(self):
        return self.hint

    def get_image_name(self):
        return self.image_name

    def get_attempts(self):
        return self.attempts

    def get_completion_message(self):
        return self.completion_message

    def test_answer(self, response):
        logging.debug(f"Testing {response} against {self.answer}.")
        self.attempts += 1
        response = response.lower()
        if response in self.answer:
            logging.debug("Returning True.")
            return True
        else:
            logging.debug("Returning False.")
            return False

    def get_random_incorrect_response(self):
        return random.choice(self.incorrect_responses)

    def get_random_correct_response(self):
        return random.choice(self.correct_responses)


class RiddleManager(object):

    def __init__(self, riddles):
        self.riddles = riddles
        self.current_riddle_index = 0

    def get_current_riddle(self):
        try:
            return self.riddles[self.current_riddle_index]
        except KeyError:
            return None

    def get_current_riddle_number(self):
        return self.current_riddle_index + 1

    def next_riddle(self):
        self.current_riddle_index += 1

    def get_total_attempt_count(self):
        attempts = 0
        for riddle_id, riddle in self.riddles.items():
            attempts += riddle.get_attempts()
        return attempts

    def reset_progress(self):
        self.current_riddle_index = 0


