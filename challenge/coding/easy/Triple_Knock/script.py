# chiavi per il quale ordinare la lista
def parse_key(entry):
    parts = entry.split()
    user = parts[0]
    day, month = parts[1].split("/")
    hour, minute = parts[2].split(":")
    return (int(month), int(day), user, int(hour), int(minute))

# trasforma mese, giorno, ora e minuti in minuti
def to_minutes(entry):
    parts = entry.split()
    day, month = parts[1].split("/")
    hour, minute = parts[2].split(":")
    return int(month) * 30 * 24 * 60 + int(day) * 24 * 60 + int(hour) * 60 + int(minute)

# numero di righe
raws = int(input().split()[0]) + 1
# lista delle righe
total_entries = []
for n in range(1, raws):
    total_entries.append(input())

# lista con solo i tentativi falliti
failed_attempts = [attempt for attempt in total_entries if "[failure]" in attempt]
# lista ordinita per data, utente e ora
attempts_sorted = sorted(failed_attempts, key=parse_key)

# lista degli utenti che hanno subito un attacco
targeted = []
for i in range(len(attempts_sorted) - 2):
    # 3 tentativi consecutivi
    attempt_a, attempt_b, attempt_c = attempts_sorted[i], attempts_sorted[i + 1], attempts_sorted[i + 2]
    # attempt_a.split()[0] è il nome utente
    if (attempt_a.split()[0] == attempt_b.split()[0] == attempt_c.split()[0] and to_minutes(attempt_c) - to_minutes(attempt_a) < 10):
        targeted.append(attempt_a.split()[0])

# dalla lista creaimo una stringa con i nomi ordinati e separati da spazio
print(" ".join(sorted(targeted)))
