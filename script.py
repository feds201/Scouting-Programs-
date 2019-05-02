import xlwt
import requests

''' Use pip3 to install xlwt and requests.'''
''' Made by Karan Arora.'''

# Useful links for me
    # https://www.thebluealliance.com/api/v3/events/2019/keys?X-TBA-Auth-Key=4lrD467ePfemtjf19Wga60f2xKg0yDn4qVvDjLByw12EbwQ8jDgJhO5zFX1m7qgG
        # Link to all of the keys for this year
    # https://www.thebluealliance.com/api/v3/events/2019?X-TBA-Auth-Key=4lrD467ePfemtjf19Wga60f2xKg0yDn4qVvDjLByw12EbwQ8jDgJhO5zFX1m7qgG
        # Link to all of the events for this year (more useful)

# Figure out if having text or integers matters or not in excel
# LOOK OVER ALL OTHER DATA
# no totals

# TODO
    # Minor stuff (probably next year)
        # Make Excel Sheet look nicer
        #Make APP that has QR codes and has cycle times by allowing you to hit a button and recording the time between the hits
        #TALK TO 1188
        # GZIP
        # WEBHOOKS
        # Look into checking if stuff was modified or not
        # Make sure X-TBA Auth Key doesn't expire
        # Make code modularized
        # Make something that grabs data from all rest of the API, user doesnt have to go searching through links and can instead just enter options through script

    # Questions
        # Do they care about comp level and the order of matches?
        # Check through all of the data's meaning on FRCAPIARY with Nikhil and Tejas, delete unecessary stuff, make sure they don't want any other data
            # Confirm meaning of all statistics - specifically fouls, sandstorm data, and total (sandstorm bonus points?)
        # Do they have a way of tracking fouls for each team. if a robot breaks?
        # Ask if they want a GUI
        # Think of other ways I could help them, program some kind of data analyzer?
        # Any other data they would like output to files, maybe like teams that were DQED add that to an external txt file?
        # DQed teams?
        # Surrogate team keys?

    # Current
        # Confirm data matches BlueAlliance API
        # Go through code line by line and make sure everything makes sense, no logical errors
        # Maybe scrape BlueAlliance website as well
        # - Add cross checker
        # Add effectiveness in saving cargo from prematch
        # Update backup script
        # Revise raw data
        # Push to FEDS Github
        # Eventualy move match number column to beginning
        # Calculate if hatch fell out?
        #Confirm prematch cargo efficiency counter works
        # Write email to Nikhil and Tejas - prematch efficiency counter yet to work, actual match number, don't have to type number anymore, writes available videos of each match to another file, cross checker hard to get working, cargo cannot be negative anymore, hatches can still be negative but i left it in, can explain later if needed, ask if they want to know if a team was disqualified, fouls, overall changes that restructured code slightly and made it easier to read, keep the old copy of the code on your computer just in case this one has some issues at marysville, null hatch panels mess everything up, there is a way the score and the total number pf panels can differ but whatever


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

# Get data
r = requests.get("https://www.thebluealliance.com/api/v3/event/" + match_key + "/matches", headers=headers).json()

# Create spreadsheet and add red and blue sheets
file = xlwt.Workbook()
red = file.add_sheet("Red Alliance")
blue = file.add_sheet("Blue Alliance")

sheets = (red, blue)
teams = ("red", "blue")

video_message = ""
raw_data_message = ""

columns = {"record#": 0, "teams": 1, "starting_level": 2, "sstorm_action": 3, "bonus": 4, "sstorm_total": 5, "cargo": 6,
           "panels": 7, "comp_NR": 8, "comp_FR": 9, "hatch_pts": 10, "cargo_pts": 11, "endgame": 12, "hab_pts": 13,
           "teleop_pts": 14, "adjust_pts": 15, "comp_R_RP": 16, "hab_rp": 17, "foul_count": 18, "tech_foul_count": 19,
           "foul_pts": 20, "total_pts": 21, "winner": 22, "total_rp": 23, "match#": 24, "efficiency": 25}

# List of necessary headings - labels is not used for anything
labels = ("General", "Sandstorm", "Teleop", "Endgame/Totals", "Fouls", "Final Stats", "Fix Later")

labels2 = ("Record #", "Robots", "Starting Spot", "SStorm Action",

           "Bonus Points", "Total Auto Pts",

           "Total Cargo", "Total Panels",
                          
           # N = Near, F = Far
           "N Rocket Complete", "F Rocket Complete",

           "Hatch Points", "Cargo Points", "Endgame Action", "Total HAB Points",
           "Total Teleop Points", "Adjust Points",

           "Completed Rocket RP", "HAB RP",

           "Foul Count", "Tech Foul Count", "Foul Points Earned",

           "Total Points", "Win/Lose", "Total RP",
           
           "Match #", "Efficiency")

# Add labels in first row
for s in sheets:
    s.write(0, columns["record#"], "General")
    s.write(0, columns["starting_level"], "Sandstorm")
    s.write(0, columns["cargo"], "Teleop")
    s.write(0, columns["endgame"], "Endgame/Totals")
    s.write(0, columns["foul_count"], "Fouls")
    s.write(0, columns["total_pts"], "Final Stats")
    s.write(0, columns["match#"], "Fix Later")

# Add match numbers
row = 0

for match in range(len(r)):
    for s in sheets:
        s.write(row + 2, columns["record#"], match + 1)
    row += 3

# Add labels in second row
for l in range(len(labels2)):
    for s in sheets:
        s.write(1, l, labels2[l])

# Fill in data
current_row = 2

cargo = 0
panels = 0
cargo_list = []

for match in range(len(r)):
    try:
        for team in range(2):
            sheet = sheets[team]

            # Add team numbers
            for team_key in range(3):
                data = r[match]["alliances"][teams[team]]["team_keys"][team_key]
                sheet.write(current_row + team_key, columns["teams"], int(data.replace("frc", "")))

            data = r[match]["score_breakdown"][teams[team]]

            # Starting level of robot
            for robot in range(3):
                temp = data["preMatchLevelRobot" + str(robot+1)]
                sheet.write(current_row + robot, columns["starting_level"], temp)

            # Sandstorm action of each robot
            for robot in range(3):

                temp = data["habLineRobot" + str(robot+1)]

                if temp == "CrossedHabLineInSandstorm":
                    temp = "CrossedHabInStorm"

                elif temp == "CrossedHabLineInTeleop":
                    temp = "CrossedHabInTeleop"

                sheet.write(current_row + robot, columns["sstorm_action"], temp)

            # Sandstorm bonus and total
            sheet.write(current_row, columns["bonus"], data["sandStormBonusPoints"])
            sheet.write(current_row, columns["sstorm_total"], data["autoPoints"])

            # Cargo and panel counter - also counts number of pre-match cargo an alliance was able to save
            temp = 0

            for count in ["1", "2", "3", "6", "7", "8"]:
                '''if "Cargo" in str(data["preMatchBay" + count]):
                    cargo -= 1'''

                if "Cargo" in str(data["preMatchBay" + count]):
                    cargo_list.append("bay" + count)
                if "Panel" in str(data["preMatchBay" + count]):
                    panels -= 1

            for count in range(8):
                if "Cargo" in str(data["bay" + str(count + 1)]):
                    cargo += 1

                    ''' If the bay was filled with cargo before the match and ended with it after the match, it is 
                        reasonable to assume that the alliance was successful in placing a hatch for the bay during the
                        sandstorm. '''

                    if ("bay" + str(count + 1)) in cargo_list:
                        temp += 1

                if "Panel" in str(data["bay" + str(count + 1)]):
                    panels += 1

            for word in ("Near", "Far"):
                for word2 in ("Left", "Right"):

                    if "Cargo" in data["low" + str(word2) + "Rocket" + str(word)]:
                        cargo += 1
                    if "Panel" in data["low" + str(word2) + "Rocket" + str(word)]:
                        panels += 1

                    if "Cargo" in data["mid" + str(word2) + "Rocket" + str(word)]:
                        cargo += 1
                    if "Panel" in data["mid" + str(word2) + "Rocket" + str(word)]:
                        panels += 1

                    if "Cargo" in data["top" + str(word2) + "Rocket" + str(word)]:
                        cargo += 1
                    if "Panel" in data["top" + str(word2) + "Rocket" + str(word)]:
                        panels += 1

            sheet.write(current_row, columns["cargo"], cargo)
            sheet.write(current_row, columns["panels"], panels)

            temp = str(temp) + "/" + str(len(cargo_list))
            sheet.write(current_row, columns["efficiency"], temp)

            # Rockets are completed
            temp = str(data["completedRocketNear"])

            if temp == "False":
                temp = "No"
            elif temp == "True":
                temp = "Yes"

            sheet.write(current_row, columns["comp_NR"], temp)

            temp = str(data["completedRocketFar"])

            if temp == "False":
                temp = "No"
            elif temp == "True":
                temp = "Yes"

            sheet.write(current_row, columns["comp_FR"], temp)

            # Hatch panel points
            sheet.write(current_row, columns["hatch_pts"], data["hatchPanelPoints"])

            # Cargo points
            sheet.write(current_row, columns["cargo_pts"], data["cargoPoints"])

            # Endgame action
            for robot in range(3):
                temp = data["endgameRobot" + str(robot + 1)]
                sheet.write(current_row + robot, columns["endgame"], temp)

            # Total HAB climbing points
            sheet.write(current_row, columns["hab_pts"], data["habClimbPoints"])

            # Total teleop points
            sheet.write(current_row, columns["teleop_pts"], data["teleopPoints"])

            # Adjust points (remove later if needed)
            sheet.write(current_row, columns["adjust_pts"], data["adjustPoints"])

            # Completed rocket ranking point
            temp = str(data["completeRocketRankingPoint"])

            if temp == "False":
                temp = 0
            elif temp == "True":
                temp = 1

            sheet.write(current_row, columns["comp_R_RP"], temp)

            # HAB docking ranking point
            temp = str(data["habDockingRankingPoint"])

            if temp == "False":
                temp = 0
            elif temp == "True":
                temp = 1

            sheet.write(current_row, columns["hab_rp"], temp)

            # Fouls
            sheet.write(current_row, columns["foul_count"], data["foulCount"])
            sheet.write(current_row, columns["tech_foul_count"], data["techFoulCount"])
            sheet.write(current_row, columns["foul_pts"], data["foulPoints"])

            # Total points
            sheet.write(current_row, columns["total_pts"], data["totalPoints"])

            # Win or lose (potential source for error due to if-else?)
            temp = str(r[match]["winning_alliance"])

            if temp == teams[team]:
                temp = "Win"
            else:
                temp = "Loss"

            sheet.write(current_row, columns["winner"], temp)

            # Total ranking points
            sheet.write(current_row, columns["total_rp"], data["rp"])

            # Actual match number
            temp = r[match]["key"]
            temp = temp.replace(match_key + "_", "")
            sheet.write(current_row, columns["match#"], temp)

            # Make sure data is correct - assumes that null hatch panels don't fall off
            if panels >= 0 and panels * 2 != int(data["hatchPanelPoints"]):
                print("WARNING (Record " + str(match) + "): Number of panels *2 doesn't equal total hatch panel points")

            if cargo >= 0 and cargo * 3 != int(data["cargoPoints"]):
                print("WARNING (Record " + str(match) + "): Number of cargo *2 doesn't equal total cargo points")

            # Reset cargo and panels
            cargo = 0
            panels = 0
            cargo_list.clear()

    except TypeError as e:
        print("Ends at Record " + str(match))
        print(e)

    current_row += 3

    # Add video to message
    video_message += str(match + 1) + ": "
    temp = r[match]["videos"]

    for video in temp:
        if video["type"] == "youtube":
            video_message += ("youtube.com/watch?v=" + str(video["key"]) + ", ")
        else:
            video_message(str(video["key"] + "(video type is " + video["type"] + ")" + ", "))

    video_message += "\n"

# Write raw data to file
try:
    raw_data_file = open("rawdata.json", "w")

    for entry in r:
        raw_data_file.write(str(entry))
        raw_data_file.write("\n \n")

    raw_data_file.close()

except IOError as e:
    print("WARNING: IOError in writing raw data to file")
    print(e)

# Write video data to file
try:
    video_file = open("videos.txt", "w")
    video_file.write(video_message)
    video_file.close()

except IOError as e:
    print("WARNING: IOError in writing videos to file")
    print(e)

file.save(file_name + ".xls")
