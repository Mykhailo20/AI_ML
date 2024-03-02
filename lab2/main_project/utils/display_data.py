def print_matrix(matrix, precision=3):
    """
    Prints a NumPy matrix.

    Args:
        matrix (numpy.ndarray): The matrix to be printed.
        precision (int): The number of decimal places to display (default is 2).
    
    Returns: None
    """
    for row in matrix:
        print("[", end="")
        row_el_no = len(row)
        for i in range(row_el_no):
            print(f"{row[i]:.{precision}f}", end=", " if i != row_el_no - 1 else "")
        print("]")



