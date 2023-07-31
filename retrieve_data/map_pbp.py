from typing import Dict, List
import json
import boto3
import pandas as pd
from pandas import DataFrame
from py_ball import playbyplay


HEADERS = {'Connection': 'keep-alive',
           'Host': 'stats.nba.com',
           'Origin': 'http://stats.nba.com',
           'Upgrade-Insecure-Requests': '1',
           'Referer': 'stats.nba.com',
           'x-nba-stats-origin': 'stats',
           'x-nba-stats-token': 'true',
           'Accept-Language': 'en-US,en;q=0.9',
           "X-NewRelic-ID": "VQECWF5UChAHUlNTBwgBVw==",
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6)' +\
                         ' AppleWebKit/537.36 (KHTML, like Gecko)' + \
                         ' Chrome/81.0.4044.129 Safari/537.36'}


def get_pbp_for_game_pk(game_pk:int) -> DataFrame:
    """
    Retrieves `play by play` data from py_ball

    Parameters:
        game_pk: specific game of listing data

    Returns:
        DataFrame: data from py_ball
    """
    plays = playbyplay.PlayByPlay(
        headers=HEADERS, endpoint='playbyplayv2', game_id=game_pk
    )
    play_df = pd.DataFrame(plays.data['PlayByPlay'])
    return play_df


def get_wisd_data() -> List[Dict]:
    """
    Retrieves data from Sportsradar.

    Returns:
        List[DataFrame]: the wisd data
    """
    s3_client = boto3.client('s3')
    bucket = "sportradar-wisd-data"
    prefix = "games"

    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    files = response.get("Contents")
    list_of_data = {}
    for file in files:
        data_for_game = []
        current_file = file['Key']
        # I am only interest in events file
        if "events" not in current_file:
            continue
        split_path = current_file.split("/")
        # game pk used as key - need this for accessing pbp data
        game_pk = split_path[1]
        file_to_copy = split_path[2]
        s3_client.download_file(bucket, current_file, file_to_copy)
        with open(file_to_copy) as play_file:
            for line in play_file:
                # convert to json to access as dict
                json_object = json.loads(line)
                data_for_game.append(json_object)
        list_of_data[game_pk] = data_for_game
    return list_of_data


def map_wisd_data_to_py_ball_data(wisd_data: Dict) -> List[DataFrame]:
    """
    Maps data received from Sportsradar with data from py ball.

    Parameters:
        wisd_data: event data retrieved from sportsradar

    Returns:
        List[DataFrame]: the pbp dataframe of data mapping to wisd data
    """
    pbp_data_list = list()
    for key, value in wisd_data.items():
        pbp_game_pk = get_pbp_for_game_pk(key)
        for play in value:
            if play.get('pbpId') != None:
                pbp_data = pbp_game_pk.loc[pbp_game_pk['EVENTNUM'] == play['pbpId']]
                pbp_data_list.append(pbp_data)
    return pbp_data_list


def print_data_to_file(pbp_data) -> None:
    """
    Prints out files with mapped play by play data from Sportradar and py ball

    Parameters:
        pbp_data: mapped pbp data from Sportradar and py ball
    """
    pbp_file = open("pbp_file.json", "a")
    pbp_file.write(str(pbp_data))
    pbp_file.close()

    wisd_file = open("wisd_file.json", "a")
    wisd_file.write(str(wisd_file))
    wisd_file.close()


def main():
    """
    Basic set up code for retrieving and accessing wisd sportsradar data
    """
    wisd_data = get_wisd_data()
    pbp_data = map_wisd_data_to_py_ball_data(wisd_data)
    print_data_to_file(pbp_data)


if __name__ == "__main__":
    main()
