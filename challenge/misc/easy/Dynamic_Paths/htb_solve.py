import socket

HOST = "IP"     # Sostituisci con l'indirizzo IP corretto
PORT = 0        # Sostituisci con la porta corretta          

def min_path_sum(grid):
    rows = len(grid)
    cols = len(grid[0])
    # crea una griglia con tutti zeri
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    # modifica la prima riga con le somme
    for j in range(1, cols):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    # modifica la prima colonna con le somme
    for i in range(1, rows):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    # modifica il resto della griglia con le somme minime
    for i in range(1, rows):
        for j in range(1, cols):
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j]
    # ultima riga, ultima colonna
    return dp[rows - 1][cols - 1]

def recv_until_prompt(s):
    """Accumulate data until the '> ' prompt appears."""
    data = ""
    while True:
        # legge i primi 4096 bytes e decodifica
        chunk = s.recv(4096).decode()
        if not chunk:
            break
        data += chunk
        if data.endswith("> "):
            break
    return data

def parse_and_solve(data):
    # lista di righe
    lines = [l for l in data.strip().split('\n') if l.strip()]
    #lista con i numeri della griglia
    flat   = list(map(int, lines[-2].split()))
    raws_cols = list(map(int, lines[-3].split()))
    n_rows = raws_cols[0]
    n_cols = raws_cols[1]
    # crea la griglia
    grid   = [flat[i * n_cols:(i + 1) * n_cols] for i in range(n_rows)]
    return min_path_sum(grid)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.settimeout(10)

    data = recv_until_prompt(s)
    print(data)

    for i in range(1, 101):
        try:
            # risolve la sfida
            answer = parse_and_solve(data)
        except Exception as e:
            print(f"[!] Round {i} parse error: {e}")
            print(f"[!] Raw data:\n{repr(data)}")
            break

        print(f"[{i}/100] Answer: {answer}")
        s.sendall((str(answer) + '\n').encode())

        try:
            # riceve le istruzioni per la prossima sfida
            data = recv_until_prompt(s)
            print(data)
        except socket.timeout:
            print("[*] No more data — done.")
            break

    s.close()

main()
