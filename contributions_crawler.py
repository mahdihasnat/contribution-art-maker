import requests
from typing import Dict
from icecream import ic
from bs4 import BeautifulSoup
from datetime import date

def get_contributions(username: str, year: int) -> Dict[date, int]:
    # get request to the following url with appropriate parameters
    # https://github.com/users/mahdihasnat/contributions?from=2022-12-01&to=2022-12-31
    url = f"https://github.com/users/{username}/contributions?from={year}-01-01&to={year}-12-31"
    ic(url)
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch contributions: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    contributions = {}

    # Locate the contribution calendar table
    table = soup.find("table", {"class": "js-calendar-graph-table"})
    if not table:
        raise Exception("Could not find contribution graph in the response")

    ic(len(table))


    table_datas = table.find_all("td", {"class": "ContributionCalendar-day"})
    ic(len(table_datas))

    tool_tips = table.find_all("tool-tip")
    ic(len(tool_tips))

    if len(table_datas) != len(tool_tips):
        raise Exception("Number of table data and tool tips do not match")


    def parseContribution(text: str) -> int:
        # No contributions on January 2nd.
        # 1 contribution on January 23rd.
        # 2 contributions on January 24th.
        text = text.strip()
        text = text.split("contribution")[0]
        text = text.strip()
        if text == "No":
            return 0
        else:
            return int(text)

    contributions_for_data_ids = {}
    for tool_tip in tool_tips:
        contributions_for_data_ids[tool_tip["for"]] = parseContribution(tool_tip.contents[0])


    for table_data in table_datas:
        date_str = table_data["data-date"]
        date_obj = date.fromisoformat(date_str)
        contributions[date_obj] = contributions_for_data_ids[table_data["id"]]

    return contributions

contributions = get_contributions("mahdihasnat", 2020)
ic(len(contributions))