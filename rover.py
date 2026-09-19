import sys


# ---------------------------------------------------------------------------
# INPUT PARSING
# ---------------------------------------------------------------------------

def lire_lignes(chemin_fichier):
    """
    Reads the file and returns a list of non-empty, cleaned lines
    (no extra whitespace or newline characters).
    """
    with open(chemin_fichier, "r") as f:
        lignes = [ligne.strip() for ligne in f.readlines()]
    return [ligne for ligne in lignes if ligne]  # remove empty lines


def parser_plateau(ligne):
    """
    Parses the first line of the file: the upper-right corner
    coordinates of the plateau.
    Example: "5 5" -> (5, 5)
    """
    x, y = ligne.split()
    return int(x), int(y)


def parser_position(ligne):
    """
    Parses a rover's position line.
    Example: "1 2 N" -> (1, 2, "N")
    """
    x, y, direction = ligne.split()
    return int(x), int(y), direction


def parser_instructions(ligne):
    """
    Parses a rover's instruction line.
    Example: "LMLMLMLMM" -> "LMLMLMLMM"
    (kept as-is, but could be cleaned further if needed)
    """
    return ligne.strip()


def lire_input(chemin_fichier):
    """
    Reads and parses the entire input file.

    Returns a tuple:
        (plateau, rovers)

    where:
        plateau = (max_x, max_y)
        rovers  = list of dicts, one per rover:
            {"position": (x, y, direction), "instructions": "LMLMM..."}
    """
    lignes = lire_lignes(chemin_fichier)

    if not lignes:
        raise ValueError("The input file is empty.")

    plateau = parser_plateau(lignes[0])

    rovers = []
    i = 1
    while i + 1 < len(lignes):
        position = parser_position(lignes[i])
        instructions = parser_instructions(lignes[i + 1])
        rovers.append({"position": position, "instructions": instructions})
        i += 2

    return plateau, rovers


# ---------------------------------------------------------------------------
# SIMULATION LOGIC
# ---------------------------------------------------------------------------

# Cardinal directions listed clockwise. This order lets us turn left/right
# just by moving backward/forward in this list (with wraparound).
DIRECTIONS = ["N", "E", "S", "W"]

# How x, y change for a forward move ("M"), depending on current heading.
MOVES = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


def tourner(direction, commande):
    """
    Returns the new heading after turning left ('L') or right ('R').
    Turning does not change the rover's position.
    """
    index = DIRECTIONS.index(direction)
    if commande == "L":
        index = (index - 1) % 4
    elif commande == "R":
        index = (index + 1) % 4
    return DIRECTIONS[index]


def avancer(x, y, direction, max_x, max_y):
    """
    Returns the new (x, y) position after moving forward one step,
    clamped to stay within the plateau boundaries [0, max_x] x [0, max_y].
    If the move would go out of bounds, the rover simply stays in place.
    """
    dx, dy = MOVES[direction]
    nouveau_x, nouveau_y = x + dx, y + dy

    if 0 <= nouveau_x <= max_x and 0 <= nouveau_y <= max_y:
        return nouveau_x, nouveau_y
    return x, y  # ignore the move if it would leave the plateau


def deplacer_rover(position, instructions, max_x, max_y):
    """
    Executes a full instruction string on a single rover and returns
    its final (x, y, direction).
    """
    x, y, direction = position

    for commande in instructions:
        if commande in ("L", "R"):
            direction = tourner(direction, commande)
        elif commande == "M":
            x, y = avancer(x, y, direction, max_x, max_y)
        # any other character is silently ignored

    return x, y, direction


# ---------------------------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------------------------

def resoudre(chemin_fichier):
    """
    Reads the input file and returns a list of final rover states
    (one string "x y direction" per rover), in the same order as the input.
    Rovers are processed sequentially, one after another.
    """
    plateau, rovers = lire_input(chemin_fichier)
    max_x, max_y = plateau

    resultats = []
    for rover in rovers:
        x, y, direction = deplacer_rover(
            rover["position"], rover["instructions"], max_x, max_y
        )
        resultats.append(f"{x} {y} {direction}")

    return resultats


def main():
    if len(sys.argv) < 2:
        print("Usage: python rover.py input.txt")
        sys.exit(1)

    chemin_fichier = sys.argv[1]
    resultats = resoudre(chemin_fichier)

    for ligne in resultats:
        print(ligne)


if __name__ == "__main__":
    main()