from PyQt5.QtCore import QObject, pyqtSignal
from bk.elements_1_bk import PeaShooterLogic, SunFlowerLogic
import parametros as p


class WelcomeLogic(QObject):

    signal_check_results = pyqtSignal(bool, set)
    signal_start_game = pyqtSignal(str)

    signal_dance_plant = pyqtSignal(str, int)

    def __init__(self) -> None:
        super().__init__()

        # Container
        self.plants: dict[str, object] = dict()

        # Decoration handler
        self.plants['1'] = SunFlowerLogic(sgn_produce=None, static=False,
        sgn_dance=self.signal_dance_plant, sgn_death=None, where='1')

        self.plants['2'] = PeaShooterLogic(sgn_shoot=None, static=False,
        sgn_dance=self.signal_dance_plant, sgn_death=None, where='2')

    def launch(self) -> None:
        for plant in self.plants.values(): plant.start_timers()

    def check_user(self, user: str) -> None:
        errors: set = set()
        if user == '': errors.add('void')
        if not user.isalnum(): errors.add('alnum')
        if len(user) < p.MIN_CARACTERES or len(user) > p.MAX_CARACTERES:
            errors.add('len')
        if errors: self.signal_check_results.emit(False, errors)
        else:
            for plant in self.plants.values(): plant.stop_timers()
            self.signal_check_results.emit(True, errors)
            self.signal_start_game.emit(user)
