from .. import CONFIG_DIR
from ..manage import config
from .utils import handle_error
from tabulate import tabulate

import json
import os
import typer

app = typer.Typer(
    help="Manages under-the-hood configuration settings.",
    name="config"
)

@app.command()
def get(
    name: str = typer.Argument(
        ...,
        help="The name of the configuration setting."
    )
):
    """
    Retrieves the value of a configuration setting.
    """
    try:
        if config.exists(name):
            typer.echo(config.get(name))
        else:
            typer.secho("<not set>", err=True, fg=typer.colors.RED)
    except BaseException as error:
        handle_error(error)

@app.command(name="list")
def listing():
    """
    Lists the available configuration settings.
    """
    try:
        paths = os.listdir(CONFIG_DIR)
        paths.sort()

        table = []

        for path in paths:
            name = os.path.splitext(path)[0]
            value = config.get(name)

            table.append([name, value])

        typer.echo(tabulate(table, headers=["key", "value"]))
    except BaseException as error:
        handle_error(error)

@app.command()
def set(
    name: str = typer.Argument(
        ...,
        help="The name of the configuration setting."
    ),
    value: str = typer.Argument(
        ...,
        help="The new value for the configuration setting."
    ),
    is_json: bool = typer.Option(
        False,
        "-j",
        "--json",
        help="The value is JSON encoded.",
        metavar="BOOL"
    )
):
    """
    Sets the value of a configuration setting.

    All settings are stored as JSON encoded values. By default the given value
    is encoded as a string. Alternatively, a JSON encoded value can be directly
    provided by using the -j, --json option. If JSON is provided, it will be
    parsed to ensure it is valid.

    As a string:

        dev config set example "My example string."

    As a JSON encoded value:

        dev config set --json example '{"example":"My example string."}'
    """
    try:
        if is_json:
            value = json.loads(value)

        config.set(name, value)
    except BaseException as error:
        handle_error(error)
