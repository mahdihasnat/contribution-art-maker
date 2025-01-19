import requests
from typing import Dict, Tuple
from icecream import ic
from bs4 import BeautifulSoup
from datetime import date

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from datetime import date, timedelta


def get_contributions(username: str, year: int) -> Dict[date, Tuple[int, int]]:
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
        data_level = int(table_data["data-level"])
        date_obj = date.fromisoformat(date_str)
        contributions[date_obj] = (contributions_for_data_ids[table_data["id"]], data_level)

    return contributions




# Define the color mapping for data levels
colors = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}

# Function to generate a 7x52 grid based on input data
def draw_contribution_chart(contributions, year):
    # Create a 7x52 grid filled with zeros (default data-level 0)
    grid = np.zeros((7, 54), dtype=int)

    # Find the first Sunday of the year
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    current_date = start_date
    current_column = 0

    # Fill the grid with data-levels from the contributions
    while current_date <= end_date:

        current_row = current_date.isoweekday() % 7
        grid[current_row][current_column] = contributions.get(current_date, (0, 0))[1]
        if current_row == 6:
            current_column += 1
        current_date += timedelta(days=1)

    # Create a custom colormap
    cmap = mcolors.ListedColormap([colors[i] for i in range(5)])
    bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(15, 4))
    ax.imshow(grid, cmap=cmap, norm=norm, aspect="equal")

    # Customize the chart
    ax.set_yticks(range(7))
    ax.set_yticklabels(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
    ax.set_xticks(range(0, 52, 4))  # Add ticks every 4 weeks
    ax.set_xticklabels([f"Week {i}" for i in range(0, 52, 4)])
    ax.set_title("Contribution Chart")
    ax.grid(False)

    # Hide spines and ticks
    ax.spines[:].set_visible(False)
    ax.tick_params(left=False, bottom=False)

    plt.show()
    plt.savefig(f"contribution_chart_{year}.png")

year = 2023
contributions = get_contributions("mahdihasnat", year)
ic(len(contributions))

# Draw the chart
draw_contribution_chart(contributions, year)
