def truncate_value(value, max_str_len=3, max_list_len=10, max_depth=2, _depth=0):
    if _depth >= max_depth:
        return '...'

    if isinstance(value, dict):
        return {
            k: truncate_value(v, max_str_len, max_list_len, max_depth, _depth + 1)
            for k, v in list(value.items())[:max_list_len]
        }

    if isinstance(value, (list, tuple)):
        truncated = [
            truncate_value(v, max_str_len, max_list_len, max_depth, _depth + 1)
            for v in value[:max_list_len]
        ]
        if len(value) > max_list_len:
            truncated.append("...")
        return tuple(truncated) if isinstance(value, tuple) else truncated

    if isinstance(value, str):
        return value if len(value) <= max_str_len else value[:max_str_len] + '...'

    return value
