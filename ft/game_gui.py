from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QHBoxLayout,\
    QVBoxLayout, QPushButton
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from custom_elements import SelectableLabel
from ft.elements_ft import CrazyCruz, IcePeaShooterVisual, NutVisual, Shovel,\
    SunFlowerVisual, PeaShooterVisual
import parameters as pt
import parametros as p

class GameGui(QWidget):

    # Store signals
    signal_store_plant_clicked = pyqtSignal(int)
    signal_cancel_purchase = pyqtSignal()
    signal_shovel_picked = pyqtSignal()
    signal_shovel_canceled = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        # Music
        ## .state: 1 is playing, 2 is paused
        self.song: QMediaContent = QMediaContent(
            QUrl.fromLocalFile(pt.pt_s_music_1))
        self.playlist: QMediaPlaylist = QMediaPlaylist()
        self.playlist.addMedia(self.song)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.music_player: QMediaPlayer = QMediaPlayer()
        self.music_player.setPlaylist(self.playlist)
        self.music_player.setVolume(30)

        # Centered, not resizable, window
        self.setGeometry(0, 0, 1600, 800)
        sillhouette = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        sillhouette.moveCenter(center_point)
        self.move(sillhouette.topLeft())
        self.setFixedSize(self.size())
        self.setWindowTitle('Garden')

        # Window initialization
        self.gui()

    def gui(self) -> None:
        
        # Pre-set scenario
        self.garden: SelectableLabel = SelectableLabel(self)
        self.garden.setGeometry(200, 0, 1400, 600)
        self.garden.setFixedSize(self.garden.size())
        self.garden.setScaledContents(True)

        # Ruz
        self.ruz = CrazyCruz(parent=self.garden)
        self.ruz.resize(240, 240)
        self.ruz.move(20, self.garden.height() - 240)
        self.ruz.speak(pt.ruz_diag_5)

        self.store_gui() # presents left panel
        self.control_gui() # presents bottom panel

    def store_gui(self) -> None:
        
        """
        Panel
        """
        self.store: QLabel = QLabel(self)
        self.store.setGeometry(0, 0,
            self.width() - self.garden.width() + 1, self.height())
        left_panel_color: QPixmap = QPixmap(self.store.size())
        left_panel_color.fill(QColor('green'))
        self.store.setPixmap(left_panel_color)

        """
        Plant options and shovel
        """
        # Sunflower
        self.st_sunflower: SunFlowerVisual = SunFlowerVisual(
            sgn_clicked=None, sgn_cancel_pruchase=self.signal_cancel_purchase,
            sgn_shovelled=None, draggable=True, opt=1,
            sgn_act_purchase=self.signal_store_plant_clicked, where=None)
        self.st_sunflower.setStyleSheet(pt.store_plant)
        self.st_sunflower.setPixmap(self.st_sunflower.secuence[0])
        price_sunflower = QLabel(str(p.COSTO_GIRASOL))
        price_sunflower.setStyleSheet(pt.label_style_2)
        
        # PeaShooter
        self.st_peashooter: PeaShooterVisual = PeaShooterVisual(
            sgn_clicked=None, sgn_cancel_pruchase=self.signal_cancel_purchase,
            sgn_shovelled=None, draggable=True, opt=2,
            sgn_act_purchase=self.signal_store_plant_clicked, where=None)
        self.st_peashooter.setStyleSheet(pt.store_plant)
        self.st_peashooter.setPixmap(self.st_peashooter.secuence[0])
        price_peashooter = QLabel(str(p.COSTO_LANZAGUISANTE))
        price_peashooter.setStyleSheet(pt.label_style_2)
        
        # IcePeaShooter
        self.st_iceshooter: IcePeaShooterVisual = IcePeaShooterVisual(
            sgn_clicked=None, sgn_cancel_pruchase=self.signal_cancel_purchase,
            sgn_shovelled=None, draggable=True, opt=3,
            sgn_act_purchase=self.signal_store_plant_clicked, where=None)
        self.st_iceshooter.setStyleSheet(pt.store_plant)
        self.st_iceshooter.setPixmap(self.st_iceshooter.secuence[0])
        price_iceshooter = QLabel(str(p.COSTO_LANZAGUISANTE_HIELO))
        price_iceshooter.setStyleSheet(pt.label_style_2)
        
        # Nut
        self.st_nut: NutVisual = NutVisual(
            sgn_clicked=None, sgn_cancel_purchase=self.signal_cancel_purchase,
            sgn_shovelled=None, draggable=True, opt=4,
            sgn_act_purchase=self.signal_store_plant_clicked, where=None)
        self.st_nut.setStyleSheet(pt.store_plant)
        self.st_nut.setPixmap(self.st_nut.secuence[0])
        price_nut = QLabel(str(p.COSTO_PAPA))
        price_nut.setStyleSheet(pt.label_style_2)

        # Shovel
        self.shovel: Shovel = Shovel(sgn_act=self.signal_shovel_picked,
        sgn_cancel=self.signal_shovel_canceled)
        self.shovel.setStyleSheet(pt.store_plant)

        """
        Non-interactive elements
        """
        # Title
        title = QLabel('Store')
        title.setStyleSheet(pt.title_style_2)
        
        # Decorative suns
        decorative_sun_1 = QLabel()
        decorative_sun_map = QPixmap(pt.pt_sun)
        decorative_sun_1.setPixmap(decorative_sun_map)
        decorative_sun_1.setFixedSize(30, 30)
        decorative_sun_1.setScaledContents(True)

        decorative_sun_2 = QLabel()
        decorative_sun_2.setPixmap(decorative_sun_map)
        decorative_sun_2.setFixedSize(30, 30)
        decorative_sun_2.setScaledContents(True)

        decorative_sun_3 = QLabel()
        decorative_sun_3.setPixmap(decorative_sun_map)
        decorative_sun_3.setFixedSize(30, 30)
        decorative_sun_3.setScaledContents(True)

        decorative_sun_4 = QLabel()
        decorative_sun_4.setPixmap(decorative_sun_map)
        decorative_sun_4.setFixedSize(30, 30)
        decorative_sun_4.setScaledContents(True)

        """
        Layout creation
        """
        # Boxing
        box_0: QVBoxLayout = self.hpad_this(
            title)
        box_1: QVBoxLayout = self.hpad_this(
            self.st_sunflower,
            (decorative_sun_1, price_sunflower))
        box_2: QVBoxLayout = self.hpad_this(
            self.st_peashooter,
            (decorative_sun_2, price_peashooter))
        box_3: QVBoxLayout = self.hpad_this(
            self.st_iceshooter,
            (decorative_sun_3, price_iceshooter))
        box_4: QVBoxLayout = self.hpad_this(
            self.st_nut,
            (decorative_sun_4, price_nut))
        box_5: QVBoxLayout = self.hpad_this(
            self.shovel)

        # Packing
        store_lay = QVBoxLayout()
        store_lay.addStretch()
        store_lay.addLayout(box_0)
        store_lay.addStretch()
        store_lay.addLayout(box_1)
        store_lay.addStretch()
        store_lay.addLayout(box_2)
        store_lay.addStretch()
        store_lay.addLayout(box_3)
        store_lay.addStretch()
        store_lay.addLayout(box_4)
        store_lay.addStretch()
        store_lay.addLayout(box_5)
        store_lay.addStretch()

        # Set layout to panel
        self.store.setLayout(store_lay)

    def control_gui(self) -> None:
        """
        Panel
        """
        self.controls: QLabel = QLabel(self)
        self.controls.setGeometry(
            self.store.width(),
            self.garden.height(),
            self.width() - self.store.width(),
            self.height() - self.garden.height())
        bottom_panel_color :QPixmap = QPixmap(self.controls.size())
        bottom_panel_color.fill(QColor('brown'))
        self.controls.setPixmap(bottom_panel_color)

        """
        Elements
        """
        # Sun indicator
        sun_label: QLabel = QLabel('Sun')
        sun_label.setStyleSheet(pt.title_style)
        self.ind_sun: QLabel = QLabel('0')
        self.ind_sun.setStyleSheet(pt.label_style_2)
        decorative_sun_1 = QLabel()
        decorative_sun_map = QPixmap(pt.pt_sun)
        decorative_sun_1.setPixmap(decorative_sun_map)
        decorative_sun_1.setFixedSize(40, 40)
        decorative_sun_1.setScaledContents(True)

        # Round indicator
        round_label: QLabel = QLabel('Round')
        round_label.setStyleSheet(pt.title_style)
        self.ind_round: QLabel = QLabel('0')
        self.ind_round.setStyleSheet(pt.label_style_2)

        # Score indicator
        score_label: QLabel = QLabel('Score')
        score_label.setStyleSheet(pt.title_style)
        self.ind_score: QLabel = QLabel('0')
        self.ind_score.setStyleSheet(pt.label_style_2)

        # Zombies killed indicator
        kill_label: QLabel = QLabel('Zombies killed')
        kill_label.setStyleSheet(pt.title_style)
        self.ind_kill: QLabel = QLabel('0')
        self.ind_kill.setStyleSheet(pt.label_style)

        # Zombies remaining indicator
        remaining_label: QLabel = QLabel('Zombies remaining')
        remaining_label.setStyleSheet(pt.title_style)
        self.ind_remaining: QLabel = QLabel('0')
        self.ind_remaining.setStyleSheet(pt.label_style_2)

        # Buttons
        self.bt_start: QPushButton = QPushButton(text='Start round')
        self.bt_start.setStyleSheet(pt.button_style)

        self.bt_skip: QPushButton = QPushButton(text='Skip round')
        self.bt_skip.setStyleSheet(pt.button_style)

        self.bt_pause: QPushButton = QPushButton(text='Pause')
        self.bt_pause.setStyleSheet(pt.button_style)
        
        self.bt_exit: QPushButton = QPushButton(text='Exit')
        self.bt_exit.setStyleSheet(pt.button_style)
        
        """
        Layout
        """
        # Boxing
        box_1: QVBoxLayout = self.hpad_this(
            sun_label,
            (decorative_sun_1, self.ind_sun))
        box_2: QVBoxLayout = self.hpad_this(
            round_label,
            self.ind_round)
        box_3: QVBoxLayout = self.hpad_this(
            score_label,
            self.ind_score)
        box_4: QVBoxLayout = self.hpad_this(
            (kill_label, self.ind_kill),
            (remaining_label, self.ind_remaining))
        box_5: QVBoxLayout = self.hpad_this(
            self.bt_start,
            self.bt_skip)
        box_6: QVBoxLayout = self.hpad_this(
            self.bt_pause,
            self.bt_exit)

        # Packing
        control_lay: QHBoxLayout = QHBoxLayout()
        control_lay.addStretch()
        control_lay.addLayout(box_1)
        control_lay.addStretch()
        control_lay.addLayout(box_2)
        control_lay.addStretch()
        control_lay.addLayout(box_3)
        control_lay.addStretch()
        control_lay.addLayout(box_4)
        control_lay.addStretch()
        control_lay.addLayout(box_5)
        control_lay.addStretch()
        control_lay.addLayout(box_6)
        control_lay.addStretch()

        # Set layout to the panel
        self.controls.setLayout(control_lay)

    # Magical function to align elements vertically
    def hpad_this(self, *args) -> QVBoxLayout:
        padded_boxes: list = list()
        layout = QVBoxLayout()
        for widget in args:
            local_pad = QHBoxLayout()
            local_pad.addStretch()
            if type(widget) == type(args):
                for each in widget: local_pad.addWidget(each)
            elif type(widget) == type(QVBoxLayout) or\
                type(widget) == type(QHBoxLayout):
                local_pad.addLayout(widget)
            else: local_pad.addWidget(widget)
            local_pad.addStretch()
            padded_boxes.append(local_pad)
        for box in padded_boxes:
            layout.addLayout(box)
        return layout