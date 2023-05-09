from PyQt5.QtCore import pyqtSignal, QObject, QPoint, QMutex
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtWidgets import QLabel
from ft.game_gui import GameGui
from custom_elements import SensibleLabel
from ft.elements_ft import IcePeaShooterVisual, NutVisual, PeaShooterVisual, PlantVisual, PeaVisual, SunFlowerVisual, SunVisual, ZombieVisual
import parameters as pt


class GameWindow(GameGui):

    """
    Signals
    """
    # Module
    signal_launched = pyqtSignal(int, str)

    # Buttons
    signal_start_round = pyqtSignal()
    signal_request_pause = pyqtSignal()
    signal_skip_round = pyqtSignal()

    # Object interaction
    sgn_cell_click = pyqtSignal(tuple)
    sgn_plant_clicked = pyqtSignal(str)
    sgn_plant_shovelled = pyqtSignal(str)
    sgn_sun_grab = pyqtSignal(int)

    # Other
    signal_key_pressed = pyqtSignal(str)


    """
    Module initialization
    """
    def __init__(self) -> None:
        super().__init__()

        # Set up
        self.cell_coordinates: dict = pt.cell_coord
        self.sensible_grid: dict = self.create_grid()
        self.create_containers()
        self.event_connection()
        self.signal_connection()

    def create_grid(self) -> dict:
        grid: dict = dict()
        for key in self.cell_coordinates:
            cell = SensibleLabel(
                parent=self.garden,
                signal_clicked=self.sgn_cell_click)
            cell.setGeometry(
                self.cell_coordinates[key][0],
                self.cell_coordinates[key][1],
                73, 97)
            grid[key] = cell
        return grid

    def create_containers(self) -> None:
        self.plants_in_grid: dict[str, PlantVisual] = dict()
        self.bullets_row1: dict[int, PeaVisual] = dict()
        self.bullets_row2: dict[int, PeaVisual] = dict()
        self.zombies_row1: dict[int, ZombieVisual] = dict()
        self.zombies_row2: dict[int, ZombieVisual] = dict()
        self.suns: dict[int, SunVisual] = dict()

    def launch(self, packed_level: tuple, user: str) -> None:
        path, level = packed_level
        garden_map: QPixmap = QPixmap(path)
        self.garden.setPixmap(garden_map)
        self.setWindowTitle(user)
        self.signal_launched.emit(level, user)
        self.show()
        self.music_player.play()

    def event_connection(self) -> None:
        self.bt_start.clicked.connect(
            self.start_round)

        self.bt_pause.clicked.connect(
            self.signal_request_pause.emit)
        
        self.bt_skip.clicked.connect(
            self.signal_skip_round.emit)

        self.bt_exit.clicked.connect(exit)

    def signal_connection(self) -> None:
        self.signal_shovel_picked.connect(
            self.prepare_shovel)

        self.signal_shovel_canceled.connect(
            self.cancel_shovel)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        self.signal_key_pressed.emit(event.text())
        return super().keyReleaseEvent(event)
    
    """
    Stats updating system
    """
    def update_sun(self, quantity: int) -> None:
        self.ind_sun.setText(str(quantity))
        self.ind_sun.repaint()

    def update_round(self, round: int) -> None:
        self.ind_round.setText(str(round))
        self.ind_round.repaint()

    def update_score(self, score: int) -> None:
        self.ind_score.setText(str(score))
        self.ind_score.repaint()

    def update_kill(self, kills: int) -> None:
        self.ind_kill.setText(str(kills))
        self.ind_kill.repaint()

    def update_remaining(self, remaining: int) -> None:
        self.ind_remaining.setText(str(remaining))
        self.ind_remaining.repaint()

    """
    General effects
    """
    def mute(self) -> None:
        self.music_player.setVolume(0)

    def unmute(self) -> None:
        self.music_player.setVolume(30)

    def pause(self) -> None:
        self.music_player.pause()
        self.store.setEnabled(False)
        self.garden.setEnabled(False)
        self.bt_pause.setText('Unpause')
        self.ruz.bubble.hide()

    def unpause(self) -> None:
        self.store.setEnabled(True)
        self.garden.setEnabled(True)
        self.bt_pause.setText('Pause')
        self.music_player.play()
        self.ruz.bubble.show()

    def start_round(self) -> None:
        self.bt_start.setEnabled(False)
        self.signal_start_round.emit()

    def lose(self) -> None:
        self.you_lost: QLabel = QLabel(parent=self.garden)
        self.you_lost.resize(700, 500)
        self.you_lost.setFixedSize(self.you_lost.size())
        map = QPixmap(pt.pt_text)
        self.you_lost.setPixmap(map)
        self.you_lost.setScaledContents(True)
        self.you_lost.move(350, 40)
        self.you_lost.show()
        self.music_player.stop()
        self.ruz.sing()
        self.ruz.speak('Ouch!')
        self.store.setEnabled(False)
        self.controls.setEnabled(False)
        
    def win(self) -> None:
        self.music_player.stop()
        self.ruz.speak(pt.ruz_diag_17)
        self.ruz.sing()
        self.store.setEnabled(False)
        self.controls.setEnabled(False)

    def reset_all(self) -> None:
        plant = list(self.plants_in_grid.keys())
        for each in plant: self.kill_plant(each)
        bullet1 = list(self.bullets_row1.keys())
        for each in bullet1: self.kill_pea(1, each)
        bullet2 = list(self.bullets_row2.keys())
        for each in bullet2: self.kill_pea(2, each)
        zomb1 = list(self.zombies_row1.keys())
        for each in zomb1: self.kill_zombie(1, each)
        zomb2 = list(self.zombies_row2.keys())
        for each in zomb2: self.kill_zombie(2, each)
        suns = list(self.suns.keys())
        for each in suns: self.kill_sun(each)
        self.store.setEnabled(True)
        self.controls.setEnabled(True)
        self.bt_start.setEnabled(True)
    
    def new_round(self, user: str, lvl: int) -> None:
        self.reset_all()
        self.create_containers()
        self.ruz.speak(pt.ruz_diag_5)
        self.signal_launched.emit(lvl, user)
        self.store.setEnabled(True)
        self.controls.setEnabled(True)
        self.show()
        self.music_player.play()
    
    def disappear(self, *args) -> None:
        self.music_player.stop()
        self.hide()

    """
    Animation creation
    """
    def dance_plant(self, index_in_grid: str, move: int) -> None:
        self.plants_in_grid[index_in_grid].setPixmap(
            self.plants_in_grid[index_in_grid].secuence[move])

    def dance_zombie(self, walk: bool, row: int, ref: int, move: int) -> None:
        match row:
            case 1:
                if walk:
                    self.zombies_row1[ref].setPixmap(
                    self.zombies_row1[ref].secuence[move])
                else:
                    self.zombies_row1[ref].setPixmap(
                    self.zombies_row1[ref].eat_secuence[move])
            case 2:
                if walk:
                    self.zombies_row2[ref].setPixmap(
                    self.zombies_row2[ref].secuence[move])
                else:
                    self.zombies_row2[ref].setPixmap(
                    self.zombies_row2[ref].eat_secuence[move])

    def dance_pea(self, row: int, ref: int, move: int) -> None:
        match row:
            case 1:
                self.bullets_row1[ref].setPixmap(
                self.bullets_row1[ref].secuence[move])
            case 2:
                self.bullets_row2[ref].setPixmap(
                self.bullets_row2[ref].secuence[move])

    """
    Movement creation
    """
    def travel_sun(self, ref: int, where: tuple) -> None:
        self.suns[ref].move(where[0], where[1])

    def travel_zombie(self, row: int, ref: int, where: tuple) -> None:
        x, y = where
        match row:
            case 1: self.zombies_row1[ref].move(x, y)
            case 2: self.zombies_row2[ref].move(x, y)

    def travel_pea(self, row: int, ref: int, where: tuple) -> None:
        x, y = where
        match row:
            case 1: 
                if ref in self.bullets_row1.keys():
                    self.bullets_row1[ref].move(x, y)
                    
            case 2:
                if ref in self.bullets_row2.keys():
                    self.bullets_row2[ref].move(x, y)

    """
    Store
    """
    def prepare_shovel(self) -> None:
        self.ruz.speak(pt.ruz_diag_12)
        for plant in self.plants_in_grid.values():
            plant.awaiting_death = True
            plant.setAcceptDrops(True)

    def cancel_shovel(self) -> None:
        self.ruz.speak(pt.ruz_diag_15)
        for plant in self.plants_in_grid.values():
            plant.awaiting_death = False
            plant.setAcceptDrops(False)

    """
    Generation and degeneration
    """

    def create_plant(self, index: str, type: int) -> None:
        where = self.cell_coordinates[index]
        match type:
            case 1:
                self.plants_in_grid[index] = SunFlowerVisual(
                    parent=self.garden,
                    where=index,
                    sgn_clicked=self.sgn_plant_clicked,
                    sgn_cancel_pruchase=None,
                    sgn_shovelled=self.sgn_plant_shovelled,
                    draggable=False,
                    pos=QPoint(where[0], where[1]))
            case 2:
                self.plants_in_grid[index] = PeaShooterVisual(
                    parent=self.garden,
                    where=index,
                    sgn_clicked=self.sgn_plant_clicked,
                    sgn_cancel_pruchase=None,
                    sgn_shovelled=self.sgn_plant_shovelled,
                    draggable=False,
                    pos=QPoint(where[0], where[1]))
            case 3:
                self.plants_in_grid[index] = IcePeaShooterVisual(
                    parent=self.garden,
                    where=index,
                    sgn_clicked=self.sgn_plant_clicked,
                    sgn_cancel_pruchase=None,
                    sgn_shovelled=self.sgn_plant_shovelled,
                    draggable=False,
                    pos=QPoint(where[0], where[1]))
            case 4:
                self.plants_in_grid[index] = NutVisual(
                    parent=self.garden,
                    where=index,
                    sgn_clicked=self.sgn_plant_clicked,
                    sgn_cancel_purchase=None,
                    sgn_shovelled=self.sgn_plant_shovelled,
                    draggable=False,
                    pos=QPoint(where[0], where[1]))
        self.plants_in_grid[index].setPixmap(self.plants_in_grid[index].secuence[0])
        self.plants_in_grid[index].show()

    def kill_plant(self, index: str) -> None:
        try:
            plant = self.plants_in_grid[index]
            plant.deleteLater()
            del self.plants_in_grid[index]
        except KeyError: pass

    def create_sun(self, ref: int, x: int, y: int) -> None:
        self.suns[ref] = SunVisual(sgn_take=self.sgn_sun_grab, pos=QPoint(x, y),
        parent=self.garden, ref=ref)
        self.suns[ref].show()
    
    def kill_sun(self, ref: int) -> None:
        try:
            sun = self.suns[ref]
            sun.deleteLater()
            del self.suns[ref]
        except KeyError: pass

    def pea_shoot(self, inform: dict) -> None:
        match inform['row']:
            case 1:
                self.bullets_row1[inform['ref']] = PeaVisual(ice=inform['typ'],
                parent=self.garden, pos=QPoint(inform['x'], inform['y']))
                self.bullets_row1[inform['ref']].show()
            case 2:
                self.bullets_row2[inform['ref']] = PeaVisual(ice=inform['typ'],
                parent=self.garden, pos=QPoint(inform['x'], inform['y']))
                self.bullets_row2[inform['ref']].show()

    def kill_pea(self, row: int, ref: int) -> None:
        try:    
            match row:
                case 1: bullet = self.bullets_row1[ref]
                case 2: bullet = self.bullets_row2[ref]
            bullet.deleteLater()
            match row:
                case 1: del self.bullets_row1[ref]
                case 2: del self.bullets_row2[ref]
        except KeyError: pass

    def create_zombie(self, where: tuple, row: int, ref: int, fast: bool) -> None:
        x, y = where
        match row:
            case 1:
                self.zombies_row1[ref] = ZombieVisual(
                    fast=fast, pos=QPoint(x, y), parent=self.garden)
                self.zombies_row1[ref].show()
            case 2:
                self.zombies_row2[ref] = ZombieVisual(
                    fast=fast, pos=QPoint(x, y), parent=self.garden)
                self.zombies_row2[ref].show()

    def kill_zombie(self, row: int, ref: int) -> None:
        try:
            match row:
                case 1: creature = self.zombies_row1[ref]
                case 2: creature = self.zombies_row2[ref]
            creature.deleteLater()
            match row:
                case 1: del self.zombies_row1[ref]
                case 2: del self.zombies_row2[ref]
            self.ruz.sing()
        except KeyError: pass

    """
    Other
    """
    def ruz_speak(self, motto: str) -> None: self.ruz.speak(motto)