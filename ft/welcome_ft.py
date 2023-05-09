from PyQt5.QtWidgets import QHBoxLayout, QLabel, QDesktopWidget, \
    QPushButton, QLineEdit, QGridLayout, QVBoxLayout, QWidget,\
        QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from ft.elements_ft import SunFlowerVisual, PeaShooterVisual
import parameters as pt
import parametros as p

class WelcomeWindow(QWidget):

    signal_launched = pyqtSignal()
    signal_request_check_user = pyqtSignal(str)
    signal_go_ranks = pyqtSignal()

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

        # Containers
        self.plants: dict[str, QLabel] = dict()

        # Window gui
        self.setWindowTitle('New Game')
        self.gui()
        self.event_conection()

    def gui(self) -> None:

        # Logo
        logo: QLabel = QLabel()
        logo_map: QPixmap = QPixmap(pt.pt_logo)
        logo.resize(logo_map.size())
        logo.setPixmap(logo_map)
        logo.setScaledContents(True)
        logo.setMaximumSize(logo_map.size())
        logo_lay: QHBoxLayout = QHBoxLayout()
        logo_lay.addStretch()
        logo_lay.addWidget(logo)
        logo_lay.addStretch()
        
        
        # Buttons and user
        self.play_button: QPushButton = QPushButton(parent=self, text='Play')
        self.play_button.setStyleSheet(pt.button_style)
        self.exit_button: QPushButton = QPushButton(parent=self, text='Exit')
        self.exit_button.setStyleSheet(pt.button_style)
        self.rank_button: QPushButton = QPushButton(parent=self, text='Rankings')
        self.rank_button.setStyleSheet(pt.button_style)
        self.user_textbox: QLineEdit = QLineEdit(self)
        self.user_textbox.setPlaceholderText('Insert Username')
        holder: QGridLayout = QGridLayout()
        holder.addWidget(self.user_textbox, 0, 0, 1, 2)
        holder.addWidget(self.play_button, 1, 0, 1, 2)
        holder.addWidget(self.rank_button, 2, 0)
        holder.addWidget(self.exit_button, 2, 1)
        

        # Decoration
        
        self.plants['1'] = SunFlowerVisual(sgn_clicked=None, sgn_act_purchase=None,
            sgn_cancel_pruchase=None, sgn_shovelled=None, parent=self, where=None)
        self.plants['1'].show()
        
        self.plants['2'] = PeaShooterVisual(sgn_clicked=None, sgn_act_purchase=None,
        sgn_cancel_pruchase=None, sgn_shovelled=None, parent=self, where=None)
        self.plants['2'].show()

        # Welcome layout
        left_layout: QVBoxLayout = QVBoxLayout()
        left_layout.addSpacing(self.height() - self.plants['1'].height() + 100)
        left_layout.addWidget(self.plants['1'])
        
        middle_layout: QVBoxLayout = QVBoxLayout()
        middle_layout.addStretch()
        middle_layout.addLayout(logo_lay)
        middle_layout.addSpacing(30)
        middle_layout.addLayout(holder)
        middle_layout.addStretch()
        
        right_layout: QVBoxLayout = QVBoxLayout()
        right_layout.addSpacing(self.height() - self.plants['2'].height() + 100)
        right_layout.addWidget(self.plants['2'])
        
        self.welcome_layout: QHBoxLayout = QHBoxLayout()
        self.welcome_layout.addLayout(left_layout, 1)
        self.welcome_layout.addStretch(1)
        self.welcome_layout.addLayout(middle_layout, 3)
        self.welcome_layout.addStretch(1)
        self.welcome_layout.addLayout(right_layout, 1)

        # Window layout
        self.setLayout(self.welcome_layout)

    def dance(self, ref: str, move: int) -> None:
        self.plants[ref].setPixmap(self.plants[ref].secuence[move])

    def event_conection(self) -> None:
        self.play_button.clicked.connect(self.request_check_user)
        self.rank_button.clicked.connect(self.go_rank)
        self.exit_button.clicked.connect(exit)

    def go_rank(self) -> None:
        self.music_player.stop()
        self.hide()
        self.signal_go_ranks.emit()

    def request_check_user(self) -> None:
        name: str = self.user_textbox.text()
        self.signal_request_check_user.emit(name)

    def receive_check(self, valid: bool, errors: set) -> None:
        if valid:
            self.music_player.stop()
            self.hide()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Invalid Username")
            msg.setWindowTitle("Error")
            error = ''
            if 'void' in errors:
                error = error + 'Please enter a name.\n'
            if 'alnum' in errors:
                error = error + 'Please enter only alphanumeric characters.\n'
            if 'len' in errors:
                error = error + f"Your name's length must be between \
{p.MIN_CARACTERES} and {p.MAX_CARACTERES} characters\n" 
            msg.setInformativeText(error)            
            msg.exec_()

    def launch(self) -> None:
        self.music_player.play()
        self.signal_launched.emit()
        self.show()
