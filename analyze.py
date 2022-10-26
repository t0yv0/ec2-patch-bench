from os import walk


def stdout_log_file(bench_file):
    return 'stdout-' + bench_file.strip('.txt').strip('time-') + '.log'


def stderr_log_file(bench_file):
    return 'stderr-' + bench_file.strip('.txt').strip('time-') + '.log'


def read_duration(d, bench_file):
    with open(f"{d}/{bench_file}", 'r') as fp:
        raw = fp.read()

    if len(raw) == 0:
        return None

    if 'elapsed' in raw:
        dur = raw.split(' ')[2].strip('elapsed')
        minutes, sec = dur.split(':')
        total_sec = float(minutes) * 60 + float(sec)
        return total_sec

    parts = [p for p in raw.split(' ') if p]
    assert parts[1] == 'real'
    return float(parts[0].strip())


def read_stderr(d, bench_file):
    f = stderr_log_file(bench_file)

    with open(f"{d}/{f}", 'r') as fp:
        raw = fp.read()

    return raw


fs = {}
for (dirpath, dirnames, filenames) in walk('data'):
    if len(filenames):
        fs[dirpath] = list(filenames)


for k in fs:
    fs[k] = [f for f in fs[k] if f.startswith('time-')]


print("pulumi_version,ec2_size,region,patch,resource_count,resource_payload_bytes,up_sec,errors")

puver = 'v3.44.1'
size = 'm6i.large'

for d in fs:
    for f in fs[d]:

        region = d.split('.')[1]
        (_, _, control, n, p, _) = f.split('-')

        total_sec = read_duration(d, f)

        try:
            stderr = read_stderr(d, f)
            errs = 'none' if len(read_stderr(d, f)) == 0 else 'some'
        except FileNotFoundError:
            errs = 'unknown'

        total_sec = '' if total_sec is None else total_sec

        print(f"{puver},{size},{region},{control},{n},{p},{total_sec},{errs}")
