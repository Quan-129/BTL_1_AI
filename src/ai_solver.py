"""
ai_solver.py - Comprehensive AI Agent and Heuristics for Minesweeper.
Author: Group Students (CO3061) - HCMUT
Course: Introduction to Artificial Intelligence (CO3061) - HCMUT

This module answers the core assignment question:
"What heuristics could be used in the game?"

It implements:
1. Deterministic Single-Point Deduction (Rule-based).
2. Set-based / CSP Frontier Deduction (Subset reduction).
3. Minimum Mine Probability Heuristic: h_prob(cell) = P(cell is mine).
4. Information Gain Tie-breaking Heuristic.
"""

from typing import List, Tuple, Dict, Set, Optional
from game_logic import MinesweeperGame


class Move:
    """Represents an AI action."""
    REVEAL = "REVEAL"
    FLAG = "FLAG"
    GUESS = "GUESS"

    def __init__(self, action: str, row: int, col: int, reason: str, probability: float = 0.0):
        self.action = action
        self.row = row
        self.col = col
        self.reason = reason
        self.probability = probability  # Probability that this cell is a mine (0.0 = safe, 1.0 = mine)

    def __repr__(self):
        return f"Move({self.action} at ({self.row}, {self.col}), P(mine)={self.probability:.1%}, Reason='{self.reason}')"


class MinesweeperAI:
    """Intelligent agent capable of step-by-step solving and heuristic evaluation."""
    def __init__(self, game: MinesweeperGame):
        self.game = game

    def get_cell_frontier_info(self):
        """
        Analyzes the current board to extract:
        - revealed_numbered: List of (r, c) with value > 0 and at least one unrevealed neighbor.
        - unrevealed_neighbors: Dict mapping (r, c) -> Set of (nr, nc) unrevealed, unflagged neighbors.
        - remaining_mines_needed: Dict mapping (r, c) -> int (value - flagged neighbors).
        - all_frontier_cells: Set of unrevealed cells adjacent to at least one revealed number.
        - all_isolated_cells: Set of unrevealed cells not adjacent to any revealed number.
        """
        revealed_numbered = []
        unrevealed_neighbors: Dict[Tuple[int, int], Set[Tuple[int, int]]] = {}
        remaining_mines_needed: Dict[Tuple[int, int], int] = {}
        all_frontier_cells: Set[Tuple[int, int]] = set()

        for r in range(self.game.rows):
            for c in range(self.game.cols):
                cell = self.game.board[r][c]
                if cell.is_revealed and cell.neighbor_mines > 0:
                    nbrs = self.game.get_neighbors(r, c)
                    flagged = {n for n in nbrs if self.game.board[n[0]][n[1]].is_flagged}
                    unrev = {n for n in nbrs if not self.game.board[n[0]][n[1]].is_revealed and not self.game.board[n[0]][n[1]].is_flagged}
                    
                    needed = cell.neighbor_mines - len(flagged)
                    if unrev:
                        revealed_numbered.append((r, c))
                        unrevealed_neighbors[(r, c)] = unrev
                        remaining_mines_needed[(r, c)] = needed
                        all_frontier_cells.update(unrev)

        all_unrevealed = {
            (r, c) for r in range(self.game.rows) for c in range(self.game.cols)
            if not self.game.board[r][c].is_revealed and not self.game.board[r][c].is_flagged
        }
        all_isolated_cells = all_unrevealed - all_frontier_cells

        return revealed_numbered, unrevealed_neighbors, remaining_mines_needed, all_frontier_cells, all_isolated_cells

    def find_deterministic_move(self) -> Optional[Move]:
        """
        Tier 1: Single-Point Deterministic Logic.
        - If remaining needed mines == count(unrevealed neighbors): ALL ARE MINES -> FLAG.
        - If remaining needed mines == 0: ALL ARE SAFE -> REVEAL.
        """
        rev_numbered, unrev_nbrs, needed_dict, _, _ = self.get_cell_frontier_info()

        # Check for safe moves first
        for (r, c) in rev_numbered:
            needed = needed_dict[(r, c)]
            unrev = unrev_nbrs[(r, c)]
            if needed == 0 and len(unrev) > 0:
                target = next(iter(unrev))
                return Move(
                    action=Move.REVEAL,
                    row=target[0],
                    col=target[1],
                    reason=f"Suy luận chắc chắn: Ô ({r}, {c}) đã có đủ cờ, các ô quanh nó an toàn 100%.",
                    probability=0.0
                )

        # Check for confirmed mines
        for (r, c) in rev_numbered:
            needed = needed_dict[(r, c)]
            unrev = unrev_nbrs[(r, c)]
            if needed == len(unrev) and len(unrev) > 0:
                target = next(iter(unrev))
                return Move(
                    action=Move.FLAG,
                    row=target[0],
                    col=target[1],
                    reason=f"Suy luận chắc chắn: Ô ({r}, {c}) thiếu {needed} mìn và chỉ còn đúng {len(unrev)} ô chưa mở $\\rightarrow$ Là mìn 100%.",
                    probability=1.0
                )

        return None

    def find_subset_csp_move(self) -> Optional[Move]:
        """
        Tier 2: Constraint Satisfaction Problem (CSP) / Subset Frontier Reduction.
        Examines pairs of adjacent revealed numbered cells (A, B).
        If unrevealed neighbors of A are a subset of unrevealed neighbors of B:
        - diff = unrev(B) - unrev(A)
        - diff_mines = needed(B) - needed(A)
        - If diff_mines == 0: diff cells are SAFE.
        - If diff_mines == len(diff): diff cells are MINES.
        """
        rev_numbered, unrev_nbrs, needed_dict, _, _ = self.get_cell_frontier_info()

        for i in range(len(rev_numbered)):
            for j in range(len(rev_numbered)):
                if i == j:
                    continue
                cell_a = rev_numbered[i]
                cell_b = rev_numbered[j]
                
                unrev_a = unrev_nbrs[cell_a]
                unrev_b = unrev_nbrs[cell_b]
                needed_a = needed_dict[cell_a]
                needed_b = needed_dict[cell_b]

                if unrev_a.issubset(unrev_b) and len(unrev_a) < len(unrev_b):
                    diff = unrev_b - unrev_a
                    diff_mines = needed_b - needed_a

                    if diff_mines == 0:
                        target = next(iter(diff))
                        return Move(
                            action=Move.REVEAL,
                            row=target[0],
                            col=target[1],
                            reason=f"Suy luận tập hợp CSP: Ô ({cell_b[0]}, {cell_b[1]}) chứa tập con ô ({cell_a[0]}, {cell_a[1]}), phần bù an toàn 100%.",
                            probability=0.0
                        )
                    elif diff_mines == len(diff):
                        target = next(iter(diff))
                        return Move(
                            action=Move.FLAG,
                            row=target[0],
                            col=target[1],
                            reason=f"Suy luận tập hợp CSP: Ô ({cell_b[0]}, {cell_b[1]}) chứa tập con ô ({cell_a[0]}, {cell_a[1]}), phần bù là mìn 100%.",
                            probability=1.0
                        )

        return None

    def find_heuristic_guess_move(self) -> Optional[Move]:
        """
        Tier 3: Probabilistic Heuristic Evaluation.
        Used when all deductive logic fails (e.g. 50-50 situations or game opening).
        
        Calculates:
        1. Local mine probability for each frontier cell:
           P_local(u) = max_{k in neighbors(u)} (needed(k) / count(unrev(k)))
        2. Global density for isolated cells:
           P_isolated = remaining_mines / remaining_unrevealed
        3. Information Gain Tie-breaker:
           Prefers cells with higher number of unrevealed neighbors to uncover more clues.
        """
        rev_numbered, unrev_nbrs, needed_dict, frontier_cells, isolated_cells = self.get_cell_frontier_info()

        # First move of the game: Pick center or corner
        if self.game.first_click:
            center_r, center_c = self.game.rows // 2, self.game.cols // 2
            return Move(
                action=Move.REVEAL,
                row=center_r,
                col=center_c,
                reason="Nước đi khởi đầu (First Move Heuristic): Mở ô trung tâm để tối đa hóa khả năng mở rộng bàn cờ.",
                probability=0.0
            )

        cell_probabilities: Dict[Tuple[int, int], float] = {}

        # 1. Evaluate Frontier Cells
        for u in frontier_cells:
            # Estimate probability using conservative upper-bound of adjacent constraints
            max_p = 0.0
            for (r, c), unrev in unrev_nbrs.items():
                if u in unrev and len(unrev) > 0:
                    local_p = max(0.0, min(1.0, needed_dict[(r, c)] / len(unrev)))
                    if local_p > max_p:
                        max_p = local_p
            cell_probabilities[u] = max_p

        # 2. Evaluate Isolated Cells
        all_unrev_count = len(frontier_cells) + len(isolated_cells)
        remaining_mines = max(0, self.game.get_remaining_mines())
        
        if isolated_cells and all_unrev_count > 0:
            # Estimate how many mines are accounted for in the frontier
            est_frontier_mines = sum(cell_probabilities.values()) if cell_probabilities else 0
            remaining_for_isolated = max(0.0, remaining_mines - est_frontier_mines)
            p_isolated = min(1.0, remaining_for_isolated / len(isolated_cells)) if len(isolated_cells) > 0 else 1.0
            for u in isolated_cells:
                cell_probabilities[u] = p_isolated

        if not cell_probabilities:
            # Fallback if no unrevealed cells left
            return None

        # Sort candidate cells by minimum probability (safest first)
        min_p = min(cell_probabilities.values())
        candidates = [cell for cell, p in cell_probabilities.items() if abs(p - min_p) < 1e-5]

        # Tie-breaker: Information Gain Heuristic (Maximize unexplored neighbors)
        best_candidate = candidates[0]
        max_info_gain = -1

        for c in candidates:
            info_gain = sum(
                1 for nr, nc in self.game.get_neighbors(c[0], c[1])
                if not self.game.board[nr][nc].is_revealed and not self.game.board[nr][nc].is_flagged
            )
            if info_gain > max_info_gain:
                max_info_gain = info_gain
                best_candidate = c

        return Move(
            action=Move.REVEAL,
            row=best_candidate[0],
            col=best_candidate[1],
            reason=f"Heuristic Xác Suất: Ô ({best_candidate[0]}, {best_candidate[1]}) có xác suất mìn thấp nhất ({min_p:.1%}) và độ lợi thông tin cao nhất ({max_info_gain} lân cận).",
            probability=min_p
        )

    def get_next_move(self) -> Optional[Move]:
        """
        Determines the single best move using the hierarchical AI strategy:
        1. Deterministic Rule-based.
        2. Set-based CSP Deduction.
        3. Probabilistic & Information Gain Heuristic.
        """
        if self.game.game_over:
            return None

        # Tier 1
        move = self.find_deterministic_move()
        if move:
            return move

        # Tier 2
        move = self.find_subset_csp_move()
        if move:
            return move

        # Tier 3
        return self.find_heuristic_guess_move()

    def execute_move(self, move: Move) -> bool:
        """Executes the given Move on the game board."""
        if move.action == Move.FLAG:
            return self.game.toggle_flag(move.row, move.col)
        elif move.action in (Move.REVEAL, Move.GUESS):
            return self.game.reveal_cell(move.row, move.col)
        return False
