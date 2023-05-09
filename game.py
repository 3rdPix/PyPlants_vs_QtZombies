from PyQt5.QtWidgets import QApplication
from bk.game_bk import GameLogic
from bk.post_bk import PostLogic
from ft.game_ft import GameWindow
from bk.main_bk import MainLogic
from bk.rank_bk import RankingLogic
from bk.welcome_bk import WelcomeLogic
from ft.main_ft import MainWindow
from ft.post_ft import PostWindow
from ft.rank_ft import RankingWindow
from ft.welcome_ft import WelcomeWindow

class CruzVsZombies(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        
        # instance front
        self.welcome: WelcomeWindow = WelcomeWindow()
        self.rank: RankingWindow = RankingWindow()
        self.main: MainWindow = MainWindow()
        self.game: GameWindow = GameWindow()
        self.post: PostWindow = PostWindow()

        # instance back
        self.welcome_bk: WelcomeLogic = WelcomeLogic()
        self.rank_bk: RankingLogic = RankingLogic()
        self.main_bk: MainLogic = MainLogic()
        self.game_bk: GameLogic = GameLogic()
        self.post_bk: PostLogic = PostLogic()

        # connections
        self.signal_connection()

    def launch(self): self.welcome.launch()

    def signal_connection(self) -> None:
        
        """
        Welcome: user verification and request rankings
        """
        self.welcome.signal_launched.connect(
            self.welcome_bk.launch)

        self.welcome_bk.signal_dance_plant.connect(
            self.welcome.dance)

        self.welcome.signal_request_check_user.connect(
            self.welcome_bk.check_user)

        self.welcome_bk.signal_check_results.connect(
            self.welcome.receive_check)

        self.welcome.signal_go_ranks.connect(
            self.rank.launch)

        self.welcome_bk.signal_start_game.connect(
            self.main.launch)

        """
        Ranks: Info and go back
        """
        self.rank.signal_go_welcome.connect(
            self.welcome.launch)
        
        self.rank.signal_request_players.connect(
            self.rank_bk.give_players)
        
        self.rank_bk.signal_with_players.connect(
            self.rank.assign_players)

        """
        Main: level selection
        """
        self.main.signal_request_check_selection.connect(
            self.main_bk.check_selection)

        self.main_bk.signal_send_check_result.connect(
            self.main.receive_check)

        self.main_bk.signal_go_game.connect(
            self.game.launch)

        """
        Game: playing
        """
        # Module
        self.game.signal_launched.connect(
            self.game_bk.launch)

        # Store
        self.game.signal_store_plant_clicked.connect(
            self.game_bk.buying)

        self.game.signal_cancel_purchase.connect(
            self.game_bk.cancel_purchase)

        self.game.signal_shovel_picked.connect(
            self.game_bk.shovelling)

        self.game.signal_shovel_canceled.connect(
            self.game_bk.cancel_shovelling)
        
        # Stats updaters
        self.game_bk.signal_update_sun.connect(
            self.game.update_sun)

        self.game_bk.signal_update_round.connect(
            self.game.update_round)

        self.game_bk.signal_update_score.connect(
            self.game.update_score)

        self.game_bk.signal_update_kill.connect(
            self.game.update_kill)

        self.game_bk.signal_update_remaining.connect(
            self.game.update_remaining)
        
        # General effects
        self.game_bk.signal_mute.connect(
            self.game.mute)

        self.game_bk.signal_unmute.connect(
            self.game.unmute)

        self.game_bk.signal_pause.connect(
            self.game.pause)

        self.game_bk.signal_unpause.connect(
            self.game.unpause)

        self.game_bk.signal_lose.connect(
            self.game.lose)

        self.game_bk.signal_win.connect(
            self.game.win)

        self.game_bk.signal_new_round.connect(
            self.game.new_round)

        self.game_bk.signal_go_post_game.connect(
            self.post_bk.launch)

        self.game_bk.signal_go_post_game.connect(
            self.game.disappear)

        self.game.signal_skip_round.connect(
            self.game_bk.skip_round)

        # User interaction
        self.game.signal_request_pause.connect(
            self.game_bk.pause_handler)

        self.game.signal_start_round.connect(
            self.game_bk.start_round)

        self.game.signal_key_pressed.connect(
            self.game_bk.user_wrote)

        self.game.sgn_cell_click.connect(
            self.game_bk.cell_clicked)

        self.game.sgn_plant_clicked.connect(
            self.game_bk.planted_clicked)

        self.game.sgn_plant_shovelled.connect(
            self.game_bk.planted_clicked)

        self.game.sgn_sun_grab.connect(
            self.game_bk.grab_sun)

        # Object generation and degeneration
        self.game_bk.signal_create_plant.connect(
            self.game.create_plant)

        self.game_bk.signal_kill_plant.connect(
            self.game.kill_plant)

        self.game_bk.signal_create_sun.connect(
            self.game.create_sun)

        self.game_bk.signal_kill_sun.connect(
            self.game.kill_sun)

        self.game_bk.sgn_peashooter_shoot_inform.connect(
            self.game.pea_shoot)

        self.game_bk.signal_kill_pea.connect(
            self.game.kill_pea)

        self.game_bk.signal_create_zombie.connect(
            self.game.create_zombie)

        self.game_bk.sgn_zombie_death.connect(
            self.game.kill_zombie)

        # Entities
        self.game_bk.sgn_plant_dance.connect(
            self.game.dance_plant)

        self.game_bk.sgn_pea_dance.connect(
            self.game.dance_pea)

        self.game_bk.sgn_zombie_dance.connect(
            self.game.dance_zombie)

        self.game_bk.sgn_travel_sun.connect(
            self.game.travel_sun)

        self.game_bk.sgn_travel_pea.connect(
            self.game.travel_pea)

        self.game_bk.sgn_travel_zombie.connect(
            self.game.travel_zombie)
        

        # Other
        self.game_bk.signal_ruz_speak.connect(
            self.game.ruz_speak)

        """
        Post: round stats, and exit game
        """
        self.post_bk.signal_with_info.connect(
            self.post.launch)

        self.post_bk.signal_hide_game.connect(
            self.game.hide)

        self.post.signal_next_round.connect(
            self.post_bk.next_round)

        self.post_bk.signal_new_round.connect(
            self.game_bk.new_round)

        self.post.signal_exit.connect(
            self.post_bk.save_and_exit)

        self.post_bk.signal_restart_game.connect(
            self.welcome.launch)
        
        self.post_bk.signal_restart_game.connect(
            self.main.reset_all)

        self.post_bk.signal_restart_game.connect(
            self.game.reset_all)

        self.post_bk.signal_restart_game.connect(
            self.game_bk.reset_all)
