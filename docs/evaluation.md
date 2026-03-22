# Measuring Progress Toward AGI - Cognitive Abilities - Evaluation

## Minimum Requirements

- Target one primary domain (to keep the signal sharp),
- Clearly state which capability is being isolated, and
- Explain what new insight the benchmark reveals about model behavior within that domain.

## Evaluation Criteria

Submissions are evaluated on the following criteria:

### Dataset quality & task construction (50%)

Is the data defensible?
- Verifiably correct answers (no ambiguity)
- Sufficient sample size to be statistically significant

Are the tasks and benchmark built well?
- Clean, readable code
- Input prompt and output verification are robust.

### Writeup quality (20%)

Can the community use and learn from this? High quality writeups covering:
- **Problem Statement:** Which domains are you trying to solve and why
- **Task & benchmark construction:** How you've structured the code for the actual tasks and benchmark
- **Dataset:** its provenance, columns, and data types
- **Technical details:** Any additional details on how you implemented the benchmark or techniques
- **Results, insights, and conclusions:** How did the LLMs perform and what unique insights did you learn
- **Organizational affiliations:** Which organizations you might be affiliated with
- **References & citations:** Cite relevant work or papers that are similar or relevant to your submission.

### Discriminatory power (15%)

Does the benchmark provide a meaningful signal?
We are looking for a gradient of performance. Can the benchmark significantly distinguish model performance?
A benchmark where everyone scores 0% is as useless as one where everyone scores 100%.

### Community upvotes (15%)

How many upvotes the benchmark gets from other Kaggle users. Only benchmark votes will be counted, not Writeup votes.
