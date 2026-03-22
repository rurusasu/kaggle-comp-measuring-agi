# Measuring Progress Toward AGI - Cognitive Abilities

## Competition Info

- **URL:** https://www.kaggle.com/competitions/kaggle-measuring-agi
- **Deadline:** 2026-04-16 23:59 UTC
- **Prize:** $200,000
- **Category:** Featured
- **Organizer:** Google DeepMind

## Task

AIシステムの認知能力を評価するベンチマークを設計する。以下5つの認知能力トラックから選択:
1. **Learning** — 新しい情報の内在化と適用
2. **Metacognition** — 自身の推論の限界の認識
3. **Attention** — 複雑な環境での重要タスクへの集中
4. **Executive Functions** — 認知的柔軟性と制約下での計画
5. **Social Cognition** — 社会的情報の解釈と関与

## Evaluation

3段階評価プロトコル:
1. Stage 1: 認知タスクスイートでAIシステムを評価
2. Stage 2: 同タスクの人間ベースライン収集
3. Stage 3: 人間パフォーマンス分布に対するAIスコアのマッピング

## Submission Format

- Kaggle Community Benchmarks プラットフォームで評価を設計・提出
- フロンティアモデルに対してテスト可能な評価を構築

## Prize Structure

- トラック別賞: 各トラック上位2名に $10,000（計 $100,000）
- グランプリ: 全体上位4名に $25,000（計 $100,000）

---

# Kaggle Competition Workspace

## Structure

- `src/config.py` — All configuration (paths, params, seed). Change settings HERE, not in other modules.
- `src/dataset.py` — Stateless data I/O. `load_train()` / `load_test()` return raw DataFrames.
- `src/features.py` — Feature engineering. Stateful transforms (fit on train only).
- `src/model.py` — Model train/predict/save/load.
- `src/evaluate.py` — CV splitter, metrics, experiment logging. Owns all writes to `logs/`.
- `src/submit.py` — Generates timestamped submission CSVs.
- `src/utils.py` — `set_seed()`, `Timer`.
- `scripts/train.py` — Training entrypoint. Runs full CV pipeline.
- `scripts/predict.py` — Inference entrypoint. Loads saved models, generates submission.

## Conventions

- Format with ruff (line-length=120, Python 3.14)
- Type hints encouraged
- Config changes go in `src/config.py` only
- Experiment logs go in `logs/` via `src/evaluate.py` only

## Commands

- `task setup` — Install deps + download data
- `task train` — Train models
- `task predict` — Generate predictions
- `task submit` — Submit to Kaggle
- `task lint` — Check code style
- `task test` — Run tests
