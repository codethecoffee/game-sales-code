import csv


def parse(filename):
    '''
    takes a filename and returns attribute information
    '''
    # initialize variables

    raw_data = []
    csvfile = open(filename, 'r')
    fileToRead = csv.reader(csvfile)

    headers = next(fileToRead)

    for row in fileToRead:
        raw_data.append(dict(zip(headers, row)))

    for game in raw_data:
        NA, EU = (game["NA_Sales"], "NA"), (game["EU_Sales"], "EU")
        JP, Other = (game["JP_Sales"],
                     "JP"), (game["Other_Sales"], "Other")

        sales = sorted([NA, EU, JP, Other], key=lambda x: x[0], reverse=True)
        # Greatest_Sales: the region the game sold the most copies in
        game["Greatest_Sales"] = sales[0][1]
        # print(game + "\n")

    return raw_data


if __name__ == "__main__":
    parse("data/game_data.csv")
