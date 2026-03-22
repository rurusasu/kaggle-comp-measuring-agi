# Next Task: Measuring Progress Toward AGI

## Status

- **Track: Metacognition** を選択済み
- ベンチマーク設計は `docs/benchmark-design.md` に完成
- Kaggle Notebook のコードは `kaggle-notebook/notebook.py` に準備済み
- Writeup ドラフトは `docs/writeup-draft.md` に作成済み
- **kaggle-benchmarks SDK はローカルでも `kaggle kernels push` でも動かない**。Web UI から New Notebook を作成する必要がある。

## Step 1: Kaggle Web UI でベンチマーク作成

**この手順はすべてブラウザで実行する:**

1. https://www.kaggle.com/competitions/kaggle-measuring-agi に移動
2. **Code** タブ → **New Notebook** をクリック
3. 新しい Notebook が開いたら:
   - `kaggle-notebook/notebook.py` の内容をコピペ
   - **Settings** → **Internet** を ON に設定
   - **Run All** を実行
4. ベンチマークが作成されたら、Benchmark の URL をメモ

### SDK が動かない場合
- `MODEL_PROXY_URL` が設定されていない旨のエラーが出たら、コンペの Notebooks タブから直接作成する必要がある
- コンペ参加時に追加 quota ($50/日) が付与されているか確認

## Step 2: Writeup 作成

1. https://www.kaggle.com/competitions/kaggle-measuring-agi/submit に移動
2. **New Writeup** をクリック
3. `docs/writeup-draft.md` の内容をベースに入力（1,500 語以内）
4. **Track**: Metacognition を選択
5. **Cover Image**: 3タスクの概要図を作成してアップロード（Mermaid → PNG 等）
6. **Attachments > Add a link** でベンチマーク URL をリンク
7. **Submit** ボタンをクリック

## Step 3: カバー画像の作成

以下の内容を図示した画像を作成:

```
Metacognitive Calibration & Error Monitoring Benchmark
┌─────────────────────┬──────────────────────┬──────────────────────┐
│  Task 1             │  Task 2              │  Task 3              │
│  Confidence         │  Error Detection     │  Knowledge Boundary  │
│  Calibration        │  & Correction        │  Probing             │
│  (200 items)        │  (50 items)          │  (150 items)         │
│                     │                      │                      │
│  Answer + Confidence│  Phase A: Solve      │  Self-classify:      │
│  → ECE scoring      │  Phase B: Review     │  Know/Uncertain/     │
│                     │  → Sensitivity/      │  Don't Know          │
│                     │    Specificity       │  → ROC-AUC           │
└─────────────────────┴──────────────────────┴──────────────────────┘
```

Matplotlib や HTML で作成して PNG にエクスポート。

## Step 4: 改善案（初回提出後）

- フロンティアモデル比較結果を Writeup に追加
- より多くの test items を追加（統計的検出力向上）
- 人間ベースラインの参考値（文献から）を追加
- 採点の自動化パイプラインをベンチマークに含める

## Important Notes

- **Deadline: 2026-04-16** — 残り 24 日
- **1 チーム 1 提出のみ**: 再提出不可。十分な検証後に提出すること。
- **提出後にタスク・ベンチマークが自動公開される**: データ汚染防止のため手続き的生成を使用。
- **追加 quota**: $50/日、$500/月。フロンティアモデル実行用。
- **docs/writeup-draft.md** に Writeup の下書きあり。
- **docs/benchmark-design.md** にベンチマーク設計の全文あり。
