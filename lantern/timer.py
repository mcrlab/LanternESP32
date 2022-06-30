from .logging import logger
try:
    from time import ticks_ms
except (ImportError, ModuleNotFoundError) as e:
    from mocks import ticks_ms

timer_offset = 0
last_time_sync = 0

def get_local_time():
    internal_clock = ticks_ms()
    return internal_clock

def get_server_time():
    global timer_offset
    now = get_local_time()
    return now - timer_offset

def update_time_offset(server_time):
    global timer_offset
    internal_time = ticks_ms()
    timer_offset = internal_time - server_time