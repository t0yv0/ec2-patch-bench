import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv('raw.csv')

# Only consider rows without errors.
df = df[df['errors'] == 'none']

# Clean rows with NaN values.
df = df[~df['up_sec'].isna()]

# Separate experiment (patch) and control (base).
df_t = df[df['patch'] == True]
df_f = df[df['patch'] == False]

# Merge back to align experiment and control on the same row.
df_m = df_f.merge(df_t,
                  how='inner',
                  on=['pulumi_version',
                      'ec2_size',
                      'region',
                      'resource_count',
                      'resource_payload_bytes'],
                  suffixes=('_base', '_patch'))

df_m['stacksz'] = df['resource_count'] * df['resource_payload_bytes']

df_m['speedup'] = 100.0 * (1.0 - df_m['up_sec_patch'] / df_m['up_sec_base'])


def speedup_hist(df, by_col='stacksz'):
    df_m = df.copy()
    df_m['tot_mb']        = df['stacksz'] /1024 / 1024
    df_m['tot_sec_base']  = df['up_sec_base']
    df_m['tot_sec_patch'] = df['up_sec_patch']
    df_m['count']            = 1
    df_r = df_m[[by_col, 'tot_mb', 'tot_sec_base', 'tot_sec_patch', 'count']].groupby(by=[by_col]).agg({
        'tot_mb':        'sum',
        'tot_sec_base':  'sum',
        'tot_sec_patch': 'sum',
        'count':         'sum',
    })

    df_r['agg_speedup'] = 100 * (1.0 - df_r['tot_sec_patch'] / df_r['tot_sec_base'])
    return df_r


cols = ['region', 'resource_count', 'stacksz', 'up_sec_base', 'up_sec_patch', 'speedup']


print('\n\n== Speedup % by stack size ==\n\n')
print(speedup_hist(df_m, 'stacksz'))

print('\n\n== Speedup % by region ==\n\n')
print(speedup_hist(df_m, 'region'))

print('\n\n== Speedup % by res count ==\n\n')
print(speedup_hist(df_m, 'resource_count'))

print('\n\n== Worst speedup % examples ==\n\n')
print(df_m.sort_values(by=['speedup'], ascending=True)[cols][0:10])

print('\n\n== Best speedup % examples ==\n\n')
print(df_m.sort_values(by=['speedup'], ascending=False)[cols][0:10])
