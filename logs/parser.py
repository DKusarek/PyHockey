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
            raise validator.NotSuchFile("no file")

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
    p = open('players_scores.csv', 'w')
    p.write(points)
    p.close()
