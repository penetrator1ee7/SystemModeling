import matplotlib.pyplot as plt
import numpy as np
import math
from UIv3 import Ui_MainWindow
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
TIME_RESTRICTION = '?'
ALPHA = '?'


def graphics_plot(alpha, line=''):
    time = DISTANCE / (SPEED * math.cos(alpha))
    i = 0
    x_plot = []
    y_plot = []
    if TIME_RESTRICTION != '?':
        time = TIME_RESTRICTION
    tmp_distance = SPEED * time * math.cos(alpha)
    for x_pos in np.arange(0, tmp_distance + STEP, STEP):
        x_plot.insert(i, x_pos)
        dot_time = (x_pos / (SPEED * math.cos(alpha)))
        tmp = (BALL_HEIGHT + SPEED * dot_time * math.sin(alpha) - (G * dot_time ** 2) / 2)
        if tmp < 0:
            tmp = 0
        y_plot.insert(i, tmp)
    plt.plot(x_plot, y_plot, line)
    return 0


def try_alpha(alpha):
    time = DISTANCE / (SPEED * math.cos(alpha))
    if TIME_RESTRICTION != '?':
        time = TIME_RESTRICTION
    y = BALL_HEIGHT + SPEED * time * math.sin(alpha) - (G * time ** 2) / 2
    x = SPEED * time * math.cos(alpha)
    return y, x


def alpha_binary_search(min, max, tries_left):
    out_of_tries_flag = 0
    while tries_left >= 0:
        tries_left -= 1
        if tries_left < 0:
            out_of_tries_flag = 1
            return -1, out_of_tries_flag
        mid = (min + max) / 2
        y, x = try_alpha(mid)
        if (tries_left >= (TRIES_RESTRICTION - DRAW_FIRST)) or (tries_left < DRAW_LAST):
            graphics_plot(mid)
        if y == TARGET_HEIGHT and x == DISTANCE:
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

    # special cases check
    if SPEED == 0:
        i = 0
        x_plot = []
        y_plot = []
        for y_pos in np.arange(0, 4, 0.01):
            y_plot.insert(i, y_pos)
            x_plot.insert(i, 0)
        plt.plot(x_plot, y_plot)
        plt.show()
        return "Корректная траектория не может быть найдена. \n"
    elif DISTANCE == 0:
        return "Корректная траектория не может быть найдена. \n"
    elif ALPHA != '?':
        graphics_plot(math.radians(ALPHA))
        plt.show()
        y, x = try_alpha(math.radians(ALPHA))
        if y == TARGET_HEIGHT and x == DISTANCE:
            return "Попадание!"
        else:
            return "Промах!"

    # find alpha suitable for set conditions
    min_alpha = math.atan((TARGET_HEIGHT - BALL_HEIGHT) / DISTANCE)
    max_alpha = math.pi / 2
    if min_alpha > max_alpha:
        print('Error')
        return -1
    alpha, out_of_tries_flag = alpha_binary_search(min_alpha, max_alpha, TRIES_RESTRICTION)

    # results display
    plt.show()
    if alpha != -1:
        msg = "Совершайте бросок под углом " + str(math.degrees(alpha)) + " градусов. \n"
    elif out_of_tries_flag == 1:
        msg = "Попытки исчерпаны! Корректная траектория не может быть найдена. \n"
    else:
        msg = "Программная ошибка. \n"
    return msg


if __name__ == '__main__':
    class MyWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super(MyWindow, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.pushButton.clicked.connect(self.handler)

        def handler(self):
            global BALL_HEIGHT, TARGET_HEIGHT, DISTANCE, SPEED, G, TRIES_RESTRICTION, DRAW_FIRST, DRAW_LAST\
                , TIME_RESTRICTION, ALPHA
            try:
                BALL_HEIGHT = float(self.ui.textEdit_BallHeight.toPlainText())
                TARGET_HEIGHT = float(self.ui.textEdit_TargetHeight.toPlainText())
                DISTANCE = float(self.ui.textEdit_TargetDistance.toPlainText())
                SPEED = float(self.ui.textEdit_Speed.toPlainText())
                G = float(self.ui.textEdit_G.toPlainText())
                TRIES_RESTRICTION = float(self.ui.textEdit_TriesRestriction.toPlainText())
                DRAW_FIRST = float(self.ui.textEdit_DrawFirst.toPlainText())
                DRAW_LAST = float(self.ui.textEdit_DrawLast.toPlainText())
                TIME_RESTRICTION = self.ui.textEdit_TimeRestriction.toPlainText()
                if TIME_RESTRICTION != '?':
                    TIME_RESTRICTION = float(TIME_RESTRICTION)
                ALPHA = self.ui.textEdit_ALPHA.toPlainText()
                if ALPHA != '?':
                    ALPHA = float(ALPHA)
                result = main()
                self.ui.textBrowser_Result.setText(result)
            except ValueError:
                self.ui.textBrowser_Result.setText(
                    'Введенные вами данные не является(-ются) числом(-ами) ! \nПовторите ввод. \n')


    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec())
