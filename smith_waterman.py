import numpy as np


def match_matrix(seq1, seq2, match, mismatch):
    """
    Creating a match/missmatch matrix. Stores match value is in matrix if corresponding chars in sequences match and
    missmatch value if there is no match.
    :param seq1: (str) Input sequence.
    :param seq2: (str) Input sequence.
    :param match: (int) Match value.
    :param mismatch: (int) Mismatch value.
    :return matrix_is_match: (numpy array) Match matrix.
    """
    if not isinstance(seq1, str) or not isinstance(seq2, str):
        raise TypeError('Sequences need to be a type of string.')
    if not isinstance(match, int) or not isinstance(mismatch, int):
        raise TypeError('Match value, missmatch value and gap penalty needs to be integers.')

    matrix_is_match = np.zeros((len(seq1), len(seq2)))
    for x in range(len(seq1)):
        for y in range(len(seq2)):
            if seq1[x] == seq2[y]:
                matrix_is_match[x][y] = match
            else:
                matrix_is_match[x][y] = mismatch
    return matrix_is_match


def _smith_waterman_initialization(seq1, seq2):
    """
    Function performing initialization of the Smith-Waterman algorithm.
    :param seq1: (str) Input sequence.
    :param seq2: (str) Input sequence.
    :return matrix: (list of numpy arrays) Initialized matrix.
    :return matrices: (list of numpy arrays) List how each step of initializing the matrix.
    """
    if not isinstance(seq1, str) or not isinstance(seq2, str):
        raise TypeError('Sequences need to be a type of string.')

    # Matrix for the Smith-Waterman algorithm
    matrix = np.zeros((len(seq1) + 1, len(seq2) + 1))
    matrices = []  # List of matrices for the animation

    # Initialization - all zeros
    return matrix, matrices


def _smith_waterman_filling(seq1, seq2, matrix, matrix_is_match, gap):
    """
    Function performing filling phase of Smith-Waterman algorithm.
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
        raise TypeError('Gap penalty value needs to be an integer.')

    matrices = []  # List of matrices for the animation

    # Filling of the matrix
    for x in range(1, len(seq1) + 1):
        for y in range(1, len(seq2) + 1):
            matrix[x][y] = max(0,
                               matrix[x - 1][y - 1] + matrix_is_match[x - 1][y - 1],
                               matrix[x - 1][y] + gap,
                               matrix[x][y - 1] + gap)
            matrices.append(matrix.copy())

    return matrix, matrices


def _smith_waterman_traceback(seq1, seq2, matrix, matrix_is_match, gap):
    """
    Function performing traceback phase of Smith-Waterman algorithm.
    :param seq1: (str) Input sequence.
    :param seq2: (str) Input sequence.
    :param matrix: (numpy array) Matrix after filling phase.
    :param matrix_is_match: (numpy array) Match matrix.
    :param gap (int): Gap penalty value.
    :return aligned_1: (str) Output of sequence 1 - local alignments of sequence 1.
    :return aligned_2: (str) Output of sequence 2 - local alignments of sequence 2.
    """

    if not isinstance(seq1, str) or not isinstance(seq2, str):
        raise TypeError('Sequences need to be a type of string.')

    if not isinstance(gap, int):
        raise TypeError('Gap penalty needs to be a string')

    # In this part of code I used more simple approach, because first I did SMA and then NWA.
    matrices = []

    # Find the highest scoring cell
    max_score = matrix.max()
    max_position = np.where(matrix == max_score)
    x, y = max_position[0][0], max_position[1][0]

    aligned_1, aligned_2 = "", ""

    # Traceback
    while matrix[x][y] > 0:
        # Diagonal move
        if x > 0 and y > 0 and matrix[x][y] == matrix[x - 1][y - 1] + matrix_is_match[x - 1][y - 1]:
            aligned_1 = seq1[x - 1] + aligned_1
            aligned_2 = seq2[y - 1] + aligned_2
            x -= 1
            y -= 1
        elif x > 0 and matrix[x][y] == matrix[x - 1][y] + gap:  # Up move
            aligned_1 = seq1[x - 1] + aligned_1
            x = "-" + aligned_2
            x -= 1
        elif y > 0 and matrix[x][y] == matrix[x][y - 1] + gap:  # Left move
            aligned_1 = "-" + aligned_1
            aligned_2 = seq2[y - 1] + aligned_2
            y -= 1

    return aligned_1, aligned_2


def smith_waterman_algorithm(seq1, seq2, match, missmatch, gap):
    """
    Function performing Smith-Waterman algorithm with all the steps - initialization, filling, traceback, returns
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

    if not isinstance(seq1, str) or not isinstance(seq2, str):
        raise TypeError('Sequences need to be a type of string.')

    if not isinstance(match, int) or not isinstance(missmatch, int) or not isinstance(gap, int):
        raise TypeError('Match value, missmatch value and gap penalty needs to be integers.')

    matrix_is_match = match_matrix(seq1, seq2, match, missmatch)
    all_matrices = []  # List of all matrices for the animation

    # Initialization step
    matrix, init_matrices = _smith_waterman_initialization(seq1, seq2)
    all_matrices.extend(init_matrices)

    # Matrix filling step
    matrix, filling_matrices = _smith_waterman_filling(seq1, seq2, matrix, matrix_is_match, gap)
    all_matrices.extend(filling_matrices)

    # Traceback
    aligned_1, aligned_2 = _smith_waterman_traceback(seq1, seq2, matrix, matrix_is_match, gap)

    return aligned_1, aligned_2, all_matrices
