import sys
import io
import tkinter as tk
from tkinter import messagebox

from .core import judge, make_secret
from .revel import validate_digits  # ★ CUI用の入力処理を避けて共通ロジックをインポート
from .sound import play_result_sound
from .score import show_score


class HitAndBlowGUI:
    def __init__(self, root):
        self.root = root

        # ウィンドウ設定
        self.root.title("Hit & Blow")
        self.root.geometry("380x520")
        self.root.resizable(False, False)

        # 桁数選択用変数
        self.difficulty_choice = tk.StringVar(value="3")
        
        # ★ revel.py の validate_digits を通して桁数を判定・決定
        self.digits = validate_digits(self.difficulty_choice.get())
        
        # core.py で問題を作成
        self.secret = make_secret(self.digits)
        self.tries = 0

        # 1. タイトル
        self.title_label = tk.Label(
            root, text="Hit & Blow", font=("Helvetica", 16, "bold")
        )
        self.title_label.pack(pady=(10, 2))

        # 2. 桁数選択エリア
        difficulty_frame = tk.Frame(root)
        difficulty_frame.pack(pady=5)

        tk.Label(
            difficulty_frame, text="桁数選択:", font=("Helvetica", 10)
        ).pack(side=tk.LEFT, padx=5)

        self.radio_3 = tk.Radiobutton(
            difficulty_frame,
            text="3桁",
            value="3",
            variable=self.difficulty_choice,
            command=self.change_difficulty,
        )
        self.radio_3.pack(side=tk.LEFT, padx=5)

        self.radio_4 = tk.Radiobutton(
            difficulty_frame,
            text="4桁",
            value="4",
            variable=self.difficulty_choice,
            command=self.change_difficulty,
        )
        self.radio_4.pack(side=tk.LEFT, padx=5)

        # 3. 入力エリア
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="予想:", font=("Helvetica", 12)).pack(
            side=tk.LEFT, padx=5
        )

        self.entry = tk.Entry(
            input_frame, font=("Helvetica", 14), width=10, justify="center"
        )
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.focus()

        # Enterキーで判定実行
        self.entry.bind("<Return>", lambda event: self.check_guess())

        self.btn_submit = tk.Button(
            input_frame,
            text="判定",
            font=("Helvetica", 10),
            command=self.check_guess,
        )
        self.btn_submit.pack(side=tk.LEFT, padx=5)

        # 4. 履歴表示エリア
        self.history_list = tk.Listbox(
            root, font=("Courier", 11), width=38, height=13
        )
        self.history_list.pack(pady=10)

        # 5. リセットボタン
        self.btn_reset = tk.Button(
            root, text="リセットして新しいゲーム開始", command=self.reset_game
        )
        self.btn_reset.pack(pady=5)

    def change_difficulty(self):
        """桁数が変更されたとき"""
        # ★ revel.py の共通ロジックに選択値を渡す
        self.digits = validate_digits(self.difficulty_choice.get())
        self.reset_game()

    def check_guess(self):
        guess = self.entry.get().strip()

        # 入力チェック
        if len(guess) != self.digits or not guess.isdigit():
            messagebox.showwarning(
                "入力エラー", f"{self.digits}桁の数字で入力してください。"
            )
            return

        if len(set(guess)) != self.digits:
            messagebox.showwarning(
                "入力エラー", "数字に重複がないように入力してください。"
            )
            return

        self.tries += 1
        
        # 判定＆効果音
        hit, blow = judge(self.secret, guess)
        try:
            play_result_sound(hit, blow)
        except Exception:
            pass

        # 履歴追加
        result_str = (
            f" [{self.tries:2d}回目]  {guess}  ->  {hit} Hit / {blow} Blow"
        )
        self.history_list.insert(tk.END, result_str)
        self.history_list.see(tk.END)

        self.entry.delete(0, tk.END)

        # 勝利判定
        if hit == self.digits:
            score_text = self._capture_show_score(self.tries, self.digits)
            messagebox.showinfo("🎉 クリア！", score_text)

            self.entry.config(state="disabled")
            self.btn_submit.config(state="disabled")

    def _capture_show_score(self, tries, digits):
        buffer = io.StringIO()
        stdout_bak = sys.stdout
        try:
            sys.stdout = buffer
            show_score(tries, digits)
        finally:
            sys.stdout = stdout_bak
        return buffer.getvalue().strip()

    def reset_game(self):
        self.secret = make_secret(self.digits)
        self.tries = 0
        self.history_list.delete(0, tk.END)

        self.entry.config(state="normal")
        self.btn_submit.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()


def start_gui():
    root = tk.Tk()
    app = HitAndBlowGUI(root)
    root.mainloop()