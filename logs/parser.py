import os
import validator


class LogParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_log(input_file, string_to_find):
        if os.path.isfile(input_file):
            file_to_check = open(input_file).read()
            file_lines = file_to_check.split('\n')
            lines_with_string = [line for line in file_lines if string_to_find in line]
            return lines_with_string
        else:
            raise validator.NotSuchFile()

file_name = "INFO.log"
myValidator=validator.InputFileValidator(file_name)


if myValidator.validate():
    parsed_data = LogParser.parse_log(file_name,"player 1 scored a point")
    parsed_data += LogParser.parse_log(file_name, "player 2 scored a point")
    p1_points,p2_points = 0, 0
    for line in parsed_data:
        if "player 1 scored a point" in line:
            p1_points += 1
        else:
            p2_points += 1
    points = str(p1_points)+"\n"+str(p2_points)
    file_for_scores = open('players_scores.csv', 'w')
    file_for_scores.write(points)
    file_for_scores.close()

    game_init_time = LogParser.parse_log(file_name, "GAME INIT: Starting game loop")
    game_end_time = LogParser.parse_log(file_name, "GAME INIT: Game loop ended")
    game_init_time_splitted = game_init_time[0].split(" ")
    init_time = game_init_time_splitted[1]
    game_end_time_splitted = game_end_time[0].split(" ")
    end_time = game_end_time_splitted[1]
    end_time_ss = int(end_time[-3]+end_time[-2]+end_time[-1]) + (1000 - int(init_time[-3]+init_time[-2]+init_time[-1]))
    check = 0
    if end_time_ss > 1000:
        check = 1
        end_time_ss = end_time_ss - 1000
    if int(end_time[3]+end_time[4]) == int(init_time[3]+init_time[4]):
        end_time_s = int(end_time[-6]+end_time[-5]) - (int(init_time[-6]+init_time[-5])+1)
    else:
        end_time_s = 60 - (int(init_time[-6]+init_time[-5])+1) + int(end_time[-6]+end_time[-5])
    if end_time_s > 60:
        check = 1
        end_time_s = end_time_s - 60
    if int(end_time[0]+end_time[1]) == int(init_time[0]+init_time[1]):
        end_time_m = int(end_time[3]+end_time[4]) - int(init_time[3]+init_time[4])
    else:
        end_time_m = (60 - (int(init_time[3]+init_time[4])+1)) + int(end_time[3]+end_time[4]) + check
    file_for_game_timelines = open('timeline.csv', 'w')
    file_for_game_timelines.write(str(end_time_m)+'\n'+str(end_time_s)+'\n'+str(end_time_ss))
    file_for_game_timelines.close()