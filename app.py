import os
import logging
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from application.JsonLoader import ConfigLoader

logging_format = (
    "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s"
)
logging.basicConfig(level=logging.INFO, format=logging_format)

app = Flask(__name__)
config_file = os.getenv("VERMUTEN_CONFIG")
config_loader = ConfigLoader(config_file)
riddle_manager = config_loader.get_riddle_manager()
reset_url_name = config_loader.get_config_file_name()


@app.route("/")
def riddle():
    guess = request.args.get("guess")
    current_riddle = riddle_manager.get_current_riddle()
    riddle_id = riddle_manager.get_current_riddle_number()
    if guess is None and current_riddle is not None:
        return render_template(
            "index.html.j2",
            riddle_id=riddle_id,
            riddle=current_riddle.get_riddle(),
            image_name=current_riddle.get_image_name(),
            hint=current_riddle.get_hint(),
        )
    elif guess is not None and current_riddle is not None:
        if current_riddle.test_answer(guess):
            riddle_manager.next_riddle()
            return render_template(
                "index.html.j2",
                riddle_id=riddle_id,
                riddle=current_riddle.get_riddle(),
                image_name=current_riddle.get_image_name(),
                hint=current_riddle.get_hint(),
                response=current_riddle.get_random_correct_response(),
                advance=True,
            )
        else:
            return render_template(
                "index.html.j2",
                riddle_id=riddle_id,
                riddle=current_riddle.get_riddle(),
                image_name=current_riddle.get_image_name(),
                hint=current_riddle.get_hint(),
                response=current_riddle.get_random_incorrect_response(),
            )
    else:
        return render_template(
            "complete.html.j2",
            completion_message=riddle_manager.get_completion_message(),
            attempts=riddle_manager.get_total_attempt_count(),
        )


@app.route(f"/admin/{reset_url_name}/reset")
def reset():
    riddle_manager.reset_progress()
    return redirect(url_for("riddle"))


@app.route(f"/admin/progress")
def progress():
    return render_template(
        "progress.html.j2",
        current_riddle=riddle_manager.get_current_riddle().get_riddle(),
        attempts=riddle_manager.get_total_attempt_count(),
    )


if __name__ == "__main__":
    app.run()
