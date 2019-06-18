#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sys

def StatGrab(player_name):
    _URL = "https://www.basketball-reference.com/players/"

    inv_player_name = player_name.lower().split(" ")[::-1]

    player_tag = inv_player_name[0][0]+"/"+inv_player_name[0][0:5]+inv_player_name[1][0:2]+"01.html"

    _FULL_URL = _URL + player_tag

    response = requests.get(_FULL_URL)

    if response.status_code == 200:
        print("Data Accessed Successfully")
    else:
        print("Problem Accessing Data")

    soup = bs(response.content, "html.parser")

    stats = dict.fromkeys( list( set( stat.get("data-stat") for stat in soup.findAll("td") ) ), [] )

    for stat in soup.findAll("td"):
        stats[stat.get("data-stat")] += [stat.get_text()]

    return pd.DataFrame.from_dict(stats)


def main():
    player_name = str(input("Player Name: "))
    stats_df = StatGrab(player_name)
    print(stats_df)

if __name__ == "__main__":
    main()



