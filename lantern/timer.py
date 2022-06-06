try:
    from time import ticks_ms
except (ImportError, ModuleNotFoundError) as e:
    from mocks import ticks_ms

timer_offset = 0
last_time_sync = 0

def get_current_time():
    internal_clock = ticks_ms()
    return internal_clock

def update_time_offset(server_time):
    internal_time = ticks_ms()
    last_time_sync = internal_time
    timer_offset = internal_time - server_time