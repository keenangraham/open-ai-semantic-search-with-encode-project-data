from typing import Any


def dict_to_text(dict_: dict[str, Any]) -> str:
    result = []
    for k, v in dict_.items():
        serialized_key = k.replace('_', ' ').replace('@', '')
        if isinstance(v, str):
            serialized_value = v
            verb = 'is'
        elif isinstance(v, list):
            if v and isinstance(v[0], dict):
                serialized_value = ', '.join(
                    [
                        dict_to_text(vv)
                        for vv in v
                    ]
                )
            else:
                serialized_value = ', '.join(
                    [
                        str(vv)
                        for vv in v
                    ]
                )
            verb = 'are'
        elif isinstance(v, dict):
            serialized_value = dict_to_text(v)
            verb = ''
        result.append(
            f'{serialized_key} {verb} {serialized_value}'
        )
    return ', '.join(result)
