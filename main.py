import matplotlib.pyplot as plt
import numpy as np
import math
from UIv2 import Ui_MainWindow
import sys
from PyQt5 import QtWidgets
BALL_HEIGHT = 2
TARGET_HEIGHT = 4
DISTANCE = 10
SPEED = 12
G = 10
TRIES_RESTRICTION = 1000000
DRAW_FIRST = 0
DRAW_LAST = 0
STEP = 0.1


def graphics_plot(alpha, line = ''):
    i = 0
    x_plot = []
    y_plot = []
    for x_pos in np.arange(0, DISTANCE + STEP, STEP):
        x_plot.insert(i, x_pos)
        tmp = (BALL_HEIGHT + SPEED * (x_pos / (SPEED * math.cos(alpha))) * math.sin(alpha) - (
                    G * (x_pos / (SPEED * math.cos(alpha))) ** 2) / 2)
        if tmp < 0:
            tmp = 0
        y_plot.insert(i, tmp)
    plt.plot(x_plot, y_plot, line)
    return 0


def try_alpha(alpha):
    time = DISTANCE / (SPEED * math.cos(alpha))
    y = BALL_HEIGHT + SPEED * time * math.sin(alpha) - (G * time ** 2) / 2
    x = SPEED * time * math.cos(alpha)
    return y


def alpha_binary_search(min, max, tries_left):
    out_of_tries_flag = 0
    while tries_left >= 0:
        tries_left -= 1
        if tries_left < 0:
            out_of_tries_flag = 1
            return -1, out_of_tries_flag
        mid = (min + max) / 2
        y = try_alpha(mid)
        if (tries_left >= (TRIES_RESTRICTION - DRAW_FIRST)) or (tries_left <= DRAW_LAST):
            graphics_plot(mid)
        if y == TARGET_HEIGHT:
            graphics_plot(mid, '+')
            return mid, out_of_tries_flag
        elif y < TARGET_HEIGHT:
            min = mid
        else:
            max = mid
    print('Error')
    return -1, out_of_tries_flag


def main():
    plt.close()
    min_alpha = math.atan((TARGET_HEIGHT - BALL_HEIGHT) / DISTANCE)
    max_alpha = math.pi / 2
    if min_alpha > max_alpha:
        print('Error')
        return -1
    alpha, out_of_tries_flag = alpha_binary_search(min_alpha, max_alpha, TRIES_RESTRICTION)
    plt.show()
    if alpha != -1:
        msg = "Throw your ball at " + str(math.degrees(alpha)) + " degrees. \n"
    elif out_of_tries_flag == 1:
        msg = "Out of tries! Correct trajectory cannot be found. \n"
    else:
        msg = "Program error. \n"
    return msg


if __name__ == '__main__':
    class MyWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super(MyWindow, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.pushButton.clicked.connect(self.handler)

        def handler(self):
            global BALL_HEIGHT, TARGET_HEIGHT, DISTANCE, SPEED, G, TRIES_RESTRICTION, DRAW_FIRST, DRAW_LAST
            BALL_HEIGHT = int(self.ui.textEdit_BallHeight.toPlainText())
            TARGET_HEIGHT = int(self.ui.textEdit_TargetHeight.toPlainText())
            DISTANCE = int(self.ui.textEdit_TargetDistance.toPlainText())
            SPEED = int(self.ui.textEdit_Speed.toPlainText())
            G = int(self.ui.textEdit_G.toPlainText())
            TRIES_RESTRICTION = int(self.ui.textEdit_TriesRestriction.toPlainText())
            DRAW_FIRST = int(self.ui.textEdit_DrawFirst.toPlainText())
            DRAW_LAST = int(self.ui.textEdit_DrawLast.toPlainText())
            result = main()
            self.ui.textBrowser_Result.setText(result)


    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())
