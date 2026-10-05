"""
benchmark.py - Automated experiments and evaluation for Minesweeper AI.
Author: Group Students (CO3061) - HCMUT
Course: Introduction to Artificial Intelligence (CO3061) - HCMUT
"""

import time
import sys
from game_logic import MinesweeperGame
from ai_solver import MinesweeperAI, Move

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def run_single_simulation(rows: int, cols: int, num_mines: int, flood_algo: str = "BFS"):
    """Runs a single automated game from start to finish using the AI."""
    game = MinesweeperGame(rows, cols, num_mines, flood_algorithm=flood_algo)
    ai = MinesweeperAI(game)

    moves_count = 0
    guesses_count = 0
    start_t = time.perf_counter()

    while not game.game_over:
        move = ai.get_next_move()
        if not move:
            break
        
        moves_count += 1
        if "Heuristic" in move.reason or move.probability > 0.0 and move.action == Move.REVEAL:
            # If not turn 1 and had to risk
            if moves_count > 1:
                guesses_count += 1

        ai.execute_move(move)

    duration_ms = (time.perf_counter() - start_t) * 1000
    return {
        "won": game.won,
        "moves": moves_count,
        "guesses": guesses_count,
        "time_ms": duration_ms,
        "revealed": game.revealed_count
    }


def run_benchmark(num_games: int = 100):
    """Runs benchmark across multiple configurations and prints summary tables."""
    configs = [
        {"name": "5x5 Mini (3 Mìn)", "rows": 5, "cols": 5, "mines": 3, "algo": "BFS"},
        {"name": "5x5 Thử thách (5 Mìn)", "rows": 5, "cols": 5, "mines": 5, "algo": "BFS"},
        {"name": "9x9 Chuẩn (10 Mìn) - BFS", "rows": 9, "cols": 9, "mines": 10, "algo": "BFS"},
        {"name": "9x9 Chuẩn (10 Mìn) - DFS", "rows": 9, "cols": 9, "mines": 10, "algo": "DFS"},
    ]

    results_summary = []

    print(f"{'='*60}")
    print(f"BẮT ĐẦU CHẠY THỰC NGHIỆM AI MINESWEEPER ({num_games} VÁN MỖI CẤU HÌNH)")
    print(f"{'='*60}")

    for cfg in configs:
        wins = 0
        total_moves = 0
        total_guesses = 0
        total_time = 0

        for _ in range(num_games):
            res = run_single_simulation(cfg["rows"], cfg["cols"], cfg["mines"], cfg["algo"])
            if res["won"]:
                wins += 1
            total_moves += res["moves"]
            total_guesses += res["guesses"]
            total_time += res["time_ms"]

        win_rate = (wins / num_games) * 100
        avg_moves = total_moves / num_games
        avg_guesses = total_guesses / num_games
        avg_time = total_time / num_games

        summary = {
            "name": cfg["name"],
            "win_rate": win_rate,
            "avg_moves": avg_moves,
            "avg_guesses": avg_guesses,
            "avg_time_ms": avg_time,
            "algo": cfg["algo"]
        }
        results_summary.append(summary)

        print(f"[-] {cfg['name']}: Win Rate = {win_rate:.1f}%, Nước đi TB = {avg_moves:.1f}, "
              f"Lần đoán TB = {avg_guesses:.2f}, Thời gian TB = {avg_time:.2f} ms")

    print(f"{'='*60}\n")
    return results_summary


if __name__ == "__main__":
    run_benchmark(100)
