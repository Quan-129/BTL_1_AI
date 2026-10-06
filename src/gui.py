"""
gui.py - Graphical User Interface for Minesweeper with AI and Algorithm Visualizer.
Author: Group Students (CO3061) - HCMUT
Course: Introduction to Artificial Intelligence (CO3061) - HCMUT
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
from game_logic import MinesweeperGame
from ai_solver import MinesweeperAI, Move


class MinesweeperGUI:
    """Tkinter-based GUI for Minesweeper supporting custom sizes, BFS/DFS, and AI solver."""

    COLOR_MAP = {
        1: "#1976D2",  # Blue
        2: "#388E3C",  # Green
        3: "#D32F2F",  # Red
        4: "#512DA8",  # Purple
        5: "#C2185B",  # Maroon
        6: "#0097A7",  # Teal
        7: "#212121",  # Dark
        8: "#616161",  # Gray
    }

    BG_UNREVEALED = "#E0E0E0"
    BG_REVEALED = "#FFFFFF"
    BG_MINE_EXPLODED = "#FFCDD2"
    BG_HINT = "#C8E6C9"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("HCMUT - Minesweeper AI (CO3061) | BTL 1")
        self.root.resizable(False, False)

        # Game state configuration
        self.current_rows = 9
        self.current_cols = 9
        self.current_mines = 10
        self.flood_algo_var = tk.StringVar(value="BFS")
        
        self.game = MinesweeperGame(self.current_rows, self.current_cols, self.current_mines, self.flood_algo_var.get())
        self.ai = MinesweeperAI(self.game)

        # AI autoplay controls
        self.is_auto_playing = False
        self.auto_play_delay_ms = 180  # Delay between AI moves in milliseconds
        self.hint_cells = []

        # Setup GUI Components
        self._setup_styles()
        self._build_menu()
        self._build_header()
        self._build_control_panel()
        self._build_board()
        self._build_status_bar()
        self._adjust_window_size()

        # Timer loop
        self._update_timer()

    def _setup_styles(self):
        """Sets up ttk styles for clean aesthetics."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"))
        style.configure("Counter.TLabel", font=("Consolas", 14, "bold"), foreground="#D32F2F")
        style.configure("Status.TLabel", font=("Segoe UI", 9))
        style.configure("Action.TButton", font=("Segoe UI", 9, "bold"))

    def _build_menu(self):
        """Creates top menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Game Menu
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="5x5 Mini (3 Mìn)", command=lambda: self.change_difficulty(5, 5, 3))
        game_menu.add_command(label="9x9 Chuẩn (10 Mìn)", command=lambda: self.change_difficulty(9, 9, 10))
        game_menu.add_command(label="16x16 Trung cấp (40 Mìn)", command=lambda: self.change_difficulty(16, 16, 40))
        game_menu.add_separator()
        game_menu.add_command(label="Tùy chỉnh kích thước...", command=self._open_custom_dialog)
        game_menu.add_separator()
        game_menu.add_command(label="Ván mới (F2)", command=self.restart_game)
        game_menu.add_command(label="Thoát", command=self.root.quit)
        menubar.add_cascade(label="Trò chơi", menu=game_menu)

        # Algorithm Menu
        algo_menu = tk.Menu(menubar, tearoff=0)
        algo_menu.add_radiobutton(label="BFS (Breadth-First Search)", variable=self.flood_algo_var, value="BFS", command=self._on_algo_change)
        algo_menu.add_radiobutton(label="DFS (Depth-First Search)", variable=self.flood_algo_var, value="DFS", command=self._on_algo_change)
        menubar.add_cascade(label="Thuật toán loang", menu=algo_menu)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Thông tin nhóm BTL", command=self._show_about)
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)

        self.root.bind("<F2>", lambda e: self.restart_game())

    def _build_header(self):
        """Creates top LCD-style header with mine counter, smiley face, and timer."""
        header_frame = tk.Frame(self.root, bg="#263238", pady=6, padx=10)
        header_frame.pack(fill=tk.X)

        # Mine counter (LCD style)
        self.lbl_mines = tk.Label(
            header_frame, text=f"🚩 {self.game.get_remaining_mines():03d}",
            font=("Consolas", 15, "bold"), fg="#FF5252", bg="#1E1E1E", width=8, relief=tk.SUNKEN, bd=2
        )
        self.lbl_mines.pack(side=tk.LEFT, padx=5)

        # Smiley restart button
        self.btn_smiley = tk.Button(
            header_frame, text="😊", font=("Segoe UI Emoji", 14), width=3,
            command=self.restart_game, relief=tk.RAISED, bd=2, bg="#ECEFF1", cursor="hand2"
        )
        self.btn_smiley.pack(side=tk.LEFT, expand=True)

        # Timer (LCD style)
        self.lbl_timer = tk.Label(
            header_frame, text="⏱️ 000",
            font=("Consolas", 15, "bold"), fg="#69F0AE", bg="#1E1E1E", width=8, relief=tk.SUNKEN, bd=2
        )
        self.lbl_timer.pack(side=tk.RIGHT, padx=5)

    def _build_control_panel(self):
        """Creates toolbar for AI actions and Algorithm selection."""
        ctrl_frame = tk.Frame(self.root, bg="#ECEFF1", pady=6, padx=8)
        ctrl_frame.pack(fill=tk.X)

        # Preset difficulty buttons
        preset_frame = tk.Frame(ctrl_frame, bg="#ECEFF1")
        preset_frame.pack(side=tk.TOP, fill=tk.X, pady=2)

        tk.Button(preset_frame, text="5x5 Mini", font=("Segoe UI", 8), bg="#CFD8DC", command=lambda: self.change_difficulty(5, 5, 3)).pack(side=tk.LEFT, padx=2)
        tk.Button(preset_frame, text="9x9 Chuẩn", font=("Segoe UI", 8), bg="#CFD8DC", command=lambda: self.change_difficulty(9, 9, 10)).pack(side=tk.LEFT, padx=2)
        tk.Button(preset_frame, text="16x16", font=("Segoe UI", 8), bg="#CFD8DC", command=lambda: self.change_difficulty(16, 16, 40)).pack(side=tk.LEFT, padx=2)

        # Algorithm selection label
        tk.Label(preset_frame, text=" | Loang:", font=("Segoe UI", 8, "bold"), bg="#ECEFF1").pack(side=tk.LEFT, padx=2)
        rb_bfs = tk.Radiobutton(preset_frame, text="BFS", variable=self.flood_algo_var, value="BFS", bg="#ECEFF1", command=self._on_algo_change, font=("Segoe UI", 8))
        rb_bfs.pack(side=tk.LEFT)
        rb_dfs = tk.Radiobutton(preset_frame, text="DFS", variable=self.flood_algo_var, value="DFS", bg="#ECEFF1", command=self._on_algo_change, font=("Segoe UI", 8))
        rb_dfs.pack(side=tk.LEFT)

        # AI Action Buttons
        ai_frame = tk.Frame(ctrl_frame, bg="#ECEFF1")
        ai_frame.pack(side=tk.TOP, fill=tk.X, pady=4)

        self.btn_hint = tk.Button(ai_frame, text="💡 Gợi ý AI", bg="#E8F5E9", fg="#2E7D32", font=("Segoe UI", 8, "bold"), command=self.give_ai_hint, cursor="hand2")
        self.btn_hint.pack(side=tk.LEFT, padx=3)

        self.btn_step = tk.Button(ai_frame, text="⚡ AI Đi 1 Bước", bg="#E1F5FE", fg="#0277BD", font=("Segoe UI", 8, "bold"), command=self.step_ai, cursor="hand2")
        self.btn_step.pack(side=tk.LEFT, padx=3)

        self.btn_autoplay = tk.Button(ai_frame, text="🤖 AI Tự Giải", bg="#EDE7F6", fg="#512DA8", font=("Segoe UI", 8, "bold"), command=self.toggle_autoplay, cursor="hand2")
        self.btn_autoplay.pack(side=tk.LEFT, padx=3)

    def _build_board(self):
        """Constructs the grid of buttons representing the Minesweeper board."""
        if hasattr(self, "board_frame"):
            self.board_frame.destroy()

        self.board_frame = tk.Frame(self.root, bg="#B0BEC5", padx=6, pady=6, bd=3, relief=tk.SUNKEN)
        self.board_frame.pack()

        # Fix row and column dimensions so individual cell states never scale or twitch the grid
        for r in range(self.current_rows):
            self.board_frame.grid_rowconfigure(r, uniform="cell")
        for c in range(self.current_cols):
            self.board_frame.grid_columnconfigure(c, uniform="cell")

        self.buttons = []
        cell_size = 28 if self.current_cols <= 9 else 24

        for r in range(self.current_rows):
            row_btns = []
            for c in range(self.current_cols):
                btn = tk.Button(
                    self.board_frame, text="", width=2, height=1, font=("Segoe UI", 10, "bold"),
                    bg=self.BG_UNREVEALED, relief=tk.RAISED, bd=2, cursor="hand2"
                )
                btn.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                btn.bind("<Button-1>", lambda event, row=r, col=c: self._on_left_click(row, col))
                btn.bind("<Button-3>", lambda event, row=r, col=c: self._on_right_click(row, col))
                row_btns.append(btn)
            self.buttons.append(row_btns)

    def _build_status_bar(self):
        """Builds bottom status message bar with fixed height and text wrapping."""
        self.status_bar = tk.Label(
            self.root, text="Sẵn sàng! Click chuột trái để mở ô, click chuột phải để cắm cờ.",
            font=("Segoe UI", 9), bd=1, relief=tk.SUNKEN, anchor=tk.W, justify=tk.LEFT,
            padx=8, pady=4, bg="#ECEFF1", height=3
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _adjust_window_size(self):
        """Adjusts and locks window geometry based on current board size, preventing text jitter."""
        self.root.geometry("")
        self.root.update_idletasks()
        w = max(390, self.root.winfo_reqwidth())
        self.status_bar.config(wraplength=w - 16, height=3)
        self.root.update_idletasks()
        h = self.root.winfo_reqheight()
        self.root.geometry(f"{w}x{h}")

    def _on_algo_change(self):
        """Updates flood algorithm on change."""
        algo = self.flood_algo_var.get()
        self.game.flood_algorithm = algo
        self.set_status(f"Đã chuyển thuật toán loang sang: {algo}")

    def _on_left_click(self, r: int, c: int):
        """Handles human left-click (reveal)."""
        if self.is_auto_playing:
            self.toggle_autoplay()  # Stop autoplay if user manually clicks

        self._clear_hints()
        success = self.game.reveal_cell(r, c)
        self._update_board_display()

        if not success:
            self.btn_smiley.config(text="😵")
            self.set_status(f"💥 Bạn đã đạp trúng mìn tại ô ({r}, {c})! Trò chơi kết thúc.")
        elif self.game.won:
            self.btn_smiley.config(text="😎")
            self.set_status(f"🎉 CHIẾN THẮNG! Toàn bộ mìn đã được gỡ trong {self.game.get_elapsed_time()} giây.")
        else:
            revealed_cnt = len(self.game.last_flood_revealed)
            if revealed_cnt > 1:
                self.set_status(f"[{self.game.last_algorithm_used} Flood Fill] Đã loang mở {revealed_cnt} ô trống.")
            else:
                self.set_status(f"Đã mở ô ({r}, {c}).")

    def _on_right_click(self, r: int, c: int):
        """Handles human right-click (flag)."""
        if self.is_auto_playing:
            return

        self._clear_hints()
        self.game.toggle_flag(r, c)
        self._update_board_display()
        self.set_status(f"Đã đổi cờ tại ô ({r}, {c}). Số mìn còn lại: {self.game.get_remaining_mines()}")

    def _update_board_display(self):
        """Refreshes button states, colors, and LCD numbers."""
        self.lbl_mines.config(text=f"🚩 {max(0, self.game.get_remaining_mines()):03d}")

        for r in range(self.current_rows):
            for c in range(self.current_cols):
                btn = self.buttons[r][c]
                cell = self.game.board[r][c]

                if cell.is_revealed:
                    btn.config(relief=tk.SUNKEN, bd=2)
                    if cell.is_mine:
                        btn.config(text="💣", bg=self.BG_MINE_EXPLODED, fg="#B71C1C")
                    elif cell.neighbor_mines > 0:
                        btn.config(
                            text=str(cell.neighbor_mines),
                            bg=self.BG_REVEALED,
                            fg=self.COLOR_MAP.get(cell.neighbor_mines, "#000000")
                        )
                    else:
                        btn.config(text="", bg=self.BG_REVEALED)
                elif cell.is_flagged:
                    btn.config(text="🚩", bg=self.BG_UNREVEALED, fg="#D32F2F", relief=tk.RAISED, bd=2)
                else:
                    if (r, c) not in self.hint_cells:
                        btn.config(text="", bg=self.BG_UNREVEALED, relief=tk.RAISED, bd=2)

    def _clear_hints(self):
        """Clears highlighted hint cells."""
        for r, c in self.hint_cells:
            if not self.game.board[r][c].is_revealed and not self.game.board[r][c].is_flagged:
                self.buttons[r][c].config(bg=self.BG_UNREVEALED)
        self.hint_cells.clear()

    def give_ai_hint(self):
        """Calculates and visually highlights the best next move with reasoning."""
        if self.game.game_over:
            return

        self._clear_hints()
        self.btn_smiley.config(text="🤔")
        move = self.ai.get_next_move()
        self.btn_smiley.config(text="😊")

        if not move:
            self.set_status("Không còn nước đi nào khả dụng.")
            return

        # Highlight cell
        self.hint_cells.append((move.row, move.col))
        btn = self.buttons[move.row][move.col]
        btn.config(bg=self.BG_HINT)

        action_text = "Cắm cờ" if move.action == Move.FLAG else "Mở ô"
        self.set_status(f"[💡 GỢI Ý] {action_text} ({move.row}, {move.col}) (P={move.probability:.0%}): {move.reason}")

    def step_ai(self):
        """Executes a single step calculated by the AI."""
        if self.game.game_over:
            return

        self._clear_hints()
        self.btn_smiley.config(text="🤔")
        move = self.ai.get_next_move()
        self.btn_smiley.config(text="😊")

        if not move:
            return

        self.ai.execute_move(move)
        self._update_board_display()

        if self.game.game_over:
            if self.game.won:
                self.btn_smiley.config(text="😎")
                self.set_status(f"🎉 CHIẾN THẮNG! AI đã hoàn thành bàn cờ trong {self.game.get_elapsed_time()} giây.")
            else:
                self.btn_smiley.config(text="😵")
                self.set_status(f"💥 AI đoán phải mìn tại ({move.row}, {move.col}) do tình huống xác suất.")
        else:
            action_text = "Cắm cờ" if move.action == Move.FLAG else "Mở ô"
            self.set_status(f"[🤖 AI Step] {action_text} ({move.row}, {move.col}) | {move.reason}")

    def toggle_autoplay(self):
        """Starts or pauses the continuous AI autoplay."""
        if self.is_auto_playing:
            self.is_auto_playing = False
            self.btn_autoplay.config(text="🤖 AI Tự Giải", bg="#EDE7F6")
            self.set_status("Đã tạm dừng AI tự giải.")
        else:
            if self.game.game_over:
                self.restart_game()
            self.is_auto_playing = True
            self.btn_autoplay.config(text="⏸️ Dừng AI", bg="#FFCDD2")
            self.set_status("Đang chạy AI tự giải liên tục...")
            self._run_autoplay_step()

    def _run_autoplay_step(self):
        """Recursively triggers autoplay moves with timer delay."""
        if not self.is_auto_playing or self.game.game_over:
            self.is_auto_playing = False
            self.btn_autoplay.config(text="🤖 AI Tự Giải", bg="#EDE7F6")
            return

        self.step_ai()

        if not self.game.game_over and self.is_auto_playing:
            self.root.after(self.auto_play_delay_ms, self._run_autoplay_step)
        else:
            self.is_auto_playing = False
            self.btn_autoplay.config(text="🤖 AI Tự Giải", bg="#EDE7F6")

    def _update_timer(self):
        """Updates elapsed timer display every second."""
        if not self.game.game_over and not self.game.first_click:
            self.lbl_timer.config(text=f"⏱️ {self.game.get_elapsed_time():03d}")
        self.root.after(1000, self._update_timer)

    def change_difficulty(self, rows: int, cols: int, mines: int):
        """Switches board size and mine count."""
        if self.is_auto_playing:
            self.toggle_autoplay()
        self.current_rows = rows
        self.current_cols = cols
        self.current_mines = mines
        self.restart_game(size_changed=True)

    def restart_game(self, size_changed: bool = False):
        """Resets the current game state."""
        if self.is_auto_playing:
            self.toggle_autoplay()
        self.hint_cells.clear()
        self.btn_smiley.config(text="😊")
        self.game.reset(self.current_rows, self.current_cols, self.current_mines, self.flood_algo_var.get())
        self.lbl_timer.config(text="⏱️ 000")

        old_rows = len(self.buttons) if hasattr(self, "buttons") else 0
        old_cols = len(self.buttons[0]) if old_rows > 0 else 0
        if size_changed or old_rows != self.current_rows or old_cols != self.current_cols:
            self._build_board()
            self._adjust_window_size()
        else:
            for r in range(self.current_rows):
                for c in range(self.current_cols):
                    btn = self.buttons[r][c]
                    btn.config(text="", bg=self.BG_UNREVEALED, fg="#000000", relief=tk.RAISED, bd=2)

        self._update_board_display()
        self.set_status("Ván mới đã sẵn sàng. Chúc bạn chơi vui vẻ!")

    def set_status(self, text: str):
        """Updates status text bar."""
        self.status_bar.config(text=text)

    def _open_custom_dialog(self):
        """Dialog to input custom board parameters."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tùy chỉnh bàn cờ")
        dialog.geometry("260x180")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Số hàng (5 - 30):").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        entry_r = tk.Entry(dialog, width=8)
        entry_r.insert(0, str(self.current_rows))
        entry_r.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Số cột (5 - 30):").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        entry_c = tk.Entry(dialog, width=8)
        entry_c.insert(0, str(self.current_cols))
        entry_c.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Số mìn:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        entry_m = tk.Entry(dialog, width=8)
        entry_m.insert(0, str(self.current_mines))
        entry_m.grid(row=2, column=1, padx=10, pady=5)

        def apply_custom():
            try:
                r = int(entry_r.get())
                c = int(entry_c.get())
                m = int(entry_m.get())
                if not (5 <= r <= 30 and 5 <= c <= 30):
                    messagebox.showerror("Lỗi", "Kích thước bàn cờ phải từ 5 đến 30.")
                    return
                if not (1 <= m < r * c):
                    messagebox.showerror("Lỗi", f"Số mìn phải từ 1 đến {r * c - 1}.")
                    return
                dialog.destroy()
                self.change_difficulty(r, c, m)
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ.")

        tk.Button(dialog, text="Đồng ý", command=apply_custom, bg="#C8E6C9", font=("Segoe UI", 9, "bold")).grid(row=3, column=0, columnspan=2, pady=10)

    def _show_about(self):
        """Displays group and project information dialog."""
        info = (
            "TRƯỜNG ĐH BÁCH KHOA - ĐHQG TP.HCM\n"
            "Khoa Khoa học và Kỹ thuật Máy tính\n"
            "Môn: Nhập môn Trí Tuệ Nhân Tạo (CO3061)\n"
            "GVHD: TS. Nguyễn Quốc Minh\n\n"
            "BÀI TẬP LỚN 1 - TOPIC 1: MINESWEEPER\n\n"
            "Nhóm sinh viên thực hiện:\n"
            "1. Trần Bá Minh Quân - MSSV: 2353015 (Thiết kế GUI & Báo cáo)\n"
            "2. Đặng Thế Lâm Anh - MSSV: 2352027 (Game Logic, BFS/DFS)\n"
            "3. Nguyễn Trần Hoàng Khánh - MSSV: 2352530 (Tối ưu BFS/DFS, Kiểm thử)\n"
            "4. Hồng Chấn Phước - MSSV: 2352963 (Thuật toán Heuristic & AI Solver)\n"
            "5. Hồ Gia Bảo - MSSV: 2352089 (Benchmark tự động & Đánh giá)\n"
        )
        messagebox.showinfo("Thông tin đồ án", info)
