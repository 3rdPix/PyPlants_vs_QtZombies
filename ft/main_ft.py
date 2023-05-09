from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget,\
    QGraphicsOpacityEffect, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QPixmap
from custom_elements import SelectableLabel
from ft.elements_ft import CrazyCruz
import parameters as pt


class MainWindow(QWidget):

    signal_request_check_selection = pyqtSignal(float, float, str)
    signal_me_cell_clicked = pyqtSignal(QLabel)

    def __init__(self) -> None:
        super().__init__()
        self.user: str = str()
        
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
        
        # Centered, not resizable, window
        self.setGeometry(0, 0, 1600, 800)
        sillhouette = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        sillhouette.moveCenter(center_point)
        self.move(sillhouette.topLeft())
        self.setFixedSize(self.size())
        self.setWindowTitle('Main window')

        # Background image
        self.background: QLabel = QLabel(self)
        self.background_map: QPixmap = QPixmap(pt.pt_back_menu)
        self.background.resize(self.size())
        self.background.setPixmap(self.background_map)
        self.background.setScaledContents(True)
        
        # Initialize elements
        self.gui()

    def gui(self):
        
        """
        Level options on the left side
        """
        # Day
        self.day_option: SelectableLabel = SelectableLabel(self)
        self.day_option.setFixedSize(500, 300)
        day_option_map: QPixmap = QPixmap(pt.pt_back_day)
        self.day_option.setPixmap(day_option_map)
        self.day_option.setScaledContents(True)
        self.day_opacity: QGraphicsOpacityEffect = QGraphicsOpacityEffect()
        self.day_opacity.setOpacity(1)
        self.day_option.setGraphicsEffect(self.day_opacity)
        day_option_lay: QHBoxLayout = QHBoxLayout()
        day_option_lay.addStretch()
        day_option_lay.addWidget(self.day_option)
        day_option_lay.addStretch()

        # Night
        self.night_option: SelectableLabel = SelectableLabel(self)
        self.night_option.setFixedSize(500, 300)
        night_option_map: QPixmap = QPixmap(pt.pt_back_night)
        self.night_option.setPixmap(night_option_map)
        self.night_option.setScaledContents(True)
        self.night_opacity: QGraphicsOpacityEffect = QGraphicsOpacityEffect()
        self.night_opacity.setOpacity(1)
        self.night_option.setGraphicsEffect(self.night_opacity)
        night_option_lay :QHBoxLayout = QHBoxLayout()
        night_option_lay.addStretch()
        night_option_lay.addWidget(self.night_option)
        night_option_lay.addStretch()

        # Set layout
        left_layout = QVBoxLayout()
        left_layout.addLayout(day_option_lay)
        left_layout.addLayout(night_option_lay)

        """
        Character and button on the right side
        """
        # CrazyCruz
        self.ruz: CrazyCruz = CrazyCruz(parent=self)
        self.ruz.setFixedSize(400, 400)
        self.ruz.speak(pt.ruz_diag_1)
        ruz_lay: QHBoxLayout = QHBoxLayout()
        ruz_lay.addStretch()
        ruz_lay.addWidget(self.ruz)
        ruz_lay.addStretch()

        # Button
        self.play_button: QPushButton = QPushButton(text='Start game')
        self.play_button.setStyleSheet(pt.button_style)
        button_lay: QHBoxLayout = QHBoxLayout()
        button_lay.addStretch()
        button_lay.addWidget(self.play_button)
        button_lay.addStretch()

        # Set layout
        right_layout: QVBoxLayout = QVBoxLayout()
        right_layout.addLayout(ruz_lay)
        right_layout.addLayout(button_lay)

        """
        Final window's settings
        """
        win_lay: QHBoxLayout = QHBoxLayout()
        win_lay.addLayout(left_layout)
        win_lay.addLayout(right_layout)
        self.setLayout(win_lay)

    def launch(self, user: str) -> None:
        self.user = user
        self.signals_connection()
        self.event_connection()
        self.show()
        self.music_player.play()

    def event_connection(self) -> None:
        self.play_button.clicked.connect(self.request_check)

    def request_check(self):
        self.signal_request_check_selection.emit(
            self.day_opacity.opacity(),
            self.night_opacity.opacity(),
            self.user)
        
    def receive_check(self, valid: bool) -> None:
        if valid:
            self.music_player.stop()
            self.hide()
        else:
            self.ruz.speak(pt.ruz_diag_2)

    def signals_connection(self) -> None:
        self.day_option.signal_clicked.connect(self.choose_day)
        self.night_option.signal_clicked.connect(self.choose_night)

    def choose_day(self) -> None:
        self.day_opacity.setOpacity(1)
        self.night_opacity.setOpacity(0.5)
        self.ruz.speak(pt.ruz_diag_3)

    def choose_night(self) -> None:
        self.day_opacity.setOpacity(0.5)
        self.night_opacity.setOpacity(1)
        self.ruz.speak(pt.ruz_diag_4)

    def reset_all(self) -> None:
        self.day_opacity.setOpacity(1)
        self.night_opacity.setOpacity(1)
        self.ruz.speak(pt.ruz_diag_1)