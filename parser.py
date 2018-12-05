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

    normalizeData(raw_data)

    for game in raw_data:
        # Greatest_Norm
        NA, EU = (game["NA_Norm"], "NA"), (game["EU_Norm"], "EU")
        JP, Other = (game["JP_Norm"],
                     "JP"), (game["Other_Norm"], "Other")

        norms = sorted([NA, EU, JP, Other], key=lambda x: x[0], reverse=True)
        # Greatest_Sales: the region the game sold the most copies in
        game["Greatest_Sales"] = norms[0][1]

        deleteFields(game)
        print(game)
        print("\n")

    return raw_data


def normalizeData(raw_data):
    num_entries = len(raw_data)
    print("{} entries".format(num_entries))
    max_NA, max_EU, max_JP, max_Other = 0, 0, 0, 0

    for game in raw_data:
        max_NA = max(float(game["NA_Sales"]), max_NA)
        max_EU = max(float(game["EU_Sales"]), max_EU)
        max_JP = max(float(game["JP_Sales"]), max_JP)
        max_Other = max(float(game["Other_Sales"]), max_Other)

    for game in raw_data:
        game["NA_Norm"] = float(game["NA_Sales"]) / max_NA
        game["EU_Norm"] = float(game["EU_Sales"]) / max_EU
        game["JP_Norm"] = float(game["JP_Sales"]) / max_JP
        game["Other_Norm"] = float(game["Other_Sales"]) / max_Other


def deleteFields(entry):
    # Delete the name for now
    # Add ability to parse the name/bag of words?
    del entry["Name"]

    # Including platform makes the tree perform at 63%
    # efficiency
    del entry["Platform"]

    # The number of sales is not an attribute we should
    # consider; it's the result!
    del entry["NA_Sales"]
    del entry["EU_Sales"]
    del entry["JP_Sales"]
    del entry["Other_Sales"]
    del entry["Global_Sales"]
    del entry["NA_Norm"]
    del entry["EU_Norm"]
    del entry["JP_Norm"]
    del entry["Other_Norm"]

    # TODO: Somehow accommodate for continuous values like
    # scores in our binary decision tree
    del entry["Critic_Score"]
    del entry["User_Score"]
    del entry["User_Count"]
    del entry["Critic_Count"]
    del entry["Year_of_Release"]


if __name__ == "__main__":
    parse("data/game_data.csv")
