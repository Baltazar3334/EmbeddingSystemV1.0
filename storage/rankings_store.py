"""
LLM rankings storage.
"""

import json
import os


RANKINGS_PATH = "rankings.json"


# LOAD ====================================================
def load_rankings(path=RANKINGS_PATH):

    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# SAVE ====================================================
def save_ranking(
    contract_id,
    ranking,
    path=RANKINGS_PATH
):

    data = load_rankings(path)

    data[contract_id] = ranking

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)