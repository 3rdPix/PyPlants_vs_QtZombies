from game import CruzVsZombies
import sys

if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = CruzVsZombies(sys.argv)
    app.launch()
    sys.exit(app.exec())