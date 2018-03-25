from .simulated_execution_handler import SimulatedExecutionHandler


def create(execution_type, *args, **kwargs):
    if execution_type == 'simulated':
        return SimulatedExecutionHandler(*args, **kwargs)
    else:
        raise ImportError('{} is not a valid execution handler.'.format(execution_type))
