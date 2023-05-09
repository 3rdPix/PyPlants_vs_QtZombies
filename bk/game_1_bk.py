from PyQt5.QtCore import QObject, pyqtSignal
from bk.elements_1_bk import PlantLogic
from bk.elements_2_bk import PeaLogic, SunLogic, ZombieLogic
import parametros as p
import parameters as pt


class GameLogicLoad(QObject):

    """
    Signals
    """
    # Stats updaters
    signal_update_sun = pyqtSignal(int)
    signal_update_round = pyqtSignal(int)
    signal_update_score = pyqtSignal(int)
    signal_update_kill = pyqtSignal(int)
    signal_update_remaining = pyqtSignal(int)

    # General effects
    signal_mute = pyqtSignal()
    signal_unmute = pyqtSignal()
    signal_pause = pyqtSignal()
    signal_unpause = pyqtSignal()
    signal_lose = pyqtSignal()
    signal_win = pyqtSignal()
    signal_go_post_game = pyqtSignal(dict)
    signal_new_round = pyqtSignal(str, int)

    # Object generation and degeneration
    signal_create_plant = pyqtSignal(str, int)
    signal_kill_plant = pyqtSignal(str)
    signal_create_sun = pyqtSignal(int, int, int)
    signal_kill_sun = pyqtSignal(int)
    signal_kill_pea = pyqtSignal(int, int)
    signal_create_zombie = pyqtSignal(tuple, int, int, bool)
    signal_kill_zombie = pyqtSignal(int, int)
    
    """
    Signals to lower levels
    """
    # Animation related
    sgn_plant_dance = pyqtSignal(str, int)
    sgn_pea_dance = pyqtSignal(int, int, int)
    sgn_zombie_dance = pyqtSignal(bool, int, int, int)

    # Movement related
    sgn_travel_sun = pyqtSignal(int, tuple)
    sgn_travel_pea = pyqtSignal(int, int, tuple)
    sgn_travel_zombie = pyqtSignal(int, int, tuple)

    # Special effects
    sgn_sunflower_produce = pyqtSignal(str, int)
    sgn_peashooter_shoot = pyqtSignal(str, bool)
    sgn_peashooter_shoot_inform = pyqtSignal(dict)
    sgn_zombie_won = pyqtSignal()
    sgn_zombie_eat = pyqtSignal(str)

    # Active piece
    sgn_plant_death = pyqtSignal(str)
    sgn_pea_death = pyqtSignal(int, int)
    sgn_zombie_death = pyqtSignal(int, int)
    

    """
    Other signals
    """
    signal_ruz_speak = pyqtSignal(str)

    """
    Module initialization
    """
    def __init__(self) -> None:
        super().__init__()

        # Attributes creation
        self.create_round_properties(1)
        self.create_status_variables()
        self.create_containers()
        self.signal_connection()

    def create_round_properties(self, round: int) -> None:
        self._sun: int = p.SOLES_INICIALES
        self._round: int = round
        self._score: int = 0
        self._kill: int = 0
        self._remaining: int = p.N_ZOMBIES * 2
        self._writing_secuence: str = '000'
        self._row1_zombies_counter: int = 0
        self._row2_zombies_counter: int = 0
        self.most_left_zomb_row1: ZombieLogic = None
        self.most_left_zomb_row2: ZombieLogic = None
        self._bullets_counter: int = 0
        self._zombies_counter: int = 0
        self._won: bool = True
        
    def create_status_variables(self) -> None:
        # Gameplay related
        self._in_round: bool = False
        self._muted: bool = False
        self._paused: bool = False
        
        # Gardening?) related
        self._shovelling: bool = False
        self._buying: bool = False
        self._to_buy: int = 0
        
    def create_containers(self) -> None:
        self.plants_in_grid: dict[str, PlantLogic] = dict()
        self.bullets_row1: dict[int, PeaLogic] = dict()
        self.bullets_row2: dict[int, PeaLogic] = dict()
        self.zombies_row1: dict[int, ZombieLogic] = dict()
        self.zombies_row2: dict[int,ZombieLogic] = dict()
        self.suns: dict[int, SunLogic] = dict()

    def launch(self, lvl: int, user: str) -> None:
        self.create_instance_attributes(lvl, user)

    def create_instance_attributes(self, lvl: int, user: str) -> None:
        self._lvl: int = lvl
        self._user: str = user
        self.sun = self.sun
        self.round = self.round
        self.score = self.score
        self.kill = self.kill
        self.remaining = self.remaining
        match self._lvl:
            case 1: self._pond: int = p.PONDERADOR_DIURNO
            case 2: self._pond: int = p.PONDERADOR_NOCTURNO

    """
    Properties
    """
    def get_sun(self) -> int: return self._sun
    def set_sun(self, value) -> None:
        self._sun = value
        self.signal_update_sun.emit(self.sun)
    sun = property(get_sun, set_sun)

    def get_round(self) -> int: return self._round
    def set_round(self, value) -> None:
        self._round = value
        self.signal_update_round.emit(self.round)
    round = property(get_round, set_round)

    def get_score(self) -> int: return self._score
    def set_score(self, value) -> None:
        self._score = value
        self.signal_update_score.emit(self.score)
    score = property(get_score, set_score)

    def get_kill(self) -> int: return self._kill
    def set_kill(self, value) -> None:
        self._kill = value
        self.signal_update_kill.emit(self.kill)
        if self.kill == 2 * p.N_ZOMBIES and self._in_round:
            self.win()
    kill = property(get_kill, set_kill)

    def get_remaining(self) -> int: return self._remaining
    def set_remaining(self, value) -> None:
        self._remaining = value
        self.signal_update_remaining.emit(self.remaining)
    remaining = property(get_remaining, set_remaining)

    def get_secuence(self) -> str: return self._writing_secuence
    def set_secuence(self, letter) -> None:
        self._writing_secuence += letter
        if 'sun' in self.phrase:
            self.sun += p.SOLES_EXTRA
            self.signal_ruz_speak.emit(pt.ruz_diag_6)
            self._writing_secuence = '000'
        if 'kil' in self.phrase: self.kill_cheat()
        if len(self.phrase) >= 6:
            self._writing_secuence = self.phrase[3::]
    phrase = property(get_secuence, set_secuence)