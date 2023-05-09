from PyQt5.QtCore import QObject, pyqtSignal
from custom_elements import PausableTimer
import parametros as p
from random import randint as rint


class PlantLogic(QObject):

    def __init__(self, health_points: int, static: bool, cost: int,
    sgn_dance: pyqtSignal, sgn_death: pyqtSignal, where: str) -> None:
        super().__init__()
        self._hp: int = health_points
        self.cost: int = cost
        self.static: bool = static
        self.where: str = where
        self._dance_move: int = 0

        # Set signals
        self.signal_dance: pyqtSignal = sgn_dance
        self.signal_death: pyqtSignal = sgn_death
        
    def get_hp(self): return self._hp
    def set_hp(self, value):
        if value <= 0:
            self._hp = 0
            self.signal_death.emit(self.where)
        else: self._hp = value
    HP = property(get_hp, set_hp)

    def start_timers(self): pass
    def pause_timers(self): pass
    def unpause_timers(self): pass
    def stop_timers(self): pass


class SunFlowerLogic(PlantLogic):

    cost = p.COSTO_GIRASOL

    def __init__(self, sgn_produce: pyqtSignal, static: bool,
    sgn_dance: pyqtSignal, sgn_death: pyqtSignal, where: str) -> None:
        super().__init__(
            health_points=p.VIDA_PLANTA,
            static=static,
            cost=p.COSTO_GIRASOL,
            sgn_dance=sgn_dance,
            sgn_death=sgn_death,
            where=where)
        
        # Set signals
        self.signal_produce: pyqtSignal = sgn_produce

        # Set up flower
        self.create_timers()

    def get_move(self): return self._dance_move
    def set_move(self, val):
        if val > 1: self._dance_move = 0
        else: self._dance_move = val
    dance_move = property(get_move, set_move)

    def create_timers(self) -> None:
        self.dance_timer: PausableTimer = PausableTimer()
        self.dance_timer.setInterval(rint(450, 550))
        self.dance_timer.timeout.connect(self.dance)

        self.production_timer: PausableTimer = PausableTimer()
        self.production_timer.setInterval(p.INTERVALO_SOLES_GIRASOL)
        self.production_timer.timeout.connect(self.produce)

    def dance(self) -> None:
        self.signal_dance.emit(self.where, self.dance_move)
        self.dance_move += 1

    def produce(self) -> None:
        if self.signal_produce: self.signal_produce.emit(self.where, p.CANTIDAD_SOLES)

    def start_timers(self) -> None:
        if self.static: return
        self.dance_timer.start()
        self.production_timer.start()

    def pause_timers(self) -> None:
        if self.dance_timer.isActiving(): self.dance_timer.pause()
        if self.production_timer.isActiving(): self.production_timer.pause()

    def unpause_timers(self) -> None:
        if self.dance_timer.isPaused(): self.dance_timer.unpause()
        if self.production_timer.isPaused(): self.production_timer.unpause()

    def stop_timers(self) -> None:
        self.dance_timer.stop()
        self.production_timer.stop()


class ShooterLogic(PlantLogic):

    def __init__(self, sgn_shoot: pyqtSignal, static: bool, cost: int,
    sgn_dance: pyqtSignal, sgn_death: pyqtSignal, where: str, typ: bool) -> None:
        super().__init__(
            health_points=p.VIDA_PLANTA,
            static=static, 
            cost=cost,
            sgn_dance=sgn_dance,
            sgn_death=sgn_death,
            where=where)
        
        # Attributes
        self.typ: bool = typ

        # Set signals
        self.signal_shoot: pyqtSignal = sgn_shoot

        # Set up plant
        self.create_timers()

    def get_move(self): return self._dance_move
    def set_move(self, val):
        if val > 2: self._dance_move = 0
        else: self._dance_move = val
    dance_move = property(get_move, set_move)

    def create_timers(self) -> None:
        self.shoot_timer: PausableTimer = PausableTimer()
        self.shoot_timer.setInterval(p.INTERVALO_DISPARO)
        self.shoot_timer.timeout.connect(self.shoot)

        self.dance_timer: PausableTimer = PausableTimer()
        self.dance_timer.setInterval(int(p.INTERVALO_DISPARO / 3))
        self.dance_timer.timeout.connect(self.dance)

    def shoot(self) -> None:
        if self.signal_shoot: self.signal_shoot.emit(self.where, self.typ)

    def dance(self) -> None:
        self.signal_dance.emit(self.where, self.dance_move)
        self.dance_move += 1

    def start_timers(self) -> None:
        if self.static: return
        self.shoot_timer.start()
        self.dance_timer.start()

    def pause_timers(self) -> None:
        if self.dance_timer.isActiving(): self.dance_timer.pause()
        if self.shoot_timer.isActiving(): self.shoot_timer.pause()

    def unpause_timers(self) -> None:
        if self.dance_timer.isPaused(): self.dance_timer.unpause()
        if self.shoot_timer.isPaused(): self.shoot_timer.unpause()

    def stop_timers(self) -> None:
        self.shoot_timer.stop()
        self.dance_timer.stop()


class PeaShooterLogic(ShooterLogic):

    cost = p.COSTO_LANZAGUISANTE

    def __init__(self, sgn_shoot: pyqtSignal, static: bool, sgn_dance: pyqtSignal,
    sgn_death: pyqtSignal, where: str) -> None:
        super().__init__(
            sgn_shoot=sgn_shoot,
            static=static,
            cost=p.COSTO_LANZAGUISANTE,
            sgn_dance=sgn_dance,
            sgn_death=sgn_death,
            where=where,
            typ=False)


class IcePeaShooterLogic(ShooterLogic):

    cost = p.COSTO_LANZAGUISANTE_HIELO
    
    def __init__(self, sgn_shoot: pyqtSignal, static: bool, sgn_dance: pyqtSignal,
    sgn_death: pyqtSignal, where: str) -> None:
        super().__init__(
            sgn_shoot=sgn_shoot,
            static=static,
            cost=p.COSTO_LANZAGUISANTE_HIELO,
            sgn_dance=sgn_dance,
            sgn_death=sgn_death,
            where=where,
            typ=True)


class NutLogic(PlantLogic):

    cost = p.COSTO_PAPA
    
    def __init__(self, static: bool, sgn_dance: pyqtSignal,
    sgn_death: pyqtSignal, where: str) -> None:
        super().__init__(
            health_points=(p.VIDA_PLANTA * 2),
            static=static,
            cost=p.COSTO_PAPA,
            sgn_dance=sgn_dance,
            sgn_death=sgn_death,
            where=where)

    def get_hp(self): return self._hp
    def set_hp(self, value):
        if value > ((4 * p.VIDA_PLANTA) / 3): self._hp = value
        elif value > ((2 * p.VIDA_PLANTA) / 3):
            self.dance_move = 1
            self.signal_dance.emit(self.where, self.dance_move)
            self._hp = value
        elif value > 0:
            self._hp = value
            self.dance_move = 2
            self.signal_dance.emit(self.where, self.dance_move)
        else:
            self.signal_death.emit(self.where)
    HP = property(get_hp, set_hp)

    def get_move(self): return self._dance_move
    def set_move(self, val):
        if val > 2: self._dance_move = 0
        else: self._dance_move = val
    dance_move = property(get_move, set_move)