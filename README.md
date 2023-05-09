# Nuudel best time finder

In a poll like this:

|         | 2023-06-05 | 2023-06-07 | 2023-06-08 | 2023-06-12 | ... |
|---------|------------|------------|------------|------------|-----|
| Alice   | Yes        | No         | No         | Yes        | ... |
| Bob     | No         | No         | No         | Yes        | ... |
| Carl    | Yes        | Yes        | No         | No         | ... |
| Dave    | Yes        | No         | No         | Yes        | ... |
| Eve     | No         | No         | No         | Yes        | ... |
| Francis | No         | No         | No         | No         | ... |
| ...     | ...        | ...        | ...        | ...        | ... |

a common task is to find the set of two or more days that cover as many people as
possible.

This tool works with the poll service nuudel (<https://nuudel.digitalcourage.de/>),
reads the data directly from a given poll and finds the best combinations for any number
of times.

## Install

Install using pip:

```console
pip install nuudel-best-time-finder

```

## How to use

Say we have a nuudel poll at: <https://nuudel.digitalcourage.de/nuudel-poll-id> and want
to find two dates that cover the most amount of people simply run:

```python
from nuudel_best_time_finder import find_best_times

find_best_times(poll = "{nuudel-poll-id}", n =2, results_file = "results.csv")
```

The results are then written to a file called `results.csv` with three columns:

* Time combinations
* Number of people covered by the combination
* Percent coverage out of all participants
