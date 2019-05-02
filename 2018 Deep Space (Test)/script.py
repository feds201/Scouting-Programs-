import xlwt
import requests

#Include what the robot did at the end (climbing, levitate, parking)
#Confirm what to do with powerups (played vs total?)
#Confirm meaning of all statisitics - specifically fouls
#Figure out if having text or integers matters or not in excel

#Tell nikhil to look over API
#Fix ordering of matches
#Use for loop to shorten series of write statements

headers = {"X-TBA-Auth-Key": "4lrD467ePfemtjf19Wga60f2xKg0yDn4qVvDjLByw12EbwQ8jDgJhO5zFX1m7qgG",
           "User-agent": "Mozilla/5.0"}

url = "https://www.thebluealliance.com/api/v3/"

r = requests.get("https://www.thebluealliance.com/api/v3/event/2018miwat/matches", headers=headers).json()

file = xlwt.Workbook()
red = file.add_sheet("Red Alliance")
blue = file.add_sheet("Blue Alliance")

sheets = (red, blue)
teams = ("red", "blue")
labels1 = ("General", "Autonomous Run Points", "Auto Ownership (seconds)", "Tele-Op Ownership (seconds)", "Power-Ups",
           "Endgame Points", "Ranking Points")
labels2 = ("Match", "Robots", "By Robot", "Run Total", "Scale", "Switch", "Owner Points", "Auto Total", "Scale",
           "Switch", "Owner Points", "Force", "Levitate", "Boost", "Vault Points", "By Robot", "Endgame Total",
           "Tele-op Points", "Auto Quest", "Face the Boss", "Fouls", "Points Earned")

for s in sheets:
    s.write(0, 0, "General")
    s.write(0, 2, "Autonomous Run Points")
    s.write(0, 4, "Auto Ownership (seconds)")
    s.write(0, 8, "Tele-Op Ownership (seconds)")
    s.write(0, 11, "Power-Ups (# of Cubes When Played)")
    s.write(0, 15, "Endgame Points")
    s.write(0, 18, "Ranking Points")

#Add match numbers
row = 0

for match in range(96):
    for s in sheets:
        s.write(row + 2, 0, match + 1)
    row += 3

#Add labels in second row
for label in range(len(labels2)):
    for s in sheets:
        s.write(1, label, labels2[label])

row = 0

#Fill in remaining data
current_row = 0

for match in range(97):
    for team in range(2):
        sheet = sheets[team]

        #Add team numbers
        for team_key in range(3):
            data = r[match]["alliances"][teams[team]]["team_keys"][team_key]
            sheet.write(current_row + team_key + 2, 1, int(data.replace("frc", "")))

        #Auto action of robot
        for robot in range(3):
            data = r[match]["score_breakdown"][teams[team]]["autoRobot" + str(robot+1)]

            #Data could also be unknown
            if data == "AutoRun":
                data = 5
            else:
                data = 0

            sheet.write(current_row + robot + 2, 2, data)

        data = r[match]["score_breakdown"][teams[team]]

        #Number of points earned for AutoRun by the alliance
        sheet.write(current_row + 2, 3, data["autoRunPoints"])

        #Seconds of Ownership by the Alliance in Auto
        sheet.write(current_row + 2, 4, data["autoScaleOwnershipSec"])

        #Seconds of Ownership by the Alliance in Auto
        sheet.write(current_row + 2, 5, data["autoSwitchOwnershipSec"])

        #Number of points earned for Switch/Scale Ownership in Auto
        sheet.write(current_row + 2, 6, data["autoOwnershipPoints"])

        #Total number of points earned in the Auto stage
        sheet.write(current_row + 2, 7, data["autoPoints"])

        #Seconds of Ownership by the Alliance in Teleop (includes force, but not boost)
        sheet.write(current_row + 2, 8, data["teleopScaleOwnershipSec"])

        #Seconds of Ownership by the Alliance in Teleop (includes force, but not boost)
        sheet.write(current_row + 2, 9, data["teleopSwitchOwnershipSec"])

        #Number of points earned for Switch/Scale Ownership in Teleop
        sheet.write(current_row + 2, 10, data["teleopOwnershipPoints"])

        #Number of Power Cubes in the Force Boost column when Powerup was played (or 0 for not played)
        sheet.write(current_row + 2, 11, data["vaultBoostPlayed"])

        #Number of Power Cubes in the Force vault column when Powerup was played (or 0 for not played)
        sheet.write(current_row + 2, 12, data["vaultForcePlayed"])

        #3 if Levitate was played, or 0 for not played
        sheet.write(current_row + 2, 13, data["vaultLevitatePlayed"])

        #Number of points earned for Power Cubes in the Vault (does not include points for any benefits, like Ownership)
        sheet.write(current_row + 2, 14, data["vaultPoints"])

        #Total number of points earned in the Teleop stage (includes Endgame and Vault)
        sheet.write(current_row + 2, 17, data["teleopPoints"])

        #Whether or not the Auto Quest Ranking Point was achieved
        if bool(data["autoQuestRankingPoint"]):
            sheet.write(current_row + 2, 18, 1)
        else:
            sheet.write(current_row + 2, 18, 0)

        #Whether or not the Face The Boss Ranking Point was achieved
        if bool(data["faceTheBossRankingPoint"]):
            sheet.write(current_row + 2, 19, 1)
        else:
            sheet.write(current_row + 2, 19, 0)

    current_row += 3

file.save("Waterford Data.xls")
