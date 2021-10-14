import json
import logging
from application.Riddle import Riddle, RiddleManager


class ConfigLoadException(Exception):
    pass


class ConfigLoader(object):
    def __init__(self, path_to_json_config):
        self.path_to_json_config = path_to_json_config
        self.riddle_collection = dict()
        self._load_config()

    def _load_config(self):
        try:
            logging.info(f"Loading {self.path_to_json_config}.")
            config_file = open(self.path_to_json_config, "r")
            json_config = json.loads(config_file.read())
            config_file.close()
            logging.debug(f"Config:\n{json_config}")
            incorrect_responses = json_config["incorrect_responses"]
            correct_responses = json_config["correct_responses"]
            completion_message = json_config["completion_message"]
            for riddle in json_config["riddles"]:
                logging.debug(f"Creating riddle object for {riddle}.")
                riddle_object = Riddle(
                    riddle["question"],
                    riddle["answer"],
                    riddle["hint"],
                    riddle["image_name"],
                    correct_responses,
                    incorrect_responses,
                    completion_message,
                )
                self.riddle_collection[len(self.riddle_collection)] = riddle_object
            logging.info(f"Successfully loaded {self.path_to_json_config}.")
            logging.info(f"Riddle count: {len(self.riddle_collection)}")
            logging.info(f"Incorrect response count: {len(incorrect_responses)}")
            logging.info(f"Correct response count: {len(correct_responses)}")
        except Exception as err:
            logging.error(f"{err}")
            raise ConfigLoadException

    def get_riddles(self):
        return self.riddle_collection

    def get_riddle_manager(self):
        riddle_manager = RiddleManager(self.get_riddles())
        return riddle_manager
