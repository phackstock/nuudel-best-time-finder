import importlib.metadata
from io import StringIO
from itertools import combinations
from typing import Optional

import pandas as pd
import requests
import typer
from typing_extensions import Annotated

__version__ = importlib.metadata.version("nuudel_best_time_finder")


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


app = typer.Typer()


@app.command()
def main(
    poll: Annotated[str, typer.Argument(help="Id of the nuudel poll")],
    n: Annotated[int, typer.Argument(help="Number of times to find")],
    results_file: Annotated[
        Optional[str], typer.Option(help="Name of the file to export results")
    ] = None,
    version: Annotated[
        Optional[bool],
        typer.Option("--version", callback=version_callback, is_eager=True),
    ] = None,
) -> None:
    data = pd.read_csv(
        StringIO(
            requests.get(
                "https://nuudel.digitalcourage.de/exportcsv.php",
                params={"poll": poll},
                timeout=10,
            ).text
        )
    )
    data = data[[c for c in data.columns if not c.startswith("Unnamed")]].replace(
        {"Ja": 1, "Nein": 0, "Unter Vorbehalt": 0.5}
    )
    number_of_answers = len(data) - 1
    day_combinations = list(combinations(data.columns, r=n))

    best_days = [(days, data[[*days]].max(axis=1).sum()) for days in day_combinations]
    best_days = pd.DataFrame(
        best_days, columns=["Times", "Number of people"]
    ).sort_values("Number of people", ascending=False)
    best_days["Coverage [%]"] = (
        best_days["Number of people"] / number_of_answers * 100
    ).round(1)

    print(best_days.head())
    if results_file:
        best_days.to_csv(results_file, index=False)
