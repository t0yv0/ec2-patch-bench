import pandas as pd

df = pd.read_csv('raw.csv')
df = df[df['errors'] == 'none']

df_t = df[df['patch'] == True]
df_f = df[df['patch'] == False]

df_m = df_f.merge(df_t, how='inner', on=['pulumi_version',
                                         'ec2_size',
                                         'region',
                                         'resource_count',
                                         'resource_payload_bytes'])

df_m['stacksz'] = df['resource_count'] * df['resource_payload_bytes']

df_m['speedup'] = 100.0 * (1.0 - df_m['up_sec_y'] / df_m['up_sec_x'])


def speedup_hist(df, by_col='stacksz'):
    df_m = df.copy()
    df_m['speedup_min'] = df_m['speedup']
    df_m['speedup_avg'] = df_m['speedup']
    df_m['speedup_max'] = df_m['speedup']
    return df_m[[by_col, 'speedup_min', 'speedup_avg', 'speedup_max']].groupby(by=[by_col]).agg({
        'speedup_min': 'min',
        'speedup_avg': 'mean',
        'speedup_max': 'max',
    })


print('\n\n== Speedup % by stack size ==\n\n')
print(speedup_hist(df_m))


print('\n\n== Worst speedup % examples ==\n\n')
print(df_m[df_m['speedup'] < -10])


print('\n\n== Best speedup % examples ==\n\n')
print(df_m[df_m['speedup'] > 40])
