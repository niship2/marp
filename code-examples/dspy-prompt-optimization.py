"""
DSPy によるプロンプトの自動最適化
ナルト口調変換の例
"""

import dspy
from dspy.teleprompt import COPRO, GEPA

# 1. モデルの作成
class NarutoTransform(dspy.Signature):
    """丁寧な文をナルト口調に変換する"""
    polite_sentence: str = dspy.InputField()
    rationale: str = dspy.OutputField(desc="変換の意図やねらいの説明")
    transformed: str = dspy.OutputField(desc="ナルト口調に書き換えた文")

# チェーンの作成
make_naruto_chain = dspy.ChainOfThought(NarutoTransform)

# 2. 最適化前の出力
polite_sentence = "今日の会議では議論を丁寧にまとめます。"
response = make_naruto_chain(polite_sentence=polite_sentence)
print(f'生成推論: {response.rationale}')
print(f'生成出力: {response.transformed}')

# 3. 教師データ相当の作成
# 訓練データの準備
trainset = [
    dspy.Example(
        polite_sentence="会議の議事録を作成します。",
        rationale="ナルトの特徴的なフレーズ「ってばよ」を活用し、親しみやすい表現に変換",
        transformed="会議の議事録を作るってばよ！"
    ),
    # 複数の例を追加...
]

# 4. 評価指標の設定
def naruto_quality_score(example, pred, trace=None):
    # ナルトらしさを評価する指標
    score = 0
    if "ってばよ" in pred.transformed:
        score += 1
    if "オレ" in pred.transformed or "おれ" in pred.transformed:
        score += 1
    # その他の評価基準...
    return score

# 5. COPRO（Collaborative Prompt Optimization）
# COPROによる最適化
copro_optimizer = COPRO(
    metric=naruto_quality_score,
    breadth=10,
    depth=3,
    init_temperature=1.0
)

copro_compiled = copro_optimizer.compile(
    student=make_naruto_chain,
    trainset=trainset
)

# 6. GEPA（Genetic Evolution for Prompt Adaptation）
# GEPAによる最適化
gepa_optimizer = GEPA(
    metric=naruto_quality_score,
    num_candidates=20,
    init_temperature=1.0
)

gepa_compiled = gepa_optimizer.compile(
    student=make_naruto_chain,
    trainset=trainset
)

