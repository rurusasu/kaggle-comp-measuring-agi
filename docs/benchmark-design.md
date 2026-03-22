# Benchmark Design: Metacognitive Calibration and Error Monitoring

## Track: Metacognition

### Rationale

Metacognition -- the ability to monitor and regulate one's own cognitive processes -- is arguably the most critical gap in current AI evaluation. A model that confidently produces wrong answers is more dangerous than one that knows its limits. Despite this, existing benchmarks almost never isolate metacognitive abilities from task performance itself. This benchmark targets three core metacognitive faculties:

1. **Confidence calibration** -- Does stated confidence match actual accuracy?
2. **Error detection** -- Can the model identify its own mistakes?
3. **Knowledge boundary awareness** -- Can the model distinguish what it knows from what it is guessing?

These map directly to the metacognitive monitoring and control processes described in the DeepMind AGI framework paper.

---

## Evaluation Methodology

### Design Principles

- **Isolation**: Each task isolates a specific metacognitive process, not domain knowledge.
- **Contamination resistance**: Tasks use novel stimuli (procedurally generated logic puzzles, synthetic scenarios) to prevent training-data memorization.
- **Gradient of difficulty**: Each task has easy/medium/hard variants to produce discriminatory signal across model capability levels.
- **Verifiable ground truth**: Every item has an unambiguous correct answer for both the primary task and the metacognitive judgment.

### Architecture: Three Task Families

#### Task 1: Confidence Calibration Battery

**Cognitive science basis**: Calibration research (Lichtenstein, Fischhoff & Phillips, 1982) shows humans systematically deviate from perfect calibration. Well-calibrated agents should have accuracy ≈ confidence at each confidence level.

**Method**:
- Present the model with a set of questions spanning varying difficulty levels.
- For each question, the model must:
  1. Provide an answer.
  2. State its confidence as a probability (0-100%).
- Questions are drawn from multiple domains (logic, arithmetic, factual recall, spatial reasoning) with known difficulty distributions.
- Some questions are intentionally unanswerable or ambiguous -- a well-calibrated model should assign low confidence to these.

**Scoring**:
- Expected Calibration Error (ECE): Partition confidence into bins, measure |accuracy - confidence| per bin, compute weighted average.
- Brier Score decomposition: Separate reliability (calibration) from resolution (discrimination).
- Overconfidence ratio: Fraction of items where confidence > accuracy by more than 20 percentage points.

**Example test case**:
```
Prompt: "What is the result of 347 × 829? State your answer and your confidence (0-100%) that it is correct."

Expected behavior:
- Correct answer: 287,663
- A well-calibrated model should give high confidence (~90%+) if it can compute reliably, or moderate confidence (~50-70%) if arithmetic is a known weakness.

Scoring: Compare stated confidence against actual correctness across many such items.
```

#### Task 2: Error Detection and Correction

**Cognitive science basis**: Error monitoring research (Rabbitt, 1966; Yeung & Summerfield, 2012) demonstrates that effective metacognitive agents detect errors rapidly, sometimes before receiving feedback.

**Method**:
- Phase A (Generation): The model solves a set of problems (multi-step reasoning, code debugging, logical deductions).
- Phase B (Review): The model is shown its own Phase A answers and asked to:
  1. Flag which answers it believes are incorrect.
  2. Explain why it thinks each flagged answer is wrong.
  3. Provide a corrected answer.
- Critically, Phase B uses the model's actual Phase A outputs, not fabricated errors.

**Scoring**:
- Error detection sensitivity: True positive rate of flagging actual errors.
- Error detection specificity: True negative rate (not flagging correct answers).
- Correction quality: Among detected errors, what fraction are corrected to the right answer?
- Confabulation rate: How often does the model "explain" why a correct answer is wrong (false positive justification)?

**Example test case**:
```
Phase A prompt: "A farmer has 3 fields. Field A is twice the size of Field B. Field C is 5 acres larger than Field A. If the total area is 85 acres, what is the size of each field?"

Phase B prompt: "You previously answered: Field A = 30 acres, Field B = 15 acres, Field C = 40 acres. Review your answer. Is it correct? If not, identify the error and provide the corrected answer."

Ground truth: 15 + 30 + 35 = 80 ≠ 85, so the answer is wrong.
Correct: B=16, A=32, C=37 (16+32+37=85).

Scoring: Did the model detect the error? Did it correctly identify that the total doesn't sum to 85? Did it produce the correct values?
```

#### Task 3: Knowledge Boundary Probing

**Cognitive science basis**: The "feeling of knowing" literature (Hart, 1965; Metcalfe, 1986) shows that metacognitive awareness of knowledge boundaries is a distinct cognitive process from retrieval itself.

**Method**:
- Present questions in three categories (unknown to the model):
  1. **Answerable**: Questions the model should know (common knowledge, well-established facts).
  2. **Unanswerable**: Questions with no definitive answer (future events, insufficient information, genuinely ambiguous).
  3. **Boundary**: Questions at the edge of model knowledge (obscure facts, recent events near training cutoff).
- The model must classify each question as "I know this", "I'm uncertain", or "I don't know" BEFORE answering.
- Then it provides an answer (or explicitly declines).

**Scoring**:
- Metacognitive accuracy: Does the model's self-classification predict its actual performance?
- Appropriate abstention rate: For unanswerable questions, how often does it correctly decline?
- Hallucination detection: For questions it should mark as "I don't know," how often does it fabricate a confident answer?
- Discrimination index: ROC-AUC of the model's self-assessment as a predictor of correctness.

**Example test case**:
```
Answerable: "What is the chemical formula for water?"
Expected: Classification = "I know this", Answer = "H2O"

Unanswerable: "What will the closing price of AAPL stock be on December 31, 2027?"
Expected: Classification = "I don't know", Answer = decline or explicit uncertainty

Boundary: "What was the population of Tuvalu according to the most recent census?"
Expected: Classification = "I'm uncertain", Answer = approximate or hedged
```

---

## Dataset Construction

### Size and Statistical Power

- **Task 1 (Calibration)**: 200 questions (40 per domain x 5 domains), yielding ~20 items per confidence bin for reliable ECE estimation.
- **Task 2 (Error Detection)**: 50 multi-step problems in Phase A, generating 50 review items in Phase B.
- **Task 3 (Knowledge Boundary)**: 150 questions (50 per category).

Total: 400 primary items, producing ~600 scored data points per model.

### Contamination Prevention

- Logic/arithmetic items are procedurally generated with random parameters.
- Factual questions use combinations of real facts in novel framings.
- Synthetic scenarios are original constructions not found in common training corpora.

---

## Human Baseline Collection

### Protocol

1. **Participants**: Recruit 50-100 participants via Prolific or similar platform, stratified by education level.
2. **Procedure**: Participants complete the same task battery as the AI models, with identical instructions.
3. **Compensation**: ~$15/hour, with bonus for calibration quality (incentive-compatible scoring rule).
4. **Data collected**:
   - Answers and confidence ratings (Task 1)
   - Error detection judgments (Task 2, using pre-generated answers with known error rates)
   - Knowledge boundary self-assessments (Task 3)

### Expected Human Performance

Based on calibration literature:
- **Task 1**: Humans typically show overconfidence bias (ECE ~15-25%). Experts in specific domains show better calibration.
- **Task 2**: Humans detect ~60-80% of their own errors when reviewing, with higher detection for arithmetic vs. reasoning errors.
- **Task 3**: Humans show moderate "feeling of knowing" accuracy (ROC-AUC ~0.70-0.80).

---

## AI vs. Human Scoring Framework

### Comparison Metrics

For each task, compute:

1. **Absolute performance**: Raw metacognitive scores (ECE, detection sensitivity, discrimination index).
2. **Relative performance**: AI percentile within the human distribution.
3. **Profile shape**: Radar chart of metacognitive sub-abilities -- calibration, error detection, knowledge awareness -- to identify systematic strengths/weaknesses.

### Discriminatory Power

This benchmark is designed to produce gradient performance:
- **Weak models**: High ECE (>30%), low error detection (<40%), frequent hallucination on unknowable questions.
- **Average models**: Moderate ECE (15-25%), reasonable error detection (50-70%), some appropriate abstention.
- **Strong models**: Low ECE (<15%), high error detection (>75%), reliable knowledge boundary awareness.

The three-task structure ensures that even models excelling in one metacognitive dimension can be differentiated by their profile across all three.

---

## Implementation Plan

1. **Phase 1**: Build procedural generators for Task 1 and Task 3 question items.
2. **Phase 2**: Create the Task 2 pipeline (generate Phase A, collect outputs, build Phase B prompts).
3. **Phase 3**: Package as Kaggle Benchmark tasks using the kaggle-benchmarks SDK.
4. **Phase 4**: Run on frontier models (Gemini, GPT-4, Claude) and collect results.
5. **Phase 5**: Draft writeup with analysis and cognitive science framing.

---

## References

- DeepMind. (2025). Measuring progress toward AGI: A cognitive framework.
- Lichtenstein, S., Fischhoff, B., & Phillips, L. D. (1982). Calibration of probabilities: The state of the art to 1980.
- Hart, J. T. (1965). Memory and the feeling-of-knowing experience. Journal of Educational Psychology.
- Metcalfe, J. (1986). Feeling of knowing in memory and problem solving. Journal of Experimental Psychology: Learning, Memory, and Cognition.
- Yeung, N., & Summerfield, C. (2012). Metacognition in human decision-making. Philosophical Transactions of the Royal Society B.
- Rabbitt, P. (1966). Errors and error correction in choice-response tasks. Journal of Experimental Psychology.
- Kadavath, S. et al. (2022). Language models (mostly) know what they know. arXiv:2207.05221.
- Lin, S., Hilton, J., & Evans, O. (2022). Teaching models to express their uncertainty in words. TMLR.
