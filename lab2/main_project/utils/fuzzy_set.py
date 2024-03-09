import numpy as np
from main_project.utils.display_data import print_matrix

class FuzzySet:
    def __init__(self, parameter_name: str, parameter_values: list|tuple, expert_evaluations: list|tuple):
        self.parameter_name = parameter_name
        self.parameter_values = np.array(parameter_values)
        self.n = len(self.parameter_values)
        self.expert_evaluations = np.array(expert_evaluations)
        self.A = np.zeros(shape=[self.n, self.n], dtype='float32')
        self.__calc_A()
        self.column_sums = self.A.sum(axis=0)
        self.inverted_sums = 1.0 / self.column_sums
        self.membership_function = self.inverted_sums / max(self.inverted_sums)
        
    def __calc_A(self):
        if len(self.expert_evaluations) == len(self.parameter_values) - 1:
            self.A[self.n - 1] = np.append(self.expert_evaluations, np.ones(1, dtype='float32'))
        else:
            self.A[self.n - 1] = self.expert_evaluations
        i = self.n - 2
        while i >= 0:
            k = i + 1
            for j in range(self.n):
                if i > j:
                    self.A[i, j] = self.A[k, j] / self.A[k, i]
                elif i < j:
                    self.A[i, j] = 1.0 / self.A[j, i]
                else:
                    self.A[i, j] = 1.0
            i -= 1


if __name__ == "__main__":
    parameter_values = np.array((170, 175, 180, 185, 190, 195))
    expert_evaluations = np.array((9, 7, 5, 3, 1))
    fuzzy_set = FuzzySet('ріст', parameter_values, expert_evaluations)

    print(f"fuzzy_set.parameter_name = {fuzzy_set.parameter_name}")
    print(f"fuzzy_set.parameter_values = {fuzzy_set.parameter_values}")
    print(f"fuzzy_set.expert_evaluations = {fuzzy_set.expert_evaluations}")
    print('\nfuzzy_set.A:')
    print_matrix(fuzzy_set.A)
    print(f"\nfuzzy_set.column_sums = {fuzzy_set.column_sums}")
    print(f"fuzzy_set.inverted_sums = {fuzzy_set.inverted_sums}")
    print(f"fuzzy_set.membership_function = {fuzzy_set.membership_function}")