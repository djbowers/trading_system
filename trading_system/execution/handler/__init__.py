from enum import Enum

from .simulated import SimulatedExecutionHandler


def create_handler(execution_type, *args, **kwargs):
    if execution_type == ExecutionType.SIMULATED:
        return SimulatedExecutionHandler(*args, **kwargs)
    else:
        raise ImportError('{} is not a valid execution handler.'.format(execution_type))


class ExecutionType(Enum):
    SIMULATED: 1
