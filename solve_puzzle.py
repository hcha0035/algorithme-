# Les commentaires en gris (et uniquement eux) sont générés par ChatGPT.
import utils
from sys import argv

def hashable(board:list) -> tuple:
    """
    :param board: un plateau, donc une liste de liste
    :return: le plateau en format hashable, ici tuple de tuple
    l'intérêt étant d'utiliser l'historique sous forme de dict au lieu d'une liste afin
    de faire des recherche bien plus rapide
    """
    return tuple(tuple(row) for row in board)

# Fonction récursive qui cherche une solution au puzzle
# board : état actuel du plateau
# goal : état final souhaité
# history : liste des plateaux déjà visités (pour éviter les boucles)
# path : liste des coups effectués jusqu'à présent
# max_step : nombre maximum de coups autorisés
def solver(board, goal, history: dict, path: list, max_step):

    # Si le plateau actuel est égal au plateau objectif
    if utils.boards_equal(board, goal):
        # On renvoie la suite des coups sous forme de chaîne de caractères
        return ''.join(path)

    else:
        # Si on a déjà atteint la limite maximale de coups
        if len(path) >= max_step:
            return None
        else:
            # On parcourt tous les coups légaux possibles
            for i in utils.legal_moves(board):

                # On applique le coup i au plateau
                board_ = utils.apply_move(board, i)

                # Si ce nouveau plateau n'a pas encore été visité ou a été visité d'une manière plus courte qu'avant
                if hashable(board_) not in history or history[hashable(board_)] > len(path) +1:

                    # On ajoute le coup au chemin courant
                    path.append(i)

                    # On ajoute ce plateau à l'historique ou améliore sa valeur
                    history[hashable(board_)] = len(path)

                    # Appel récursif pour continuer la recherche
                    a = solver(board_, goal, history, path, max_step)

                    # Si une solution est trouvée, on la renvoie
                    if a is not None:
                        return a

                    # Sinon on retire le dernier coup (backtracking)
                    path.pop()

    # Si aucune solution n'a été trouvée
    return None


# Point d'entrée du programme
if __name__ == '__main__':

    # Lecture du plateau initial depuis un fichier CSV donné en argument
    board = utils.read_board_csv(argv[1])

    # Vérifie si le puzzle est solvable
    if not utils.is_solvable(board):
        print(" Le jeu est insolvable. ")

    else:
        # Nombre maximal de coups par défaut
        step = 40

        # Si un nombre de coups max est donné en argument
        if len(argv) > 3:
            step = int(argv[3])

        # Lancement du solveur
        s = solver(board, utils.goal_board(len(board)), {hashable(board):0}, [], step)

        # Si aucune solution n'a été trouvée dans la limite de coups
        if s is None:
            print(f" Le jeu est insolvable en moins de {step} coups. ")

        else:
            # Écriture de la solution dans le fichier donné en argument
            with open(argv[2], 'w') as f:
                f.write(str(s))

            print(f' Solution généré et écrite dans {argv[2]} ')

