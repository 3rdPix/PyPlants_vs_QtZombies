from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QMouseEvent, QDropEvent, QDragEnterEvent


class SelectableLabel(QLabel):

    signal_clicked = pyqtSignal(QLabel)

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == Qt.LeftButton: self.signal_clicked.emit(self)
        return super().mousePressEvent(ev)

class PausableTimer(QTimer):

    def __init__(self) -> None:
        super().__init__()
        self._paused: bool = False
        self.to_return: QTimer = QTimer()
        self.to_return.setSingleShot(True)
        self.to_return.timeout.connect(self.resume)
        
    def pause(self) -> None:
        if self.to_return.isActive():
            self.where = self.to_return.remainingTime()
            self.to_return.stop()
        else: self.where: int = self.remainingTime()
        self.stop()
        if self.where != -1: self.to_return.setInterval(self.where)
        self._paused = True

    def unpause(self) -> None:
        self.to_return.start()
        self._paused = False

    def isPaused(self) -> bool: return self._paused

    def isActiving(self) -> bool:
        return (self.to_return.isActive() or self.isActive())

    def resume(self) -> None:
        self.timeout.emit()
        self.start()

class SensibleLabel(QLabel):

    def __init__(self, parent,
    signal_clicked: pyqtSignal=pyqtSignal(), **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self.signal_clicked: pyqtSignal = signal_clicked
        self.setAcceptDrops(True)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == Qt.LeftButton:
            self.signal_clicked.emit((self.x(), self.y()))
        return super().mousePressEvent(ev)

    def dragEnterEvent(self, ev: QDragEnterEvent) -> None:
        if ev.mimeData().hasImage() and self.acceptDrops():
            ev.acceptProposedAction()
        return super().dragEnterEvent(ev)

    def dropEvent(self, ev: QDropEvent) -> None:
        self.signal_clicked.emit((self.x(), self.y()))
        return super().dropEvent(ev)