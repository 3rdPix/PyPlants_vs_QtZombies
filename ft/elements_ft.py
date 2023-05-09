from random import choice
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QMouseEvent, QDrag, QPainter, \
    QDragEnterEvent, QDropEvent
from PyQt5.QtCore import pyqtSignal, Qt, QMimeData, QPoint
from PyQt5.QtMultimedia import QSound
import parameters as pt

class PlantVisual(QLabel):

    def __init__(self, where: str, paths: tuple, sgn_clicked: pyqtSignal,
    sgn_shovelled: pyqtSignal, sgn_act_purchase: pyqtSignal=None,
    draggable: bool=False, sgn_cancel_purchase: pyqtSignal=None,
    opt: int=0, **kwargs) -> None:
        super().__init__(**kwargs)
        self.secuence: tuple = self.create_states(paths)
        self.draggable: bool = draggable
        self.index: str = where
        self.opt: int = opt
        self.set_general_attributes()

        # Set signals
        self.signal_clicked: pyqtSignal = sgn_clicked
        self.signal_act_purchase: pyqtSignal = sgn_act_purchase
        self.signal_cancel_purchase: pyqtSignal = sgn_cancel_purchase
        self.signal_shovelled: pyqtSignal = sgn_shovelled

    def create_states(self, paths: tuple) -> tuple:
        moves: list = list()
        for image in paths:
            local: QPixmap = QPixmap(image)
            moves.append(local)
        return tuple(moves)

    def set_general_attributes(self) -> None:
        self.setScaledContents(True)
        self.setFixedSize(71, 98)
        self.awaiting_death: bool = False

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.LeftButton: return
        if self.signal_clicked:
            self.signal_clicked.emit(self.index)
            return
        if self.signal_act_purchase: self.signal_act_purchase.emit(self.opt)
        self.drag_start_position = event.pos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self.draggable: return
        if not(event.buttons() & Qt.LeftButton): return
        else:
            # Create a general dragger
            dragger: QDrag = QDrag(self)
            
            # Mimic-ing the pixmap data each time helps cleaning previous drags
            mime_data: QMimeData = QMimeData()
            image_data: QPixmap = self.secuence[0].copy()
            image_data.scaled(self.size())
            image_data.toImage()
            mime_data.setImageData(image_data)
            dragger.setMimeData(mime_data)

            # To actually display what is being dragged
            pixmap: QPixmap = QPixmap(self.size())
            displayed: QPixmap = self.secuence[0].copy()
            displayed.scaled(self.size())
            painter: QPainter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), displayed)
            painter.end()

            dragger.setPixmap(pixmap)
            dragger.setHotSpot(event.pos())
            dragger.exec_(Qt.MoveAction)
            self.signal_cancel_purchase.emit()
        return super().mouseMoveEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if self.awaiting_death: event.acceptProposedAction()
        return super().dragEnterEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        self.signal_shovelled.emit(self.index)
        return super().dropEvent(event)


class SunFlowerVisual(PlantVisual):

    def __init__(self, sgn_clicked: pyqtSignal, sgn_cancel_pruchase: pyqtSignal,
    sgn_shovelled: pyqtSignal, draggable: bool = False, **kwargs) -> None:
        super().__init__(
            paths=(pt.pt_sunflower_1, pt.pt_sunflower_2),
            sgn_clicked=sgn_clicked,
            sgn_cancel_purchase=sgn_cancel_pruchase,
            sgn_shovelled=sgn_shovelled,
            draggable=draggable, **kwargs)


class PeaShooterVisual(PlantVisual):

    def __init__(self, sgn_clicked: pyqtSignal,
    sgn_cancel_pruchase: pyqtSignal, sgn_shovelled: pyqtSignal,
    draggable: bool = False, **kwargs) -> None:
        super().__init__(
            paths=(pt.pt_shooter_1, pt.pt_shooter_2, pt.pt_shooter_3),
            sgn_clicked=sgn_clicked,
            sgn_cancel_purchase=sgn_cancel_pruchase,
            sgn_shovelled=sgn_shovelled,
            draggable=draggable, **kwargs)


class IcePeaShooterVisual(PlantVisual):

    def __init__(self, sgn_clicked: pyqtSignal,
    sgn_cancel_pruchase: pyqtSignal, sgn_shovelled: pyqtSignal,
    draggable: bool = False, **kwargs) -> None:
        super().__init__(
            paths=(pt.pt_ice_shooter_1, pt.pt_ice_shooter_2, pt.pt_ice_shooter_3),
            sgn_clicked=sgn_clicked,
            sgn_cancel_purchase=sgn_cancel_pruchase,
            sgn_shovelled=sgn_shovelled,
            draggable=draggable, **kwargs)


class NutVisual(PlantVisual):

    def __init__(self, sgn_clicked: pyqtSignal, sgn_cancel_purchase: pyqtSignal,
    sgn_shovelled: pyqtSignal, draggable: bool = False, **kwargs) -> None:
        super().__init__(
            paths=(pt.pt_nut_1, pt.pt_nut_2, pt.pt_nut_3),
            sgn_clicked=sgn_clicked,
            sgn_cancel_purchase=sgn_cancel_purchase,
            sgn_shovelled=sgn_shovelled,
            draggable=draggable, **kwargs)


class CrazyCruz(QLabel):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_ruz()
        self.create_bubble()
        self.microphone: tuple = (
            QSound(pt.pt_s_cruz_1),
            QSound(pt.pt_s_cruz_2),
            QSound(pt.pt_s_cruz_3),
            QSound(pt.pt_s_cruz_4),
            QSound(pt.pt_s_cruz_5),
            QSound(pt.pt_s_cruz_6))

    def set_ruz(self) -> None:
        image: QPixmap = QPixmap(pt.pt_cruz)
        self.setPixmap(image)
        self.setScaledContents(True)

    def create_bubble(self) -> None:
        self.bubble: QLabel = QLabel(parent=self)
        self.bubble.setStyleSheet(pt.dialog_style)

    def speak(self, motto: str) -> None:
        self.bubble.setMaximumWidth(self.width())
        self.bubble.setText(motto)
        self.bubble.resize(self.bubble.sizeHint())
        self.bubble.move(self.where_to_speak(self.bubble))
        
    def where_to_speak(self, bubble: QLabel) -> QPoint:
        in_x: int = int((self.width() - bubble.width()) / 2)
        in_y: int = int((3  / 5) * self.height())
        return QPoint(in_x, in_y)

    def sing(self) -> None:
        choice(self.microphone).play()



class SunVisual(QLabel):

    def __init__(self, sgn_take: pyqtSignal, ref: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.ref: int = ref
        self.signal_take: pyqtSignal = sgn_take
        self.set_general_attributes()

    def set_general_attributes(self) -> None:
        image: QPixmap = QPixmap(pt.pt_sun)
        self.setPixmap(image)
        self.setScaledContents(True)
        self.setFixedSize(50, 50)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton: self.signal_take.emit(self.ref)
        return super().mousePressEvent(event)


class Shovel(QLabel):

    def __init__(self, sgn_act: pyqtSignal,
    sgn_cancel: pyqtSignal, **kwargs) -> None:
        super().__init__(**kwargs)
        self.set_general_attributes()

        # Set signals
        self.signal_act: pyqtSignal = sgn_act
        self.signal_cancel: pyqtSignal = sgn_cancel

    def set_general_attributes(self) -> None:
        self.map: QPixmap = QPixmap(pt.pt_shovel)
        self.setPixmap(self.map)
        self.setFixedSize(60, 60)
        self.setScaledContents(True)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() != Qt.LeftButton: return
        self.signal_act.emit()
        self.drag_start_position = event.pos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if not(ev.buttons() & Qt.LeftButton): return
        else:
            # Create a general dragger
            dragger: QDrag = QDrag(self)
            
            # Mimic-ing the pixmap data each time helps cleaning previous drags
            mime_data: QMimeData = QMimeData()
            image_data: QPixmap = self.map.copy()
            image_data.scaled(self.size())
            image_data.toImage()
            mime_data.setImageData(image_data)
            dragger.setMimeData(mime_data)

            # To actually display what is being dragged
            pixmap: QPixmap = QPixmap(self.size())
            displayed: QPixmap = self.map.copy()
            displayed.scaled(self.size())
            painter: QPainter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), displayed)
            painter.end()

            # Dragger execution
            dragger.setPixmap(pixmap)
            dragger.setHotSpot(ev.pos())
            dragger.exec_(Qt.MoveAction)
            self.signal_cancel.emit()
        return super().mouseMoveEvent(ev)


class PeaVisual(QLabel):

    def __init__(self, ice: bool, **kwargs) -> None:
        super().__init__(**kwargs)
        self.ice: bool = ice
        self.secuence: tuple = self.create_secuence(ice)
        self.set_general_attributes()

    def set_general_attributes(self) -> None:
        self.setFixedSize(40, 35)
        self.setScaledContents(True)
        self.setPixmap(self.secuence[0])

    def create_secuence(self, ice: bool) -> tuple:
        if ice:
            map_1: QPixmap = QPixmap(pt.pt_ice_pea_1)
            map_2: QPixmap = QPixmap(pt.pt_ice_pea_2)
            map_3: QPixmap = QPixmap(pt.pt_ice_pea_3)
        else:
            map_1: QPixmap = QPixmap(pt.pt_pea_1)
            map_2: QPixmap = QPixmap(pt.pt_pea_2)
            map_3: QPixmap = QPixmap(pt.pt_pea_3)
        return (map_1, map_2, map_3)


class ZombieVisual(QLabel):

    def __init__(self, fast: bool, **kwargs) -> None:
        super().__init__(**kwargs)

        # Attributes
        self.set_general_attributes(fast)
        self.secuence: tuple = self.create_dance_secuence()
        self.eat_secuence: tuple = self.create_eat_secuence()
        self.setPixmap(self.secuence[0])

    def set_general_attributes(self, fast: bool) -> None:
        self._fast: bool = fast
        self.setFixedSize(80, 140)
        self.setScaledContents(True)
        

    def create_dance_secuence(self) -> tuple:
        if not self._fast:
            move_1: QPixmap = QPixmap(pt.pt_walk_nico_1)
            move_2: QPixmap = QPixmap(pt.pt_walk_nico_2)
            return (move_1, move_2)
        else:
            move_1: QPixmap = QPixmap(pt.pt_walk_hernan_1)
            move_2: QPixmap = QPixmap(pt.pt_walk_hernan_2)
            return (move_1, move_2)

    def create_eat_secuence(self) -> tuple:
        if not self._fast:
            move_1: QPixmap = QPixmap(pt.pt_eat_nico_1)
            move_2: QPixmap = QPixmap(pt.pt_eat_nico_2)
            move_3: QPixmap = QPixmap(pt.pt_eat_nico_3)
            return (move_1, move_2, move_3)
        else:
            move_1: QPixmap = QPixmap(pt.pt_eat_hernan_1)
            move_2: QPixmap = QPixmap(pt.pt_eat_hernan_2)
            move_3: QPixmap = QPixmap(pt.pt_eat_hernan_3)
            return (move_1, move_2, move_3)