import xlwt
import requests

# Useful links for me
    # https://www.thebluealliance.com/api/v3/events/2019/keys?X-TBA-Auth-Key=4lrD467ePfemtjf19Wga60f2xKg0yDn4qVvDjLByw12EbwQ8jDgJhO5zFX1m7qgG
        # Link to all of the keys for this year
    # https://www.thebluealliance.com/api/v3/events/2019?X-TBA-Auth-Key=4lrD467ePfemtjf19Wga60f2xKg0yDn4qVvDjLByw12EbwQ8jDgJhO5zFX1m7qgG
        # Link to all of the events for this year (more useful)

# TODO
    # Fix headings

''' READ: THIS FILE IS ONLY TO BE USED IF YOU MANUALLY WANT TO CONFIRM THE CARGO AND PANEL TOTALS FROM SCRIPT.PY'''

##################################  FOR NIKHIL AND TEJAS TO EDIT  ###########################################

''' Enter match key and what you want the file name to be. 
    READ: The match keys for the Southfield Competition and the Marysville Competition are, respectively, 
    2019misou and 2019mimar. The key for the Week 0 competition is 2019week0 (if you need this for some reason). 
    Put the correct key in for each competition. If the keys somehow don't work (yikes) visit the second link in
    the top of the program and use the filter bar in the top right of the website. '''

match_key = "2019misou"
file_name = "Week0_DeepSpace"


''' READ: If using Chrome put Chrome/72.0.3626.109 instead of Mozilla/5.0 between the quotes next to user-agent.
    Not sure if this really matters but do it just in case. Now that I think about it this really shouldn't matter
    at all but whatever. '''

headers = {"X-TBA-Auth-Key": "4lrD467ePfemtjf19Wga60f2xKg0yDn4qVvDjLByw12EbwQ8jDgJhO5zFX1m7qgG",
           "User-agent": "Mozilla/5.0"}

############################################################################################################


url = "https://www.thebluealliance.com/api/v3/"

r = requests.get("https://www.thebluealliance.com/api/v3/event/" + match_key + "/matches", headers=headers).json()

file = xlwt.Workbook()
red = file.add_sheet("Red Alliance")
blue = file.add_sheet("Blue Alliance")

sheets = (red, blue)
teams = ("red", "blue")

# Write data to file
try:
    raw_data_file = open("rawdata.json", "w")

    for entry in r:
        raw_data_file.write(str(entry))
        raw_data_file.write("\n \n")

except IOError:
    print("WARNING: IOError")
    pass

labels = ("General", "Sandstorm", "Teleop", "Endgame", "Ranking Points")

labels2 = ("Record #", "Robots", "Starting Spot", "SStorm Action",

           "Bonus Points", "Total Auto Pts",

           # T = Top, M = Middle, B = Bottom, L = Left, R = Right, N = Near, F = Far
           "TL N Rocket", "TR N Rocket", "ML N Rocket", "MR N Rocket", "BL N Rocket", "BR N Rocket",
           "N Rocket Complete",

           "TL F Rocket", "TR F Rocket", "ML F Rocket", "MR F Rocket", "BL F Rocket", "BR F Rocket",
           "F Rocket Complete",

           "Pre-Storm Bay 1", "Pre-Storm Bay 2", "Pre-Storm Bay 3", "Pre-Storm Bay 6",
           "Pre-Storm Bay 7", "Pre-Storm Bay 8",

           "Bay 1", "Bay 2", "Bay 3", "Bay 4", "Bay 5", "Bay 6", "Bay 7", "Bay 8",

           "Hatch Points", "Cargo Points", "Endgame Action", "Total HAB Points",
           "Total Teleop Points", "Adjust Points",

           "Completed Rocket RP", "HAB RP",

           "Foul Count", "Tech Foul Count", "Foul Points Earned",

           "Total Points", "Win/Lose", "Total RP")

# Add labels in first row
for s in sheets:
    s.write(0, 0, "General")
    s.write(0, 2, "Sandstorm")
    s.write(0, 6, "Teleop")
    s.write(0, 20, "Endgame/Totals")
    s.write(0, 25, "Ranking Points")

# Add match numbers
row = 0

for match in range(len(r)):
    for s in sheets:
        s.write(row + 2, 0, match + 1)
    row += 3

# Add labels in second row
for label in range(len(labels2)):
    for s in sheets:
        s.write(1, label, labels2[label])

# Fill in data
current_row = 2

for match in range(len(r)):
    try:
        for team in range(2):
            sheet = sheets[team]

            # Add team numbers
            for team_key in range(3):
                data = r[match]["alliances"][teams[team]]["team_keys"][team_key]
                sheet.write(current_row + team_key, 1, int(data.replace("frc", "")))

            data = r[match]["score_breakdown"][teams[team]]

            # Starting level of robot
            for robot in range(3):
                temp = data["preMatchLevelRobot" + str(robot+1)]
                sheet.write(current_row + robot, 2, temp)

            # Sandstorm action of each robot
            for robot in range(3):

                temp = data["habLineRobot" + str(robot+1)]

                if temp == "CrossedHabLineInSandstorm":
                    temp = "CrossedHabInStorm"

                elif temp == "CrossedHabLineInTeleop":
                    temp = "CrossedHabInTeleop"

                sheet.write(current_row + robot, 3, temp)

            # Sandstorm bonus and total
            sheet.write(current_row, 4, data["sandStormBonusPoints"])
            sheet.write(current_row, 5, data["autoPoints"])

            # Near Rocket
            sheet.write(current_row, 6, data["lowLeftRocketNear"])
            sheet.write(current_row, 7, data["lowRightRocketNear"])
            sheet.write(current_row, 8, data["midLeftRocketNear"])
            sheet.write(current_row, 9, data["midRightRocketNear"])
            sheet.write(current_row, 10, data["topLeftRocketNear"])
            sheet.write(current_row, 11, data["topRightRocketNear"])

            temp = str(data["completedRocketNear"])

            if temp == "False":
                temp = "No"
            elif temp == "True":
                temp = "Yes"

            sheet.write(current_row, 12, temp)

            # Far Rocket
            sheet.write(current_row, 13, data["lowLeftRocketFar"])
            sheet.write(current_row, 14, data["lowRightRocketFar"])
            sheet.write(current_row, 15, data["midLeftRocketFar"])
            sheet.write(current_row, 16, data["midRightRocketFar"])
            sheet.write(current_row, 17, data["topLeftRocketFar"])
            sheet.write(current_row, 18, data["topRightRocketFar"])

            temp = str(data["completedRocketFar"])

            if temp == "False":
                temp = "No"
            elif temp == "True":
                temp = "Yes"

            sheet.write(current_row, 19, temp)

            # Pre-Sandstorm Bays
            sheet.write(current_row, 20, data["preMatchBay1"])
            sheet.write(current_row, 21, data["preMatchBay2"])
            sheet.write(current_row, 22, data["preMatchBay3"])
            sheet.write(current_row, 23, data["preMatchBay6"])
            sheet.write(current_row, 24, data["preMatchBay7"])
            sheet.write(current_row, 25, data["preMatchBay8"])

            # After match bays
            for count in range(8):

                temp = data["bay" + str(count+1)]

                if temp == "PanelAndCargo":
                    temp = "Both"

                sheet.write(current_row, 26 + count, temp)

            # Hatch panel points
            sheet.write(current_row, 34, data["hatchPanelPoints"])

            # Cargo points
            sheet.write(current_row, 35, data["cargoPoints"])

            # Endgame action
            for robot in range(3):
                temp = data["endgameRobot" + str(robot + 1)]
                sheet.write(current_row + robot, 36, temp)

            # Total HAB climbing points
            sheet.write(current_row, 37, data["habClimbPoints"])

            # Total teleop points
            sheet.write(current_row, 38, data["teleopPoints"])

            # Adjust points (remove later)
            sheet.write(current_row, 39, data["adjustPoints"])

            # Completed rocket ranking point
            temp = str(data["completeRocketRankingPoint"])

            if temp == "False":
                temp = 0
            elif temp == "True":
                temp = 1

            sheet.write(current_row, 40, temp)

            # HAB docking ranking point
            temp = str(data["habDockingRankingPoint"])

            if temp == "False":
                temp = 0
            elif temp == "True":
                temp = 1

            sheet.write(current_row, 41, temp)

            # Fouls
            sheet.write(current_row, 42, data["foulCount"])
            sheet.write(current_row, 43, data["techFoulCount"])
            sheet.write(current_row, 44, data["foulPoints"])

            # Total points
            sheet.write(current_row, 45, data["totalPoints"])

            # Win or lose (potential source for error due to if-else?)
            temp = str(r[match]["winning_alliance"])

            if temp == teams[team]:
                temp = "Win"
            else:
                temp = "Loss"

            sheet.write(current_row, 46, temp)

            # Total ranking points
            sheet.write(current_row, 47, data["rp"])

    except TypeError:
        print("Ends at " + str(match))

    current_row += 3

file.save(file_name + ".xls")
