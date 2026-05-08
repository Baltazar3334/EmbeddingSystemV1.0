def clean_contract_text(text: str) -> str:
    lines = text.split("\n")

    filtered = []

    for line in lines:
        line = line.strip()

        if len(line) < 30:
            continue

        if line.isdigit():
            continue

        filtered.append(line)

    return " ".join(filtered)