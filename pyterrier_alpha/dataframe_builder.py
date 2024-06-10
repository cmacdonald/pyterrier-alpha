import pandas as pd
import numpy as np

class DataFrameBuilder:
    def __init__(self, columns):
        self._data = {c: [] for c in columns}

    def extend(self, values):
        assert all(c in values.keys() for c in self._data), f"all columns must be provided: {list(self._data)}"
        lens = {k: len(v) for k, v in values.items() if hasattr(v, '__len__') and not isinstance(v, str)}
        assert any(lens), "at least one value must have a length"
        first_len = list(lens.values())[0]
        assert all(l == first_len for l in lens.values()), f"all values must have the same length {lens}"
        for k, v in values.items():
            if k not in lens:
                self._data[k].append([v] * first_len)
            elif isinstance(v, pd.Series):
                self._data[k].append(v.values)
            else:
                self._data[k].append(v)

    def to_df(self):
        return pd.DataFrame({
            k: np.concatenate(v)
            for k, v in self._data.items()
        })
