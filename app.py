import argparse
import logging
from flask import Flask
from flask import request
from flask import render_template
from application.JsonLoader import ConfigLoader

logging_format = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=logging_format)

app = Flask(__name__)
config_file = "config.json"  # TODO: Expose this as a runtime parameter.
riddle_manager = ConfigLoader(config_file).get_riddle_manager()


@app.route("/")
def riddle():
    guess = request.args.get("guess")
    current_riddle = riddle_manager.get_current_riddle()
    riddle_id = riddle_manager.get_current_riddle_number()
    if guess is None and current_riddle is not None:
        return render_template('index.html.j2',
                               riddle_id=riddle_id,
                               riddle=current_riddle.get_riddle(),
                               image_name=current_riddle.get_image_name(),
                               hint=current_riddle.get_hint())
    elif guess is not None and current_riddle is not None:
        if current_riddle.test_answer(guess):
            riddle_manager.next_riddle()
            return render_template('index.html.j2',
                                   riddle_id=riddle_id,
                                   riddle=current_riddle.get_riddle(),
                                   image_name=current_riddle.get_image_name(),
                                   hint=current_riddle.get_hint(),
                                   response=current_riddle.get_random_correct_response(),
                                   advance=True)
        else:
            return render_template('index.html.j2',
                                   riddle_id=riddle_id,
                                   riddle=current_riddle.get_riddle(),
                                   image_name=current_riddle.get_image_name(),
                                   hint=current_riddle.get_hint(),
                                   response=current_riddle.get_random_incorrect_response())
    else:
        return render_template('complete.html.j2',
                               attempts=riddle_manager.get_total_attempt_count())


# TODO: Remove this. It's only here for demo purposes.
@app.route("/reset")
def reset():
    riddle_manager.reset_progress()
    return "Progress reset."


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
