#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import sys

class Data:

    class player:
        
        def __init__(self, player_name):
            self.player_name = player_name
            self._URL = "https://www.basketball-reference.com/players/"
            
        def fetch(self, **kwargs):
            #flip the player's name (e.g. "Michael Jordan" -> ["Jordan", "Michael"])
            inv_player_name = self.player_name.lower().split(" ")[::-1]
            
            #create an url extension from the player name ("j/jordami01.html")
            player_tag = inv_player_name[0][0]+"/"+inv_player_name[0][0:5]+inv_player_name[1][0:2]+"01.html"

            #create the full url ("https://www.basketball-reference.com/players/j/jordami01.html")
            _FULL_URL = self._URL + player_tag

            #make a request to the page and report status of response
            response = requests.get(_FULL_URL)
            print("<status: "+str(response.status_code)+">")

            #parse the raw html
            soup = bs(response.content, "html.parser")

            #find all the tables
            tables = soup.findAll("div", {"class": "table_wrapper"})

            #find the schema for the data table
            schema = list(set([d.get("data-stat") for d in tables[0].findAll("td")]))

            #initialize a dictionary of empty lists mapped to the schema
            stats = {}
            for s in schema:
                stats[s] = []
                
            #add the data from each tag to the appropriate list
            for d in tables[0].findAll("td"):
                if str(d.string)[0].isdigit() or str(d.string)[0] == ".":
                    value = float(d.string) 
                else:
                    value = d.string
                
                stats[d.get("data-stat")].append(value)
                
            #remove the last entry from the data (i.e. the b-ref's "Totals" row)
            for s in schema:
                stats[s].pop()
                
            #create a dataframe from data
            stats_df = pd.DataFrame.from_dict(stats)
        
            #return dataframe, dropping rows where data has been aggregated (i.e. only return raw data)
            return stats_df.dropna(subset=["age"])



def main():
    name = input("Player Name: ")
    player = Data.player(name).fetch()
    print(player)

if __name__ == "__main__":
    main()
