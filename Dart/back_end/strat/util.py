def get_d_prrt(d_df, close):
    if d_df.__len__() <= 0 or close <= 0:
        return 0, 0
    d_close = int(d_df[-1:]['close'].values[0])
    d_rt    = round((d_close - close) / close * 100,2)
    return d_close, d_rt

def get_content_value(content, key):
    s_idx = content.find(key)

    if s_idx < 0:
        return '-'
    s_idx = s_idx + key.__len__()
    e_idx = content[s_idx:].find('\n')
    if e_idx < 0:
        e_idx = content.__len__()
    else:
        e_idx = e_idx + s_idx
    return content[s_idx:e_idx]

