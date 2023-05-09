from PyQt5.QtCore import QObject, pyqtSignal
from custom_elements import PausableTimer
import parametros as p
from random import randint as rint, choice
from math import ceil


class SunLogic(QObject):

    """
    Must receive starting position as raw coords. We save suns under a
    numeric reference in a dictionary in both front and back
    """

    def __init__(self, sgn_travel: pyqtSignal, mode: str, where: tuple,
    ref: int) -> None:
        super().__init__()

        # Attributes
        self.mode: str = mode
        self.ref: int = ref
        self._x: int = where[0]
        self._y: int = where[1]
        self.limits: tuple = self.set_limits(where, mode)

        # Set signals
        self.signal_travel: pyqtSignal = sgn_travel

        # Set up entity
        self.create_timers()

    def set_limits(self, where: tuple, mode: str) -> tuple:
        match mode:
            
            case 'fall':
                limx = where[0]
                limy = choice(range(211, 350))
                return (limx, limy)
            
            case 'produce':
                limx = where[0] + 50 * ((-1) ** rint(1, 2))
                limy = where[1] + 70
                return (limx, limy)

    def travel(self) -> None:
        if self.me_y == self.limits[1]: self.travel_timer.stop()
        self.me_x += rint(3, 6)
        self.me_y += rint(6, 10)
        self.signal_travel.emit(self.ref, (self.me_x, self.me_y))

    def get_x(self): return self._x
    def set_x(self, val): 
        if val <= self.limits[0]: self._x = val
    me_x = property(get_x, set_x)

    def get_y(self): return self._y
    def set_y(self, val):
        if val <= self.limits[1]: self._y = val
        else: self._y = self.limits[1]
    me_y = property(get_y, set_y)

    def create_timers(self) -> None:
        self.travel_timer: PausableTimer = PausableTimer()
        self.travel_timer.setInterval(20)
        self.travel_timer.timeout.connect(self.travel)

    def start_timers(self) -> None:
        self.travel_timer.start()

    def pause_timers(self) -> None:
        if self.travel_timer.isActiving(): self.travel_timer.pause()

    def unpause_timers(self) -> None:
        if self.travel_timer.isPaused(): self.travel_timer.unpause()
    
    def stop_timers(self) -> None:
        self.travel_timer.stop()
    

class PeaLogic(QObject):

    def __init__(self, sgn_dance: pyqtSignal, sgn_death: pyqtSignal, ref: int,
    sgn_travel: pyqtSignal, where: tuple, ice: bool, row: int) -> None:
        super().__init__()

        # Attributes
        self.ice: bool = ice
        self.damage: int = p.DANO_PROYECTIL
        self._x: int = where[0]
        self._y: int = where[1]
        self.row: int = row
        self.ref: int = ref
        self._dance_move: int = 0

        # Set signals
        self.signal_travel: pyqtSignal = sgn_travel
        self.signal_death: pyqtSignal = sgn_death
        self.signal_dance: pyqtSignal = sgn_dance

        # Set up entity
        self.create_timers()

    def get_x(self): return self._x
    def set_x(self, val):
        if val < 1400: self._x = val
        else:
            self.stop_timers()
            self.signal_death.emit(self.row, self.ref)
    me_x = property(get_x, set_x)

    def get_y(self): return self._y
    def set_y(self, val): self._y = val
    me_y = property(get_y, set_y)

    def get_move(self): return self._dance_move
    def set_move(self, val):
        if val > 2: self.signal_death.emit(self.row, self.ref)
        else: self._dance_move = val
    dance_move = property(get_move, set_move)

    def create_timers(self) -> None:
        self.travel_timer: PausableTimer = PausableTimer()
        self.travel_timer.setInterval(15)
        self.travel_timer.timeout.connect(self.travel)
        
        self.explode_timer: PausableTimer = PausableTimer()
        self.explode_timer.setInterval(60)
        self.explode_timer.timeout.connect(self.explode_animate)

    def travel(self) -> None:
        self.me_x += 4
        self.signal_travel.emit(self.row, self.ref, (self.me_x, self.me_y))

    def explode_animate(self) -> None:
        self.signal_dance.emit(self.row, self.ref, self.dance_move)
        self.dance_move += 1

    def explode(self) -> None:
        self.travel_timer.stop()
        self.explode_timer.start()

    def start_timers(self) -> None:
        self.travel_timer.start()

    def pause_timers(self) -> None:
        if self.travel_timer.isActiving(): self.travel_timer.pause()
        if self.explode_timer.isActiving(): self.explode_timer.pause()

    def unpause_timers(self) -> None:
        if self.travel_timer.isPaused(): self.travel_timer.unpause()
        if self.explode_timer.isPaused(): self.explode_timer.unpause()

    def stop_timers(self) -> None:
        self.travel_timer.stop()
        self.explode_timer.stop()


class ZombieLogic(QObject):

    def __init__(self, sgn_dance: pyqtSignal, sgn_death: pyqtSignal,
    sgn_travel: pyqtSignal, sgn_eat: pyqtSignal, fast: bool,
    row: int, ref: int, where: tuple, sgn_won: pyqtSignal) -> None:
        super().__init__()

        # Attributes
        self.row: int = row
        self.ref: int = ref
        self._fast: bool = fast
        self._x: int = where[0]
        self._y: int = where[1]
        self._slowed: bool = False
        self._hp: int = p.VIDA_ZOMBIE
        self._eating: bool = False
        self._walk_dance_move: int = 0
        self._eat_dance_move: int = 0
        self._eating_at: str = str()

        # Set signals
        self.signal_dance: pyqtSignal = sgn_dance
        self.signal_death: pyqtSignal = sgn_death
        self.signal_travel: pyqtSignal = sgn_travel
        self.signal_eat: pyqtSignal = sgn_eat
        self.signal_won: pyqtSignal = sgn_won

        # Set up entity
        self.create_timers()

    def get_hp(self): return self._hp
    def set_hp(self, val):
        if val <= 0: self.signal_death.emit(self.row, self.ref)
        self._hp = val
    HP = property(get_hp, set_hp)

    def get_x(self): return self._x
    def set_x(self, val):
        if val > 200: self._x = val
        else: self.signal_won.emit()
    me_x = property(get_x, set_x)

    def get_y(self): return self._y
    def set_y(self, val): self._y = val
    me_y = property(get_y, set_y)

    def get_walk_move(self): return self._walk_dance_move
    def set_walk_move(self, val):
        if val > 1: self._walk_dance_move = 0
        else: self._walk_dance_move = val
    walk_move = property(get_walk_move, set_walk_move)

    def get_eat_move(self): return self._eat_dance_move
    def set_eat_move(self, val):
        if val > 2: self._eat_dance_move = 0
        else: self._eat_dance_move = val
    eat_move = property(get_eat_move, set_eat_move)

    def create_timers(self):
        self.walk_dance_timer: PausableTimer = PausableTimer()
        if self._fast: self.walk_dance_timer.setInterval(rint(300, 400))
        else: self.walk_dance_timer.setInterval(rint(700, 800))
        self.walk_dance_timer.timeout.connect(self.walk_dance)

        self.eat_dance_timer: PausableTimer = PausableTimer()
        self.eat_dance_timer.setInterval(500)
        self.eat_dance_timer.timeout.connect(self.eat_dance)

        self.travel_timer: PausableTimer = PausableTimer()
        self.travel_timer.setInterval(200)
        self.travel_timer.timeout.connect(self.walk)
        
        self.eat_timer: PausableTimer = PausableTimer()
        self.eat_timer.setInterval(p.INTERVALO_TIEMPO_MORDIDA)
        self.eat_timer.timeout.connect(self.eat)

    def walk_dance(self) -> None:
        self.signal_dance.emit(True, self.row, self.ref, self.walk_move)
        self.walk_move += 1

    def eat_dance(self) -> None:
        self.signal_dance.emit(False, self.row, self.ref, self.eat_move)
        self.eat_move += 1

    def walk(self) -> None:
        if not self._slowed:
            step = p.VELOCIDAD_ZOMBIE
        else:
            step = p.VELOCIDAD_ZOMBIE * (1 - p.RALENTIZAR_ZOMBIE)
        if self._fast: step = step * 1.5
        self.me_x = ceil(self.me_x - step)
        self.signal_travel.emit(self.row, self.ref, (self.me_x, self.me_y))

    def eat(self) -> None:
        self.signal_eat.emit(self._eating_at)

    def start_eating(self, at: str) -> None:
        self.travel_timer.stop()
        self.walk_dance_timer.stop()
        self.eat_dance_timer.start()
        self.eat_timer.start()
        self._eating_at = at

    def stop_eating(self) -> None:
        self.eat_dance_timer.stop()
        self.eat_timer.stop()
        self.travel_timer.start()
        self.walk_dance_timer.start()

    def slow_down(self) -> None:
        if not self._slowed:
            self.walk_dance_timer.setInterval(self.walk_dance_timer.interval() * 2)

    def start_timers(self) -> None:
        self.walk_dance_timer.start()
        self.travel_timer.start()

    def pause_timers(self) -> None:
        if self.walk_dance_timer.isActiving(): self.walk_dance_timer.pause()
        if self.travel_timer.isActiving(): self.travel_timer.pause()
        if self.eat_timer.isActiving(): self.eat_timer.pause()
        if self.eat_dance_timer.isActiving(): self.eat_dance_timer.pause()

    def unpause_timers(self) -> None:
        if self.walk_dance_timer.isPaused(): self.walk_dance_timer.unpause()
        if self.travel_timer.isPaused(): self.travel_timer.unpause()
        if self.eat_timer.isPaused(): self.eat_timer.unpause()
        if self.eat_dance_timer.isPaused(): self.eat_dance_timer.unpause()

    def stop_timers(self) -> None:
        self.travel_timer.stop()
        self.walk_dance_timer.stop()
        self.eat_dance_timer.stop()
        self.eat_timer.stop()
