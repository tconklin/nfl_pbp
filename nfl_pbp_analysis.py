import numpy as np
import MySQLdb
import os
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def pbp_plotter(in_array,fname,year=2002,team_names='',title='',xlabel='',ylabel='',extent=[100,0,100,0],vmin=0,vmax=1):
    os.chdir('/home/tim/nfl_pbp/'+str(year))
    s = np.size(np.shape(in_array))
    o_or_d = ['o','d']
    if s > 2:
        for j in range(2):
            figname = fname+'_'+o_or_d[j]
            plt.clf()
            plt.imshow(np.transpose(in_array[:,:,j]),extent=extent, vmin=vmin, vmax=vmax, interpolation=None,aspect='auto')
            plt.colorbar()
            plt.xticks(range(np.size(team_names)),np.array(team_names),rotation=90)
            plt.ylabel(ylabel)
            plt.xlabel(xlabel)
            plt.title(title+' '+str(year))
            plt.savefig(figname)
    else:
        figname = fname
        plt.clf()
        plt.imshow(np.transpose(in_array[:,:]),extent=extent, vmin=vmin, vmax=vmax, interpolation=None,aspect='auto')
        plt.xticks(range(np.size(team_names)),np.array(team_names),rotation=90)
        plt.colorbar()
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(title+' '+str(year))
        plt.savefig(figname)

def net_punt_team(team,year):
    os.chdir('/home/tim/nfl_pbp/'+str(year)+'/'+team)
    net_punt = np.zeros((28,1))
    with open('punt.json','r') as infile:
        punt = json.load(infile)
    punt = np.array(punt)
    net_punt,yard_range,c = plt.hist(punt[:,0],normed=True,bins=28,range=(-60,80))
    return net_punt

def start_punt_team(team,year):
    os.chdir('/home/tim/nfl_pbp/'+str(year)+'/'+team)
    start_punt = np.zeros((20,1))
    with open('punt.json','r') as infile:
        punt = json.load(infile)
    punt = np.array(punt)
    start_punt,yard_range,c = plt.hist(100-(punt[:,1]-punt[:,0]),normed=True,bins=20,range=(0,100))
    return start_punt


def field_goal_team(team,year):
    os.chdir('/home/tim/nfl_pbp/'+str(year)+'/'+team)
    field_goal = np.zeros((28,1))
    with open('fg.json','r') as infile:
        fg = json.load(infile)
    fg = np.array(fg)
    nmakes,yard_range,c = plt.hist(fg[:,0]*fg[:,1]/3,bins=10,range=(.1,50.1)) #histy of fg makes
    nmiss,yard_range,c = plt.hist(fg[:,0]*(fg[:,1]-3)/-3,bins=10,range=(.1,50.1)) #histy of fg misses
    field_goal = nmakes/(nmakes+nmiss+0.00001)
    return field_goal


def first_down_team(team,year):
    os.chdir('/home/tim/nfl_pbp/'+str(year)+'/'+team)
    p_first = np.zeros((80,2))
    with open('o_down_1.json','r') as infile:
        o_down1_t = json.load(infile)
    with open('d_down_1.json','r') as infile:
        d_down1_t = json.load(infile)
    o_down1_t = np.array(o_down1_t)
    d_down1_t = np.array(d_down1_t)
    o_down1 = np.zeros((np.shape(o_down1_t)[0],3))
    d_down1 = np.zeros((np.shape(d_down1_t)[0],3))
    for j in range(np.shape(o_down1_t)[0]):
        o_down1[j,:] = float(o_down1_t[j,0]),float(o_down1_t[j,1]),float(o_down1_t[j,2])
    for j in range(np.shape(d_down1_t)[0]):
        d_down1[j,:] = float(d_down1_t[j,0]),float(d_down1_t[j,1]),float(d_down1_t[j,2])    
    p_first[:,0],yard_range,c = plt.hist(o_down1[:,0],normed=True,bins=80,range=(-30,50))
    p_first[:,1],yard_range,c = plt.hist(d_down1[:,0],normed=True,bins=80,range=(-30,50))
    return p_first


def second_down_team(team,year):
    os.chdir('/home/tim/nfl_pbp/'+str(year)+'/'+team)
    p_second = np.zeros((80,2))
    with open('o_down_2.json','r') as infile:
        o_down2_t = json.load(infile)
    with open('d_down_2.json','r') as infile:
        d_down2_t = json.load(infile)
    o_down2_t = np.array(o_down2_t)
    d_down2_t = np.array(d_down2_t)
    o_down2 = np.zeros((np.shape(o_down2_t)[0],3))
    d_down2 = np.zeros((np.shape(d_down2_t)[0],3))
    for j in range(np.shape(o_down2_t)[0]):
        o_down2[j,:] = float(o_down2_t[j,0]),float(o_down2_t[j,1]),float(o_down2_t[j,2])
    for j in range(np.shape(d_down2_t)[0]):
        d_down2[j,:] = float(d_down2_t[j,0]),float(d_down2_t[j,1]),float(d_down2_t[j,2])    
    p_second[:,0],yard_range,c = plt.hist(o_down2[:,0],normed=True,bins=80,range=(-30,50))
    p_second[:,1],yard_range,c = plt.hist(d_down2[:,0],normed=True,bins=80,range=(-30,50))
    return p_second


def third_down_team(team,year):
    os.chdir('/home/tim/nfl_pbp/'+str(year)+'/'+team)
    p_third_s = np.zeros((80,2))
    p_third_m = np.zeros((80,2))
    p_third_l = np.zeros((80,2))
    with open('o_down_3.json','r') as infile:
        o_down3_t = json.load(infile)
    with open('d_down_3.json','r') as infile:
        d_down3_t = json.load(infile)
    o_down3_t = np.array(o_down3_t)
    d_down3_t = np.array(d_down3_t)
    o_down3 = np.zeros((np.shape(o_down3_t)[0],3))
    d_down3 = np.zeros((np.shape(d_down3_t)[0],3))
    for j in range(np.shape(o_down3_t)[0]):
        o_down3[j,:] = float(o_down3_t[j,0]),float(o_down3_t[j,1]),float(o_down3_t[j,2])
    for j in range(np.shape(d_down3_t)[0]):
        d_down3[j,:] = float(d_down3_t[j,0]),float(d_down3_t[j,1]),float(d_down3_t[j,2])
    gt3d = d_down3[:,1]>3
    sd = d_down3[:,1]<=3
    lte7d = d_down3[:,1]<=7
    md = gt3d*lte7d    
    ld = d_down3[:,1]>7
    gt3o = o_down3[:,1]>3
    so = o_down3[:,1]<=3
    lte7o = o_down3[:,1]<=7
    mo = gt3o*lte7o    
    lo = o_down3[:,1]>7
    p_third_s[:,0],yard_range,c = plt.hist(o_down3[so,0],normed=True,bins=80,range=(-30,50))
    p_third_s[:,1],yard_range,c = plt.hist(d_down3[sd,0],normed=True,bins=80,range=(-30,50))
    p_third_m[:,0],yard_range,c = plt.hist(o_down3[mo,0],normed=True,bins=80,range=(-30,50))
    p_third_m[:,1],yard_range,c = plt.hist(d_down3[md,0],normed=True,bins=80,range=(-30,50))
    p_third_l[:,0],yard_range,c = plt.hist(o_down3[lo,0],normed=True,bins=80,range=(-30,50))
    p_third_l[:,1],yard_range,c = plt.hist(d_down3[ld,0],normed=True,bins=80,range=(-30,50))
    return p_third_s, p_third_m, p_third_l


def fourth_down_team(team,year):
    os.chdir('/home/tim/nfl_pbp/'+str(year)+'/'+team)
    p_fourth = np.zeros((80,2))
    with open('o_down_4.json','r') as infile:
        o_down4_t = json.load(infile)
    with open('d_down_4.json','r') as infile:
        d_down4_t = json.load(infile)
    o_down4_t = np.array(o_down4_t)
    d_down4_t = np.array(d_down4_t)
    o_down4 = np.zeros((np.shape(o_down4_t)[0],3))
    d_down4 = np.zeros((np.shape(d_down4_t)[0],3))
    for j in range(np.shape(o_down4_t)[0]):
        o_down4[j,:] = float(o_down4_t[j,0]),float(o_down4_t[j,1]),float(o_down4_t[j,2])
    for j in range(np.shape(d_down4_t)[0]):
        d_down4[j,:] = float(d_down4_t[j,0]),float(d_down4_t[j,1]),float(d_down4_t[j,2])    
    p_fourth[:,0],yard_range,c = plt.hist(o_down4[:,0]-o_down4[:,1],normed=True,bins=80,range=(-30,50))
    p_fourth[:,1],yard_range,c = plt.hist(d_down4[:,0]-d_down4[:,1],normed=True,bins=80,range=(-30,50))
    return p_fourth


def drive_start_team(team,year):
    os.chdir('/home/tim/nfl_pbp/'+str(year)+'/'+team)
    drive_start = np.zeros((20,2))
    with open('o_drive.json','r') as infile:
        o_drive = json.load(infile)
    with open('d_drive.json','r') as infile:
        d_drive = json.load(infile)
    o_drive_a = np.zeros((np.shape(o_drive)[0],3))
    d_drive_a = np.zeros((np.shape(d_drive)[0],3))
    o_drive = np.array(o_drive)
    d_drive = np.array(d_drive)
    for j in range(np.shape(o_drive_a)[0]):
        o_drive_a[j,:] = float(o_drive[j,0]),float(o_drive[j,1]),float(o_drive[j,4])
    for j in range(np.shape(d_drive_a)[0]):
        d_drive_a[j,:] = float(d_drive[j,0]),float(d_drive[j,1]),float(d_drive[j,4])
    drive_start[:,0], yard_range, c = plt.hist(o_drive_a[:,0],normed=True,bins=20,range=(0,100))
    drive_start[:,1], yard_range, c = plt.hist(d_drive_a[:,0],normed=True,bins=20,range=(0,100))
    return drive_start

def net_yards_team(team,year):
    os.chdir('/home/tim/nfl_pbp/'+str(year)+'/'+team)
    net_yards = np.zeros((26,2))
    with open('o_drive.json','r') as infile:
        o_drive = json.load(infile)
    with open('d_drive.json','r') as infile:
        d_drive = json.load(infile)
    o_drive_a = np.zeros((np.shape(o_drive)[0],3))
    d_drive_a = np.zeros((np.shape(d_drive)[0],3))
    o_drive = np.array(o_drive)
    d_drive = np.array(d_drive)
    for j in range(np.shape(o_drive_a)[0]):
        o_drive_a[j,:] = float(o_drive[j,0]),float(o_drive[j,1]),float(o_drive[j,4])
    for j in range(np.shape(d_drive_a)[0]):
        d_drive_a[j,:] = float(d_drive[j,0]),float(d_drive[j,1]),float(d_drive[j,4])
    net_yards[:,0], yard_range, c = plt.hist(o_drive_a[:,0],normed=True,bins=26,range=(-30,100))
    net_yards[:,1], yard_range, c = plt.hist(d_drive_a[:,0],normed=True,bins=26,range=(-30,100))
    return net_yards


def drive_heatmap_team(team,year):
    os.chdir('/home/tim/nfl_pbp/'+str(year)+'/'+team)
    a_points = np.zeros((20,2))
    p_end_all = np.zeros((20,20,2))
    with open('o_drive.json','r') as infile:
        o_drive = json.load(infile)
    with open('d_drive.json','r') as infile:
        d_drive = json.load(infile)
    o_drive_a = np.zeros((np.shape(o_drive)[0],3))
    d_drive_a = np.zeros((np.shape(d_drive)[0],3))
    o_drive = np.array(o_drive)
    d_drive = np.array(d_drive)
    for j in range(np.shape(o_drive_a)[0]):
        o_drive_a[j,:] = float(o_drive[j,0]),float(o_drive[j,1]),float(o_drive[j,4])
    for j in range(np.shape(d_drive_a)[0]):
        d_drive_a[j,:] = float(d_drive[j,0]),float(d_drive[j,1]),float(d_drive[j,4])
    for y in range(100,0,-5):
        high_yard_o = o_drive_a[:,0]<y
        low_yard_o = o_drive_a[:,0]>=y-5
        in_range_o = high_yard_o*low_yard_o
        high_yard_d = d_drive_a[:,0]<y
        low_yard_d = d_drive_a[:,0]>=y-5
        in_range_d = high_yard_d*low_yard_d
        p_end_o,yard_range,c = plt.hist(o_drive_a[in_range_o,1], normed=True, bins=20, range=(-.1,99.9))
        p_end_d,yard_range,c = plt.hist(d_drive_a[in_range_d,1], normed=True, bins=20, range=(-.1,99.9))
        d_index = y/5.-1
        p_end_all[:,d_index,0] = p_end_o
        p_end_all[:,d_index,1] = p_end_d
        a_points[d_index,0] = np.average(o_drive_a[in_range_o,2])
        a_points[d_index,1] = np.average(d_drive_a[in_range_d,2])
    plt.figure(1)
    plt.clf()
    plt.imshow(p_end_all[:,:,0]*5,interpolation=None,vmin=0.0,vmax=0.25,extent=[100,0,100,0])
    plt.xlabel('Starting Yard Line')
    plt.ylabel('Ending Yard Line')
    plt.title('Offensive Drive Heat Map '+team+' '+str(year))
    fname = '/home/tim/nfl_pbp/'+str(year)+'/'+team+'/offensive_heat_map.png'
    plt.savefig(fname)
    plt.figure(1)
    plt.clf()
    plt.imshow(p_end_all[:,:,1]*5,interpolation=None,vmin=0.0,vmax=0.25,extent=[100,0,100,0])
    plt.xlabel('Starting Yard Line')
    plt.ylabel('Ending Yard Line')
    plt.title('Defensive Drive Heat Map '+team+' '+str(year))
    fname = '/home/tim/nfl_pbp/'+str(year)+'/'+team+'/defensive_heat_map.png'
    plt.savefig(fname)
    return a_points,p_end_all

def plot_all_teams(year_start,year_end):
    db = MySQLdb.connect(user="root",passwd="057005223",db="nfl_pbp")
    team_query = db.cursor() #query tool for teams
    n_years = year_end-year_start
    team_query.execute("""select distinct offense from pbp order by offense asc""")
    team = team_query.fetchall()
    n_teams = np.shape(team)[0]
    net_punt = np.zeros((n_years,n_teams,28))
    start_punt = np.zeros((n_years,n_teams,20))
    field_goal = np.zeros((n_years,n_teams,10))
    first_down = np.zeros((n_years,n_teams,80,2))
    second_down = np.zeros((n_years,n_teams,80,2))
    third_down_s = np.zeros((n_years,n_teams,80,2))
    third_down_m = np.zeros((n_years,n_teams,80,2))
    third_down_l = np.zeros((n_years,n_teams,80,2))
    fourth_down = np.zeros((n_years,n_teams,80,2))
    drive_start = np.zeros((n_years,n_teams,20,2))
    net_yards = np.zeros((n_years,n_teams,26,2))
    a_points = np.zeros((n_years,n_teams,20,2))
    drive_heatmap = np.zeros((n_years,n_teams,20,20,2))
    for year in range(year_start,year_end):
        for team_index in range(n_teams):
            team_name = team[team_index][0]
            print year, team_name
            net_punt[year-year_start,team_index,:] = net_punt_team(team_name,year)
            start_punt[year-year_start,team_index,:] = start_punt_team(team_name,year)
            field_goal[year-year_start,team_index,:] = field_goal_team(team_name,year)
            first_down[year-year_start,team_index,:,:] = first_down_team(team_name,year)
            second_down[year-year_start,team_index,:,:] = second_down_team(team_name,year)
            print 'ok'
            third_down_s[year-year_start,team_index,:,:], third_down_m[year-year_start,team_index,:,:], third_down_l[year-year_start,team_index,:,:] = third_down_team(team_name,year)
            fourth_down[year-year_start,team_index,:,:] = fourth_down_team(team_name,year)
            drive_start[year-year_start,team_index,:,:] = drive_start_team(team_name,year)
            net_yards[year-year_start,team_index,:,:] = net_yards_team(team_name,year)
            a_points[year-year_start,team_index,:,:], drive_heatmap[year-year_start,team_index,:,:,:] = drive_heatmap_team(team_name,year)
        pbp_plotter(net_punt[year-year_start,:,:],'net_punt',year=year,title='Net Punting',xlabel='',ylabel='Net Yards',team_names=team,extent=[0,32,80,-60],vmin=0,vmax=.1)
        pbp_plotter(start_punt[year-year_start,:,:],'start_punt',year=year,title='Punting Starting Field Position',xlabel='',ylabel='Starting Field Position',team_names=team,extent=[0,32,100,0],vmin=0,vmax=.1)
        pbp_plotter(field_goal[year-year_start,:,:],'field_goal',year=year,title='Field Goal Percentage',xlabel='',ylabel='Field Goal Distance',team_names=team,extent=[0,32,68,18],vmin=.25,vmax=1)
        pbp_plotter(first_down[year-year_start,:,:,:],'first_down',year=year,title='Yards Gained (first down)',xlabel='',ylabel='Net Yards',team_names=team,extent=[0,32,50,-30],vmin=0,vmax=.1)
        pbp_plotter(second_down[year-year_start,:,:,:],'second_down',year=year,title='Yards Gained (second down)',xlabel='',ylabel='Net Yards',team_names=team,extent=[0,32,50,-30],vmin=0,vmax=.1)
        pbp_plotter(third_down_s[year-year_start,:,:,:],'third_down_short',year=year,title='Yards Gained (third and short)',xlabel='',ylabel='Yards from Marker',team_names=team,extent=[0,32,50,-30],vmin=0,vmax=.1)
        pbp_plotter(third_down_m[year-year_start,:,:,:],'third_down_medium',year=year,title='Yards Gained (third and medium)',xlabel='',ylabel='Yards from Marker',team_names=team,extent=[0,32,50,-30],vmin=0,vmax=.1)
        pbp_plotter(third_down_l[year-year_start,:,:,:],'third_down_long',year=year,title='Yards Gained (third and long)',xlabel='',ylabel='Yards from Marker',team_names=team,extent=[0,32,50,-30],vmin=0,vmax=.1)
        pbp_plotter(fourth_down[year-year_start,:,:,:],'fourth_down',year=year,title='Yards to Gain (fourth down)',xlabel='',ylabel='Yards from Marker',team_names=team,extent=[0,32,50,-30],vmin=0,vmax=.1)
        pbp_plotter(drive_start[year-year_start,:,:,:],'drive_start',year=year,title='Drive Starting Field Position',xlabel='',ylabel='Starting Field Position',team_names=team,extent=[0,32,100,0],vmin=0,vmax=.03333)
        pbp_plotter(net_yards[year-year_start,:,:,:],'net_yards',year=year,title='Drive Net Yards',xlabel='',ylabel='Net Yards (drive)',team_names=team,extent=[0,32,100,-30],vmin=0,vmax=.0333)
        pbp_plotter(a_points[year-year_start,:,:,:],'a_points',year=year,title='Average Points by Starting Field Position',xlabel='',ylabel='Starting Field Position',team_names=team,extent=[0,32,100,0],vmin=.5,vmax=5)


def nfl_game_simulator(team1,year1,team2,year2):
    n_plays = 140.+np.random.randn(1)*10
    home_net_punt = net_punt_team(team1,year1)
    home_start_punt = start_punt_team(team1,year1)
    home_fg = field_goal_team(team1,year1)
    home_first_down = first_down_team(team1,year1)
    home_second_down = second_down_team(team1,year1)
    home_third_down_s,home_third_down_m,home_third_down_l = third_down_team(team1,year1)
    home_fourth_down = fourth_down_team(team1,year1)
    home_start_drive = drive_start_team(team1,year1)
    home_a_points,home_heat_map = drive_heatmap_team(team1,year1)
    away_net_punt = net_punt_team(team2,year2)
    away_start_punt = start_punt_team(team2,year2)
    away_fg = field_goal_team(team2,year2)
    away_first_down = first_down_team(team2,year2)
    away_second_down = second_down_team(team2,year2)
    away_third_down_s,away_third_down_m,away_third_down_l = third_down_team(team2,year2)
    away_fourth_down = fourth_down_team(team2,year2)
    away_start_drive = drive_start_team(team2,year2)
    away_a_points,home_heat_map = drive_heatmap_team(team2,year2)
    ha_1 = [(np.cumsum(home_first_down[:,0])+np.cumsum(away_first_down[:,1]))/2.,(np.cumsum(home_first_down[:,1])+np.cumsum(away_first_down[:,0]))/2.]
    ha_2 = [(np.cumsum(home_second_down[:,0])+np.cumsum(away_second_down[:,1]))/2.,(np.cumsum(home_second_down[:,1])+np.cumsum(away_second_down[:,0]))/2.]
    ha_3_s = [(np.cumsum(home_third_down_s[:,0])+np.cumsum(away_third_down_s[:,1]))/2.,(np.cumsum(home_third_down_s[:,1])+np.cumsum(away_third_down_s[:,0]))/2.]
    ha_3_m = [(np.cumsum(home_third_down_m[:,0])+np.cumsum(away_third_down_m[:,1]))/2.,(np.cumsum(home_third_down_m[:,1])+np.cumsum(away_third_down_m[:,0]))/2.]
    ha_3_l = [(np.cumsum(home_third_down_l[:,0])+np.cumsum(away_third_down_l[:,1]))/2.,(np.cumsum(home_third_down_l[:,1])+np.cumsum(away_third_down_l[:,0]))/2.]
    punts = [np.cumsum(home_net_punt),np.cumsum(away_net_punt)]
    sfp = [(np.cumsum(home_start_drive[:,0])+np.cumsum(away_start_drive[:,1]))/2,(np.cumsum(home_start_drive[:,1])+np.cumsum(away_start_drive[:,0]))/2]
    fg = [home_fg,away_fg]
    for j in range(1,np.shape(fg)[1]-1):
        fg[0][j] = np.mean(fg[0][j-1:j+1])
        fg[1][j] = np.mean(fg[1][j-1:j+1])
    score = [0,0]
    net_yds = [0,0]
    n_plays_game = [0,0]
    third_down_c = [0,0]
    third_down_a = [0,0]
    possession = int(np.round(np.random.rand(1)))
    r_sfp = np.random.rand(1)
    down = 1
    ydline = np.interp(r_sfp,5*sfp[possession][:],range(0,100,5))
    togo = min(10,ydline)
    net_gain = 0
    for j in range(n_plays):
        if down == 1:
            r_gain = np.random.rand(1)
            net_gain = np.round(np.interp(r_gain,ha_1[possession][:],range(-30,50)))
            ydline -= net_gain
            togo -= net_gain
            net_yds[possession] += min(net_gain,ydline)
            n_plays_game[possession] += 1
            third_down_c[possession] += 0
            third_down_a[possession] += 0
            if ydline < 0:
                score[possession] += 7
                possession = np.abs(possession-1)
                ydline = np.interp(r_sfp,5*sfp[possession][:],range(0,100,5))
                print 'TOUCHDOWN', score
            elif togo < 0:
                down = 1
                togo = np.min(10,ydline)
            elif ydline > 100:
                possession = np.abs(possession-1)
                score[possession] += 2
                ydline = np.interp(r_sfp,5*sfp[possession][:],range(0,100,5))
                print 'SAFETY', score
            else:
                down += 1
        elif down == 2:
            r_gain = np.random.rand(1)
            net_gain = np.round(np.interp(r_gain,ha_2[possession][:],range(-30,50)))
            ydline -= net_gain
            togo -= net_gain
            net_yds[possession] += min(net_gain,ydline)
            n_plays_game[possession] += 1
            third_down_c[possession] += 0
            third_down_a[possession] += 0
            if ydline < 0:
                score[possession] += 7
                possession = np.abs(possession-1)
                ydline = np.interp(r_sfp,5*sfp[possession][:],range(0,100,5))
                print 'TOUCHDOWN', score
            elif togo < 0:
                down = 1
            elif ydline > 100:
                possession = np.abs(possession-1)
                score[possession] += 2
                ydline = np.interp(r_sfp,5*sfp[possession][:],range(0,100,5))
                print 'SAFETY', score
            else:
                down += 1
        elif down == 3:
            r_gain = np.random.rand(1)
            if togo <= 3:
                net_gain = np.round(np.interp(r_gain,ha_3_s[possession][:],range(-30,50)))
            elif togo < 7:
                net_gain = np.round(np.interp(r_gain,ha_3_m[possession][:],range(-30,50)))
            elif togo > 7:
                net_gain = np.round(np.interp(r_gain,ha_3_l[possession][:],range(-30,50)))
            ydline -= net_gain
            togo -= net_gain
            net_yds[possession] += min(net_gain,ydline)
            n_plays_game[possession] += 1
            third_down_a[possession] += 1
            if ydline < 0:
                score[possession] += 7
                possession = np.abs(possession-1)
                ydline = np.interp(r_sfp,5*sfp[possession][:],range(0,100,5))
                print 'TOUCHDOWN', score
                third_down_c[possession] += 1
            elif togo < 0:
                down = 1
                third_down_c[possession] += 1
            elif ydline > 100:
                possession = np.abs(possession-1)
                score[possession] += 2
                ydline = np.interp(r_sfp,5*sfp[possession][:],range(0,100,5))
                print 'SAFETY', score
            else:
                down += 1
        elif down == 4:
            down = 1
            if ydline < 38:
                r_kick = np.random.rand(1)
                is_good = np.interp(ydline,range(0,50,5),fg[possession][:])
                if r_kick>is_good:
                    possession = np.abs(possession-1)
                    print 'FG MISS', score
                    ydline = 100-ydline-8
                else:
                    score[possession] += 3
                    possession = np.abs(possession-1)
                    print 'FG GOOD', score
                    ydline = np.interp(r_sfp,5*sfp[possession][:],range(0,100,5))
            else:
                r_punt = np.random.rand(1)
                ydline = np.round(100.-ydline+np.interp(r_punt,5*punts[possession][:],range(-60,80,5)))
                possession = np.abs(possession-1)
                print 'PUNT', score
                if ydline > 100:
                    ydline = 20
                elif ydline < 0:
                    score[possession] += 7
                    possession = np.abs(possession-1)
                    ydline = np.interp(r_sfp,5*sfp[possession][:],range(0,100,5))
                    print 'PUNT RETURN TOUCHDOWN', score
    return score, net_yds, third_down_a, third_down_c
