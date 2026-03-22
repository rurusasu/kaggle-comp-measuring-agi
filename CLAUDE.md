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

## Current Approach

### Track: Metacognition

ベンチマーク設計は `docs/benchmark-design.md` に詳述。3つのタスクファミリー:

1. **Confidence Calibration Battery** (200問) — 回答と信頼度を表明させ、ECE/Brier Score で評価
2. **Error Detection and Correction** (50問) — Phase A で解答 → Phase B で自己レビュー・修正
3. **Knowledge Boundary Probing** (150問) — 「知っている/不確実/知らない」の自己分類精度

### Workflow

1. `kaggle-benchmarks` SDK をインストール（`pip install kaggle-benchmarks`）
2. 3タスクの問題セットを生成（手続き的生成 + 手動作成）
3. SDK でベンチマークとタスクを作成・登録
4. フロンティアモデル（Gemini, GPT-4, Claude）で実行してスコア収集
5. Kaggle Writeup（1,500語以内）を作成
6. ベンチマークを Writeup にリンクして提出

### File Layout

- `docs/benchmark-design.md` — ベンチマーク設計全文（タスク詳細、スコアリング、人間ベースライン計画）
- `src/` — 問題生成・評価スクリプト（未実装、これから作成）

### Submission Checklist

- [ ] kaggle-benchmarks SDK でベンチマーク作成
- [ ] 3タスクの問題セット生成・登録
- [ ] フロンティアモデルでスコア収集
- [ ] Writeup 執筆（1,500語、カバー画像付き）
- [ ] Writeup にベンチマークをリンク
- [ ] 提出ボタン押下（締切: 2026-04-16）

### Improvement Ideas

- タスク数を増やして統計的検出力を向上
- より多様な認知領域（視覚推論、時間推論）を追加
- 人間ベースラインの実データ収集（Prolific 等）
- 複数モデル間の比較分析を Writeup に含める

## Lessons Learned

### kaggle-benchmarks SDK

1. **ローカルでは動かない**: `MODEL_PROXY_URL` 環境変数が必要で、Kaggle Notebook 内でのみ利用可能。ローカル開発はテストケースの生成ロジックまで。SDK 統合は Kaggle 上で行う。
2. **$50/日の追加 quota**: コンペ参加後、ベンチマーク実行用に追加 GPU quota が付与される。これを使ってフロンティアモデルに対するスコア収集を行う。

### 提出形式の特殊性

3. **Hackathon 形式**: 通常の ML コンペと異なり、Writeup（1,500語）+ Benchmark の組み合わせ。コードよりも設計思想と実験結果の質が重要。
4. **1 チーム 1 提出のみ**: 複数回の試行ができない。提出前に十分な検証が必要。
5. **プライベート→パブリック**: 提出後にベンチマークとタスクが自動公開される。データ汚染防止のため、手続き的生成の問題を使うのが正しい判断。

### ベンチマーク設計

6. **認知科学の文献引用が差別化要因**: 単なるタスクセットではなく、心理学・神経科学の先行研究に基づいた設計であることを Writeup で強調すべき。
7. **カバー画像が必須**: 提出には画像が必要。3タスクの概要を示す図解を作成する。

## Documentation

**IMPORTANT: Before starting any implementation work, you MUST read the relevant docs first.**

- [docs/overview.md](docs/overview.md) — Competition description, goal, background
- [docs/evaluation.md](docs/evaluation.md) — Evaluation metric, scoring methodology
- [docs/submission.md](docs/submission.md) — Submission format, file structure, requirements
- [docs/timeline.md](docs/timeline.md) — Important dates and deadlines
- [docs/rules.md](docs/rules.md) — Full competition rules
- [docs/prizes.md](docs/prizes.md) — Prize structure

### Required Reading Order

1. Before EDA or feature engineering → read `overview.md` and `evaluation.md`
2. Before building submission pipeline → read `submission.md`
3. Before using external data or models → read `rules.md`
4. Before final submission → read `timeline.md` to confirm deadlines

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
