import numpy as np
import MySQLdb
import os
import json


db = MySQLdb.connect(user="root",db="nfl_pbp",read_default_file="~/.my.cnf")
team_query = db.cursor() #query tool for teams
oplay = db.cursor() #query tool for original plays
count = 0
punting = ()
field_goal = ()
o_down_distance = ()
d_down_distance = ()
o_drive_results = ()
d_drive_results = ()


for year in range(2002,2003):
    team_query.execute("""select distinct offense from pbp order by offense asc""")
    team = team_query.fetchall()
    path = "/home/tim/nfl_pbp/"+str(year)+"/"
    if not os.path.exists(path):
        os.mkdir(path)
    for j in range(np.shape(team)[0]):
        team_name = team[j][0] #teams name in alphabetical order
        path_team = path+team_name
        if not os.path.exists(path_team):
            os.mkdir(path_team)
        print team_name,year
        ######################SPECIAL TEAMS#####################
        #Net Punting (offense)
        oplay.execute("""select net_yds,ydline from pbp where play_type like 'punt' and offense = %s and season = %s""",(team_name,year,))
        punt = oplay.fetchall()
        punt_outfile = path_team+"/punt.json"
        with open(punt_outfile,'w') as outfile:
             json.dump(punt,outfile)
        #Field Goals
        oplay.execute("""select end_drive,points from drive where result like '%%field goal%%' and offense = %s and season = %s""",(team_name,year,))
        fg = oplay.fetchall()
        fg_outfile = path_team+"/fg.json"
        with open(fg_outfile,'w') as outfile:
             json.dump(fg,outfile)
        ######################OFFENSE###########################
        #First/Second/Third/Fourth Down (yards gained,togo,ydline)
        for down in range(1,5):
            oplay.execute("""select net_yds,togo,ydline,defense from pbp where play_type like 'play' and play_type not like 'penalty' and down = %s and offense = %s and season = %s and abs(offscore-defscore)<=24""",(down,team_name,year,))
            odd = oplay.fetchall()
            down_outfile = path_team+"/o_down_"+str(down)+".json"
            with open(down_outfile,'w') as outfile:
               json.dump(odd,outfile)
        #Drive (start,fin,result,points gained)
        oplay.execute("""select start_drive,end_drive,defense,result,points from drive where offense = %s and season = %s and abs(home_score-away_score)<=24""",(team_name,year,))
        odsfrp = oplay.fetchall()
        drive_outfile = path_team+"/o_drive.json"
        with open(drive_outfile,'w') as outfile:
             json.dump(odsfrp,outfile)
        #####################DEFENSE#############################
        #First/Second/Third/Fourth Down (yards gained,togo,ydline)
        for down in range(1,5):
            oplay.execute("""select net_yds,togo,ydline,offense from pbp where play_type like 'play' and play_type not like 'penalty' and down = %s and defense = %s and season = %s and abs(offscore-defscore)<=24""",(down,team_name,year,))
            ddd = oplay.fetchall()
            down_outfile = path_team+"/d_down_"+str(down)+".json"
            with open(down_outfile,'w') as outfile:
               json.dump(ddd,outfile)
        #Drive (start,fin,result,points gained)
        oplay.execute("""select start_drive,end_drive,result,points from drive where offense = %s and season = %s and abs(home_score-away_score)<=24""",(team_name,year,))
        ddsfrp = oplay.fetchall()
        drive_outfile = path_team+"/d_drive.json"
        with open(drive_outfile,'w') as outfile:
             json.dump(ddsfrp,outfile)
