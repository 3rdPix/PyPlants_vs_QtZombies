from PyQt5.QtWidgets import QHBoxLayout, QLabel, QDesktopWidget, \
    QPushButton, QLineEdit, QGridLayout, QVBoxLayout, QWidget,\
        QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from ft.elements_ft import SunFlowerVisual, PeaShooterVisual
import parameters as pt
import parametros as p


class PostWindow(QWidget):

    signal_next_round = pyqtSignal()
    signal_exit = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        
        # Music
        ## .state: 1 is playing, 2 is paused
        self.song: QMediaContent = QMediaContent(
            QUrl.fromLocalFile(pt.pt_s_music_2))
        self.playlist: QMediaPlaylist = QMediaPlaylist()
        self.playlist.addMedia(self.song)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.music_player: QMediaPlayer = QMediaPlayer()
        self.music_player.setPlaylist(self.playlist)
        self.music_player.setVolume(15)
        
        # Background image
        self.background: QLabel = QLabel(self)
        self.background_map: QPixmap = QPixmap(pt.pt_back_menu)
        self.background.resize(self.background_map.size())
        self.background.setPixmap(self.background_map)
        self.background.setScaledContents(True)
        
        # Centered, not resizable, window
        self.setFixedSize(self.background.size())
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Window gui
        self.setWindowTitle('Post-round')
        self.gui()
        self.event_connection()

    def event_connection(self) -> None:
        self.next_round.clicked.connect(
            self.signal_next_round.emit)

        self.next_round.clicked.connect(
            self.disappear)

        self.bt_exit.clicked.connect(
            self.disappear)

        self.bt_exit.clicked.connect(
            self.signal_exit.emit)
        
    def gui(self) -> None:
        # Title of section
        title: QLabel = QLabel(f'{"Round Summary": ^30s}')
        title.setStyleSheet(pt.title_style_2)
        title_lay = QHBoxLayout()
        title_lay.addStretch()
        title_lay.addWidget(title)
        title_lay.addStretch()

        # Stats
        self.stats: list = \
        [[QLabel(f'{"-":-<30s}'), QLabel(f'{"-":->10s}')] for _ in range(5)]
        for line in self.stats:
            line[0].setStyleSheet(pt.label_style_2)
            line[1].setStyleSheet(pt.label_style_2)

        # List layout
        stat_grid: QGridLayout = QGridLayout()
        for index in range(len(self.stats)):
            stat_grid.addWidget(self.stats[index][0], index, 0)
            stat_grid.addWidget(self.stats[index][1], index, 1)

        # Information
        self.information = QLabel()
        self.information.setStyleSheet(pt.title_style_2)

        # Buttons to go back
        self.next_round: QPushButton = QPushButton(parent=self,
        text='Next Round')
        self.next_round.setStyleSheet(pt.button_style)
        self.next_round.setMinimumWidth(100)
        self.bt_exit: QPushButton = QPushButton(parent=self, text='Exit')
        self.bt_exit.setStyleSheet(pt.button_style)
        self.bt_exit.setMinimumWidth(100)
        go_back_lay: QHBoxLayout = QHBoxLayout()
        go_back_lay.addStretch()
        go_back_lay.addWidget(self.next_round)
        go_back_lay.addStretch()
        go_back_lay.addWidget(self.bt_exit)
        go_back_lay.addStretch()

        # Summary layout
        middle_layout: QVBoxLayout = QVBoxLayout()
        middle_layout.addStretch()
        middle_layout.addLayout(title_lay)
        middle_layout.addSpacing(40)
        middle_layout.addLayout(stat_grid)
        middle_layout.addStretch()
        middle_layout.addWidget(self.information)
        middle_layout.addStretch()
        middle_layout.addLayout(go_back_lay)
        middle_layout.addStretch()

        self.info_layout: QHBoxLayout = QHBoxLayout()
        self.info_layout.addStretch()
        self.info_layout.addLayout(middle_layout)
        self.info_layout.addStretch()
        self.setLayout(self.info_layout)

    def launch(self, info: dict) -> None:
        self.stats[0][0].setText(f'{"Current round": <30s}')
        self.stats[0][1].setText(f'{str(info["round"]): >10s}')
        self.stats[1][0].setText(f'{"Suns left": <30s}')
        self.stats[1][1].setText(f'{str(info["suns"]): >10s}')
        self.stats[2][0].setText(f'{"Zombies killed": <30s}')
        self.stats[2][1].setText(f'{str(info["kill"]): >10s}')
        self.stats[3][0].setText(f'{"Round score": <30s}')
        self.stats[3][1].setText(f'{str(info["score"]): >10s}')
        self.stats[4][0].setText(f'{"Total score": <30s}')
        self.stats[4][1].setText(f'{str(info["total"]): >10s}')
        if info['won']:
            self.information.setText('You won! ready for the next round?')
        else:
            self.information.setText('This is the end. Exit the game.')
        self.next_round.setEnabled(info['won'])
        self.setWindowTitle(info['user'])
        self.show()
        self.music_player.play()

    def disappear(self) -> None:
        self.music_player.stop()
        self.hide()