from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QDesktopWidget, \
    QPushButton, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlaylist, QMediaPlayer
import parameters as pt


class RankingWindow(QWidget):

    signal_request_players = pyqtSignal()
    signal_go_welcome = pyqtSignal()


    def __init__(self) -> None:
        super().__init__()
        
        # background image
        self.background: QLabel = QLabel(self)
        self.background_map: QPixmap = QPixmap(pt.pt_back_menu)
        self.background.resize(self.background_map.size())
        self.background.setPixmap(self.background_map)
        self.background.setScaledContents(True)
        
        # centered, not resizable, window
        self.setFixedSize(self.background.size())
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # window gui
        self.setWindowTitle('Rankings')
        self.gui()
        self.event_connection()

    def gui(self):
        # music
        ## .state: 1 is playing, 2 is paused
        self.song: QMediaContent = QMediaContent(
            QUrl.fromLocalFile(pt.pt_s_music_2))
        self.playlist: QMediaPlaylist = QMediaPlaylist()
        self.playlist.addMedia(self.song)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.music_player: QMediaPlayer = QMediaPlayer()
        self.music_player.setPlaylist(self.playlist)
        self.music_player.setVolume(15)

        # title of section
        title: QLabel = QLabel(f'{"Top players": ^30s}')
        title.setStyleSheet(pt.title_style_2)
        title_lay = QHBoxLayout()
        title_lay.addStretch()
        title_lay.addWidget(title)
        title_lay.addStretch()

        # players
        self.top_players: list = \
        [[QLabel(f'{"-":-<30s}'), QLabel(f'{"-":->10s}')] for _ in range(5)]
        for line in self.top_players:
            line[0].setStyleSheet(pt.label_style_2)
            line[1].setStyleSheet(pt.label_style_2)

        # list layout
        ranking: QGridLayout = QGridLayout()
        for index in range(len(self.top_players)):
            ranking.addWidget(self.top_players[index][0], index, 0)
            ranking.addWidget(self.top_players[index][1], index, 1)

        # button to go back
        self.go_back: QPushButton = QPushButton(parent=self, text='Back')
        self.go_back.setStyleSheet(pt.button_style)
        self.go_back.setMinimumWidth(100)
        go_back_lay: QHBoxLayout = QHBoxLayout()
        go_back_lay.addStretch()
        go_back_lay.addWidget(self.go_back)
        go_back_lay.addStretch()

        # ranking layout
        middle_layout: QVBoxLayout = QVBoxLayout()
        middle_layout.addStretch()
        middle_layout.addLayout(title_lay)
        middle_layout.addSpacing(40)
        middle_layout.addLayout(ranking)
        middle_layout.addStretch()
        middle_layout.addLayout(go_back_lay)
        middle_layout.addStretch()

        self.rank_layout: QHBoxLayout = QHBoxLayout()
        self.rank_layout.addStretch()
        self.rank_layout.addLayout(middle_layout)
        self.rank_layout.addStretch()
        self.setLayout(self.rank_layout)

    def request_players(self) -> None:
        self.signal_request_players.emit()

    def assign_players(self, top: tuple):
        for index in range(len(top)):
            player, score = top[index]
            self.top_players[index][0].setText(f'{player: <30s}')
            self.top_players[index][1].setText(f'{score: >10s} pts')

    def event_connection(self):
        self.go_back.clicked.connect(self.go_welcome)

    def go_welcome(self):
        self.music_player.stop()
        self.hide()
        self.signal_go_welcome.emit()

    def launch(self):
        self.music_player.play()
        self.signal_request_players.emit()
        self.show()