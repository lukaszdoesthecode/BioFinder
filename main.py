from tkinter import *

from matrix import MatrixDisplayApp
from needleman_wunsch import needleman_wunsch_algorithm
from smith_waterman import smith_waterman_algorithm


def display_matrix(title):
    """
    Function choosing algorithm to be performed, starts new window and prepares place for matrix to be updated.
    :param title: (str of "Needleman-Wunsch algorithm: " or different) String determining algorithm to be picked, the
    "Needleman-Wunsch algorithm: " picks tne NW algorithm, any other algorithm would choose Smith-Waterman
    algorithm.
    :return: None.
    """
    if not isinstance(title, str):
        raise TypeError('Title must be a string.')

    try:
        seq1 = input_seq1.get().upper()
        seq2 = input_seq2.get().upper()
        match = match_value.get()
        missmatch = mismatch_value.get()
        gap = gap_value.get()
    except Exception as e:
        print(f"Exception in Tkinter callback: {e}")

    if match == 0 and missmatch == 0 or gap == 0:
        match = 1
        missmatch = -1
        gap = -2

    if title == "Needleman-Wunsch algorithm: ":
        aligned_1, aligned_2, matrices = needleman_wunsch_algorithm(seq1, seq2, match, missmatch, gap)
    else:
        aligned_1, aligned_2, matrices = smith_waterman_algorithm(seq1, seq2, match, missmatch, gap)

    matrices = [matrix.tolist() for matrix in matrices]

    root = Toplevel(window, background="white")
    seq1 = [char for char in seq1]
    seq2 = [char for char in seq2]
    seq1.insert(0, " ")
    seq2.insert(0, " ")
    seq2.insert(1, " ")

    for matrix in matrices:
        matrix.insert(0, seq2)
        for i in range(len(seq1)):
            matrix[i + 1].insert(0, seq1[i])

    def update_display(index=0):
        """
        Updates the matrix to display every 500 milliseconds.
        :param index: (int) Determines from which matrix the displaying should start.
        :return: None.
        """
        if index < len(matrices):
            matrix = matrices[index]
            MatrixDisplayApp(root, matrix, title)
            window.after(500, update_display, index + 1)

    update_display()
    matrix_rows = len(matrices)
    matrix_cols = len(matrices[0])
    Label(root, text="", font=("Times New Roman", 16), fg="black", bg="white", pady=100).grid(
        row=10, columnspan=matrix_cols)
    subtitle = Label(root, text="Aligned sequences:", font=("Times New Roman", 16), fg="black", bg="white", pady=20)
    subtitle.grid(row=matrix_rows + 1, columnspan=matrix_cols + 2)
    subtitle.place(x=150, y=matrix_rows + 200)

    align1 = Label(root, text=aligned_1, font=("Times New Roman", 11), fg="black", bg="white", pady=5)
    align1.grid(row=matrix_rows + 2, columnspan=matrix_cols)
    align1.place(x=150, y=matrix_rows + 240)
    align2 = Label(root, text=aligned_2, font=("Times New Roman", 11), fg="black", bg="white", pady=5)
    align2.grid(row=matrix_rows + 3, columnspan=matrix_cols)
    align2.place(x=150, y=matrix_rows + 270)


def check_input(sequence):
    """
    Function checking if the input sequence does not consist of forbidden chars - numbers of special cases.
    :param sequence: (str) Input sequence to be checked.
    :return: (Boolean) False if input consists of forbidden chars, True is not.
    """
    forbidden = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', ',', '/' '&', '.']
    if not isinstance(sequence, str):
        raise TypeError('Sequence ought to be a string (str).')
    if len(sequence) != 0:
        for i in range(len(sequence)):
            if sequence[i] in forbidden:
                return False
    else:
        return False
    return True


def update_button():
    """
    Function enabling the checking button if both the entries for sequences are not empty and do not consist of
    forbidden chars.
    :return: None
    """
    if check_input(input_seq1.get()) and check_input(input_seq2.get()):
        compare_button.config(state=NORMAL)
    else:
        compare_button.config(state=DISABLED)


def chosen_method():
    """
    Function picking the form of the algorithm to be performed, based on the clicked radio button.
    :return: None
    """
    if x.get() == 0:
        display_matrix("Needleman-Wunsch algorithm: ")
    elif x.get() == 1:
        display_matrix("Smith-Waterman algorithm: ")
    else:
        pass


if __name__ == "__main__":
    methods = ["Needleman-Wunsch", "Smith-Waterman"]

    # Window creating
    window = Tk()
    window.title("Matrix Visualizer")
    window.geometry("600x650")
    window.config(background="white")
    logo = PhotoImage(file='logo.png')
    window.iconphoto(True, logo)

    # General instruction label
    label = Label(window, text="Type in your sequences to compare them.",
                  font=("Times New Roman", 16, "bold"), fg="black", bg="white", pady=5)
    label.pack()

    # Sequence 1 input and label
    sequence_1 = Label(window, text="Sequence 1:", font=("Times New Roman", 12), background="white")
    sequence_1.pack(pady=10)
    string1 = StringVar()
    input_seq1 = Entry(window, width=50, textvariable=string1)
    input_seq1.pack()

    # Sequence 2 input and label
    sequence_2 = Label(window, text="Sequence 2:", font=("Times New Roman", 12), background="white")
    sequence_2.pack(pady=10)
    string2 = StringVar()
    input_seq2 = Entry(window, width=50, textvariable=string2)
    input_seq2.pack()

    # Match value input and label
    match_value_info = Label(window, text="Match value:", font=("Times New Roman", 10), background="white")
    match_value_info.pack(pady=10)
    match_value = IntVar()
    input_match_value = Entry(window, width=5, textvariable=match_value)
    input_match_value.pack(pady=10)

    # Mismatch value and label
    mismatch_value_info = Label(window, text="Mismatch value:", font=("Times New Roman", 10), background="white")
    mismatch_value_info.pack(pady=10)
    mismatch_value = IntVar()
    input_mismatch_value = Entry(window, width=5, textvariable=mismatch_value)
    input_mismatch_value.pack(pady=10)

    # Gap value and label
    gap_value_info = Label(window, text="Gap value:", font=("Times New Roman", 10), background="white")
    gap_value_info.pack(pady=10)
    gap_value = IntVar()
    input_gap_value = Entry(window, width=5, textvariable=gap_value)
    input_gap_value.pack(pady=10)

    # Value's values instruction
    values_info = Label(window, text="If all the values are 0, the chosen values will be "
                                     "{match = 1, missmatch = -1 ,gap = -2 }", font=("Times New Roman", 8),
                        background="white")
    values_info.pack(pady=10)

    # Method instruction
    methods_info = Label(window, text="Choose the method you want to use:", font=("Times New Roman", 12),
                         background="white")
    methods_info.pack(pady=10)
    x = IntVar()
    for index, method in enumerate(methods):
        Radiobutton(window, text=method, variable=x, value=index, background="white",
                    font=("Times New Roman", 11)).pack()

    info_2 = Label(window,
                   text="If you cannot click the \"Compare\" button, make sure you typed the sequences correctly.",
                   font=("Times New Roman", 12), background="white")
    info_2.pack(pady=10)
    compare_button = Button(window, text="Compare", bg="white", fg="black", font=("Times New Roman", 12),
                            command=chosen_method, state=DISABLED)
    compare_button.pack(anchor="center", pady=15)

    string1.trace("w", lambda *args: update_button())
    string2.trace("w", lambda *args: update_button())

    window.mainloop()
