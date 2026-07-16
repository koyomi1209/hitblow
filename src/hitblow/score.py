def show_score(tries, digits):
    """かかった回数と桁数からスコア（点数）を計算して表示する"""
    # 基準となる基礎点（桁数が多いほど高得点）
    base_score = digits * 1000
   
    # かかった回数によるペナルティ（回数が増えるほど点数が引かれる）
    # 1回で当てたらノーペナルティ、増えるごとに100点ずつマイナス（最低100点）
    penalty = (tries - 1) * 100
    final_score = max(100, base_score - penalty)
   
    # スコアに応じたランク評価
    if final_score >= digits * 900:
        rank = "👑 Sランク (神レベルの直感と頭脳！)"
    elif final_score >= digits * 700:
        rank = "✨ Aランク (素晴らしい推理力！)"
    elif final_score >= digits * 500:
        rank = "👍 Bランク (ナイスクリア！)"
    else:
        rank = "🎮 Cランク (クリアおめでとう！次はもっと早く解けるはず！)"
       
    print("-" * 40)
    print(f"🎉 【結果発表】")
    print(f"  ・かかった回数: {tries} 回")
    print(f"  ・最終スコア  : {final_score} 点")
    print(f"  ・プレイヤー評価: {rank}")
    print("-" * 40)