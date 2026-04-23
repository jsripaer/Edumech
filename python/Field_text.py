import numpy as np
from typing import Any, Callable
from system import Particle, System
from functools import partial

type Position = np.ndarray
type Velocity = np.ndarray
type Acceleration = np.ndarray
type Fun = Callable[[Particle | System, bool], Any]

DELTA_T: float = 0.01

register: dict[str, Any] = {} # maybe a list?
# if we create an object, whatever the particle or system, add it to register

class Field:
    """the same as Field but used for text"""
    def __init__(self, *function: Fun, width: int, height: int) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        self.size = (width, height)
        self.force = np.zeros((height, width))
        self._function = function

    def response(self) -> None:
        for _object in register.values():
            _object.update(DELTA_T, self.force)

    def update(self) -> None:
        for pos in np.ndindex(self.size[1], self.size[0]):
            for fn in self._function:
                self.force[pos[0], pos[1]] += fn(*pos)

def distance(particle1: Particle, particle2: Particle | Position) -> float:
    try:
        return np.sqrt(np.sum(np.square(particle1.position - particle2.position)))
    except AttributeError:
        return np.sqrt(np.sum(np.square(particle1.position - particle2)))

def source_force(pos: Position) -> float:
    """entry: the name of the para. and its value, such as k, p(+1 | -1)"""
    # todo we can get the user's input and then determine which kind of force they choose
    # TODO get entry the source and entry
    source, args, kwargs = get_entry()
    dist = distance(source, pos)
    # fn:
    # force = fn(...)
    # return force
    pass

def get_entry(source: Particle, *args: str, **kwargs: tuple[str, float]) -> Any:
    """form gui put the entry into function and then put the function into Field"""
    # todo
    return source, args, kwargs

