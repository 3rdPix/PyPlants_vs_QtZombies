from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, QPoint, Qt, QMimeData, QSize, QMutex
from PyQt5.QtGui import QPixmap, QMouseEvent, QDrag, QPainter, QImage,\
    QDragEnterEvent, QDropEvent
from bk.custom_elements import PausableTimer
import parametros as p
import parameters as pt
from random import randint as rint, choice


# class Plant(QLabel):

#     signal_chosen_to_buy = pyqtSignal(QLabel)

#     def __init__(self, paths: tuple, signal_dance: pyqtSignal=pyqtSignal(),
#     static: bool=False, signal_me_clicked: pyqtSignal=None,
#     signal_cancel_purchase: pyqtSignal=None,
#     signal_me_death: pyqtSignal=None, **kwargs) -> None:
#         super().__init__(**kwargs)
        #self.secuence: list|tuple = list()
        #self.create_states(paths)
        #self._hp: int = int()
        #self.static: bool = static
        #self.dance_move: int = 0
        # self.setScaledContents(True)
        # self.setFixedSize(71, 98)
        #self.cost: int = int()
        #self.draggable: bool = False
        #self.signal_dance: pyqtSignal = signal_dance
        #self.signal_me_clicked: pyqtSignal = signal_me_clicked
        #self.signal_cancel_purchase: pyqtSignal = signal_cancel_purchase
        #self.signal_me_death: pyqtSignal = signal_me_death
        #self._awaiting_death: bool = False
    
    # def create_states(self, paths: tuple):
    #     for im in paths:
    #         local: QPixmap = QPixmap(im)
    #         self.secuence.append(local)

"""
    PROPERTIES
"""

    # def get_hp(self): return self._hp
    # def set_hp(self, value):
    #     if value <= 0:
    #         self._hp = 0
    #         self.signal_me_death.emit(self)
    #     else: self._hp = value
    # HP = property(get_hp, set_hp)

    # def mousePressEvent(self, ev: QMouseEvent) -> None:
    #     if ev.button() != Qt.LeftButton: return
    #     if self.signal_me_clicked != None:
    #         self.signal_me_clicked.emit(self)
    #         return
    #     self.signal_chosen_to_buy.emit(self)
    #     self.drag_start_position = ev.pos()
    #     return super().mousePressEvent(ev)

    # def mouseMoveEvent(self, ev: QMouseEvent) -> None:
    #     if not self.draggable: return
    #     if not(ev.buttons() & Qt.LeftButton): return
    #     else:
    #         # create a general dragger
    #         dragger: QDrag = QDrag(self)
            
    #         # mimic-ing the pixmap data each time helps cleaning previous drags
    #         mime_data: QMimeData = QMimeData()
    #         image_data: QPixmap = self.secuence[0].copy()
    #         image_data.scaled(self.size())
    #         image_data.toImage()
    #         mime_data.setImageData(image_data)
    #         dragger.setMimeData(mime_data)

    #         # to actually display what is being dragged
    #         pixmap: QPixmap = QPixmap(self.size())
    #         displayed: QPixmap = self.secuence[0].copy()
    #         displayed.scaled(self.size())
    #         painter: QPainter = QPainter(pixmap)
    #         painter.drawPixmap(self.rect(), displayed)
    #         painter.end()

    #         dragger.setPixmap(pixmap)
    #         dragger.setHotSpot(ev.pos())
    #         dragger.exec_(Qt.MoveAction)
    #         self.signal_cancel_purchase.emit()
    #     return super().mouseMoveEvent(ev)

    # def dragEnterEvent(self, ev: QDragEnterEvent) -> None:
    #     if self._awaiting_death:
    #         ev.acceptProposedAction()
    #     return super().dragEnterEvent(ev)
    
    # def dropEvent(self, ev: QDropEvent) -> None:
    #     self.signal_me_death.emit(self)
    #     return super().dropEvent(ev)


# class Sunflower(Plant):

    # def __init__(self, static: bool=False,
    # signal_me_sun_production: pyqtSignal=None, **kwargs) -> None:
    #     super().__init__(paths=(pt.pt_sunflower_1, pt.pt_sunflower_2),
    #                         static=static, **kwargs)
        # self.HP = p.VIDA_PLANTA
        # self.cost = p.COSTO_GIRASOL
        # self.signal_sun_production: pyqtSignal = signal_me_sun_production
        # self.create_dance_timer()
        # self.create_production_timer()

    # def create_dance_timer(self) -> None:
    #     self.dance_timer: PausableTimer = PausableTimer()
    #     self.dance_timer.setInterval(rint(450, 550))
    #     self.dance_timer.timeout.connect(self.dance)

    # def create_production_timer(self) -> None:
    #     self.production_timer: PausableTimer = PausableTimer()
    #     self.production_timer.setInterval(p.INTERVALO_SOLES_GIRASOL)
    #     self.production_timer.timeout.connect(self.produce)

    # def dance(self) -> None:
    #     match self.dance_move:
    #         case 0:
    #             self.signal_dance.emit(self, self.secuence[1])
    #             self.dance_move = 1

    #         case 1:
    #             self.signal_dance.emit(self, self.secuence[0])
    #             self.dance_move = 0

    # def produce(self):
    #     if self.signal_sun_production != None:
    #         self.signal_sun_production.emit(p.CANTIDAD_SOLES, self)

    # def start_timers(self):
    #     if self.static: return
    #     self.dance_timer.start()
    #     self.production_timer.start()

    # def pause_timers(self) -> None:
    #     if self.dance_timer.isActiving(): self.dance_timer.pause()
    #     if self.production_timer.isActiving(): self.production_timer.pause()

    # def unpause_timers(self) -> None:
    #     if self.dance_timer.isPaused(): self.dance_timer.unpause()
    #     if self.production_timer.isPaused(): self.production_timer.unpause()


# class Shooter(Plant):

#     # def __init__(self, paths: tuple, static: bool=False,
#     # signal_shoot: pyqtSignal=None, **kwargs) -> None:
#     #     super().__init__(paths=paths, static=static, **kwargs)
#     #     self.signal_shoot: pyqtSignal = signal_shoot
#     #     self.HP = p.VIDA_PLANTA
#         self.create_dance_timer()
#         self.create_shoot_timer()

    # def create_shoot_timer(self) -> None:
    #     self.shoot_timer: PausableTimer = PausableTimer()
    #     self.shoot_timer.setInterval(p.INTERVALO_DISPARO)
    #     self.shoot_timer.timeout.connect(self.shoot)

    # def create_dance_timer(self):
    #     self.dance_timer: PausableTimer = PausableTimer()
    #     self.dance_timer.setInterval(int(p.INTERVALO_DISPARO / 3))
    #     self.dance_timer.timeout.connect(self.dance)

    # def shoot(self) -> None:
    #     if self.signal_shoot:
    #         self.signal_shoot.emit(self)

    # def start_timers(self) -> None:
    #     if self.static: return
    #     self.dance_timer.start()
    #     self.shoot_timer.start()

    # def pause_timers(self) -> None:
    #     if self.dance_timer.isActiving(): self.dance_timer.pause()
    #     if self.shoot_timer.isActiving(): self.shoot_timer.pause()

    # def unpause_timers(self) -> None:
    #     if self.dance_timer.isPaused(): self.dance_timer.unpause()
    #     if self.shoot_timer.isPaused(): self.shoot_timer.unpause()

    # def dance(self):
    #     if self.static: return
    #     match self.dance_move:
    #         case 0:
    #             self.signal_dance.emit(self, self.secuence[1])
    #             self.dance_move = 1

    #         case 1:
    #             self.signal_dance.emit(self, self.secuence[2])
    #             self.dance_move = 2

    #         case 2:
    #             self.signal_dance.emit(self, self.secuence[0])
    #             self.dance_move = 0


# class PeaShooter(Shooter):

#     def __init__(self, static: bool=False, **kwargs) -> None:
#         super().__init__(
#             paths=(pt.pt_shooter_1, pt.pt_shooter_2, pt.pt_shooter_3),
#             static=static,
#             **kwargs)
#         self.cost = p.COSTO_LANZAGUISANTE


# class IcePeaShooter(Shooter):

#     def __init__(self, static: bool=False, **kwargs) -> None:
#         super().__init__(
#             paths=(pt.pt_ice_shooter_1,\
#                 pt.pt_ice_shooter_2,\
#                 pt.pt_ice_shooter_3),
#             static=static, **kwargs)
#         self.cost = p.COSTO_LANZAGUISANTE_HIELO


# class Nut(Plant):

#     def __init__(self, static: bool = False, **kwargs) -> None:
#         super().__init__(
#             paths=(pt.pt_nut_1, pt.pt_nut_2, pt.pt_nut_3),
#             static=static, **kwargs)
#         self.cost = p.COSTO_PAPA
#         self._hp: int = 2 * p.VIDA_PLANTA

#     def get_hp(self): return self._hp
#     def set_hp(self, val):
#         if val > ((4 * p.VIDA_PLANTA) / 3): self._hp = val
#         elif val > ((2 * p.VIDA_PLANTA) / 3):
#             self.signal_dance.emit(self, self.secuence[1])
#             self._hp = val
#         elif val > 0:
#             self.signal_dance.emit(self, self.secuence[2])
#         else:
#             self.signal_me_death.emit(self)
#     HP = property(get_hp, set_hp)

#     def start_timers(self): pass
#     def pause_timers(self): pass
#     def unpause_timers(self): pass


# class CrazyCruz(QLabel):

#     signal_show_dialog = pyqtSignal(str)

#     def __init__(self, parent, **kwargs) -> None:
#         super().__init__(parent, **kwargs)
#         self.crazy: QPixmap = QPixmap(pt.pt_cruz)
#         self.setScaledContents(True)
        
#     def where_to_speak(self, bubble: QLabel) -> QPoint:
#         in_x: int = int((self.width() - bubble.width()) / 2)
#         in_y: int = int((3  / 5) * self.height())
#         return QPoint(in_x, in_y)


# class Sun(QLabel):


#     # def __init__(self, 
#     # where: QPoint, # entering as pos
#     # mode: str='fall',
#     signal_travel: pyqtSignal=pyqtSignal(),
    # signal_grab: pyqtSignal=None, 
    # **kwargs) -> None:
        # super().__init__(**kwargs)
        # self.signal_travel: pyqtSignal = signal_travel
        # self.signal_grab: pyqtSignal = signal_grab
        # self.map: QPixmap = QPixmap(pt.pt_sun)
        # self.setFixedSize(50, 50)
        # self.setScaledContents(True)
    #     self._me_x: int = where.x()
    #     self._me_y: int = where.y()
    #     self.limits: tuple = self.set_limits(where, mode)
    #     self.create_timers()

    # def set_limits(self, where: QPoint, mode: str) -> tuple:
    #     match mode:

    #         case 'fall':
    #             limx = where.x()
    #             limy = choice(range(211, 350))
    #             return (limx, limy)

    #         case 'produce':
    #             limx = where.x() + 50 * ((-1) ** rint(1, 2))
    #             limy = where.y() + 70
    #             return (limx, limy)

    # def get_x(self): return self._me_x
    # def set_x(self, val): 
    #     if val <= self.limits[0]: self._me_x = val
    # me_x = property(get_x, set_x)

    # def get_y(self): return self._me_y
    # def set_y(self, val):
    #     if val <= self.limits[1]: self._me_y = val
    #     else: self._me_y = self.limits[1]
    # me_y = property(get_y, set_y)

    # def create_timers(self) -> None:
    #     self.travel_timer: PausableTimer = PausableTimer()
    #     self.travel_timer.setInterval(10)
    #     self.travel_timer.timeout.connect(self.travel)

    # def start_timers(self) -> None:
    #     self.travel_timer.start()
    
    # def pause_timers(self) -> None:
    #     if self.travel_timer.isActiving(): self.travel_timer.pause()

    # def unpause_timers(self) -> None:
    #     if self.travel_timer.isPaused(): self.travel_timer.unpause()

    # def travel(self):
    #     if self.me_y == self.limits[1]: self.travel_timer.stop()
    #     self.me_x += rint(1, 3)
    #     self.me_y += rint(2, 5)
    #     self.signal_travel.emit(self, QPoint(self.me_x, self.me_y))

    # def mousePressEvent(self, ev: QMouseEvent) -> None:
    #     if ev.button() == Qt.RightButton: self.signal_grab.emit(self)
    #     return super().mousePressEvent(ev)


# class Shovel(QLabel):

#     def __init__(self, signal_shovel_act: pyqtSignal=None) -> None:
#         super().__init__()
#         self.map: QPixmap = QPixmap(pt.pt_shovel)
#         self.setFixedSize(QSize(60, 60))
#         self.setScaledContents(True)
#         self.signal_shovel_act: pyqtSignal = signal_shovel_act

#     def mousePressEvent(self, ev: QMouseEvent) -> None:
#         if ev.button() != Qt.LeftButton: return
#         self.signal_shovel_act.emit()
#         self.drag_start_position = ev.pos()
#         return super().mousePressEvent(ev)

#     def mouseMoveEvent(self, ev: QMouseEvent) -> None:
#         if not(ev.buttons() & Qt.LeftButton): return
#         else:
#             # create a general dragger
#             dragger: QDrag = QDrag(self)
            
#             # mimic-ing the pixmap data each time helps cleaning previous drags
#             mime_data: QMimeData = QMimeData()
#             image_data: QPixmap = self.map.copy()
#             image_data.scaled(QSize(60, 60))
#             image_data.toImage()
#             mime_data.setImageData(image_data)
#             dragger.setMimeData(mime_data)

#             # to actually display what is being dragged
#             pixmap: QPixmap = QPixmap(self.size())
#             displayed: QPixmap = self.map.copy()
#             displayed.scaled(self.size())
#             painter: QPainter = QPainter(pixmap)
#             painter.drawPixmap(self.rect(), displayed)
#             painter.end()

#             dragger.setPixmap(pixmap)
#             dragger.setHotSpot(ev.pos())
#             dragger.exec_(Qt.MoveAction)
#         return super().mouseMoveEvent(ev)


# class Pea(QLabel):

#     def __init__(self, signal_dance: pyqtSignal=None,
#     signal_me_death: pyqtSignal=None, ice: bool=False,
#     signal_travel: pyqtSignal=None, where: QPoint=None,
#     emition_lock: QMutex=None, signal_me_travel: pyqtSignal=None,
#     **kwargs) -> None:
#         super().__init__(**kwargs)
#         self.signal_dance: pyqtSignal = signal_dance
#         self.signal_death: pyqtSignal = signal_me_death
#         self.signal_travel: pyqtSignal = signal_travel
#         self.signal_me_travel: pyqtSignal = signal_me_travel
#         self.emition_lock: QMutex = emition_lock
#         self.is_ice: bool = ice
#         self.damage: int = p.DANO_PROYECTIL
#         # self.secuence: tuple = self.create_secuence()
#         self.phase: int = 0
#         # self.setFixedSize(QSize(40, 35))
#         # self.setScaledContents(True)
#         self._x: int = where.x()
#         self.create_timers()

    # def get_x(self): return self._x
    # def set_x(self, val):
    #     if val < self.parent().width(): self._x = val
    #     else: self.signal_death.emit(self)
    # me_x = property(get_x, set_x)

    # def create_timers(self) -> None:
    #     self.travel_timer: PausableTimer = PausableTimer()
    #     self.travel_timer.setInterval(40)
    #     self.travel_timer.timeout.connect(self.travel)
        
    #     self.explode_timer: PausableTimer = PausableTimer()
    #     self.explode_timer.setInterval(50)
    #     self.explode_timer.timeout.connect(self.explode)

    # def travel(self) -> None:
    #     self.me_x += 9
    #     self.emition_lock.lock()
    #     self.signal_travel.emit(self, QPoint(self.me_x, self.y()))
    #     self.signal_me_travel.emit(self)
    #     self.emition_lock.unlock()

    # def create_secuence(self) -> tuple:
    #     if self.is_ice:
    #         map_1: QPixmap = QPixmap(pt.pt_ice_pea_1)
    #         map_2: QPixmap = QPixmap(pt.pt_ice_pea_2)
    #         map_3: QPixmap = QPixmap(pt.pt_ice_pea_3)
    #     else:
    #         map_1: QPixmap = QPixmap(pt.pt_pea_1)
    #         map_2: QPixmap = QPixmap(pt.pt_pea_2)
    #         map_3: QPixmap = QPixmap(pt.pt_pea_3)
    #     return (map_1, map_2, map_3)

    # def explode(self) -> None:
    #     match self.phase:
    #         case 0:
    #             self.signal_dance.emit(self, self.secuence[1])
    #             self.phase = 1
    #             return
    #         case 1:
    #             self.signal_dance.emit(self, self.secuence[2])
    #             self.phase = 2
    #             return
    #         case 2:
    #             self.signal_death.emit(self)
    #             return

    # def explode_animation(self) -> None:
    #     self.travel_timer.stop()
    #     self.explode_timer.start()

    # def start_timers(self) -> None:
    #     self.travel_timer.start()

    # def pause_timers(self) -> None:
    #     if self.travel_timer.isActiving(): self.travel_timer.pause()
    #     if self.explode_timer.isActiving(): self.explode_timer.pause()

    # def unpause_timers(self) -> None:
    #     if self.travel_timer.isPaused(): self.travel_timer.unpause()
    #     if self.explode_timer.isPaused(): self.explode_timer.unpause()


# class Zombie(QLabel):

#     def __init__(self, signal_dance: pyqtSignal=None,
#     signal_of_death: pyqtSignal=None, signal_travel: pyqtSignal=None,
#     signal_eat: pyqtSignal=None, fast: bool=False,
#     **kwargs) -> None:
        # super().__init__(**kwargs)
        # self.signal_dance: pyqtSignal = signal_dance
        # self.signal_me_death: pyqtSignal = signal_of_death
        # self.signal_travel: pyqtSignal = signal_travel
        # self.signal_eat: pyqtSignal = signal_eat
        # self._hp: int = p.VIDA_ZOMBIE
        # self._fast: bool = fast
        # self._slowed: bool = False
        # self.eating: bool = False
        # self._dance_move: int = 0
        # self._eat_dance_move: int = 0
    #     self.eating_at: str = str()
    #     # self.setFixedSize(80, 140)
    #     # self.setScaledContents(True)
    #     # self.secuence: tuple = self.create_secuence()
    #     # self.eat_secuence: tuple = self.create_eat_secuence()
    #     self.create_timers()

    # def get_hp(self): return self._hp
    # def set_hp(self, val):
    #     if val <= 0: self.signal_me_death.emit(self)
    #     self._hp = val
    # HP = property(get_hp, set_hp)

    # def create_secuence(self) -> tuple:
    #     if not self._fast:
    #         move_1: QPixmap = QPixmap(pt.pt_walk_nico_1)
    #         move_2: QPixmap = QPixmap(pt.pt_walk_nico_2)
    #         return (move_1, move_2)
    #     else:
    #         move_1: QPixmap = QPixmap(pt.pt_walk_hernan_1)
    #         move_2: QPixmap = QPixmap(pt.pt_walk_hernan_2)
    #         return (move_1, move_2)

    # def create_eat_secuence(self) -> tuple:
    #     if not self._fast:
    #         move_1: QPixmap = QPixmap(pt.pt_eat_nico_1)
    #         move_2: QPixmap = QPixmap(pt.pt_eat_nico_2)
    #         move_3: QPixmap = QPixmap(pt.pt_eat_nico_3)
    #         return (move_1, move_2, move_3)
    #     else:
    #         move_1: QPixmap = QPixmap(pt.pt_eat_hernan_1)
    #         move_2: QPixmap = QPixmap(pt.pt_eat_hernan_2)
    #         move_3: QPixmap = QPixmap(pt.pt_eat_hernan_3)
    #         return (move_1, move_2, move_3)

    # def create_timers(self):
    #     self.dance_timer: PausableTimer = PausableTimer()
    #     if self._fast: self.dance_timer.setInterval(rint(300, 400))
    #     else: self.dance_timer.setInterval(rint(700, 800))
    #     self.dance_timer.timeout.connect(self.dance)

    #     self.eat_dance_timer: PausableTimer = PausableTimer()
    #     self.eat_dance_timer.setInterval(500)
    #     self.eat_dance_timer.timeout.connect(self.eating_dance)

    #     self.travel_timer: PausableTimer = PausableTimer()
    #     self.travel_timer.setInterval(200)
    #     self.travel_timer.timeout.connect(self.walk)
        
    #     self.eat_timer: PausableTimer = PausableTimer()
    #     self.eat_timer.setInterval(p.INTERVALO_TIEMPO_MORDIDA)
    #     self.eat_timer.timeout.connect(self.eat)
    #     pass

    # def dance(self) -> None:
    #     match self._dance_move:
    #         case 0:
    #             self.signal_dance.emit(self, self.secuence[1])
    #             self._dance_move = 1
    #         case 1:
    #             self.signal_dance.emit(self, self.secuence[0])
    #             self._dance_move = 0

    # def eating_dance(self) -> None:
    #     match self._eat_dance_move:
    #         case 0:
    #             self.signal_dance.emit(self, self.eat_secuence[1])
    #             self._eat_dance_move = 1
    #         case 1:
    #             self.signal_dance.emit(self, self.eat_secuence[2])
    #             self._eat_dance_move = 2
    #         case 2:
    #             self.signal_dance.emit(self, self.eat_secuence[0])
    #             self._eat_dance_move = 0

    # def walk(self) -> None:
    #     if not self._slowed:
    #         step = p.VELOCIDAD_ZOMBIE
    #     else:
    #         step = p.VELOCIDAD_ZOMBIE * (1 - p.RALENTIZAR_ZOMBIE)
    #     if self._fast: step = step * 1.5
    #     point = QPoint(int(self.x() - step), self.y())
    #     self.signal_travel.emit(self, point)

    # def eat(self) -> None:
    #     self.signal_eat.emit(self.eating_at)

    # def start_eating(self, index_in_grid: str) -> None:
    #     self.pause_timers()
    #     self.eat_dance_timer.start()
    #     self.eating_at = index_in_grid
    #     self.eat_timer.start()

    # def finish_eating(self) -> None:
    #     pass



    # def slow_down(self) -> None:
    #     if not self._slowed:
    #         self.dance_timer.setInterval(self.dance_timer.interval() * 2)

    # def start_timers(self) -> None:
    #     self.dance_timer.start()
    #     self.travel_timer.start()

    # def pause_timers(self) -> None:
    #     if self.dance_timer.isActiving(): self.dance_timer.pause()
    #     if self.travel_timer.isActiving(): self.travel_timer.pause()
    #     if self.eat_timer.isActiving(): self.eat_timer.pause()
    #     if self.eat_dance_timer.isActiving(): self.eat_dance_timer.pause()

    # def unpause_timers(self) -> None:
    #     if self.dance_timer.isPaused(): self.dance_timer.unpause()
    #     if self.travel_timer.isPaused(): self.travel_timer.unpause()
    #     if self.eat_timer.isPaused(): self.eat_timer.unpause()
    #     if self.eat_dance_timer.isPaused(): self.eat_dance_timer.unpause()