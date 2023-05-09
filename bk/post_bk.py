from PyQt5.QtCore import pyqtSignal, QObject


class PostLogic(QObject):

    signal_with_info = pyqtSignal(dict)
    signal_hide_game = pyqtSignal()
    signal_new_round = pyqtSignal(int, str, int)
    signal_restart_game = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.create_game_attributes()

    def create_game_attributes(self) -> None:
        self.total_score = 0
        self.continues_playing = True
        self.user = str()
        self.round = 1

    def launch(self, info: dict) -> None:
        self.total_score += info['score']
        self.user = info['user']
        self.continues_playing = info['won']
        if info['won']: self.round += 1
        info['total'] = self.total_score
        self.lvl = info['lvl']
        self.signal_with_info.emit(info)
        self.signal_hide_game.emit()

    def next_round(self) -> None:
        self.signal_new_round.emit(self.round, self.user, self.lvl)

    def save_and_exit(self) -> None:
        with open('puntajes.txt', 'a', encoding='utf-8') as raw:
            raw.write(f'\n{self.user},{self.total_score}')
        self.signal_restart_game.emit()
        self.total_score = 0
        self.user = str()
        self.round = 1