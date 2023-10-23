from collections import UserList
import typing as tp


class ListTwist(UserList[tp.Any]):
    def __init__(self, data: None) -> None:
        super().__init__(data if data is not None else [])

    def __getattr__(self, name: tp.Any) -> tp.Any:
        if name == 'reversed' or name == 'R':
            return self.data[::-1]
        elif name == 'first' or name == 'F':
            if not self.data:
                raise AttributeError("mpty")
            return self.data[0]
        elif name == 'last' or name == 'L':
            if not self.data:
                raise AttributeError("mpty")
            return self.data[-1]
        elif name == 'size' or name == 'S':
            return len(self.data)
        else:
            raise AttributeError(f"no '{name}'")

    def __setattr__(self, name: tp.Any, value: tp.Any) -> None:
        if name == 'first' or name == 'F':
            if not self.data:
                raise AttributeError("empty")
            self.data[0] = value
        elif name == 'last' or name == 'L':
            if not self.data:
                raise AttributeError("mpty")
            self.data[-1] = value
        elif name == 'size' or name == 'S':
            if value < 0:
                raise ValueError("size < 0")
            if value < len(self.data):
                self.data = self.data[:value]
            elif value > len(self.data):
                self.data.extend([None] * (value - len(self.data)))
        else:
            super().__setattr__(name, value)
