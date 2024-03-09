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


def prepare_graph_data(parameter_values, membership_function):
    graph_dict = {}
    for i in range(len(parameter_values)):
        par_value = parameter_values[i]
        membership_function_value = membership_function[i]
        graph_dict[par_value] = membership_function_value
    sorted_graph_list = sorted(graph_dict.items(), key=lambda x:x[0])

    sorted_graph_dict = {}
    for i in range(len(sorted_graph_list)):
        par_value = sorted_graph_list[i][0]
        membership_function_value = sorted_graph_list[i][1]
        sorted_graph_dict[par_value] = membership_function_value
    
    return sorted_graph_dict
