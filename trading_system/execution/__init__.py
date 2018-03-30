from .execution_handler import ExecutionHandler
from .simulated import SimulatedExecutionHandler
from .type import ExecutionType


def create_handler(execution_type, *args, **kwargs):
    if execution_type == ExecutionType.SIMULATED:
        return SimulatedExecutionHandler(*args, **kwargs)
    else:
        raise ImportError('{} is not a valid execution handler.'.format(execution_type))
