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
        deleteFields(game)
        print(game)
        print("\n")

    return raw_data


def deleteFields(entry):
    # Delete the name for now
    # Add ability to parse the name/bag of words?
    del entry["Name"]

    del entry["Platform"]
    del entry["NA_Sales"]
    del entry["EU_Sales"]
    del entry["JP_Sales"]
    del entry["Other_Sales"]
    del entry["Global_Sales"]

    # TODO: Somehow accommodate for continuous values like
    # scores in our binary decision tree
    del entry["Critic_Score"]
    del entry["User_Score"]
    del entry["User_Count"]
    del entry["Critic_Count"]


if __name__ == "__main__":
    parse("data/game_data.csv")
