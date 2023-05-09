from PyQt5.QtCore import QTimer
from aparicion_zombies import intervalo_aparicion
from bk.elements_1_bk import IcePeaShooterLogic, NutLogic, \
    PeaShooterLogic, SunFlowerLogic
from bk.elements_2_bk import PeaLogic, SunLogic, ZombieLogic
from bk.game_1_bk import GameLogicLoad
from custom_elements import PausableTimer
from random import choice, randint as rint
import parametros as p
import parameters as pt


class GameLogic(GameLogicLoad):

    """
    Module initialization
    """
    def __init__(self) -> None:
        super().__init__()

    def signal_connection(self) -> None:
        self.sgn_sunflower_produce.connect(
            self.sunflower_sun_production)

        self.sgn_peashooter_shoot.connect(
            self.pea_shoot)

        self.sgn_travel_pea.connect(
            self.check_pea_colision)

        self.sgn_pea_death.connect(
            self.kill_pea)

        self.sgn_plant_death.connect(
            self.kill_plant)

        self.sgn_travel_zombie.connect(
            self.detect_eating_time)

        self.sgn_zombie_eat.connect(
            self.zombie_bite)

        self.sgn_zombie_death.connect(
            self.kill_zombie)

        self.sgn_zombie_won.connect(
            self.lose)

    """
    Store
    """
    def buying(self, option: int) -> None:
        self._shovelling = False
        self._buying = True
        self._to_buy = option
        self.signal_ruz_speak.emit(pt.ruz_diag_7)

    def cancel_purchase(self) -> None:
        self._buying = False
        self._to_buy = 0

    def shovelling(self) -> None:
        self._buying = False
        self._to_buy = 0
        self._shovelling = True

    def cancel_shovelling(self) -> None:
        self._shovelling = False

    """
    User interaction
    """
    def cell_clicked(self, coord: tuple) -> None:
        # Tried to shovel an empty cell
        if self._shovelling:
            self.signal_ruz_speak.emit(pt.ruz_diag_14)
            self._shovelling = False
            return
        
        # If not buying, then do nothing
        if not self._buying: return
        
        # Check for enough suns
        costs = [SunFlowerLogic.cost, PeaShooterLogic.cost,
                IcePeaShooterLogic.cost, NutLogic.cost]
        if self.sun < costs[self._to_buy - 1]:
            self.signal_ruz_speak.emit(pt.ruz_diag_8)
            self._buying = False
            self._to_buy = None
            return
        
        # Identify if the cell is already used
        buy_index = self.cell_identifier(coord)
        if buy_index in self.plants_in_grid.keys():
            self.signal_ruz_speak.emit(pt.ruz_diag_9)
            self._buying = False
            self._to_buy = None
            return
        
        # If everything went well, plant it
        self.create_plant(buy_index)

    def user_wrote(self, letter: str) -> None:
        if letter == 'p':
            self.phrase = '000'
            self.pause_handler()
        if letter == 'm' and self._muted:
            self.signal_unmute.emit()
            self._muted = False
        elif letter == 'm' and not self._muted:
            self.signal_mute.emit()
            self._muted = True
        self.phrase += letter    

    def planted_clicked(self, index: str) -> None:
        if self._shovelling:
            self.kill_plant(index)
            self._shovelling = False
        
        if not self._buying: return
        self.signal_ruz_speak.emit(pt.ruz_diag_9)
        self._buying = False
        self._to_buy = None
    
    """
    General effects
    """
    def start_round(self) -> None:
        self.remaining = 2 * p.N_ZOMBIES
        for each in self.plants_in_grid.values(): each.start_timers()
        self._in_round = True
        self.random_suns()
        self.random_zombies()

    def random_suns(self) -> None:
        self.random_sun_generator: PausableTimer = PausableTimer()
        self.random_sun_generator.setInterval(p.INTERVALO_APARICION_SOLES)
        self.random_sun_generator.timeout.connect(self.create_random_sun)
        if self._lvl == 1: self.random_sun_generator.start()

    def random_zombies(self) -> None:
        self.spawning_timer: PausableTimer = PausableTimer()
        interval = intervalo_aparicion(self._round, self._pond)
        self.spawning_timer.setInterval(int(interval * 10000))
        self.spawning_timer.timeout.connect(self.spawn_zombie)
        self.spawning_timer.start()

    def pause_handler(self) -> None:
        if not self._paused and self._in_round:
            for each in self.plants_in_grid.values(): each.pause_timers()
            for each in self.suns.values(): each.pause_timers()
            for each in self.bullets_row1.values(): each.pause_timers()
            for each in self.bullets_row2.values(): each.pause_timers()
            for each in self.zombies_row1.values(): each.pause_timers()
            for each in self.zombies_row2.values(): each.pause_timers()
            if self._lvl == 1: self.random_sun_generator.pause()
            self.spawning_timer.pause()
            self._buying = False
            self._to_buy = None
            self._paused = True
            self.signal_pause.emit()
            return
        elif not self._paused and not self._in_round:
            self.signal_pause.emit()
            self._paused = True
        elif self._paused and not self._in_round:
            self.signal_unpause.emit()
            self._paused = False
        elif self._paused and self._in_round:
            for each in self.plants_in_grid.values(): each.unpause_timers()
            for each in self.suns.values(): each.unpause_timers()
            for each in self.bullets_row1.values(): each.unpause_timers()
            for each in self.bullets_row2.values(): each.unpause_timers()
            for each in self.zombies_row1.values(): each.unpause_timers()
            for each in self.zombies_row2.values(): each.unpause_timers()
            if self._lvl == 1: self.random_sun_generator.unpause()
            self.spawning_timer.unpause()
            self.signal_unpause.emit()
            self._paused = False

    def win(self) -> None:
        for each in self.plants_in_grid.values(): each.stop_timers()
        for each in self.suns.values(): each.stop_timers()
        for each in self.bullets_row1.values(): each.stop_timers()
        for each in self.bullets_row2.values(): each.stop_timers()
        for each in self.zombies_row1.values(): each.stop_timers()
        for each in self.zombies_row2.values(): each.stop_timers()
        if self._lvl == 1 and self._in_round: self.random_sun_generator.stop()
        self._won = True
        self.signal_win.emit()
        self.winning: QTimer = QTimer()
        self.winning.setInterval(4000)
        self.winning.setSingleShot(True)
        self.winning.timeout.connect(self.go_post_game)
        self.winning.start()

    def kill_cheat(self) -> None:
        for each in self.plants_in_grid.values(): each.stop_timers()
        for each in self.suns.values(): each.stop_timers()
        for each in self.bullets_row1.values(): each.stop_timers()
        for each in self.bullets_row2.values(): each.stop_timers()
        for each in self.zombies_row1.values(): each.stop_timers()
        for each in self.zombies_row2.values(): each.stop_timers()
        if self._lvl == 1 and self._in_round: self.random_sun_generator.stop()
        if self._in_round: self.spawning_timer.stop()
        self.remaining = 0
        self.kill = 2 * p.N_ZOMBIES
        match self._lvl:
            case 1:
                self.score = p.PUNTAJE_ZOMBIE_DIURNO * 2 * p.N_ZOMBIES
            case 2:
                self.score = p.PUNTAJE_ZOMBIE_NOCTURNO * 2 * p.N_ZOMBIES
        self.win()

    def skip_round(self):
        if self.sun < p.COSTO_AVANZAR:
            self.signal_ruz_speak.emit(pt.ruz_diag_16)
            return
        self.sun -= p.COSTO_AVANZAR
        for each in self.plants_in_grid.values(): each.stop_timers()
        for each in self.suns.values(): each.stop_timers()
        for each in self.bullets_row1.values(): each.stop_timers()
        for each in self.bullets_row2.values(): each.stop_timers()
        for each in self.zombies_row1.values(): each.stop_timers()
        for each in self.zombies_row2.values(): each.stop_timers()
        if self._lvl == 1 and self._in_round: self.random_sun_generator.stop()
        if self._in_round: self.spawning_timer.stop()
        self._won = True
        self.go_post_game()

    def lose(self) -> None:
        for each in self.plants_in_grid.values(): each.stop_timers()
        for each in self.suns.values(): each.stop_timers()
        for each in self.bullets_row1.values(): each.stop_timers()
        for each in self.bullets_row2.values(): each.stop_timers()
        for each in self.zombies_row1.values(): each.stop_timers()
        for each in self.zombies_row2.values(): each.stop_timers()
        if self._lvl == 1: self.random_sun_generator.stop()
        self.spawning_timer.stop()
        self.signal_lose.emit()
        self._won = False
        self.losing = QTimer()
        self.losing.setInterval(4000)
        self.losing.setSingleShot(True)
        self.losing.timeout.connect(self.go_post_game)
        self.losing.start()    

    def go_post_game(self) -> None:
        info: dict = dict()
        info['won'] = self._won
        info['round'] = self._round
        info['kill'] = self._kill
        info['suns'] = self.sun
        if self.remaining == 0:
            match self._lvl:
                case 1: info['score'] = \
                    int(self.score + self.score * p.PONDERADOR_DIURNO)
                case 2: info['score'] = \
                    int(self.score + self.score * p.PONDERADOR_NOCTURNO)
        else:
            info['score'] = self.score
        info['user'] = self._user
        info['lvl'] = self._lvl
        self.signal_go_post_game.emit(info)

    def reset_all(self) -> None:
        plant = list(self.plants_in_grid.keys())
        for each in plant: self.kill_plant(each)
        bullet1 = list(self.bullets_row1.keys())
        for each in bullet1: self.kill_pea(1, each)
        bullet2 = list(self.bullets_row2.keys())
        for each in bullet2: self.kill_pea(2, each)
        zomb1 = list(self.zombies_row1.keys())
        for each in zomb1: self.kill_zombie(1, each)
        zomb2 = list(self.zombies_row2.keys())
        for each in zomb2: self.kill_zombie(2, each)
        suns = list(self.suns.keys())
        for each in suns: self.kill_sun(each)
        self.round = 1
        self.sun = p.SOLES_INICIALES
        self.score = 0
        self.remaining = 0
        self.kill = 0

    def new_round(self, round: int, user: str, lvl: int) -> None:
        self.reset_all()
        self.create_round_properties(round)
        self.create_status_variables()
        self.signal_new_round.emit(user, lvl)
        self.round = round

    """
    Generation and degeneration
    """
    def create_plant(self, index: str) -> None:
        match self._to_buy:
            case 1:
                self.plants_in_grid[index] = SunFlowerLogic(
                    static=False,
                    sgn_produce=self.sgn_sunflower_produce,
                    sgn_dance=self.sgn_plant_dance,
                    sgn_death=self.sgn_plant_death,
                    where=index)
                self.signal_create_plant.emit(index, 1)
            case 2:
                self.plants_in_grid[index] = PeaShooterLogic(
                    static=False,
                    sgn_shoot=self.sgn_peashooter_shoot,
                    sgn_dance=self.sgn_plant_dance,
                    sgn_death=self.sgn_plant_death,
                    where=index)
                self.signal_create_plant.emit(index, 2)
            case 3:
                self.plants_in_grid[index] = IcePeaShooterLogic(
                    static=False,
                    sgn_shoot=self.sgn_peashooter_shoot,
                    sgn_dance=self.sgn_plant_dance,
                    sgn_death=self.sgn_plant_death,
                    where=index)
                self.signal_create_plant.emit(index, 3)
            case 4:
                self.plants_in_grid[index] = NutLogic(
                    static=False,
                    sgn_dance=self.sgn_plant_dance,
                    sgn_death=self.sgn_plant_death,
                    where=index)
                self.signal_create_plant.emit(index, 4)
        if self._in_round: self.plants_in_grid[index].start_timers()
        self.sun -= self.plants_in_grid[index].cost
        self._buying = False
        self._to_buy = None
        self._shovelling = False
        self.signal_ruz_speak.emit(pt.ruz_diag_10)

    def kill_plant(self, index: str) -> None:
        plant = self.plants_in_grid[index]
        plant.stop_timers()
        plant.deleteLater()
        del self.plants_in_grid[index]
        self.signal_kill_plant.emit(index)
        match index[0]:
            case 'A':
                for zombie in self.zombies_row1.values():
                    if zombie._eating_at == index: zombie.stop_eating()
            case 'B':
                for zombie in self.zombies_row2.values(): 
                    if zombie._eating_at == index: zombie.stop_eating()

    def sunflower_sun_production(self, index: str, quantity: int) -> None:
        x, y = pt.cell_coord[index]
        for _ in range(quantity):
            ref = len(self.suns) + 1
            self.suns[ref] = SunLogic(sgn_travel=self.sgn_travel_sun,
            mode='produce', where=(x, y), ref=ref)
            self.signal_create_sun.emit(ref, x, y)
            self.suns[ref].start_timers()

    def create_random_sun(self) -> None:
        x = rint(253, 919)
        y = 0
        ref = len(self.suns) + 1
        self.suns[ref] = SunLogic(sgn_travel=self.sgn_travel_sun,
        mode='fall', where=(x, y), ref=ref)
        self.signal_create_sun.emit(ref, x, y)
        self.suns[ref].start_timers()

    def grab_sun(self, ref: int) -> None:
        sun = self.suns[ref]
        sun.stop_timers()
        sun.deleteLater()
        del self.suns[ref]
        self.signal_kill_sun.emit(ref)
        match self._lvl:
            case 1: self.sun += p.SOLES_POR_RECOLECCION * 2
            case 2: self.sun += p.SOLES_POR_RECOLECCION

    def kill_sun(self, ref: int) -> None:
        sun = self.suns[ref]
        sun.stop_timers()
        sun.deleteLater()
        del self.suns[ref]

    def kill_pea(self, row: int, ref: int) -> None:
        match row:
            case 1: bullet = self.bullets_row1[ref]
            case 2: bullet = self.bullets_row2[ref]
        bullet.stop_timers()
        bullet.deleteLater()
        match row:
            case 1: del self.bullets_row1[ref]
            case 2: del self.bullets_row2[ref]
        self.signal_kill_pea.emit(row, ref)

    def check_pea_colision(self, row: int, ref: int, where: tuple) -> None:
        if where[0] > 1395: return
        match row:
            case 1:
                if not self.most_left_zomb_row1:
                    return
                if where[0] >= self.most_left_zomb_row1.me_x:
                    if self.bullets_row1[ref].ice:
                        self.most_left_zomb_row1.slow_down()
                        self.most_left_zomb_row1._slowed = True
                    self.most_left_zomb_row1.HP -= p.DANO_PROYECTIL
                    self.bullets_row1[ref].explode()
            case 2:
                if not self.most_left_zomb_row2:
                    return
                if where[0] >= self.most_left_zomb_row2.me_x:
                    if self.bullets_row2[ref].ice:
                        self.most_left_zomb_row2.slow_down()
                        self.most_left_zomb_row2._slowed = True
                    self.most_left_zomb_row2.HP -= p.DANO_PROYECTIL
                    self.bullets_row2[ref].explode()

    def detect_eating_time(self, row: int, ref: int, where: tuple) -> None:
        self.zombie_in_front_detector(row, ref, where)
        match row:
            case 1:
                for index in pt.food_ranges_row1:
                    if not index in self.plants_in_grid.keys(): continue
                    l_lim = pt.food_ranges_row1[index][0]
                    r_lim = pt.food_ranges_row1[index][1]
                    if not (l_lim <= where[0] <= r_lim): continue
                    self.zombies_row1[ref].start_eating(index)
            case 2:
                for index in pt.food_ranges_row2:
                    if not index in self.plants_in_grid.keys(): continue
                    l_lim = pt.food_ranges_row2[index][0]
                    r_lim = pt.food_ranges_row2[index][1]
                    if not (l_lim <= where[0] <= r_lim): continue
                    self.zombies_row2[ref].start_eating(index)

    def zombie_in_front_detector(self, row: int, ref: int, where: tuple) -> None:
        match row:
            case 1:
                if not self.most_left_zomb_row1:
                    self.most_left_zomb_row1 = self.zombies_row1[ref]
                    return
                if where[0] < self.most_left_zomb_row1.me_x:
                    self.most_left_zomb_row1 = self.zombies_row1[ref]
                    return
            case 2:
                if not self.most_left_zomb_row2:
                    self.most_left_zomb_row2 = self.zombies_row2[ref]
                    return
                if where[0] < self.most_left_zomb_row2.me_x:
                    self.most_left_zomb_row2 = self.zombies_row2[ref]
                    return

    def force_front_detector(self, row: int) -> None:
        try:    
            match row:
                case 1:
                    closer = choice(list(self.zombies_row1.values()))
                    for creature in list(self.zombies_row1.values()):
                        if creature.me_x < closer.me_x: closer = creature
                    self.most_left_zomb_row1 = closer
                case 2:
                    closer = choice(list(self.zombies_row2.values()))
                    for creature in list(self.zombies_row2.values()):
                        if creature.me_x < closer.me_x: closer = creature
                    self.most_left_zomb_row2 = closer
        except IndexError: return

    def zombie_bite(self, where: str) -> None:
        if where in self.plants_in_grid.keys():
            self.plants_in_grid[where].HP -= p.DANO_MORDIDA
                
    def pea_shoot(self, where: str, typ: bool) -> None:
        ref = self._bullets_counter + 1
        self._bullets_counter += 1
        inform: dict = dict()
        x = pt.cell_coord[where][0] + 60
        inform['x'] = x
        y = pt.cell_coord[where][1] + 15
        inform['y'] = y
        inform['typ'] = typ
        match where[0]:
            case 'A':
                inform['row'] = 1
                inform['ref'] = ref
                self.bullets_row1[ref] = PeaLogic(sgn_dance=self.sgn_pea_dance,
                sgn_death=self.sgn_pea_death, ref=ref,
                sgn_travel=self.sgn_travel_pea, ice=typ, row=1, where=(x, y))
                self.sgn_peashooter_shoot_inform.emit(inform)
                self.bullets_row1[ref].start_timers()
            case 'B':
                inform['row'] = 2
                inform['ref'] = ref
                self.bullets_row2[ref] = PeaLogic(sgn_dance=self.sgn_pea_dance,
                sgn_death=self.sgn_pea_death, ref=ref,
                sgn_travel=self.sgn_travel_pea, ice=typ, row=2, where=(x, y))
                self.sgn_peashooter_shoot_inform.emit(inform)
                self.bullets_row2[ref].start_timers()
        
    def spawn_zombie(self) -> None:
        if self._row1_zombies_counter == p.N_ZOMBIES and\
            self._row2_zombies_counter < p.N_ZOMBIES:
            coord = (1350, 250)
        elif self._row2_zombies_counter == p.N_ZOMBIES and \
            self._row1_zombies_counter < p.N_ZOMBIES:
            coord = (1352, 150)
        elif self._row2_zombies_counter == p.N_ZOMBIES and \
            self._row1_zombies_counter == p.N_ZOMBIES:
            self.spawning_timer.stop()
            return
        else:
            coord = choice(((1350, 250), (1352, 150)))
        fast = choice((True, False))
        match coord[1]:
            case 150:
                row = 1
                ref = self._zombies_counter + 1
                self.zombies_row1[ref] = ZombieLogic(
                    sgn_dance=self.sgn_zombie_dance,
                    sgn_death=self.sgn_zombie_death,
                    sgn_travel=self.sgn_travel_zombie,
                    sgn_eat=self.sgn_zombie_eat,
                    fast=fast,
                    row=row, ref=ref, where=coord,
                    sgn_won=self.sgn_zombie_won)
                self.zombies_row1[ref].start_timers()
                self._row1_zombies_counter += 1
                self._zombies_counter += 1
            case 250:
                row = 2
                ref = self._zombies_counter + 1
                self.zombies_row2[ref] = ZombieLogic(
                    sgn_dance=self.sgn_zombie_dance,
                    sgn_death=self.sgn_zombie_death,
                    sgn_travel=self.sgn_travel_zombie,
                    sgn_eat=self.sgn_zombie_eat,
                    fast=fast,
                    row=row, ref=ref, where=coord,
                    sgn_won=self.sgn_zombie_won)
                self.zombies_row2[ref].start_timers()
                self._row2_zombies_counter += 1
                self._zombies_counter += 1
        self.signal_create_zombie.emit(coord, row, ref, fast)
        
    def kill_zombie(self, row: int, ref: int) -> None:
        match row:
            case 1: creature = self.zombies_row1[ref]
            case 2: creature = self.zombies_row2[ref]
        if creature == self.most_left_zomb_row1:
            self.most_left_zomb_row1 = None
        if creature == self.most_left_zomb_row2:
            self.most_left_zomb_row2 = None
        creature.stop_timers()
        creature.deleteLater()
        match row:
            case 1: del self.zombies_row1[ref]
            case 2: del self.zombies_row2[ref]
        self.signal_kill_zombie.emit(row, ref)
        match self._lvl:
            case 1: self.score += p.PUNTAJE_ZOMBIE_DIURNO
            case 2: self.score += p.PUNTAJE_ZOMBIE_NOCTURNO
        self.remaining -= 1
        self.kill += 1
        self.force_front_detector(row)

    """
    Other
    """
    def cell_identifier(self, cell: tuple) -> str:
        key_list: list = list(pt.cell_coord.keys())
        obj_list: list = list(pt.cell_coord.values())
        return key_list[obj_list.index(cell)]