from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QGraphicsOpacityEffect
import parameters as pt

class MainLogic(QObject):

    signal_send_check_result = pyqtSignal(bool)
    signal_go_game = pyqtSignal(tuple, str)

    def __init__(self) -> None:
        super().__init__()

    def check_selection(self, day: float, night: float, user: str) -> None:
        to_check: list = [day, night]
        match to_check:

            case [1.0, 1.0]:
                self.signal_send_check_result.emit(False)

            case [1.0, 0.5]:
                self.signal_send_check_result.emit(True)
                self.signal_go_game.emit((pt.pt_back_day, 1), user)

            case [0.5, 1.0]:
                self.signal_send_check_result.emit(True)
                self.signal_go_game.emit((pt.pt_back_night, 2), user)