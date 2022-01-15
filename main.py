# baseball reference link
# https://www.baseball-reference.com/players/s/sosasa01.shtml
# players/(first letter of last name)/(first five letters of last name)(first two of first name)(potential copycat)
#HOFScraping
#Author: Joe Peracchio
#Version: 1.0
#Date 1/15/2022
#Purpose: Determine the HoF worthiness of a player by their stat totals and batting stats found on baseball reference

import requests
import statistics
from bs4 import BeautifulSoup

first_grouping_totals = {"WAR": 0, "AB": 0, "H": 0, "HR": 0, "BA": 0}
second_grouping_totals= {"R": 0, "RBI": 0, "SB": 0}
third_grouping_totals= {"OBP": 0, "SLG": 0, "OPS": 0, "OPS+": 0}
first_grouping_stdev = {"WAR": 0, "AB": 0, "H": 0, "HR": 0, "BA": 0}
second_grouping_stdev= {"R": 0, "RBI": 0, "SB": 0}
third_grouping_stdev= {"OBP": 0, "SLG": 0, "OPS": 0, "OPS+": 0}
indivi_stat_group = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
hof_list=["Derek Jeter", "Larry Walker","Edgar Martinez", "Vladimir Guerrero", "Chipper Jones", "Ivan Rodriguez", "Ken Griffey Jr.",
          "Mike Piazza", "Jim Thome","Tim Raines", "Jeff Bagwell","Craig Biggio","Barry Larkin", "Roberto Alomar",
          "Andrew Dawson","Ricky Henderson","Jim Rice", "Tony Gwynn", "Cal Ripken Jr", "Wade Boggs", "Ryan Sandberg",
          "Paul Molitor","Gary Carter", "Ozzie Smith", "Kirby Puckett","Dave Winfield", "Carlton Fisk"
          ,"Tony Perez", "George Brett","Robin Yount","Mike Schmidt","Reggie Jackson","Rod Carew"]

def name_changer(name):
    #Has name as a String as a parameter
    #Changes the regular given name in the form of {First Name Last Name} into format acceptable for website
    #Acceptable format: (first five letters of last name)(first two letters of first name)
    space_index = name.index(' ')
    last_name = name[space_index+1:space_index+6]
    first_name = name[:2]
    name = last_name+first_name
    name.lower()
    return name

def hof_database_creator():
    #Searches through the list of Hall of Fame players to scrape their stats from baseball reference
    #Stats to be scraped are the career totals and averages section
    #Puts stats into three separate categories based on positioning in the wesbite
    #Creates lists of totals for averages to be calculated and individual stats of eahc player for purposes of standard
    #deviation calculation
    for name in hof_list:
        temp_name = name_changer(name).lower()
        first_letter = temp_name[0:1].lower()
        URL = f"https://www.baseball-reference.com/players/{first_letter}/{temp_name}01.shtml"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        first_results = soup.findAll("div", attrs={"class": "p1"})
        second_results = soup.findAll("div", attrs={"class": "p2"})
        third_results = soup.findAll("div", attrs={"class": "p3"})
        for x in first_results:
            for p, stat_name, indiv_stat, x in zip(x.findAll('p'), first_grouping_totals, indivi_stat_group, range(5)):
                temp = float(p.text)
                first_grouping_totals[stat_name]+=temp
                indivi_stat_group[x].append(temp)
        for x in second_results:
            for p, stat_name, indiv_stat, x in zip(x.findAll('p'), second_grouping_totals, indivi_stat_group, range(5, 8)):
                temp = float(p.text)
                second_grouping_totals[stat_name]+=temp
                indivi_stat_group[x].append(temp)
        for x in third_results:
            for p, stat_name, indiv_stat, x in zip(x.findAll('p'), third_grouping_totals, indivi_stat_group, range(8, 12)):
                temp = float(p.text)
                third_grouping_totals[stat_name]+=temp
                indivi_stat_group[x].append(temp)

def stdev_calc():
    #Calculates the standard deviation of the individual stats of the hall of fame players
    for key, x in zip(first_grouping_stdev, range(5)):
        stdev = statistics.pstdev(indivi_stat_group[x])
        first_grouping_stdev[key] = stdev
    for key, x in zip(second_grouping_stdev, range(5, 8)):
        stdev = statistics.pstdev(indivi_stat_group[x])
        second_grouping_stdev[key] = stdev
    for key, x in zip(third_grouping_stdev, range(8, 12)):
        stdev = statistics.pstdev(indivi_stat_group[x])
        third_grouping_stdev[key] = stdev


def totals_to_avg_calc():
    #Calculates the averages of each of the groupings based on the number of hof batters
    for num in first_player_totals:
        first_grouping_totals[num]=first_grouping_totals[num]/len(hof_list)
    for num in second_player_totals:
        second_grouping_totals[num]=second_grouping_totals[num]/len(hof_list)
    for num in third_player_totals:
        third_grouping_totals[num]=third_grouping_totals[num]/len(hof_list)

def points_determination():
    #Calculates
    total_points=0
    for player_stat_name_key, group_stat_name_key, st_dev_key in zip(first_player_totals, first_grouping_totals, first_grouping_stdev):
        stat_diff= first_player_totals[player_stat_name_key] - first_grouping_totals[group_stat_name_key]
        total_points = points_calc(stat_diff, first_grouping_stdev, st_dev_key, total_points)
    for player_stat_name_key, group_stat_name_key, st_dev_key in zip(second_player_totals, second_grouping_totals, second_grouping_stdev):
        stat_diff= second_player_totals[player_stat_name_key] - second_grouping_totals[group_stat_name_key]
        total_points = points_calc(stat_diff, second_grouping_stdev, st_dev_key, total_points)
    for player_stat_name_key, group_stat_name_key, st_dev_key in zip(third_player_totals, third_grouping_totals, third_grouping_stdev):
        stat_diff= third_player_totals[player_stat_name_key] - third_grouping_totals[group_stat_name_key]
        total_points = points_calc(stat_diff, third_grouping_stdev, st_dev_key, total_points)
    if total_points>=0:
        print("Based on stat totals and batting stats, the player should be in the HoF")
    else:
        print("Based on stat totals and batting stats, the player should not be in the HoF")

def points_calc(stats_difference, st_dev_dict, st_dev_key, total_points):
    #Calculates the number of points for the difference in standard deviation of the stat
    #If the player has a stat difference greater than the hof average then points will be added to their score
    #If the player has a stat difference less than the hof average then points will be taken away from their score
    #Has 4 different parameters
    #Stats_difference - difference between the player stat and hof avg
    #St_dev_dict - dictionary containing the standard deviation for each stat
    #St_dev_key - key for each stat in the standard deviation dictionary
    #Total_points - total points for the player
    if stats_difference==0:
        return total_points
    elif stats_difference<0:
        remainder = stats_difference / st_dev_dict[st_dev_key]
        if remainder == 1:
            return total_points - 1
        elif remainder == 2:
            return total_points - 2
        else:
            return total_points - 3
    else:
        remainder = stats_difference / st_dev_dict[st_dev_key]
        if remainder == 1:
            return total_points + 1
        elif remainder == 2:
            return total_points + 2
        else:
            return total_points + 3

player_name = input("Name a player in baseball to determine if they belong in the HoF: ")
temp_name = name_changer(player_name).lower()
first_letter = temp_name[0:1].lower()
URL = f"https://www.baseball-reference.com/players/{first_letter}/{temp_name}01.shtml"
#Note: If the player's name is repeated on baseball reference, there may be potential for error
#Note: I plan to add in the future the ability for the system to check based on stats if it is the correct player
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
first_results = soup.findAll("div", attrs={"class": "p1"})
second_results = soup.findAll("div", attrs={"class": "p2"})
third_results = soup.findAll("div", attrs={"class": "p3"})
first_player_totals = {"WAR": 0, "AB": 0, "H": 0, "HR": 0, "BA": 0}
second_player_totals= {"R": 0, "RBI": 0, "SB": 0}
third_player_totals= {"OBP": 0, "SLG": 0, "OPS": 0, "OPS+": 0}
for x in first_results:
    for p, stat_name in zip(x.findAll('p'), first_player_totals):
        temp = float(p.text)
        first_player_totals[stat_name]=temp
for x in second_results:
    for p, stat_name in zip(x.findAll('p'), second_player_totals):
        temp = float(p.text)
        second_player_totals[stat_name]=temp
for x in third_results:
    for p, stat_name in zip(x.findAll('p'), third_player_totals):
        temp = float(p.text)
        third_player_totals[stat_name]=temp

hof_database_creator()
stdev_calc()
totals_to_avg_calc()
points_determination()

