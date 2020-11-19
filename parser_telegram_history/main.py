import json
import pprint
from datetime import datetime
from itertools import filterfalse, groupby
from operator import itemgetter
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Union

import fire


"""
"type": ['service', 'message']

service fields:
action: ['join_group_by_link', 'remove_members', 'pin_message', 'invite_members', 'edit_group_photo', 'score_in_game']
['id', 'type', 'date', 'edited', 'actor', 'actor_id', 'text']
"""

def message(messages: List[Dict], Not_equal: bool = False, **kwargs: Dict[str, Union[str, int]]) -> Iterator:
    for key in list(kwargs.keys()):
        if key == "type_":
            kwargs["type"] = kwargs.pop(key)
        if key == "from_":
            kwargs["from"] = kwargs.pop(key)
    def select(item: Any) -> bool:
        for field, value in kwargs.items():
            try:
                if not item[field] == value:
                    return False
            except KeyError as e:
                print(item)
                print(e)
                raise Exception
        return True

    if Not_equal:
        return filterfalse(select, messages)
    else:
        return filter(select, messages)


def main(file):
    """
    парсинг истории телеграм
    """
    path = Path(file)
    decoded_json = json.loads(path.read_bytes())
    chat_bokal = decoded_json["chats"]["list"][0]["messages"]
    res = message(chat_bokal, type_='message')
    res = message(res, from_='Voicy', edited='1970-01-01T05:00:00')
    # res = message(res, from_='Voicy', edited='1970-01-01T05:00:00')
    # res = message(res, from_='собрание морских окуней', edited='1970-01-01T05:00:00')

    pprint.pprint(list(res)[10:])


def cli():
    fire.Fire(main)


if __name__ == "__main__":
    cli()