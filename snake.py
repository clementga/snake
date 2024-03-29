from upemtk import *
from time import sleep
from random import randint

# dimensions du jeu
TAILLE_CASE = 15
LARGEUR_PLATEAU = 40  # en nombre de cases
HAUTEUR_PLATEAU = 30  # en nombre de cases
DELAI_POMMES = 4   # délai entre l'apparition des pommes, en secondes
MAX_POMMES = 3   # nombre maximum de pomme présentes à l'écran en même temps

CYCLE_COULEUR = ['green', 'darkgreen', 'lightgreen', 'blue', 'cyan',
                 'lightblue', 'red', 'pink', 'yellow', 'orange',
                 'magenta', 'purple', 'black', 'white']
RAINBOW_COULEUR = ['red', 'orange', 'yellow', 'green', 'cyan',
                   'blue', 'purple']

def case_vers_pixel(case):
    """
    Reçoit les coordonnées d'une case du plateau sous la 
    forme d'un couple d'entiers (ligne, colonne) et renvoie les 
    coordonnées du pixel se trouvant au centre de cette case. Ce calcul 
    prend en compte la taille de chaque case, donnée par la variable 
    globale TAILLE_CASE.
    """
    i, j = case
    return (i + .5) * TAILLE_CASE, (j + .5) * TAILLE_CASE

def affiche_pommes(pommes, pommes_special, rainbow):
    """Affiche les pommes dans l'aire de jeu
    :param pommes: list, contenant les coordonnées des pommes
    :param pommes_special: dict, indiquant les pommes spéciales
    :param rainbow: str, couleur actuelle du cycle arc-en-ciel
    """
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        couleur = 'red'
        if pomme in pommes_special:
            if pommes_special[pomme] == 'super':
                couleur = rainbow
            elif pommes_special[pomme] == 'bleu':
                couleur = 'blue'
            elif pommes_special[pomme] == 'or':
                couleur = 'yellow'
        cercle(x, y, TAILLE_CASE/2,
               couleur='darkred', remplissage=couleur)
        rectangle(x-2, y-TAILLE_CASE*.4, x+2, y-TAILLE_CASE*.7,
                  couleur='darkgreen', remplissage='darkgreen')

def affiche_murs(murs):
    """Affiche les murs dans l'aire de jeu
    :param murs: list, contenant les coordonnéees des murs
    """
    for mur in murs:
        x, y = case_vers_pixel(mur)
        rectangle(x-TAILLE_CASE/2, y-TAILLE_CASE/2, x+TAILLE_CASE/2,
                  y+TAILLE_CASE/2, couleur='black', remplissage='grey')

def affiche_serpent(serpent, couleur, rainbow):
    """Affiche le serpent
    :param serpent: list, contenant les coordonnées des différents
    segments du serpent
    :param couleur: str, couleur du serpent
    :rainbow: bool, indique si le serpent doit être affiché avec les
    couleurs de l'arc-en-ciel
    """
    for i in range(len(serpent)):
        x, y = case_vers_pixel(serpent[i])

        if not rainbow:
            cercle(x, y, TAILLE_CASE/2 + 1,
                   couleur='black', remplissage=couleur)
        else:
            # En cas de serpent invincible, chaque segement de son corps
            # aura la couleur de l'arc-en-ciel suivant celle du segment
            # précédent
            j = RAINBOW_COULEUR.index(couleur)
            if (j+i)%len(RAINBOW_COULEUR) == len(RAINBOW_COULEUR):
                c = 0
            else:
                c = (j+i)%len(RAINBOW_COULEUR)
            cercle(x, y, TAILLE_CASE/2 + 1,
                   couleur='black', remplissage=RAINBOW_COULEUR[c])

def affiche_temps(timer):
    """Affiche le temps écoulé depuis le début de la partie
    :param timer: float, temps écoulé en secondes
    """
    texte(400, 473, "Temps : " + chaine_temps(timer), taille=18,
          police='Arial Black', couleur='white')

def affiche_score(score):
    """Affiche le score de la partie
    :param score: int"""
    texte(10, 473, 'Score : ' + str(score), taille=18,
          police='Arial Black', couleur='white')

def affiche_vitesse(framerate):
    """Affiche le vitesse actuelle d'exécution du jeu
    :param framerate: int, nombres de tours de la boucle principale
    par seconde"""
    texte(170, 473, 'Vitesse : %d' % (framerate*10) + '%', taille=18,
          police='Arial Black', couleur='white')

def affiche_hud(score, timer, framerate, ralenti):
    """Affiche l'interface en bas de la fenêtre avec les informations
    relatives au score, à la vitesse du jeu et au temps écoulé
    :param score: int
    :param timer: float, temps écoulé en secondes
    :param framerate: int, nombres de tours de la boucle principale
    par seconde
    :param ralenti: bool, indique si le temps est actuellement ralenti
    par une pomme bleue
    """
    rectangle(0, HAUTEUR_PLATEAU * TAILLE_CASE, LARGEUR_PLATEAU*TAILLE_CASE,
              HAUTEUR_PLATEAU * TAILLE_CASE + 80, couleur='', remplissage='black')
    affiche_score(score)
    affiche_temps(timer)
    if ralenti:
        affiche_vitesse(framerate/1.5)
    else:
        affiche_vitesse(framerate)

def affiche_bouton(x, y, longueur, hauteur, text='', coul='black', rempl=''):
    """Affiche un bouton en fonction des paramètres indiqués
    :param x: float, position x du centre du bouton
    :param y: float, position y du centre du bouton
    :param longueur: float, longueur du bouton
    :param hauteur: float, hauteur du bouton
    :param text: str, texte à affiche dans le bouton
    :param coul: str, couleur du contour du bouton
    :param rempl: str, couleur de remplissage du bouton
    """
    rectangle(x - longueur/2, y - hauteur/2, x + longueur/2, y + hauteur/2, remplissage=rempl, couleur=coul)
    texte(x, y, text, police='Arial Black', ancrage='center')

def affiche_boutons_options(torus, accel, nb_murs, couleur_serp, powerups):
    """Affiche les différents boutons dans le menu des options
    :param torus: bool
    :param accel: bool
    :param nb_murs: int
    :param couleur_serp: str
    :param powerups: bool
    """
    texte(300, 80, 'Couleur du serpent', ancrage='center', taille = 14)
    affiche_bouton(300, 120, 180, 60, '', rempl=couleur_serp)
    
    if torus:
        affiche_bouton(300, 200, 180, 60, 'Torus', rempl='green')
    else:
        affiche_bouton(300, 200, 180, 60, 'Torus', rempl='red')
    
    if accel:
        affiche_bouton(300, 280, 260, 60, 'Accélération', rempl='green')
    else:
        affiche_bouton(300, 280, 260, 60, 'Accélération', rempl='red')
    
    if nb_murs == 0:
        affiche_bouton(300, 360, 300, 60, 'Murs', rempl='red')
    elif nb_murs == 20:
        affiche_bouton(300, 360, 300, 60, 'Murs : peu', rempl='green')
    elif nb_murs == 50:
        affiche_bouton(300, 360, 300, 60, 'Murs : moyen', rempl='green')
    else:
        affiche_bouton(300, 360, 300, 60, 'Murs : beaucoup', rempl='green')
    
    if powerups:
        affiche_bouton(300, 440, 260, 60, 'Bonus', rempl='green')
    else:
        affiche_bouton(300, 440, 260, 60, 'Bonus', rempl='red')

def clique_bouton(x, y, longueur, largeur, ev):
    """Détermine si un clic de souris s'est fait sur le bouton dont les
    paramètres sont donnés
    :param x: float, position x centrale du bouton
    :param y: float, position y centrale du bouton
    :param longueur: float, longueur du bouton
    :param hauteur: float, hauteur du bouton
    :param ev: tuple, l'évènement du clic de souris
    :return value: bool, True si le clic sur le bouton est avéré
    """
    if (x-longueur/2 <= abscisse(ev) <= x+longueur/2) and (y-largeur/2 <= ordonnee(ev) <= y+largeur/2):
        return True
    return False

def chaine_temps(timer):
    """Reçoit un temps en seconde, et renvoie une chaine sous la forme
    mm:ss
    :param timer: float, temps écoulé en secondes
    :return value: str
    """
    secondes, minutes = int(timer)%60, int(timer)//60
    if secondes < 10:
        secondes = '0' + str(secondes)
    else:
        secondes = str(secondes)
    if minutes < 10:
        minutes = '0' + str(minutes)
    else:
        minutes = str(minutes)

    return minutes + ':' + secondes

def couleur_serpent(couleur_serp, couleur_rainbow, rainbow):
    """Renvoie la couleur que le serpent doit prendre au cours du tour
    de la boucle
    :param couleur_serp: str, couleur normale du serpent
    :param couleur_rainbow: str, couleur actuelle du cycle de l'arc-en-ciel
    :param rainbow: bool, True si le serpent est invincible
    :return value: str
    """
    if not rainbow:
        return couleur_serp
    else:
        return couleur_rainbow

def cycle_rainbow(couleur):
    """Cycle les couleurs de l'arc-en-ciel en renvoyant la couleur de
    l'arc en ciel suivant celle indiquée en argument
    :param couleur: str, couleur actuelle du cycle
    :return value: str
    """
    i = RAINBOW_COULEUR.index(couleur)
    if i == len(RAINBOW_COULEUR)-1:
        return RAINBOW_COULEUR[0]
    else:
        return RAINBOW_COULEUR[i+1]

def generation_pomme(pommes, pommes_special, serpent, murs, timer, powerups):
    """Gère la génération aléatoire des pommes
    :param pommes: list, contenant les coordonnées des pommes déjà sur
    l'aire de jeu
    :param pommes_special: dict, indiquant les pommes spéciales
    :param serpent: list, contenant les coordonnées du serpent
    :param murs: list, contenant les coordonnées des murs
    :param timer: float, temps écoulé en secondes depuis la dernière
    génération d'une pomme
    :param powerups: bool, si True, génération de pommes spéciales
    :return values: list, dict, float
    """
    if len(pommes) < MAX_POMMES:
        if timer >= DELAI_POMMES:
            while True:
                # On tente de générer une pomme au hasard
                pomme = (randint(0, LARGEUR_PLATEAU-1), randint(0, HAUTEUR_PLATEAU-1))
                # Et on vérifie que l'espace ne soit pas déjà pris
                if (pomme not in pommes) and (pomme not in serpent) and (pomme not in murs):
                    pommes.append(pomme)
                    if powerups:
                        # Si les power-ups sont activés, on tire au hasard
                        # pour savoir si on fait apparaître une pomme spéciale
                        tirage = randint(1, 100)
                        if tirage <= 5:
                            pommes_special[pomme] = 'super'
                        elif tirage <= 10:
                            pommes_special[pomme] = 'bleu'
                        elif tirage <= 17:
                            pommes_special[pomme] = 'or'
                    return pommes, pommes_special, 0
    return pommes, pommes_special, timer

def generation_mur(nb_murs):
    """Gère la génération aléatoire des murs
    :param nb_murs: int, nombre de murs à générer
    :return value: list
    """
    murs = []
    for i in range(nb_murs):
        mur = (randint(0, LARGEUR_PLATEAU-1), randint(0, HAUTEUR_PLATEAU-1))
        while mur in murs or mur == (LARGEUR_PLATEAU//2, HAUTEUR_PLATEAU//2):
            mur = (randint(0, LARGEUR_PLATEAU-1), randint(0, HAUTEUR_PLATEAU-1))
        murs.append(mur)
    return murs

def change_direction(direction, touche):
    """Renvoie la direction du serpent pour le prochain mouvement du
    serpent
    :param direction: tuple, direction actuelle
    :param touche: str, dernière touche appuyée
    :return value: tuple
    """
    if touche == 'Up':
        return (0, -1)
    elif touche == 'Down':
        return (0, 1)
    elif touche == 'Left':
        return (-1, 0)
    elif touche == 'Right':
        return (1, 0)
    else:
        return direction

def avance_serpent(serpent, direction, pomme_mangee):
    """Gère le mouvement du serpent
    :param serpent: list, coordonnées du serpent
    :param direction: tuple, direction actuelle du serpent
    :pomme_mangee: bool, True si une pomme a été mangée au dernier tour
    de la boucle
    :return value: list
    """
    x, y = serpent[0]
    u, v = direction
    new_x = x + u
    new_y = y + v

    if pomme_mangee:
        serpent.insert(0, (new_x, new_y))
    else:
        # Décale tous les segments du serpent en faisant prendre à chaque
        # chaque élément de la liste la valeur de l'élément précédent
        for i in range(len(serpent)-1):
            serpent[len(serpent)-i-1] = serpent[len(serpent)-i-2]

        # Si le bord du plateau est atteint, passer la tête de l'autre
        # côté du plateau
        if new_x < 0:
            new_x = LARGEUR_PLATEAU - 1
        elif new_x >= LARGEUR_PLATEAU:
            new_x = 0

        if new_y < 0:
            new_y = HAUTEUR_PLATEAU - 1
        elif new_y >= HAUTEUR_PLATEAU:
            new_y = 0

        # Affecte à la tête du serpent ses nouvelles coordonnées
        serpent[0] = (new_x, new_y)

    return serpent

def detection(serpent, murs, direction, invincible):
    """Renvoie True si le prochain mouvement du serpent le fera entrer
    en collision avec lui-même, un mur ou les bords de l'aire de jeu
    :param serpent: list, coordonnées du serpent
    :param murs: list, coordonnées des murs
    :param direction: tuple, direction actuelle
    :param incincible: bool, True si le serpent est invincible
    :return value: bool
    """
    if invincible:
        return False
    x, y = serpent[0]
    u, v = direction
    # Collision avec le bord de l'aire de jeu
    if (x + u < 0 or x + u >= LARGEUR_PLATEAU or y + v < 0 or y + v >= HAUTEUR_PLATEAU) and not torus:
        return True
    # Collision avec le corps du serpent
    if (x + u, y + v) in serpent and direction != (0, 0):
        return True
    # Collision avec un mur
    if (x + u, y + v) in murs:
        return True
    return False

def mange_pomme(serpent, pommes, pommes_special, score, ralenti, invincible):
    """Traite et renvoie toutes les informations liées à l'éventuel
    collision du serpent avec une pomme
    :param serpent: list, coordonnées du serpent
    :param pommes: list, coordonnées des pommes
    :param pommes_special: dict, indique les pommes spéciales
    :param score: int
    :param ralenti: float, temps en secondes à rester ralenti
    :param invincible: float, temps en secondes à rester invincible
    :return values: bool, list, dict, int, float, float
    """
    if serpent[0] in pommes:
        if serpent[0] in pommes_special:
            # Gestion des pommes spéciales et des effets associés
            if pommes_special[serpent[0]] == 'or':
                pommes.remove(serpent[0])
                pommes_special.pop(serpent[0])
                return True, pommes, pommes_special, score+10, ralenti, invincible
            elif pommes_special[serpent[0]] == 'bleu':
                pommes.remove(serpent[0])
                pommes_special.pop(serpent[0])
                return True, pommes, pommes_special, score+1, 5, invincible
            elif pommes_special[serpent[0]] == 'super':
                pommes.remove(serpent[0])
                pommes_special.pop(serpent[0])
                return True, pommes, pommes_special, score+1, ralenti, 10
        else:
            # Ingestion d'une pomme normale
            pommes.remove(serpent[0])
            return True, pommes, pommes_special, score+1, ralenti, invincible
    else:
        return False, pommes, pommes_special, score, ralenti, invincible

def pause():
    texte(TAILLE_CASE*LARGEUR_PLATEAU/2, TAILLE_CASE*HAUTEUR_PLATEAU/2,
          "Pause", taille=72, ancrage='center', tag='pause', couleur='blue')
    while True:
        ev= attend_ev()
        ty = type_ev(ev)
        if ty == 'Quitte':
            ferme_fenetre()
        elif ty == 'Touche':
             if touche(ev) == 'p':
                break
    efface('pause')

def ecran_titre(torus, accel, nb_murs, couleur_serp, powerups):
    """Affiche l'écran-titre et gère les interactions du joueur avec
    celui-ci. Renvoie les options choisies par le joueur dans le menu
    des options.
    :param torus: bool
    :param accel: bool
    :param nb_murs: int
    :param couleur_serp: str
    :param powerups: bool
    :return values: bool, bool, int, str, bool
    """
    while True:
        efface_tout()
        texte(TAILLE_CASE*LARGEUR_PLATEAU/2, TAILLE_CASE*HAUTEUR_PLATEAU/8,
              "Bienvenue à", ancrage='center')
        texte(TAILLE_CASE*LARGEUR_PLATEAU/2, TAILLE_CASE*HAUTEUR_PLATEAU/4,
              "Snake", ancrage='center', taille=48, couleur='green')
        texte(TAILLE_CASE*LARGEUR_PLATEAU/2, TAILLE_CASE*HAUTEUR_PLATEAU/2,
              "Faites un clic gauche pour commencer", taille=14, ancrage='center')

        affiche_bouton(300, 346, 180, 60, 'Options', rempl='grey')
        
        while True:
                ev= attend_ev()
                ty = type_ev(ev)
                if ty == 'Quitte':
                    ferme_fenetre()
                elif ty == 'ClicGauche':
                    if clique_bouton(300, 346, 180, 60, ev):
                        torus, accel, nb_murs, couleur_serp, powerups = options(torus, accel, nb_murs, couleur_serp, powerups)
                        break
                    else:
                        return torus, accel, nb_murs, couleur_serp, powerups

def options(torus, accel, nb_murs, couleur_serp, powerups):
    """Affiche le menu des options et gère les interactions du joueur avec
    celui-ci. Renvoie les options choisies par le joueur.
    :param torus: bool
    :param accel: bool
    :param nb_murs: int
    :param couleur_serp: str
    :param powerups: bool
    :return values: bool, bool, int, str, bool
    """
    while True:
        efface_tout()
        texte(TAILLE_CASE*LARGEUR_PLATEAU/2, 40, "Options", ancrage='center')
        affiche_boutons_options(torus, accel, nb_murs, couleur_serp, powerups)
        affiche_bouton(80, 490, 140, 60, 'Retour', rempl='grey')

        while True:
            ev = attend_ev()
            ty = type_ev(ev)
            if ty == 'Quitte':
                ferme_fenetre()
            elif ty == 'ClicGauche':
                if clique_bouton(300, 200, 180, 60, ev):
                    torus = not torus
                    break
                elif clique_bouton(300, 280, 260, 60, ev):
                    accel = not accel
                    break
                elif clique_bouton(300, 360, 180, 60, ev):
                    if nb_murs == 0:
                        nb_murs = 20
                    elif nb_murs == 20:
                        nb_murs = 50
                    elif nb_murs == 50:
                        nb_murs = 70
                    else:
                        nb_murs = 0
                    break
                elif clique_bouton(300, 120, 180, 60, ev):
                    actuel = CYCLE_COULEUR.index(couleur_serp)
                    if actuel == len(CYCLE_COULEUR)-1:
                        couleur_serp = CYCLE_COULEUR[0]
                    else:
                        couleur_serp = CYCLE_COULEUR[actuel+1]
                    break
                elif clique_bouton(300, 440, 260, 60, ev):
                    powerups = not powerups
                    break
                elif clique_bouton(80, 490, 140, 60, ev):
                    return torus, accel, nb_murs, couleur_serp, powerups
            elif ty == 'ClicDroit':
                if clique_bouton(300, 120, 180, 60, ev):
                    actuel = CYCLE_COULEUR.index(couleur_serp)
                    if actuel == 0:
                        couleur_serp = CYCLE_COULEUR[-1]
                    else:
                        couleur_serp = CYCLE_COULEUR[actuel-1]
                    break

def game_over(score, timer):
    """Affiche l'écran de game over et gère les interactions du joueur avec
    celui-ci.
    :param score: int
    :param timer: float, temps en secondes de survie du joueur
    """
    efface_tout()
    texte(300, 112.5, "Game Over", ancrage='center', taille=48, couleur='red')
    texte(300, 225, "Votre score final est : " + str(score), ancrage='center', taille=14)
    texte(300, 195, "Vous avez tenu : " + chaine_temps(timer), ancrage='center', taille=14)
    
    texte(300, 300, "Voulez-vous rejouer ?", ancrage='center', taille=14)

    affiche_bouton(300, 346, 180, 60, 'Oui', rempl='green')
    affiche_bouton(300, 409, 180, 60, 'Non', rempl='red')
    
    while True:
            ev = attend_ev()
            ty = type_ev(ev)
            if ty == 'Quitte':
                ferme_fenetre()
            elif ty == 'ClicGauche':
                if clique_bouton(300, 346, 180, 60, ev):
                    break
                elif clique_bouton(300, 409, 180, 60, ev):
                    ferme_fenetre()

# programme principal
if __name__ == "__main__":

    # initialisation du jeu
    cree_fenetre(TAILLE_CASE * LARGEUR_PLATEAU,
                 TAILLE_CASE * HAUTEUR_PLATEAU + 80)

    # état par défaut des options
    torus = False
    accel = False
    powerups = False
    nb_murs = 0
    couleur_serp = 'green'


    # boucle permettant de recommencer une nouvelle partie
    while True:
        # écran titre et récupération des options choisies par le joueur
        torus, accel, nb_murs, couleur_serp, powerups = ecran_titre(torus, accel, nb_murs, couleur_serp, powerups)

        # initialisation de la partie
        framerate = 10    # taux de rafraîchissement du jeu en images/s
        direction = (0, 0)  # direction initiale du serpent
        pommes = [] # liste des coordonnées des cases contenant des pommes
        pommes_special = {} # dictionnaire permettant de retenir quelles pommes sont spéciales
        serpent = [(LARGEUR_PLATEAU//2, HAUTEUR_PLATEAU//2)] # liste des coordonnées de cases adjacentes décrivant le serpent
        murs = generation_mur(nb_murs) # liste des coordonnées des murs
        timer_pomme, score, timer, ralenti, invincible = 0, 0, 0, 0, 0
        rainbow = 'red' # variable bouclant les couleurs de l'arc-en-ciel
        frein_debut = True # booleen permettant de ne pas commencer les timers tant que le joueur n'a pas commencé à bouger
        pomme_mangee = False # booleen indiquant si une pomme a été mangée pendant ce tour de la boucle
        couleur = couleur_serp # initialisation de la couleur du serpent
        
        # boucle principale
        jouer = True
        while jouer:
            # affichage des objets
            efface_tout()
            affiche_pommes(pommes, pommes_special, rainbow) 
            affiche_serpent(serpent, couleur, invincible > 0)
            affiche_hud(score, timer, framerate, ralenti > 0)
            affiche_murs(murs)
            mise_a_jour()

            # déverouillage des timers lorsque le serpent commence à bouger
            if frein_debut:
                frein_debut = direction == (0, 0)
            
            # gestion des événements
            ev = donne_ev()
            ty = type_ev(ev)
            if ty == 'Quitte':
                ferme_fenetre()
            elif ty == 'Touche':
                print(touche(ev))
                direction = change_direction(direction, touche(ev))
                if touche(ev) == 'p':
                    pause()

            # mouvement du serpent et détection d'une collision avec le mur ou le serpent lui-même
            if detection(serpent, murs, direction, invincible > 0):
                jouer = False
            else:
                serpent = avance_serpent(serpent, direction, pomme_mangee)

            # gestion de la consommation des pommes
            pomme_mangee = False
            pomme_mangee, pommes, pommes_special, score, ralenti, invincible = mange_pomme(serpent, pommes, pommes_special, score, ralenti, invincible)


            # gestion de la génération des pommes
            pommes, pommes_special, timer_pomme = generation_pomme(pommes, pommes_special, serpent, murs, timer_pomme, powerups)

            # gestion des couleurs
            rainbow = cycle_rainbow(rainbow)
            couleur = couleur_serpent(couleur_serp, rainbow, invincible > 0)

            # gestion des timers
            if not frein_debut:
                timer_pomme += 1/framerate
                timer += 1/framerate

            if invincible > 0:
                invincible -= 1/framerate
            else:
                invincible = 0

            if ralenti > 0:
                ralenti -= 1/framerate
            else:
                ralenti = 0

            # gestion de l'accélération
            if accel and framerate < 70 and pomme_mangee:
                framerate += 0.25
                print(framerate)

            # attente avant rafraîchissement
            if ralenti > 0:
                sleep(1.5/framerate)
            else:
                sleep(1/framerate)
            

        # écran de fin
        game_over(score, timer)
        

    # fermeture et sortie
    ferme_fenetre()

