from config import LAST_NAME, FAVORITE_ARTIST, SEED_NUM

def identity_number():
    return sum(ord(c) for c in LAST_NAME + FAVORITE_ARTIST) + SEED_NUM

def telemetry_stream(count=12):
    base = identity_number()
    for idx in range(count):
        if idx == 4:
            yield 'sensor-disconnected'
        elif idx == 9:
            yield None
        else:
            yield round(20 + ((base + idx * 37) % 230) / 5 + (idx % 3) * 2, 2)

def monitor(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        res = func(*args, **kwargs)
        wrapper.last_result = res
        return res
    wrapper.calls = 0
    wrapper.last_result = None
    return wrapper

def trace_abnormal(val, threshold, depth=0):
    if val <= threshold or depth >= 3:
        return [f'Boundary reached at depth {depth}: {val:.2f}']
    next_val = val - threshold / 2
    return [f'Depth {depth}: {val:.2f} exceeds {threshold:.2f}'] + \
           trace_abnormal(next_val, threshold, depth + 1)