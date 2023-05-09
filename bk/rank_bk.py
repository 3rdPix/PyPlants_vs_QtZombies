from PyQt5.QtCore import pyqtSignal, QObject


class RankingLogic(QObject):

    signal_with_players = pyqtSignal(tuple)

    def __init__(self) -> None:
        super().__init__()

    def give_players(self) -> None:
        with open('puntajes.txt', 'r', encoding='utf-8') as raw:
            everyone: list = raw.readlines()
        for index in range(len(everyone)):
            everyone[index] = everyone[index].strip().split(',')
            everyone[index][1] = int(everyone[index][1])
        everyone.sort(key=lambda x: x[1])
        everyone.reverse()
        players: tuple = tuple(everyone[:5])
        for index in range(len(players)):
            players[index][1] = str(players[index][1])
        self.signal_with_players.emit(players)