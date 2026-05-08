import sys

from config import (
    DEFAULT_CONTRACT,
    TOP_N_WORKERS
)

from loaders.contract_loader import load_contract

from utils.text_cleaning import clean_contract_text

from services.worker_update_service import (
    update_workers_embeddings
)

from services.match_service import (
    match_contract
)

"""
CLI entrypoint for worker matching system.
"""

# MAIN =====================================================
if __name__ == "__main__":

    # COMMANDS
    # python main.py update
    # python main.py match
    # python main.py match contract.pdf




    if len(sys.argv) < 2:

        print("\nUsage:")
        print("python main.py update")
        print("python main.py match")
        print("python main.py match contract.pdf")
        sys.exit()


    command = sys.argv[1]



    # UPDATE WORKERS =======================================
    if command == "update":
        count = update_workers_embeddings()

        print(f"Updated {count} workers")

    # MATCH CONTRACT =======================================
    elif command == "match":

        # CONTRACT PATH
        if len(sys.argv) > 2:
            contract_path = sys.argv[2]
        else:
            contract_path = DEFAULT_CONTRACT


        print(f"\nUsing contract file: {contract_path}")


        # LOAD CONTRACT
        raw_contract = load_contract(contract_path)
        contract_text = clean_contract_text(raw_contract)

        # MATCH
        ranked = match_contract(contract_text)

        # OUTPUT
        print(f"\nTOP {TOP_N_WORKERS} WORKERS:")

        for r in ranked[:TOP_N_WORKERS]:

            print(
                f"\n{r['name']} "
                f"| final: {r['score']} "
                f"| kw: {r['keyword_score']} "
                f"| bio: {r['bio_score']}"
            )

            print("Keywords:")

            for kw in r["keywords"][:5]:
                print(f" - {kw}")


    # UNKNOWN COMMAND
    else:

        print(f"\nUnknown command: {command}")