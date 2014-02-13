create database nfl_pbp;
use nfl_pbp;
create table pbp (gameid varchar(20), --game id
                  qtr INT, --quarter (5 corresponds to OT)
                  minute INT, --minutes part of the remaining time
                  second INT,  --seconds part of the remaining time
                  offense varchar(3), --team on offense
                  defense varchar(3), --team on defense
                  down INT, --down
                  togo INT, --distance to first down
                  ydline INT, --distance to endzone
                  play_type varchar(32), --kickoff,play,field goal,punt,penalty,conversion attempt
                  net_yds INT, --yards gained on the play; kickoff starting position; field goal distance; net punt distance
                  description varchar(512), --play description (from original file)
                  offscore INT, --offensive score (from original file)
                  defscore INT, --defensive score (from original file)
                  season INT, --season of the play
                  drive_id INT); --drive the play is in

create table drive (gameid varchar(20), --game id
                    offense varchar(3), --offense id
                    defense varchar(3), --defense id
                    plays INT, --total number of plays on the drive
                    start_drive INT, --drive starting ydline
                    end_drive INT,  --drive ending ydline
                    result varchar(20), --end result of the drive
                    points INT, --points scored on the drive
                    home varchar(3), --home team id
                    away varchar(3), --away team id
                    home_score INT, --home score (at conclusion of drive)
                    away_score INT, --away score (at conclusion of drive)
                    time_start INT, --seconds remaining at drive start
                    time_end INT, --seconds remaining at drive end
                    season INT); --season of the drive

create table game_results (gameid varchar(20), --gameid
                           home varchar(3), --home team
                           away varchar(3), --away team
                           home_score INT, --home score
                           away_score INT); --away score

load data local infile '/home/tim/nfl_pbp/all_nfl_pbp_data.csv' -- path to directory
into table pbp
columns terminated by ','
optionally enclosed by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '/home/tim/nfl_pbp/all_nfl_drive.csv' -- path to directory
into table drive
columns terminated by ','
optionally enclosed by '"'
escaped by '"'
lines terminated by '\n'
ignore 1 lines;

load data local infile '/home/tim/nfl_pbp/all_nfl_game.csv' -- path to directory
into table game_results --table to load into
columns terminated by ',' --csv file
optionally enclosed by '"' --some columns don't include data
escaped by '"' 
lines terminated by '\n' --line break \n
ignore 1 lines; --ignore the first line
