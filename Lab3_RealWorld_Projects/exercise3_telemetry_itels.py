from config import LAST_NAME, SEED_NUM, FAVORITE_ARTIST
from telemetry_itels import telemetry_stream, monitor, trace_abnormal

@monitor
def process_telemetry(data_stream): 
    processed = valid = invalid = abnormal = 0
    traces = []
    
    for raw in data_stream:
        processed += 1
        try:
            if not isinstance(raw, (int, float)):
                raise ValueError('non-numeric reading')
            val = float(raw)
            if val < 0:
                raise ValueError('negative reading')
            valid += 1
            if val > 40:
                abnormal += 1
                traces.append(trace_abnormal(val, 40))
        except (TypeError, ValueError):
            invalid += 1
    
    status = 'UNSAFE' if abnormal > 0 else 'SAFE'
    return {
        'processed': processed,
        'valid': valid,
        'invalid': invalid,
        'abnormal': abnormal,
        'status': status,
        'traces': traces
    }

# Generate & process
transformed = map(lambda x: x if isinstance(x, (int, float)) else x, telemetry_stream())
report = process_telemetry(transformed)

# Report
print('=' * 50)
print('      EXERCISE 3: TELEMETRY MONITORING')
print('=' * 50)
print(f'Student   : {LAST_NAME}')
print(f'Seed No.  : {SEED_NUM}')
print(f'Artist    : {FAVORITE_ARTIST}')
print('-' * 50)
print(f'Processed : {report["processed"]}')
print(f'Valid     : {report["valid"]}')
print(f'Invalid   : {report["invalid"]}')
print(f'Abnormal  : {report["abnormal"]}')
print(f'Status    : {report["status"]}')
print(f'Monitored : {process_telemetry.calls} call(s)')
print('-' * 50)

for i, trace in enumerate(report['traces'], 1):
    print(f'\nAbnormal Trace {i}:')
    for step in trace:
        print(f'  {step}')

print('\n=== END OF REPORT ===')
