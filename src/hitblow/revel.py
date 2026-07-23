"""ゲームの難易度（桁数）を判定・選択する機能。"""


def validate_digits(choice, default_digits=3):
    """入力された値（文字列や数値）から桁数（3 または 4）を決定する純粋関数。
    
    GUI・CUIの両方から共通で呼び出して利用できる。
    """
    if str(choice).strip() == "4":
        return 4
    return default_digits


def select_difficulty(default_digits=3):
    """【CUI用】ターミナルから難易度（3桁または4桁）を入力させて返す。"""
    choice = input(
        "難易度を選んでください（3桁: 3 / 4桁: 4）"
        f"[Enterで{default_digits}桁] > "
    )
    return validate_digits(choice, default_digits)