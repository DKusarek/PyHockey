import time

from scripts.gamecomponents import Player, ScoreBoard

pl1 = Player.Player(1, 0)
pl2 = Player.Player(2, 0)
pl1.name = "Adam"
pl2.name = "Bartek"
pl1.clearPoints()
pl2.clearPoints()
sb = ScoreBoard.ScoreBoard(pl1, pl2)
is_finished = False

ScoreBoard.GameTime.startMeasuring()
sb.display()

n = 1
while n < 15:
    time.sleep(5)
    if not is_finished:
        try:
            pl1.addPoint()
            pl1.addPoint()
        except Player.TooManyPointsException:
            is_finished = True
            pl1.printTooManyPointsInfo()
        try:
            pl2.addPoint()
        except Player.TooManyPointsException:
            is_finished = True
            pl2.printTooManyPointsInfo()
    sb.display()
    n += 1
