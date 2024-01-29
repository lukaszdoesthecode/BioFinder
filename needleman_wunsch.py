import numpy as np
from smith_waterman import match_matrix


def _needleman_wunsch_initialization(seq1, seq2, gap):
    """
    Function performing initialization of the Needleman-Wunsch algorithm.
    :param seq1: (str) Input sequence.
    :param seq2: (str) Input sequence.
    :return matrix: (list of numpy arrays) Initialized matrix.
    :return matrices: (list of numpy arrays) List how each step of initializing the matrix.
    """
    if not isinstance(seq1, str) or not isinstance(seq2, str):
        raise TypeError('Sequences need to be a type of string.')
    if not isinstance(gap, int):
        raise TypeError('Gap penalty needs to be a string')
    # Matrix for the Needleman-Wunsch algorithm
    matrix = np.zeros((len(seq1) + 1, len(seq2) + 1))
    matrices = []  # List of matrices for the animation

    # Initialization
    for x in range(len(seq1) + 1):
        matrix[x][0] = x * gap
        matrices.append(matrix.copy())
    for y in range(len(seq2) + 1):
        matrix[0][y] = y * gap
        matrices.append(matrix.copy())

    return matrix, matrices


def _needleman_wunsch_filling(seq1, seq2, matrix, matrix_is_match, gap):
    """
    Function performing filling phase of Needleman-Wunsch algorithm.
    :param seq1: (str) Input sequence.
    :param seq2: (str) Input sequence.
    :param matrix: (numpy array) Matrix after initialization phase.
    :param matrix_is_match: (numpy array) Match matrix.
    :param gap: (int) Gap penalty value.
    :return matrix: (list of numpy arrays) Filled matrix.
    :return matrices: (list of numpy arrays) List how each step of filling the matrix.
    """
    if not isinstance(seq1, str) or not isinstance(seq2, str):
        raise TypeError('Sequences need to be a type of string.')
    if not isinstance(gap, int):
        raise TypeError('Gap penalty needs to be a string')
    matrices = []  # List of matrices for the animation

    # Filling of the matrix
    for x in range(1, len(seq1) + 1):
        for y in range(1, len(seq2) + 1):
            matrix[x][y] = max(matrix[x - 1][y - 1] + matrix_is_match[x - 1][y - 1],
                               matrix[x - 1][y] + gap,
                               matrix[x][y - 1] + gap)
            matrices.append(matrix.copy())

    return matrix, matrices


def _needleman_wunsch_traceback(seq1, seq2, matrix, gap):
    """
    Function performing traceback phase of Needleman-Wunsch algorithm.
    :param seq1: (str) Input sequence.
    :param seq2: (str) Input sequence.
    :param matrix: (numpy array) Matrix after filling phase.
    :param gap (int): Gap penalty value.
    :return aligned_1: (str) Output of sequence 1 - local alignments of sequence 1.
    :return aligned_2: (str) Output of sequence 2 - local alignments of sequence 2.
    """

    if not isinstance(seq1, str) or not isinstance(seq2, str):
        raise TypeError('Sequences need to be a type of string.')

    if not isinstance(gap, int):
        raise TypeError('Gap penalty needs to be a string')

    # This was a second traceback implemented so this time I tried to be more fancy about it.
    x, y = len(seq1), len(seq2)
    aligned_1, aligned_2 = "", ""

    # Possible the movement directions
    directions = [(0, -1), (-1, 0), (-1, -1)]

    while x > 0 or y > 0:
        # Calculating possible moves and consideration of which move should be held
        possible_moves = [(matrix[x + d1][y + d2] + (gap if d1 == 0 or d2 == 0 else 0), d1, d2) for d1, d2 in
                          directions]
        max_score, move_d1, move_d2 = max(possible_moves, key=lambda x: x[0])

        # Move execution
        if move_d1 == -1 and move_d2 == -1:  # Diagonal move
            aligned_1 = seq1[x - 1] + aligned_1
            aligned_2 = seq2[y - 1] + aligned_2
            x -= 1
            y -= 1
        elif move_d1 == 0 and move_d2 == -1:  # Left move
            aligned_1 = "-" + aligned_1
            aligned_2 = seq2[y - 1] + aligned_2
            y -= 1
        else:  # Up move
            aligned_1 = seq1[x - 1] + aligned_1
            aligned_2 = "-" + aligned_2
            x -= 1

    return aligned_1, aligned_2


def needleman_wunsch_algorithm(seq1, seq2, match, missmatch, gap):
    """
    Function performing Needleman-Wunsch algorithm with all the steps - initialization, filling, traceback, returns
    general local alignments, as well as all steps of filling the matrix with numbers.
    :param seq1: (str) Input sequence.
    :param seq2: (str) Input sequence.
    :param match: (int) Match value.
    :param missmatch: (int) Missmatch value.
    :param gap: (int) Gap penalty value.
    :return aligned_1 (str): Output of sequence 1 - local alignments of sequence 1.
    :return aligned_2 (str): Output of sequence 2 - local alignments of sequence 2.
    :return all_matrices (list of np arrays): List of numpy arrays representing each step of filling the matrix with
    numbers.
    """

    if not isinstance(match, int) or not isinstance(missmatch, int) or not isinstance(gap, int):
        raise TypeError('Match value, missmatch value and gap penalty needs to be integers.')
    if not isinstance(seq1, str) or not isinstance(seq2, str):
        raise TypeError('Sequences need to be a type of string.')

    matrix_is_match = match_matrix(seq1, seq2, match, missmatch)
    all_matrices = []  # List of all matrices for the animation

    matrix, init_matrices = _needleman_wunsch_initialization(seq1, seq2, gap)
    all_matrices.extend(init_matrices)

    matrix, filling_matrices = _needleman_wunsch_filling(seq1, seq2, matrix, matrix_is_match, gap)
    all_matrices.extend(filling_matrices)

    aligned_1, aligned_2 = _needleman_wunsch_traceback(seq1, seq2, matrix, gap)

    return aligned_1, aligned_2, all_matrices
