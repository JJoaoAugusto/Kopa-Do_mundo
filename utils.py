from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError
from datetime import datetime, timedelta, date

cup_years = [1930,]

for year in cup_years:
    if year < 2022:
        new_year = year + 4
        cup_years.append(new_year)


def data_processing(team):
    cup_year = datetime.strptime(team["first_cup"], "%Y-%m-%d")
    disputed_cups = [cup_year.year,]
    for year in disputed_cups:
        if year < 2022:
            new_year = year + 4
            disputed_cups.append(new_year)
    if team["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")
    if cup_year.year not in cup_years:
        raise InvalidYearCupError("there was no world cup this year")
    if team["titles"] > len(disputed_cups):
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
    return team
