# Certaines parties de ce code ont été générées à l’aide de ChatGPT (OpenAI, 2026),
# un grand modèle de langage développé par OpenAI.
# Le code a été relu et adapté à des fins pédagogiques.
import csv
from typing import List, Optional, Tuple


# Alphabet des mouvements pour le déplacement de la case vide.
MOVE_DELTAS = {
    "G": (0, -1),  # gauche
    "D": (0, 1),   # droite
    "H": (-1, 0),  # haut
    "B": (1, 0),   # bas
}

# Noms lisibles (affichage / messages)
MOVE_NAMES = {"G": "Gauche", "D": "Droite", "H": "Haut", "B": "Bas"}

# Mouvement inverse (utile pour éviter les annulations immédiates)
REVERSE_MOVE = {"G": "D", "D": "G", "H": "B", "B": "H"}


def read_board_csv(path: str) -> List[List[Optional[int]]]:
    """
    Lit un plateau CSV NxN. La case vide est marquée par 'x' (insensible à la casse).
    Retourne un plateau sous forme de liste de listes, avec None pour la case vide.
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = []
        for row in reader:
            if not row:
                continue
            rows.append([cell.strip() for cell in row])

    if not rows:
        raise ValueError("Le fichier du plateau est vide.")

    n = len(rows)
    if any(len(r) != n for r in rows):
        raise ValueError("Le plateau doit être un CSV carré (NxN).")

    board = []
    empty_count = 0
    flat_nums = []

    for r in range(n):
        out_row = []
        for c in range(n):
            cell = rows[r][c]
            if cell.lower() == "x":
                out_row.append(None)
                empty_count += 1
            else:
                try:
                    v = int(cell)
                except ValueError:
                    raise ValueError(f"Valeur de tuile invalide en ({r},{c}) : {cell!r}")
                out_row.append(v)
                flat_nums.append(v)
        board.append(out_row)

    if empty_count != 1:
        raise ValueError("Le plateau doit contenir exactement une case vide 'x'.")
    if len(flat_nums) != len(set(flat_nums)):
        raise ValueError("Le plateau contient des tuiles numérotées dupliquées.")

    return board


def read_solution(path: str) -> List[str]:
    """Lit une solution texte et renvoie la liste des coups (G/D/H/B)."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    moves = []
    for ch in text:
        ch = ch.strip().upper()
        if not ch:
            continue
        if ch not in MOVE_DELTAS:
            raise ValueError(f"Caractère de coup invalide : {ch!r}. Attendu uniquement G/D/H/B.")
        moves.append(ch)
    return moves


def goal_board(n: int) -> List[List[Optional[int]]]:
    """Construit l'état but : 1..n^2-1 et case vide en bas à droite."""
    vals = list(range(1, n * n)) + [None]
    return [vals[i * n : (i + 1) * n] for i in range(n)]


def find_blank(board: List[List[Optional[int]]]) -> Tuple[int, int]:
    """Retourne (ligne, colonne) de la case vide (None)."""
    for r, row in enumerate(board):
        for c, v in enumerate(row):
            if v is None:
                return r, c
    raise ValueError("Aucune case vide ('x') n'a été trouvée.")


def copy_board(board: List[List[Optional[int]]]) -> List[List[Optional[int]]]:
    """Copie superficielle d'un plateau (copie des lignes)."""
    return [row.copy() for row in board]


def apply_move(board: List[List[Optional[int]]], move: str, *, inplace: bool = False) -> List[List[Optional[int]]]:
    """
    Applique un coup (déplacement de la case vide) et retourne le plateau résultant.

    - Si inplace=False (par défaut), retourne un NOUVEAU plateau (l'original n'est pas modifié).
    - Si inplace=True, modifie le plateau sur place et le retourne.
    """
    n = len(board)
    r, c = find_blank(board)
    dr, dc = MOVE_DELTAS[move]
    nr, nc = r + dr, c + dc
    if not (0 <= nr < n and 0 <= nc < n):
        raise ValueError(f"Coup illégal {move} ({MOVE_NAMES[move]}) depuis la case vide en ({r},{c}).")

    b = board if inplace else copy_board(board)
    b[r][c], b[nr][nc] = b[nr][nc], b[r][c]
    return b


def legal_moves(board: List[List[Optional[int]]]) -> List[str]:
    """Renvoie la liste des coups légaux depuis l'état courant (mouvements possibles de la case vide)."""
    n = len(board)
    r, c = find_blank(board)
    moves = []
    for m, (dr, dc) in MOVE_DELTAS.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n:
            moves.append(m)
    return moves


def board_to_csv_str(board: List[List[Optional[int]]]) -> str:
    """Convertit le plateau en texte CSV (case vide affichée comme 'x')."""
    out_lines = []
    for row in board:
        out_lines.append(",".join("x" if v is None else str(v) for v in row))
    return "\n".join(out_lines)


def boards_equal(a: List[List[Optional[int]]], b: List[List[Optional[int]]]) -> bool:
    """Teste l'égalité de deux plateaux."""
    if len(a) != len(b):
        return False
    for r in range(len(a)):
        if a[r] != b[r]:
            return False
    return True


def precompute_states(initial: List[List[Optional[int]]], moves: List[str]) -> List[List[List[Optional[int]]]]:
    """
    Pré-calcule les états successifs.
    states[i] = plateau après application des i premiers coups (states[0] = initial).
    """
    states = [copy_board(initial)]
    cur = initial
    for m in moves:
        cur = apply_move(cur, m, inplace=False)
        states.append(cur)
    return states

def is_solvable(board: List[List[Optional[int]]]) -> bool:
    """
    Détermine si une instance du taquin (puzzle à tuiles glissantes) est solvable.

    Hypothèse :
    L'état but est en ordre ligne-par-ligne (row-major) avec la case vide en bas à droite.

    Paramètre :
    - board : plateau NxN avec None pour représenter la case vide.
    """
    n = len(board)

    # Aplatir le plateau en parcours ligne-par-ligne (row-major), en ignorant la case vide (None).
    # On mémorise aussi l'indice de ligne (0..n-1) de la case vide.
    flat = []
    blank_r = -1
    for r in range(n):
        for c in range(n):
            v = board[r][c]
            if v is None:
                blank_r = r
            else:
                flat.append(v)

    if blank_r == -1:
        raise ValueError("Aucune case vide ('x') n'a été trouvée.")

    # Compter le nombre d'inversions dans la liste aplatie (sans la case vide).
    inv = 0
    for i in range(len(flat)):
        ai = flat[i]
        for j in range(i + 1, len(flat)):
            if ai > flat[j]:
                inv += 1

    # Cas 1 : n impair (ex. 3x3) -> solvable ssi inv est pair
    if n % 2 == 1:
        return inv % 2 == 0

    # Cas 2 : n pair (ex. 4x4)
    # Ligne de la case vide en partant du bas : dernière ligne => 1, avant-dernière => 2, etc.
    blank_row_from_bottom = n - blank_r
    return (inv + blank_row_from_bottom) % 2 == 1
