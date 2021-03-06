import argparse
import logging
import os

from typing import List

import rasa.cli.run
import rasa.cli.arguments.arguments


logger = logging.getLogger(__name__)


# noinspection PyProtectedMember


def add_subparser(
    subparsers: argparse._SubParsersAction, parents: List[argparse.ArgumentParser]
):
    shell_parser = subparsers.add_parser(
        "shell",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Speak to a trained model on the command line",
    )
    rasa.cli.run.add_run_arguments(shell_parser)

    rasa.cli.arguments.arguments.add_logging_option_arguments(shell_parser)

    shell_parser.set_defaults(func=shell)


def shell(args: argparse.Namespace):
    from rasa.cli.utils import get_validated_path
    from rasa.constants import DEFAULT_MODELS_PATH
    from rasa.model import get_model, get_model_subdirectories

    args.connector = "cmdline"

    model = get_validated_path(args.model, "model", DEFAULT_MODELS_PATH)
    model_path = get_model(model)
    if not model_path:
        logger.error(
            "No model found. Train a model before running the "
            "server using `rasa train`."
        )
        return

    core_model, nlu_model = get_model_subdirectories(model_path)

    if not os.path.exists(core_model):
        import rasa.nlu.run

        rasa.nlu.run.run_cmdline(nlu_model)
    else:
        import rasa.cli.run

        rasa.cli.run.run(args)
