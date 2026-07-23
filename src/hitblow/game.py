"""ゲームの進行（入力・表示・ループ）。

★ チームで足す機能は **自分の担当の場所**に書く（1機能=1ファイル）。
   下の「ここに足す」場所は3か所（① 開始時 ② 入力コマンド ③ 勝利時）。
   ペアごとに**別の場所**を直すので、並行作業でも衝突しない。
   import も自分の場所の近くに書くこと（ファイル先頭にまとめない＝衝突回避）。
"""

from .core import judge, make_secret
from .revel import select_difficulty
from .sound import play_result_sound

def play(digits=3):
    # ===== ① 開始時に足す（難易度・あいさつ など）: ここに書く =====
    print("=== Hit & Blow ===")
    print("プレイモードを選択してください")
    mode = input("1: ターミナルで遊ぶ / 2: GUIで遊ぶ [Enterで1] > ").strip()

    if mode == "2":
        from .gui import start_gui
        start_gui()
        return  # GUIが閉じたらターミナルの処理に進まず終了

    # --- 以下、従来のターミナル版の処理（そのまま） ---
    digits = select_difficulty(digits)
    secret = make_secret(digits)
    print(f"Hit & Blow（{digits} 桁・重複なし）")

    tries = 0
    while True:
        guess = input("予想 > ").strip()

        # ===== ② 入力コマンドに足す（ヒント など）: ここに書く（import もここに） =====
        # 例:  from .hint import hint
        #      if guess == "h":
        #          print(hint(secret)); continue

        if len(guess) != digits or not guess.isdigit():
            print(f"{digits} 桁の数字で入力してね")
            continue
        tries += 1
        hit, blow = judge(secret, guess)
        play_result_sound(hit, blow)
        print(f"  Hit={hit}  Blow={blow}")
        if hit == digits:

            # ===== ③ 勝利時に足す（スコア・履歴 など）: ここに書く =====
            from .score import show_score
            show_score(tries, digits)

            print(f"正解！ {tries} 回で当たり（答え {secret}）")
            break