import importlib.metadata
from io import StringIO
from itertools import combinations
from typing import Optional

import pandas as pd
import requests
import typer

__version__ = importlib.metadata.version("nuudel_best_time_finder")


app = typer.Typer()

@app.command()
def version():
    return __version__


@app.command()
def find_best_times(poll: str, n: int, results_file: Optional[str] = None) -> None:
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
