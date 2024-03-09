import numpy as np
from json import JSONEncoder

from main_project.utils.fuzzy_set.fuzzy_set import FuzzySet

class FuzzySetEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, FuzzySet):
            return obj.__dict__
        return super().default(obj)