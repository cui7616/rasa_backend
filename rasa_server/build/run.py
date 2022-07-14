import argparse
import logging
import os
from typing import List, Text, NoReturn

from rasa.cli import SubParsersAction
from rasa.cli.arguments import run as arguments
import rasa.cli.utils
import rasa.shared.utils.cli  # noqa: F401
from rasa.shared.constants import (
    DOCS_BASE_URL,
    DEFAULT_ENDPOINTS_PATH,
    DEFAULT_CREDENTIALS_PATH,
    DEFAULT_ACTIONS_PATH,
    DEFAULT_MODELS_PATH,
)
from rasa.exceptions import ModelNotFound
import asyncio
import aiohttp
import json
import tempfile
import requests

logger = logging.getLogger(__name__)


def add_subparser(
    subparsers: SubParsersAction, parents: List[argparse.ArgumentParser]
) -> None:
    """Add all run parsers.

    Args:
        subparsers: subparser we are going to attach to
        parents: Parent parsers, needed to ensure tree structure in argparse
    """
    run_parser = subparsers.add_parser(
        "run",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Starts a Rasa server with your trained model.",
    )
    run_parser.set_defaults(func=run)

    run_subparsers = run_parser.add_subparsers()
    sdk_subparser = run_subparsers.add_parser(
        "actions",
        parents=parents,
        conflict_handler="resolve",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="Runs the action server.",
    )
    sdk_subparser.set_defaults(func=run_actions)

    arguments.set_run_arguments(run_parser)
    arguments.set_run_action_arguments(sdk_subparser)


def run_actions(args: argparse.Namespace) -> None:
    import rasa_sdk.__main__ as sdk

    args.actions = args.actions or DEFAULT_ACTIONS_PATH

    sdk.main_from_args(args)


def _validate_model_path(model_path: Text, parameter: Text, default: Text) -> Text:

    if model_path is not None and not os.path.exists(model_path):
        reason_str = f"'{model_path}' not found."
        if model_path is None:
            reason_str = f"Parameter '{parameter}' not set."

        logger.debug(f"{reason_str} Using default location '{default}' instead.")

        os.makedirs(default, exist_ok=True)
        model_path = default

    return model_path

async def query_function(bf_url, project_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(bf_url, data={"projectId":project_id}) as r:
            response = await r.json()
    return response.get('data')

def query_function2(bf_url,project_id):
    r = requests.post(bf_url, data={"projectId":project_id})
    response = r.json()
    return response.get('data')


def set_endpoints_credentials_args_from_remote(args):
    bf_url = os.environ.get("BF_URL")
    project_id = os.environ.get("BF_PROJECT_ID")
    if not project_id or not bf_url:
        return
    here = os.listdir(os.getcwd())
    config = query_function2(bf_url,project_id)
    while not config:
        config = query_function2(bf_url,project_id)

    logger.debug(repr(config["endpoints"]))
    logger.debug(repr(config["credentials"]))
 #   if not args.endpoints:
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as yamlfile1:
        rasa.shared.utils.io.write_yaml(config["endpoints"], yamlfile1.name)
        args.endpoints = yamlfile1.name
    logger.debug('endpfile:'+yamlfile1.name)
    if not args.credentials:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as yamlfile2:
            rasa.shared.utils.io.write_yaml(config["credentials"], yamlfile2.name)
            args.credentials = yamlfile2.name
    logger.debug('crfile:'+yamlfile2.name)

def run(args: argparse.Namespace) -> NoReturn:
    """Entrypoint for `rasa run`.

    Args:
        args: The CLI arguments.
    """
    import rasa
    set_endpoints_credentials_args_from_remote(args)
    logger.debug(args.endpoints)
    logger.debug(args.credentials)

    import rasa.model
    from rasa.core.utils import AvailableEndpoints

    # start server if remote storage is configured
    if args.remote_storage is not None:
        rasa.run(**vars(args))
        return

    # start server if model server is configured
    endpoints = AvailableEndpoints.read_endpoints(args.endpoints)
    logger.debug("look endpoints:  "+repr(endpoints.model))
    model_server = endpoints.model if endpoints and endpoints.model else None
    if model_server is not None:
        rasa.run(**vars(args))
        return

    # start server if local model found

    rasa.shared.utils.cli.print_error(
        f"No model found. You have three options to provide a model:\n"
        f"1. Configure a model server in the endpoint configuration and provide "
        f"the configuration via '--endpoints'.\n"
        f"2. Specify a remote storage via '--remote-storage' to load the model "
        f"from.\n"
        f"3. Train a model before running the server using `rasa train` and "
        f"use '--model' to provide the model path.\n"
        f"For more information check {DOCS_BASE_URL}/model-storage."
    )
