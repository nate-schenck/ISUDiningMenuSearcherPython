import requests as rq
import time
import datetime
import json


keyword = input("Search keyword: ")

days = input("How many days to search? ")

while not days.isdigit():
    print("Please enter a number.\nHow many days to search?")
    days = input()
    
print(f"Searching the next {days} days for \"{keyword}\"...")

curr_millis = round(time.time())

dining_center_ids = {"union-drive-marketplace-2-2", "seasons-marketplace-2-2", "conversations-2", "friley-windows-2-2"}

results_dictionary = [["Item", "Location", "Venue", "Time", "Date"]]

results_found = 0

print(f"Results Found: {results_found}", end='\r')

for i in range(int(days)):
    millis = curr_millis + i * 86400
    for dc_id in dining_center_ids:
        req_head = rq.head(f"https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug={dc_id}&time={millis}")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
        header = {"User-Agent": user_agent} #
        response = rq.get(f"https://www.dining.iastate.edu/wp-json/dining/menu-hours/get-single-location/?slug={dc_id}&time={millis}", headers=header, timeout=5)
        try:
            response.raise_for_status()
        except rq.HTTPError:
            continue
        try:
            json.loads(response.text)
        except ValueError:
            continue
        data = response.json()
        for menu in data[0]["menus"]:
            for menuDisplay in menu["menuDisplays"]:
                for category in menuDisplay["categories"]:
                    for menuItem in category["menuItems"]:
                        name_to_compare = str(menuItem["name"]).lower()
                        keyword_to_compare = keyword.lower()
                        if name_to_compare.find(keyword_to_compare) != -1:
                            dc_name = str(dc_id)
                            dc_name = dc_name.replace("-", " ")
                            dc_name = dc_name.replace("2", "")
                            dc_name = dc_name.capitalize()
                            results_dictionary.append([str(menuItem["name"]), dc_name, str(menuDisplay["name"]), str(menu["section"]), str(datetime.date.fromtimestamp(millis))])
                            results_found += 1
                            print(f"Results Found: {results_found}", end='\r')
print('\n')

for result in results_dictionary:
    item = str(result[0]).center(50)
    loc = str(result[1]).center(25)
    venue = str(result[2]).center(20)
    time = str(result[3]).center(10)
    date = str(result[4]).center(12)
    print(item + loc + venue + time+ date + "\n")
    
input("Press ENTER to exit")
