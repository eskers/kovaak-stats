"""Module to parse Kovaak stat files and save data which is useful for displaying"""

import os
import csv
import datetime
import json


def scenario_file_paths(path, scenarios):
    """
    Return a dictionary containing list of paths of statistics files, scenarios are
    used as the keys, paths are a list for the given keys.

    Keyword arguments:
    path -- string of the path to directory where Kovaak's stores statistics files
    scenario -- tuple of scenarios to generate list of file paths for
    """
    scenario_files = {}
    file_list = os.listdir(path)
    for scenario in scenarios:
        relevant_files = []
        for file in file_list:
            if file.startswith(scenario):
                relevant_files.append(path + file)
        scenario_files[scenario] = relevant_files

    return scenario_files


def get_stats(scenario_files):
    """
    Open Kovaak scenario csv stat files and returns a list of tuples containing datetime
    and the score.

    Keyword arguments:
    scenario_files -- list of paths for stat files to be read by function
    """
    scenarios_stats = []
    for scenario in scenario_files:
        date_str = scenario[-29:-19]
        datetime_str = date_str + " 00:00:00.0"
        challenge_score = -1.0
        with open(scenario, newline="") as csvfile:
            stat_reader = csv.reader(csvfile, dialect="excel")
            for row in stat_reader:
                if row and row[0] == "Score:":
                    challenge_score = float(row[1])
                if row and row[0] == "Challenge Start:":
                    datetime_str = datetime_str[:11] + row[1]

        datetime_obj = datetime.datetime.strptime(datetime_str, "%Y.%m.%d %H:%M:%S.%f")
        title_datetime = {"Date:": datetime_obj}
        title_score = {"Score:":  challenge_score}
        challenge_stats = (title_datetime, title_score)
        scenarios_stats.append(challenge_stats)

    return scenarios_stats


def mult_scen_get_stats(dict_scen_paths):
    """
    Runs get_stats() for multiple scenarios, return dictionary with the scenario as the
    key and get_stats() list as values

    Keyword arguments:
    dict_scen_paths -- Dictionary with keys of scenario names and values of filepaths
    """
    stats_dict = {}
    for key in dict_scen_paths:
        stats_dict[key] = get_stats(dict_scen_paths[key])

    return stats_dict


def write_json(data_object):
    """Writes python data_object to a json file.

    Keyword arguments:
    data_object -- any python data object??????
    """
    with open("data.json", "w", encoding="utf-8") as jsonfile:
        json.dump(data_object, jsonfile, ensure_ascii=False, indent=4, default=str)


# Temp variables for testing
STATS_DIR = "/mnt/c/Program Files (x86)/Steam/steamapps/common/FPSAimTrainer/FPSAimTrainer/stats/"
int_benchmark_scenarios = (
    "Pasu Voltaic Easy",
    "B180 Voltaic Easy",
    "Popcorn Voltaic Easy",
    "ww3t Voltaic",
    "1w4ts Voltaic",
    "6 Sphere Hipfire Voltaic",
    "Smoothbot Voltaic Easy",
    "Air Angelic 4 Voltaic Easy",
    "PGTI Voltaic Easy",
    "FuglaaXYZ Voltaic Easy",
    "Ground Plaza Voltaic Easy",
    "Air Voltaic Easy",
    "patTS Voltaic Easy",
    "psalmTS Voltaic Easy",
    "voxTS Voltaic Easy",
    "kinTS Voltaic Easy",
    "B180T Voltaic Easy",
    "Smoothbot TS Voltaic Easy",
)

# Test code
kovaak_stats = scenario_file_paths(STATS_DIR, int_benchmark_scenarios)
a = mult_scen_get_stats(kovaak_stats)

write_json(a)
