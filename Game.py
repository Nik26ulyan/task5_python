import sys
import random
import time

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, QUrl

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
CELL_SIZE = 20
start_time = time.time()

def create_grid(cell_size):
    global GRID_WIDTH, GRID_HEIGHT, CELL_SIZE
    CELL_SIZE = cell_size
    GRID_WIDTH, GRID_HEIGHT = (SCREEN_WIDTH - 150) // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE
    return [[random.choice(colors) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


class GridWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.grid = create_grid(100)

        self.buttons = []
        for i, color in enumerate(colors):
            button = QPushButton(self)
            button.setGeometry(SCREEN_WIDTH - 100, int(i * 50 * 1.5), 100, 50)
            button.setStyleSheet(f'background-color: rgb{color};')
            button.clicked.connect(lambda _, color=color: self.set_new_color(0, 0, color, self.grid[0][0]))
            self.buttons.append(button)
        self.button_rules = QPushButton("Правила", self)
        self.button_rules.setGeometry(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 100, 50)
        self.button_rules.clicked.connect(self.show_rules)

    def show_rules(self):
        self.rules_window = RulesWindow()
        self.rules_window.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = QColor(*self.grid[y][x])
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
                painter.drawRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    def set_new_color(self, x, y, new_color, old_color):
        self.change_color(x, y, new_color, old_color)
        self.is_victory()

    def change_color(self, x, y, new_color, old_color):
        if new_color == old_color:
            return
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return
        if self.grid[y][x] != old_color:
            return

        self.grid[y][x] = new_color

        self.change_color(x - 1, y, new_color, old_color)
        self.change_color(x + 1, y, new_color, old_color)
        self.change_color(x, y - 1, new_color, old_color)
        self.change_color(x, y + 1, new_color, old_color)

        self.update()
        # self.is_victory()

    def is_victory(self):
        my_set = {frozenset(x) for x in self.grid}
        if len(my_set) == 1:
            self.victory_window = VictoryWindow()
            self.victory_window.show()

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.grid_widget = GridWidget()
        layout.addWidget(self.grid_widget)
        self.grid_widget.setFocus()
        self.setLayout(layout)
        self.media_player = QMediaPlayer(self)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("music.mp3")))
        self.media_player.play()

    def closeEvent(self, event):
        self.media_player.stop()
        event.accept()


class RulesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Правила игры Перекраска')
        self.setGeometry(300, 100, 600, 400)
        rules = QLabel(self)
        rules.setText('Правила игры Перекраска:\n\n'
                      'Цель игры - перекрасить все клетки на поле в один цвет.\n\n'
                      'Игрок может выбрать цвет, на который он хочет перекрасить клетки,\n'
                      'для этого нужно нажать на кнопку с определённым цветом. Все соседние клетки\n'
                      'того же цвета автоматически перекрасятся в выбранный цвет, начиная с верхнего левого угла поля.\n\n'
                      'Игрок выигрывает, когда все клетки на поле окрашены в один цвет.\n\n'
                      'Удачи!')
        rules.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(rules)
        self.setLayout(layout)


class VictoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('УРА ПОБЕДА')
        self.setGeometry(300, 100, 500, 200)
        rules = QLabel(self)
        time_str = str(round(time.time() - start_time, 2))
        font = QFont("Comic Sans", 42)
        rules.setFont(font)
        rules.setText('Вы победили!\n'
                      'У вас получилось сделать это за:\n' + time_str)
        rules.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(rules)
        self.setLayout(layout)

        self.media_player_victory = QMediaPlayer(self)
        self.media_player_victory.setMedia(QMediaContent(QUrl.fromLocalFile("victory_music.mp3")))
        self.media_player_victory.play()

    def closeEvent(self, event):
        self.media_player_victory.stop()
        event.accept()

app = QApplication(sys.argv)
game_window = GameWindow()
game_window.show()
sys.exit(app.exec_())