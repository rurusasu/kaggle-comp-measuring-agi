# Measuring Progress Toward AGI - Cognitive Abilities - Overview

**Competition URL:** https://www.kaggle.com/competitions/kaggle-measuring-agi

**Tagline:** Design high-quality benchmarks that go beyond recall to evaluate how frontier models truly reason, act, and judge.

**Type:** Hackathon

**Host:** Google DeepMind / Kaggle

## Description

Imagine a student who gets an A+ on a history test not because they understand the underlying events, but because they memorized the textbook. Current AI models can be similar: they display remarkable flashes of brilliance and crystallized knowledge, but often rely on surface-level patterns rather than fluid intelligence. This makes it difficult to distinguish when a model is truly solving a novel problem versus when it is simply recalling a scenario it has seen in its training data.

The core problem is that we lack an empirical framework to measure these limitations. We need evaluations that isolate specific cognitive abilities, resist shortcut solutions, and expose systematic failure modes. Without such benchmarks, progress toward human-level generality becomes difficult to interpret, comparisons between models become noisy, and important weaknesses remain hidden until deployment.

To move the field forward, we must look into the core cognitive faculties -- the internal gears that determine how a system learns, monitors its own logic, and navigates nuance.

In this competition, hosted by Google DeepMind and Kaggle, we are inviting the Kaggle community to help solve this by building high-quality benchmarks designed to dig deeper than standard evaluations. Your goal is to create a Kaggle benchmark (with underlying tasks) using datasets that isolate specific cognitive abilities across five critical tracks: learning, metacognition, attention, executive functions, and social cognition. Using the new Kaggle Benchmarks platform, you will help the industry move away from broad, static scores and toward generating detailed cognitive profiles for frontier models.

A successful submission should answer a simple question: "What can this benchmark tell us about model behavior that we could not see before?"

This is your opportunity to contribute to the fast-growing field of AI research. By crowdsourcing novel benchmark ideas from researchers, practitioners, and domain experts, this hackathon aims to transform Artificial General Intelligence (AGI) from a subject of speculation into a grounded, measurable scientific endeavor.

## Overview

Current AI models often succeed by exploiting familiar data or memorized patterns, making existing evaluations poor judges of how models truly think. This hackathon challenges you to bridge that gap. Your task is to create high-quality benchmarks with Kaggle's Benchmarks (https://www.kaggle.com/discussions/product-announcements/667898) to test true understanding. We are asking you to focus on the cognitive faculties highlighted in Google DeepMind's paper -- "Measuring progress toward AGI: A cognitive framework" (https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/measuring-progress-toward-agi/measuring-progress-toward-agi-a-cognitive-framework.pdf). The five faculties and tracks to focus on are: learning, metacognition, attention, executive functions, and social cognition. Designing these rigorous standards will build detailed cognitive profiles of frontier models and reveal exactly how close we are to achieving Artificial General Intelligence (AGI).

## Tracks

### Learning

**Can the model acquire and apply new knowledge and skills -- not just recall what it was trained on?**

Learning is the ability to acquire new knowledge or skills through experience. It is fundamental to adaptive intelligence: a system that cannot learn from new experiences is inherently brittle.

Current benchmarks test what models know (crystallized knowledge) rather than their capacity to learn on the fly. This track asks participants to create evaluations that isolate learning processes -- including, reinforcement-based learning, concept formation, and skill learning.

Example evaluation targets:
- Can the model learn a new rule or concept from a handful of examples and generalize it correctly?
- Does the model retain information provided earlier in a long interaction, or does it drift and hallucinate?
- Can the model update its beliefs when given corrective feedback, or does it perseverate on initial answers?

### Metacognition

**Does the model know what it knows -- and what it doesn't?**

Metacognition is a system's knowledge about its own cognitive processes and its ability to monitor and control them. It is often under-evaluated in AI: we rarely test whether models can accurately judge their own confidence, detect errors, or adjust strategies when failing.

This track asks participants to build evaluations that probe metacognitive knowledge, monitoring, and control. Can the model understand its limitations, calibrate confidence, and adjust its behavior -- for instance, by asking for clarification instead of guessing?

Example evaluation targets:
- Is the model's stated confidence well-calibrated with its actual accuracy?
- Can the model identify which questions it is likely to get wrong before answering?
- When the model makes an error, does it detect and correct it -- or does it confabulate a justification?
- Does the model know the boundaries of its own knowledge (e.g., distinguishing "I know this" from "I'm guessing")?

### Attention

**Can the model focus on what matters and ignore what doesn't?**

Attention balances goal-relevant focus with responsiveness and is the ability to focus cognitive resources on specific aspects of perceptual stimuli, information, or task demands. In AI, failures appear as distraction by irrelevant context or missing critical details.

While sharing a name with the transformer mechanism, cognitive attention specifically refers to how a system allocates processing resources across competing information.

This track probes selective attention (filtering), sustained attention, and attention shifting (flexibility).

Example evaluation targets:
- Does the model get distracted by irrelevant but salient information inserted into a prompt?
- Does performance degrade systematically as input length increases, even when the task difficulty is held constant?
- Can the model shift focus between sub-tasks in a complex, multi-part prompt without losing track?
- How does the model perform when critical information is buried among large amounts of irrelevant context?

### Executive Functions

**Can the model plan, inhibit impulses, and adapt flexibly -- or does it default to habitual responses?**

Executive functions include planning, inhibitory control, and cognitive flexibility. These are often conflated with "reasoning," but are distinct: a model may excel at logic yet struggle with multi-step plans or overriding habitual responses. This track asks for evaluations that isolate these processes to reveal a model's true ability to orchestrate complex thoughts and actions.

Example evaluation targets:
- Can the model formulate and execute a multi-step plan, adjusting when intermediate steps fail?
- When a habitual response pattern is wrong in a new context, can the model override it?
- Can the model switch between different task rules or frameworks without perseverative errors?
- How does the model handle situations where multiple plausible actions conflict with each other?
- Can the model perform intermediate computations or mental manipulations without losing track (working memory)?

### Social Cognition

**Can the model understand and navigate social situations -- not just produce polite text?**

Social cognition is the ability to interpret and respond to social information. For AI, it underpins inferring user intent, predicting reactions, and navigating competing perspectives. This track asks for evaluations that probe genuine social abilities beyond surface-level politeness.

Example evaluation targets:
- Can the model infer a speaker's intention when it diverges from their literal statement?
- Can the model track and reason about multiple agents with different (and possibly false) beliefs?
- Does the model adjust its communication style appropriately for different social contexts and audiences?
- Can the model navigate a negotiation scenario where goals are partially misaligned?
- Does the model recognize and respond appropriately to implicit social norms?

## Submission Requirements

*Note: Upon joining this hackathon, your Kaggle account will be provisioned with extra quota ($50/day, $500/month) to run the AI models for your benchmark. Read the Rules section 3.4.b to learn more.*

A valid submission must contain the following:

- Kaggle Writeup
  - [Mandatory] Kaggle Benchmark, as an attachment > "project links" > "Benchmark"
  - [Optional] Media Gallery
  - [Optional] Attached Public Notebook

**Your final Submission must be made prior to the deadline. Any un-submitted or draft Writeups by the competition deadline will not be considered by the Judges.**

### 1. Kaggle Writeup

The Kaggle Writeup serves as your project report. This should include a title, subtitle, and a detailed analysis of your submission. You must select a Track for your Writeup in order to submit.

Your Writeup should not exceed 1,500 words. Submissions over this limit may be subject to penalty.

### a. Kaggle Benchmark [mandatory]

This is the most important part of your writeup submission. You must create a Kaggle Benchmark with underlying tasks -- all of which should be authored by you -- and link the benchmark in the writeup as a project link. The tasks and benchmark should all be set to private. After the submission deadline, all tasks and benchmarks are published publicly.

Kaggle Benchmarks (https://www.kaggle.com/benchmarks?type=community) is a product that lets you -- the Kaggle community -- build, run, and share your own custom benchmarks for evaluating AI models at no cost.

Powered by the kaggle-benchmarks SDK (https://github.com/Kaggle/kaggle-benchmarks/tree/ci), you can now create your own AI evaluations ("tasks") and put them together into a collection ("benchmark").

Helpful resources:
- Kaggle Benchmarks guide: https://www.kaggle.com/docs/benchmarks#intro
- Getting started notebook: https://www.kaggle.com/code/nicholaskanggoog/kaggle-benchmarks-getting-started-notebook?scriptVersionId=290215074
- YouTube tutorial: https://www.youtube.com/watch?v=VBlyJJ7PTD8
- Kaggle-benchmarks open source GitHub Repo: https://github.com/Kaggle/kaggle-benchmarks & DeepWiki: https://deepwiki.com/Kaggle/kaggle-benchmarks
- Benchmarks cookbook: Guide to advanced features and use cases: https://github.com/Kaggle/kaggle-benchmarks/blob/ci/cookbook.md
- Example tasks: Get inspired with a variety of pre-built tasks: https://github.com/Kaggle/kaggle-benchmarks/tree/ci/documentation/examples

### b. Media Gallery [optional]

This is where you should attach any images and/or videos associated with your submission. A cover image is required to submit your Writeup.

### c. Public Notebook [optional]

Your code should be submitted as a public notebook in the `Project Files` field. Your notebook should be publicly accessible and not require a login or paywall. If you use a private Kaggle Notebook, it will automatically be made public after the deadline.

### d. Public Project Link [mandatory]

A URL to your benchmark. This allows judges to analyze your project firsthand. Under the section "Attachments", click on "Add a link". This will open a panel on the right, where you will be able to select your benchmark and add it to the project.

## Proposed Writeup Template

```
### Project Name
### Your Team
### Problem Statement
### Task & benchmark construction
### Dataset
### Technical details
### Results, insights, and conclusions
### Organizational affiliations
### References & citations
```

**Note:** If you attach a private Kaggle Resource to your public Kaggle Writeup, your private Resource will automatically be made public after the deadline.
