# Metacognitive Calibration and Error Monitoring: Measuring What AI Knows About What It Knows

**Track: Metacognition**

## Team

koheimiki

## Problem Statement

Current AI benchmarks overwhelmingly measure *what* models know rather than *whether models know what they know*. This asymmetry creates a dangerous blind spot: a model that confidently produces wrong answers is more hazardous than one that acknowledges its limits. Metacognition -- the ability to monitor and regulate one's own cognitive processes -- is arguably the most critical gap in AI evaluation today.

Consider a medical AI that answers every question with 95% confidence regardless of whether it is reciting textbook knowledge or hallucinating a drug interaction. The raw accuracy score might look impressive, but the lack of calibrated self-assessment makes the system unreliable where it matters most. The same principle applies to legal reasoning, scientific analysis, and any domain where knowing the boundaries of one's knowledge is as important as the knowledge itself.

The DeepMind cognitive framework paper identifies metacognition as one of five core cognitive faculties necessary for progress toward AGI, yet existing benchmarks almost never isolate metacognitive abilities from task performance. Our benchmark addresses this gap directly.

## Motivation: Why Metacognition Is the Most Critical Gap

Three observations motivate our focus:

1. **Safety-critical deployment depends on calibration.** In high-stakes applications, a model's ability to say "I don't know" is more valuable than marginal accuracy gains. Overconfident errors erode trust and cause harm.

2. **Metacognition is orthogonal to domain knowledge.** A model can achieve perfect accuracy on factual recall while having terrible confidence calibration. Existing benchmarks conflate these dimensions, making it impossible to diagnose metacognitive weaknesses independently.

3. **Human intelligence research treats metacognition as foundational.** Decades of cognitive science (Flavell, 1979; Nelson & Narens, 1990) demonstrate that metacognitive monitoring and control are core components of intelligent behavior, not luxuries that emerge automatically from knowledge accumulation.

## Methodology: Three Task Families

Our benchmark isolates three distinct metacognitive faculties, each grounded in established cognitive science:

### Task 1: Confidence Calibration Battery (50 items)

**Cognitive basis:** Calibration research (Lichtenstein, Fischhoff & Phillips, 1982) shows that well-calibrated agents have accuracy approximately equal to stated confidence at each confidence level.

**Method:** The model answers questions spanning arithmetic, logic, factual recall, and deliberately unanswerable items. For each question, it must provide both an answer and a confidence rating (0-100%). We procedurally generate arithmetic items with random parameters to resist training-data contamination. Unanswerable questions (e.g., future events, unknowable historical details) test whether the model assigns appropriately low confidence.

**Scoring:** For each item, we compute the calibration error as the absolute difference between stated confidence and actual correctness (scaled to 0-100). The per-item score is 1.0 minus this normalized error. For unanswerable items, ideal confidence is 0% -- any confidence above that is penalized proportionally.

### Task 2: Error Detection and Correction (20 items)

**Cognitive basis:** Error monitoring research (Rabbitt, 1966; Yeung & Summerfield, 2012) demonstrates that effective metacognitive agents detect errors rapidly, sometimes before receiving feedback.

**Method:** This task uses a two-phase design. In Phase A, the model solves multi-step reasoning problems (word problems, sequence puzzles, rate calculations). In Phase B, the model is shown its own Phase A output and asked to review it: flag errors, explain what went wrong, and provide corrections. Critically, Phase B uses the model's *actual* Phase A outputs, not fabricated errors.

**Scoring:** We evaluate four outcomes in a metacognitive confusion matrix:
- **True negative (1.0):** Correct answer, correctly confirmed
- **True positive with correction (1.0):** Error detected and corrected to the right answer
- **True positive without correction (0.8):** Error detected but not fully corrected
- **False positive (0.2):** Correct answer falsely flagged as wrong (confabulation)
- **False negative (0.0):** Error missed entirely -- the worst metacognitive failure

A judge LLM evaluates the correctness of Phase A answers and Phase B corrections against verified ground truth.

### Task 3: Knowledge Boundary Probing (50 items)

**Cognitive basis:** The "feeling of knowing" literature (Hart, 1965; Metcalfe, 1986) shows that metacognitive awareness of knowledge boundaries is a distinct cognitive process from retrieval itself.

**Method:** The model receives questions in three hidden categories: *answerable* (common knowledge the model should know), *unanswerable* (future events, insufficient information, genuinely unknowable), and *boundary* (obscure facts at the edge of typical training data). Before answering, the model must classify its own knowledge state as "I know this," "I'm uncertain," or "I don't know."

**Scoring:** A detailed scoring matrix rewards alignment between self-classification and actual performance. The ideal model says "I know this" only when correct, "I'm uncertain" for boundary items, and "I don't know" for genuinely unanswerable questions. The worst score (0.0) is reserved for claiming "I know this" while producing a wrong or fabricated answer.

### Composite Scoring

The three tasks are combined into a composite metacognitive score weighted 40/30/30 (calibration/error detection/boundary awareness), reflecting the relative item counts and the centrality of calibration to the metacognitive construct.

## Dataset Construction and Contamination Resistance

All arithmetic and logic items are procedurally generated with randomized parameters, preventing memorization from training data. Factual questions use well-established facts but are framed in novel prompt structures. Unanswerable questions reference future events, unknowable historical details, or genuinely ambiguous scenarios that cannot be resolved through retrieval.

The total dataset comprises 120 scored items across the three tasks (50 calibration + 20 error detection + 50 boundary probing), producing approximately 120 primary data points and additional sub-scores per model.

## Expected Results: Discriminatory Power

This benchmark is designed to produce gradient performance across model capability levels:

- **Weak models** exhibit high overconfidence (calibration scores below 0.5), miss most of their own errors (error detection scores near 0.0), and hallucinate confidently on unanswerable questions (boundary scores below 0.3).

- **Average models** show moderate calibration (0.5-0.7), detect some errors but struggle with correction (0.4-0.6), and display partial boundary awareness with occasional hallucination (0.5-0.7).

- **Strong models** achieve good calibration (above 0.7), reliably detect and correct their errors (above 0.7), and demonstrate robust knowledge boundary awareness with appropriate abstention (above 0.8).

The three-task structure ensures that even models excelling in one metacognitive dimension are differentiated by their profile across all three. A model might be well-calibrated on factual questions but still hallucinate on unknowable ones, or detect arithmetic errors but miss logical ones.

## Technical Details

The benchmark is implemented using the `kaggle-benchmarks` SDK. Each task is defined as a decorated function that takes an LLM instance and returns a float score. The `@kbench.task` decorator registers tasks for evaluation. Structured outputs are enforced via Python dataclasses (e.g., `CalibratedAnswer` with `answer` and `confidence` fields). Error detection uses the `kbench.chats.new()` context manager to maintain separate conversation contexts for Phase A generation and Phase B review. Answer correctness in Tasks 2 and 3 is verified using a judge LLM (`kbench.judge_llm`) to handle natural language variation in responses.

## References & Citations

- DeepMind. (2025). Measuring progress toward AGI: A cognitive framework.
- Flavell, J. H. (1979). Metacognition and cognitive monitoring. *American Psychologist*, 34(10), 906-911.
- Nelson, T. O., & Narens, L. (1990). Metamemory: A theoretical framework and new findings. *Psychology of Learning and Motivation*, 26, 125-173.
- Lichtenstein, S., Fischhoff, B., & Phillips, L. D. (1982). Calibration of probabilities: The state of the art to 1980.
- Hart, J. T. (1965). Memory and the feeling-of-knowing experience. *Journal of Educational Psychology*, 56(4), 208-216.
- Metcalfe, J. (1986). Feeling of knowing in memory and problem solving. *Journal of Experimental Psychology: Learning, Memory, and Cognition*, 12(2), 288-294.
- Yeung, N., & Summerfield, C. (2012). Metacognition in human decision-making. *Philosophical Transactions of the Royal Society B*, 367(1594), 1310-1321.
- Rabbitt, P. (1966). Errors and error correction in choice-response tasks. *Journal of Experimental Psychology*, 71(2), 264-272.
- Kadavath, S. et al. (2022). Language models (mostly) know what they know. arXiv:2207.05221.
- Lin, S., Hilton, J., & Evans, O. (2022). Teaching models to express their uncertainty in words. *TMLR*.
