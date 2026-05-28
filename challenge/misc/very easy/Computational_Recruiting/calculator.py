import sys

weights = {
    "health":          0.20,
    "agility":         0.30,
    "charisma":        0.10,
    "knowledge":       0.05,
    "energy":          0.05,
    "resourcefulness": 0.30,
}

overall_weights = {
    "health":          0.18,
    "agility":         0.20,
    "charisma":        0.21,
    "knowledge":       0.08,
    "energy":          0.17,
    "resourcefulness": 0.16,
}

skill_names = list(weights.keys())

def skill_score(s: int, weight: float) -> int:
    """round(6 * (int(s) * skill_weight)) + 10  —  Python 3 banker's rounding."""
    return round(6 * (int(s) * weight)) + 10

def overall_value(scores: dict) -> int:
    total = (
        scores["health"]          * overall_weights["health"] +
        scores["agility"]         * overall_weights["agility"] +
        scores["charisma"]        * overall_weights["charisma"] +
        scores["knowledge"]       * overall_weights["knowledge"] +
        scores["energy"]          * overall_weights["energy"] +
        scores["resourcefulness"] * overall_weights["resourcefulness"]
    )
    return round(5 * total)

def is_data_row(parts: list) -> bool:
    """True if the line has exactly 8 fields and the last 6 are integers 1-10."""
    if len(parts) != 8:
        return False
    try:
        # prendiamo solo i punteggi come int
        values = [int(p) for p in parts[2:]]
        return all(1 <= v <= 10 for v in values)
    except ValueError:
        return False

def main(filepath: str):
    candidates = []

    with open(filepath, encoding="utf-8") as f:
        # per ogni riga
        for line in f:
            parts = line.split()
            if not is_data_row(parts):
                continue

            nome, cognome = parts[0], parts[1]
            # prendiamo solo i punteggi come int
            raw = [int(p) for p in parts[2:]]

            # dizionario con nome skill : punteggio calcolato
            scores = {
                skill: skill_score(raw[i], weights[skill])
                for i, skill in enumerate(skill_names)
            }

            # calcoliamo il totale
            ov = overall_value(scores)
            candidates.append((nome, cognome, ov))

    # ordiniamo in ordine descrescente
    candidates.sort(key=lambda x: x[2], reverse=True)

    print(", ".join(f"{nome} {cognome} - {ov}" for nome, cognome, ov in candidates[:14]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python calculator.py <file.txt>")
        sys.exit(1)
    main(sys.argv[1])