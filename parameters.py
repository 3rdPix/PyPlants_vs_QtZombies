from os.path import join as pt

"""
PATHS
"""

# sonidos
pt_s_cruz_1 = pt('sonidos', 'crazyCruz_1.wav')
pt_s_cruz_2 = pt('sonidos', 'crazyCruz_2.wav')
pt_s_cruz_3 = pt('sonidos', 'crazyCruz_3.wav')
pt_s_cruz_4 = pt('sonidos', 'crazyCruz_4.wav')
pt_s_cruz_5 = pt('sonidos', 'crazyCruz_5.wav')
pt_s_cruz_6 = pt('sonidos', 'crazyCruz_6.wav')
pt_s_music_1 = pt('sonidos', 'musica.wav')
pt_s_music_2 = pt('sonidos', 'musica2.wav')

# imagenes
pt_shovel = pt('sprites', 'Bonus', 'pala.png')
pt_cruz = pt('sprites', 'CrazyRuz', 'crazyCruz.png')
pt_pea_1 = pt('sprites', 'Elementos de juego', 'guisante_1.png')
pt_pea_2 = pt('sprites', 'Elementos de juego', 'guisante_2.png')
pt_pea_3 = pt('sprites', 'Elementos de juego', 'guisante_3.png')
pt_ice_pea_1 = pt('sprites', 'Elementos de juego', 'guisanteHielo_1.png')
pt_ice_pea_2 = pt('sprites', 'Elementos de juego', 'guisanteHielo_2.png')
pt_ice_pea_3 = pt('sprites', 'Elementos de juego', 'guisanteHielo_3.png')
pt_logo = pt('sprites', 'Elementos de juego', 'logo.png')
pt_sun = pt('sprites', 'Elementos de juego', 'sol.png')
pt_text = pt('sprites', 'Elementos de juego', 'textoFinal.png')
pt_back_menu = pt('sprites', 'Fondos', 'fondoMenu.png')
pt_back_day = pt('sprites', 'Fondos', 'jardinAbuela.png')
pt_back_night = pt('sprites', 'Fondos', 'salidaNocturna.png')
pt_sunflower_1 = pt('sprites', 'Plantas', 'girasol_1.png')
pt_sunflower_2 = pt('sprites', 'Plantas', 'girasol_2.png')
pt_shooter_1 = pt('sprites', 'Plantas', 'lanzaguisantes_1.png')
pt_shooter_2 = pt('sprites', 'Plantas', 'lanzaguisantes_2.png')
pt_shooter_3 = pt('sprites', 'Plantas', 'lanzaguisantes_3.png')
pt_ice_shooter_1 = pt('sprites', 'Plantas', 'lanzaguisantesHielo_1.png')
pt_ice_shooter_2 = pt('sprites', 'Plantas', 'lanzaguisantesHielo_2.png')
pt_ice_shooter_3 = pt('sprites', 'Plantas', 'lanzaguisantesHielo_3.png')
pt_nut_1 = pt('sprites', 'Plantas', 'papa_1.png')
pt_nut_2 = pt('sprites', 'Plantas', 'papa_2.png')
pt_nut_3 = pt('sprites', 'Plantas', 'papa_3.png')
pt_walk_hernan_1 = pt('sprites', 'Zombies', 'Caminando', 'zombieHernanRunner_1.png')
pt_walk_hernan_2 = pt('sprites', 'Zombies', 'Caminando', 'zombieHernanRunner_2.png')
pt_walk_nico_1 = pt('sprites', 'Zombies', 'Caminando', 'zombieNicoWalker_1.png')
pt_walk_nico_2 = pt('sprites', 'Zombies', 'Caminando', 'zombieNicoWalker_2.png')
pt_eat_hernan_1 = pt('sprites', 'Zombies', 'Comiendo', 'zombieHernanComiendo_1.png')
pt_eat_hernan_2 = pt('sprites', 'Zombies', 'Comiendo', 'zombieHernanComiendo_2.png')
pt_eat_hernan_3 = pt('sprites', 'Zombies', 'Comiendo', 'zombieHernanComiendo_3.png')
pt_eat_nico_1 = pt('sprites', 'Zombies', 'Comiendo', 'zombieNicoComiendo_1.png')
pt_eat_nico_2 = pt('sprites', 'Zombies', 'Comiendo', 'zombieNicoComiendo_2.png')
pt_eat_nico_3 = pt('sprites', 'Zombies', 'Comiendo', 'zombieNicoComiendo_3.png')
"""
STYLES
"""
button_style: str = "QPushButton {\
    background-color: #E7A818;\
    color: yellow;\
    font-weight: bold;\
    font-family: 'Comic Sans MS';\
    font-size: 14pt;\
    border-style: outset;\
    border-width: 2px;\
    border-radius: 6px;\
    border-color: #6C4D05;\
    padding: 10px;\
    }\n\
    QPushButton:hover {\
        background-color: #34F0E4;\
        }"
title_style: str = "QLabel {\
    color: yellow;\
    font-weight: bold;\
    font-family: 'Comic Sans MS';\
    font-size: 16pt;\
    }"
title_style_2: str = "QLabel {\
    color: yellow;\
    font-weight: bold;\
    font-family: 'Comic Sans MS';\
    font-size: 16pt;\
    }"
dialog_style: str = "QLabel {\
    background-color: white;\
    color: black;\
    font-size: 14pt;\
    font-family: 'Tempus Sans ITC';\
    border-style: outset;\
    border-width: 2px;\
    border-radius: 10px;\
    border-color: green;\
    padding: 4px\
    }"
label_style: str = "QLabel {\
    color: #FF5733;\
    font-family: 'Comic Sans MS';\
    font-size: 14pt;\
    }"
label_style_2: str = "QLabel {\
    color: #FFFFFF;\
    font-family: 'Comic Sans MS';\
    font-size: 14pt;\
    }"
store_plant: str = "QLabel:hover {\
    background-color: #005605;\
    }"
"""
Dialogs
"""
ruz_diag_1: str = "Choose a level by clicking on it!"
ruz_diag_2: str = "You must choose a level before\nstarting the game!"
ruz_diag_3: str = "It's always nice to do some\ngardening in the morning"
ruz_diag_4: str = "Oh! Spooky night"
ruz_diag_5: str = """\
Time to deal with zombies!
Start the round whenever
you feel ready"""
ruz_diag_6: str = """\
Oh!? You do know some
tricks... Don't ya?"""
ruz_diag_7: str = """\
Where should we plant
this?..."""
ruz_diag_8: str = """\
Looks like you don't
have enough suns to
plant this yet..."""
ruz_diag_9: str = """\
Only one plant is
allowed per cell!"""
ruz_diag_10: str = """\
Great spot!"""
ruz_diag_11: str = """\
Maybe try planting the
plant in the grass next
time."""
ruz_diag_12: str = """\
Sometimes we must clean
our garden... forgive
us, little plants"""
ruz_diag_13: str = """\
There goes a friend..."""
ruz_diag_14: str = """\
There is nothing there!"""
ruz_diag_15: str = """\
No plant was damaged
during the creation of
this game"""
ruz_diag_16: str = """\
You are not wealthy
enough for this."""
ruz_diag_17: str = """\
You have saved us!
Thank you!"""
"""
Game numbers
"""
cell_coord: dict = {
    'A1': (253, 211), 'A2': (327, 211), 'A3': (401, 211), 'A4': (475, 211),
    'A5': (549, 211), 'A6': (623, 211), 'A7': (697, 211), 'A8': (771, 211),
    'A9': (845, 211), 'A10': (919, 211), 'B1': (253, 311), 'B2': (327, 311),
    'B3': (401, 311), 'B4': (475, 311), 'B5': (549, 311), 'B6': (623, 311),
    'B7': (697, 311), 'B8': (771, 311), 'B9': (845, 311), 'B10': (919, 311)
}
food_ranges_row1: dict = {
    'A1': (270, 310), 'A2': (344, 384), 'A3': (418, 458), 'A4': (492, 532),
    'A5': (566, 606), 'A6': (640, 680), 'A7': (714, 754), 'A8': (788, 828),
    'A9': (862, 902), 'A10': (936, 976)
    }
food_ranges_row2: dict = {
    'B1': (270, 310), 'B2': (344, 384), 'B3': (418, 458), 'B4': (492, 532),
    'B5': (566, 606), 'B6': (640, 680), 'B7': (714, 754), 'B8': (788, 828),
    'B9': (862, 902), 'B10': (936, 976)
    }