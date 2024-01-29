import tkinter as tk


class MatrixDisplayApp:
    """
    Class representing centered matrix display.
    """
    def __init__(self, root, matrix_data, label_text):
        """
        MatrixDisplayApp initialization method.
        :param root:
        :param matrix_data:
        :param label_text:
        """
        self.root = root
        window_width = 500
        window_height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.matrix_data = matrix_data

        self.label_text = tk.StringVar()
        self.label_text.set(label_text)
        label = tk.Label(root, textvariable=self.label_text, font=("Times New Roman", 16), bg="white", padx=10)
        label.grid(row=len(matrix_data), columnspan=len(matrix_data[0]))
        label.place(x=150, y=0)

        self.matrix_vars = []
        for row in matrix_data:
            row_vars = []
            for cell in row:
                var = tk.StringVar()
                var.set(str(cell).split(".")[0])
                row_vars.append(var)
            self.matrix_vars.append(row_vars)

        matrix_width = len(matrix_data[0]) * 30
        matrix_height = len(matrix_data) * 20

        matrix_x = (window_width - matrix_width) // 2
        matrix_height = len(matrix_data) * 20

        # Add an offset to move the matrix higher
        matrix_y_offset = 120  # Adjust this value as needed
        matrix_y = (window_height - matrix_height) // 2 - matrix_y_offset

        # Create a Label widget for each cell in the matrix
        self.matrix_labels = []
        for row_index, row in enumerate(self.matrix_data):
            row_labels = []
            for col_index, cell in enumerate(row):
                label = tk.Label(root, textvariable=self.matrix_vars[row_index][col_index], font=("Courier", 11),
                                 width=3, bg="white")
                label.grid(row=row_index, column=col_index)
                label.place(x=matrix_x + col_index * 30, y=matrix_y + row_index * 20)
                row_labels.append(label)
            self.matrix_labels.append(row_labels)

        # Disable the Label widgets to make them read-only
        for row_labels in self.matrix_labels:
            for label in row_labels:
                label.config(state=tk.DISABLED)
