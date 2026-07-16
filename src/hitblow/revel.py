"""ゲームの難易度を選択する機能。"""


def select_difficulty(default_digits=3):
    """3桁または4桁を選び、選択した桁数を返す。"""
    choice = input(
        "難易度を選んでください（3桁: 3 / 4桁: 4）"
        f"[Enterで{default_digits}桁] > "
    ).strip()

    if choice == "4":
        return 4

    return 3