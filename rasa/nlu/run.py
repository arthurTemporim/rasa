import json
import logging

from rasa.nlu.model import Interpreter

logger = logging.getLogger(__name__)


def run_cmdline(model_path, component_builder=None):
    interpreter = Interpreter.load(model_path, component_builder)

    logger.info("NLU model loaded. Type a message and press enter to parse it.")
    while True:
        text = input().strip()
        r = interpreter.parse(text)
        print (json.dumps(r, indent=2))
        logger.info("Next message:")


if __name__ == "__main__":
    raise RuntimeError(
        "Calling `rasa.nlu.run` directly is no longer supported. "
        "Please use `rasa run` to start a Rasa server or `rasa shell` to use your "
        "NLU model to interpret text via the command line."
    )
