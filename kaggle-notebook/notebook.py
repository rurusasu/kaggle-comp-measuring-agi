"""
Metacognitive Calibration and Error Monitoring Benchmark
========================================================

This notebook creates a Kaggle Benchmark that evaluates LLM metacognitive abilities
across three task families:
  1. Confidence Calibration Battery
  2. Error Detection and Correction
  3. Knowledge Boundary Probing

Designed for the "Measuring Progress Toward AGI" hackathon (Metacognition track).
"""

import random
import re
from dataclasses import dataclass
from typing import List

import pandas as pd

import kaggle_benchmarks as kbench

# ---------------------------------------------------------------------------
# Seed for reproducibility of procedurally generated items
# ---------------------------------------------------------------------------
random.seed(42)

# ===========================================================================
# TASK 1: Confidence Calibration Battery
# ===========================================================================
# The model answers questions and states its confidence (0-100%).
# We measure whether stated confidence aligns with actual accuracy (ECE).

# --- Procedural generation of calibration items ---

def generate_arithmetic_items(n=10):
    """Generate arithmetic problems with known answers."""
    items = []
    for _ in range(n):
        a = random.randint(10, 999)
        b = random.randint(10, 999)
        op = random.choice(["+", "-", "*"])
        if op == "+":
            answer = a + b
            expr = f"{a} + {b}"
        elif op == "-":
            answer = a - b
            expr = f"{a} - {b}"
        else:
            answer = a * b
            expr = f"{a} * {b}"
        items.append({
            "question": f"What is {expr}?",
            "answer": str(answer),
            "domain": "arithmetic",
            "difficulty": "easy" if max(a, b) < 100 else ("medium" if op != "*" else "hard"),
        })
    return items


def generate_logic_items(n=10):
    """Generate simple logic / deduction puzzles."""
    templates = [
        {
            "q": "If all Bloops are Razzles and all Razzles are Lazzles, are all Bloops definitely Lazzles?",
            "a": "Yes",
            "difficulty": "easy",
        },
        {
            "q": "If some Floops are Troops and some Troops are Snoops, are some Floops definitely Snoops?",
            "a": "No",
            "difficulty": "medium",
        },
        {
            "q": "A is taller than B. C is shorter than B. D is taller than A. Who is the shortest?",
            "a": "C",
            "difficulty": "easy",
        },
        {
            "q": "If it rains, the ground is wet. The ground is wet. Did it definitely rain?",
            "a": "No",
            "difficulty": "medium",
        },
        {
            "q": "Every bird in Zogland can fly. Pingu is a bird in Zogland. Can Pingu fly?",
            "a": "Yes",
            "difficulty": "easy",
        },
        {
            "q": "In a room of 3 people, everyone shakes hands with everyone else exactly once. How many handshakes occur?",
            "a": "3",
            "difficulty": "easy",
        },
        {
            "q": "In a room of 5 people, everyone shakes hands with everyone else exactly once. How many handshakes occur?",
            "a": "10",
            "difficulty": "medium",
        },
        {
            "q": "If no Zips are Zaps and all Zaps are Zops, can a Zip be a Zop?",
            "a": "Yes",
            "difficulty": "hard",
        },
        {
            "q": "A clock shows 3:15. What is the angle between the hour and minute hands?",
            "a": "7.5",
            "difficulty": "hard",
        },
        {
            "q": "Three boxes are labeled Apples, Oranges, and Mixed. All labels are wrong. You pick one fruit from the box labeled Mixed and it is an Apple. What does the box labeled Oranges actually contain?",
            "a": "Mixed",
            "difficulty": "hard",
        },
    ]
    selected = random.sample(templates, min(n, len(templates)))
    return [{"question": t["q"], "answer": t["a"], "domain": "logic", "difficulty": t["difficulty"]} for t in selected]


def generate_factual_items(n=10):
    """Generate factual recall questions with unambiguous answers."""
    facts = [
        ("What is the chemical symbol for gold?", "Au", "easy"),
        ("How many sides does a hexagon have?", "6", "easy"),
        ("What planet is closest to the Sun?", "Mercury", "easy"),
        ("What is the largest ocean on Earth?", "Pacific", "easy"),
        ("In what year did the Berlin Wall fall?", "1989", "medium"),
        ("What is the speed of light in km/s (approximate integer)?", "300000", "medium"),
        ("Who wrote the novel '1984'?", "George Orwell", "easy"),
        ("What is the atomic number of carbon?", "6", "easy"),
        ("What is the capital of Mongolia?", "Ulaanbaatar", "medium"),
        ("What is the half-life of Carbon-14 in years (approximate)?", "5730", "hard"),
        ("What is the smallest prime number greater than 50?", "53", "medium"),
        ("How many chromosomes do humans have?", "46", "easy"),
    ]
    selected = random.sample(facts, min(n, len(facts)))
    return [{"question": q, "answer": a, "domain": "factual", "difficulty": d} for q, a, d in selected]


def generate_unanswerable_items(n=5):
    """Generate questions that have no definitive answer -- well-calibrated models should assign low confidence."""
    questions = [
        "What will the global average temperature be on January 1, 2090?",
        "What is the exact number of grains of sand on Earth?",
        "Who will win the Nobel Prize in Physics in 2045?",
        "What was Cleopatra's favorite color?",
        "How many undiscovered species currently exist in the deep ocean?",
        "What will the population of Mars be in 2200?",
        "What did the last speaker of the Eyak language dream about on their 30th birthday?",
    ]
    selected = random.sample(questions, min(n, len(questions)))
    return [{
        "question": q,
        "answer": "__UNANSWERABLE__",
        "domain": "unanswerable",
        "difficulty": "hard",
    } for q in selected]


# Assemble calibration dataset
calibration_items = (
    generate_arithmetic_items(15)
    + generate_logic_items(10)
    + generate_factual_items(15)
    + generate_unanswerable_items(10)
)
random.shuffle(calibration_items)

calibration_df = pd.DataFrame(calibration_items)


@dataclass
class CalibratedAnswer:
    answer: str
    confidence: int  # 0-100


@kbench.task(name="confidence_calibration")
def confidence_calibration(llm, question: str, answer: str, domain: str, difficulty: str) -> float:
    """
    Ask the model to answer a question AND state its confidence (0-100%).
    Score: 1.0 if |confidence - correctness*100| is small (well-calibrated),
    penalized proportionally to miscalibration.
    """
    prompt = (
        f"Answer the following question. Then state your confidence that your answer is correct "
        f"as an integer from 0 to 100.\n\n"
        f"Question: {question}\n\n"
        f"Respond with your answer and confidence."
    )
    result = llm.prompt(prompt, schema=CalibratedAnswer)

    # Determine correctness
    if answer == "__UNANSWERABLE__":
        # For unanswerable questions, the ideal confidence is low (<=20)
        # and the model should indicate uncertainty
        is_correct = 0.0
        # Score based on how low the confidence is (lower = better for unanswerable)
        calibration_error = abs(result.confidence - 0) / 100.0
        score = max(0.0, 1.0 - calibration_error)
    else:
        # Check if the model's answer contains the correct answer
        model_answer = result.answer.strip().lower().replace(",", "")
        correct_answer = answer.strip().lower().replace(",", "")
        is_correct = 1.0 if correct_answer in model_answer else 0.0

        # Calibration score: how close is confidence to actual correctness?
        # Perfect calibration: confident when right, uncertain when wrong
        ideal_confidence = is_correct * 100
        calibration_error = abs(result.confidence - ideal_confidence) / 100.0
        score = max(0.0, 1.0 - calibration_error)

    return score


# Run evaluation across all calibration items
calibration_runs = confidence_calibration.evaluate(
    llm=[kbench.llm],
    evaluation_data=calibration_df,
    n_jobs=5,
)
calibration_runs.as_dataframe()


# ===========================================================================
# TASK 2: Error Detection and Correction
# ===========================================================================
# Phase A: Model solves problems.
# Phase B: Model reviews its own answers and flags errors.

def generate_error_detection_items():
    """Generate multi-step reasoning problems for error detection."""
    problems = [
        {
            "problem": (
                "A farmer has 3 fields. Field A is twice the size of Field B. "
                "Field C is 5 acres larger than Field A. If the total area is 85 acres, "
                "what is the size of each field?"
            ),
            "correct_answer": "Field B = 16 acres, Field A = 32 acres, Field C = 37 acres",
            "verification": "16 + 32 + 37 = 85",
        },
        {
            "problem": (
                "A train travels from City A to City B at 60 km/h and returns at 40 km/h. "
                "The total round-trip distance is 480 km. What is the average speed for the entire trip?"
            ),
            "correct_answer": "48 km/h",
            "verification": "Average speed = 2*60*40/(60+40) = 4800/100 = 48",
        },
        {
            "problem": (
                "A store offers a 20% discount on a $150 item, then applies a 10% tax on the discounted price. "
                "What is the final price?"
            ),
            "correct_answer": "$132",
            "verification": "150 * 0.8 = 120, 120 * 1.1 = 132",
        },
        {
            "problem": (
                "A rectangular garden has a perimeter of 56 meters. Its length is 4 meters more than its width. "
                "What are the dimensions?"
            ),
            "correct_answer": "Width = 12 meters, Length = 16 meters",
            "verification": "2*(12+16) = 2*28 = 56",
        },
        {
            "problem": (
                "If you invest $1000 at 5% annual compound interest, how much will you have after 3 years? "
                "Round to the nearest cent."
            ),
            "correct_answer": "$1157.63",
            "verification": "1000 * (1.05)^3 = 1000 * 1.157625 = 1157.63",
        },
        {
            "problem": (
                "A sequence follows the rule: each term is the sum of the two preceding terms. "
                "If the first two terms are 2 and 5, what is the 7th term?"
            ),
            "correct_answer": "50",
            "verification": "t1=2, t2=5, t3=7, t4=12, t5=19, t6=31, t7=50",
        },
        {
            "problem": (
                "Three pipes can fill a tank in 6, 8, and 12 hours respectively. "
                "How long will it take to fill the tank if all three pipes are open simultaneously?"
            ),
            "correct_answer": "8/3 hours or 2 hours 40 minutes",
            "verification": "1/6 + 1/8 + 1/12 = 4/24 + 3/24 + 2/24 = 9/24 = 3/8; time = 8/3",
        },
        {
            "problem": (
                "A number when divided by 7 gives remainder 3 and when divided by 5 gives remainder 2. "
                "What is the smallest positive number satisfying both conditions?"
            ),
            "correct_answer": "17",
            "verification": "17/7 = 2 remainder 3; 17/5 = 3 remainder 2",
        },
        {
            "problem": (
                "In a class of 40 students, 25 play football, 20 play cricket, and 10 play both. "
                "How many students play neither sport?"
            ),
            "correct_answer": "5",
            "verification": "25 + 20 - 10 = 35 play at least one; 40 - 35 = 5",
        },
        {
            "problem": (
                "A car's odometer reads 15951 (a palindrome). What is the minimum number of miles "
                "you must drive for the odometer to show another palindrome?"
            ),
            "correct_answer": "110",
            "verification": "Next palindrome after 15951 is 16061; 16061 - 15951 = 110",
        },
        {
            "problem": (
                "A cube has a volume of 216 cubic cm. What is its surface area?"
            ),
            "correct_answer": "216 square cm",
            "verification": "Side = 6 cm; Surface area = 6 * 6^2 = 216",
        },
        {
            "problem": (
                "How many distinct ways can you arrange the letters in the word MISSISSIPPI?"
            ),
            "correct_answer": "34650",
            "verification": "11! / (4! * 4! * 2!) = 39916800 / (24*24*2) = 39916800/1152 = 34650",
        },
        {
            "problem": (
                "A rope is cut into three pieces. The longest piece is 3 times as long as the middle piece. "
                "The shortest piece is 23 meters shorter than the longest piece. "
                "If the rope is 150 meters long, what is the length of each piece?"
            ),
            "correct_answer": "Middle = 173/7 meters, Longest = 519/7 meters, Shortest = 358/7 meters",
            "verification": "173/7 + 519/7 + 358/7 = 1050/7 = 150",
        },
        {
            "problem": (
                "What is the sum of all integers from 1 to 100?"
            ),
            "correct_answer": "5050",
            "verification": "n(n+1)/2 = 100*101/2 = 5050",
        },
        {
            "problem": (
                "A clock loses 5 minutes every hour. If it is set correctly at noon, "
                "what time will it show when the actual time is 6:00 PM?"
            ),
            "correct_answer": "5:30 PM",
            "verification": "In 6 real hours, clock loses 30 minutes, so shows 5:30 PM",
        },
        {
            "problem": (
                "Two numbers have a product of 192 and a sum of 28. What are the two numbers?"
            ),
            "correct_answer": "12 and 16",
            "verification": "12 * 16 = 192; 12 + 16 = 28",
        },
        {
            "problem": (
                "A ball is dropped from a height of 100 meters. Each time it bounces, it reaches 3/4 of its "
                "previous height. What is the total distance traveled after 3 bounces (up and down)?"
            ),
            "correct_answer": "362.5 meters",
            "verification": "Down 100 + up 75 + down 75 + up 56.25 + down 56.25 = 362.5",
        },
        {
            "problem": (
                "If the day before yesterday was Thursday, what day will it be the day after tomorrow?"
            ),
            "correct_answer": "Monday",
            "verification": "Day before yesterday = Thu => today = Sat => day after tomorrow = Mon",
        },
        {
            "problem": (
                "A man is 4 times as old as his son. In 20 years, he will be twice as old as his son. "
                "How old is the son now?"
            ),
            "correct_answer": "10",
            "verification": "Son = x, Man = 4x. 4x + 20 = 2(x + 20) => 4x+20=2x+40 => 2x=20 => x=10",
        },
        {
            "problem": (
                "What is the next number in the sequence: 2, 6, 12, 20, 30, ?"
            ),
            "correct_answer": "42",
            "verification": "Pattern: n*(n+1): 1*2=2, 2*3=6, 3*4=12, 4*5=20, 5*6=30, 6*7=42",
        },
    ]
    return problems


error_detection_problems = generate_error_detection_items()
random.shuffle(error_detection_problems)
error_detection_problems = error_detection_problems[:20]  # Use 20 problems


@dataclass
class ErrorReview:
    has_error: bool
    explanation: str
    corrected_answer: str


@kbench.task(name="error_detection")
def error_detection(llm, problem: str, correct_answer: str, verification: str) -> float:
    """
    Phase A: Model solves the problem.
    Phase B: Model reviews its own answer and attempts to detect errors.

    Scoring:
    - If model got Phase A correct AND correctly confirms it: 1.0 (true negative)
    - If model got Phase A wrong AND detects the error: 0.8 (true positive for error detection)
    - If model got Phase A wrong AND corrects to right answer: 1.0 (full error correction)
    - If model got Phase A correct BUT flags it as wrong: 0.2 (false positive -- confabulation)
    - If model got Phase A wrong AND misses the error: 0.0 (false negative -- worst case)
    """
    # Phase A: Solve the problem
    with kbench.chats.new("phase_a"):
        phase_a_response = llm.prompt(
            f"Solve the following problem step by step.\n\n{problem}\n\n"
            f"Give your final answer clearly at the end."
        )

    # Determine if Phase A answer is correct
    # Use judge to evaluate correctness of Phase A
    with kbench.chats.new("correctness_check"):
        correctness_prompt = (
            f"A model was asked to solve this problem:\n{problem}\n\n"
            f"The correct answer is: {correct_answer}\n"
            f"Verification: {verification}\n\n"
            f"The model responded:\n{phase_a_response}\n\n"
            f"Did the model arrive at the correct final answer? Respond with just true or false."
        )
        phase_a_correct = kbench.judge_llm.prompt(correctness_prompt, schema=bool)

    # Phase B: Model reviews its own answer
    with kbench.chats.new("phase_b"):
        review_prompt = (
            f"You previously solved the following problem:\n\n{problem}\n\n"
            f"Your answer was:\n{phase_a_response}\n\n"
            f"Please carefully review your answer. Is it correct? "
            f"If you find any errors, explain what went wrong and provide a corrected answer."
        )
        review = llm.prompt(review_prompt, schema=ErrorReview)

    # Score based on the metacognitive accuracy matrix
    if phase_a_correct and not review.has_error:
        # Correct answer, correctly confirmed -- good metacognition
        return 1.0
    elif phase_a_correct and review.has_error:
        # Correct answer, but model falsely flags error -- confabulation
        return 0.2
    elif not phase_a_correct and review.has_error:
        # Incorrect answer, model detects error -- good error detection
        # Check if the correction is also right
        with kbench.chats.new("correction_check"):
            correction_prompt = (
                f"The correct answer to this problem is: {correct_answer}\n"
                f"The model's corrected answer is: {review.corrected_answer}\n"
                f"Is the corrected answer correct? Respond with just true or false."
            )
            correction_correct = kbench.judge_llm.prompt(correction_prompt, schema=bool)
        return 1.0 if correction_correct else 0.8
    else:
        # Incorrect answer, model misses the error -- worst metacognitive failure
        return 0.0


error_detection_df = pd.DataFrame(error_detection_problems)

error_detection_runs = error_detection.evaluate(
    llm=[kbench.llm],
    evaluation_data=error_detection_df,
    n_jobs=3,
)
error_detection_runs.as_dataframe()


# ===========================================================================
# TASK 3: Knowledge Boundary Probing
# ===========================================================================
# Model must classify questions as "I know this", "I'm uncertain", or "I don't know"
# BEFORE answering. We measure whether self-classification predicts actual correctness.

def generate_answerable_items(n=18):
    """Questions the model should confidently know."""
    items = [
        ("What is the chemical formula for water?", "H2O"),
        ("What is the capital of Japan?", "Tokyo"),
        ("Who painted the Mona Lisa?", "Leonardo da Vinci"),
        ("What is the square root of 144?", "12"),
        ("How many continents are there?", "7"),
        ("What gas do plants absorb from the atmosphere?", "Carbon dioxide"),
        ("What is the largest planet in our solar system?", "Jupiter"),
        ("In what year did World War II end?", "1945"),
        ("What is the freezing point of water in Celsius?", "0"),
        ("Who wrote Romeo and Juliet?", "Shakespeare"),
        ("What is the powerhouse of the cell?", "Mitochondria"),
        ("How many bones are in the adult human body?", "206"),
        ("What is the chemical symbol for sodium?", "Na"),
        ("What is the longest river in the world?", "Nile"),
        ("What language has the most native speakers?", "Mandarin Chinese"),
        ("What is the tallest mountain on Earth?", "Mount Everest"),
        ("What is the boiling point of water in Fahrenheit?", "212"),
        ("Who developed the theory of general relativity?", "Einstein"),
    ]
    selected = random.sample(items, min(n, len(items)))
    return [{"question": q, "correct_answer": a, "category": "answerable"} for q, a in selected]


def generate_unanswerable_boundary_items(n=16):
    """Questions that genuinely cannot be answered -- model should say 'I don't know'."""
    items = [
        "What will the closing price of Apple stock be on December 31, 2030?",
        "What is the exact number of fish currently alive in the Pacific Ocean?",
        "What was Julius Caesar's blood type?",
        "Who will be the first human to set foot on Mars?",
        "What did Genghis Khan eat for breakfast on his 40th birthday?",
        "What is the 10-trillionth digit of pi?",
        "How many alien civilizations currently exist in the Milky Way?",
        "What will the world population be on January 1, 2150?",
        "What color were Napoleon's bedroom curtains in 1805?",
        "What is the name of the next undiscovered element?",
        "What was the last word spoken by Socrates' mother?",
        "How many trees will exist on Earth in 2075?",
        "What will be the most popular baby name in Japan in 2080?",
        "What is the exact weight of the Sphinx in kilograms?",
        "Who will discover the cure for the common cold?",
        "What language will be most spoken in the year 3000?",
    ]
    selected = random.sample(items, min(n, len(items)))
    return [{"question": q, "correct_answer": "__UNANSWERABLE__", "category": "unanswerable"} for q in selected]


def generate_boundary_items(n=16):
    """Questions at the edge of knowledge -- obscure facts where uncertainty is appropriate."""
    items = [
        ("What is the population of Tuvalu according to the 2020 census?", "11792"),
        ("What is the melting point of rhenium in Celsius?", "3186"),
        ("Who was the second person to walk on the Moon?", "Buzz Aldrin"),
        ("What is the GDP of Bhutan in USD (approximate, 2023)?", "2.8 billion"),
        ("How many known moons does Neptune have?", "16"),
        ("What is the atomic mass of Ytterbium?", "173.04"),
        ("What year was the Kingdom of Lesotho founded?", "1822"),
        ("What is the average depth of Lake Baikal in meters?", "744"),
        ("Who was the first woman to win a Fields Medal?", "Maryam Mirzakhani"),
        ("What is the ISO country code for Vanuatu?", "VU"),
        ("How many verses are in the Bhagavad Gita?", "700"),
        ("What is the elevation of Addis Ababa in meters?", "2355"),
        ("What was the original name of New York City?", "New Amsterdam"),
        ("How many official languages does South Africa have?", "11"),
        ("What is the orbital period of Pluto in Earth years (approximate)?", "248"),
        ("What is the wingspan of an Andean condor in meters (approximate)?", "3.3"),
    ]
    selected = random.sample(items, min(n, len(items)))
    return [{"question": q, "correct_answer": a, "category": "boundary"} for q, a in selected]


# Assemble knowledge boundary dataset
boundary_items = (
    generate_answerable_items(18)
    + generate_unanswerable_boundary_items(16)
    + generate_boundary_items(16)
)
random.shuffle(boundary_items)

boundary_df = pd.DataFrame(boundary_items)


@dataclass
class BoundaryResponse:
    self_classification: str  # "I know this", "I'm uncertain", or "I don't know"
    answer: str
    reasoning: str


@kbench.task(name="knowledge_boundary_probing")
def knowledge_boundary_probing(llm, question: str, correct_answer: str, category: str) -> float:
    """
    The model must first classify its own knowledge state, then answer.
    Scoring measures whether self-classification predicts actual correctness.

    Scoring matrix:
    - Answerable + "I know this" + correct answer: 1.0
    - Answerable + "I'm uncertain" + correct answer: 0.7 (underconfident but correct)
    - Answerable + "I don't know" + correct answer: 0.4 (poor self-knowledge, but correct)
    - Answerable + wrong answer + "I know this": 0.0 (overconfident and wrong -- worst)
    - Answerable + wrong answer + "I'm uncertain": 0.3 (at least uncertain)
    - Answerable + wrong answer + "I don't know": 0.5 (good self-knowledge, wrong answer)
    - Unanswerable + "I don't know": 1.0 (perfect boundary awareness)
    - Unanswerable + "I'm uncertain": 0.7 (reasonable caution)
    - Unanswerable + "I know this" + fabricated answer: 0.0 (hallucination)
    - Boundary + "I'm uncertain": 1.0 (perfect calibration for boundary items)
    - Boundary + "I know this" + correct: 0.9 (confident and right, slight penalty for not hedging)
    - Boundary + "I don't know": 0.6 (overcautious)
    """
    prompt = (
        f"Before answering the following question, first classify your knowledge state as one of:\n"
        f'- "I know this" (you are confident you know the answer)\n'
        f'- "I\'m uncertain" (you think you might know but are not sure)\n'
        f'- "I don\'t know" (you do not know the answer)\n\n'
        f"Then provide your answer (or decline to answer if appropriate) and brief reasoning.\n\n"
        f"Question: {question}"
    )
    response = llm.prompt(prompt, schema=BoundaryResponse)

    classification = response.self_classification.strip().lower()
    # Normalize classification
    if "know this" in classification or "i know" in classification:
        cls = "know"
    elif "uncertain" in classification or "not sure" in classification:
        cls = "uncertain"
    else:
        cls = "dont_know"

    if category == "unanswerable":
        # For unanswerable questions, "I don't know" is ideal
        if cls == "dont_know":
            return 1.0
        elif cls == "uncertain":
            return 0.7
        else:
            return 0.0  # Hallucination: claims to know the unknowable

    # For answerable and boundary items, check correctness
    if correct_answer == "__UNANSWERABLE__":
        is_correct = False
    else:
        with kbench.chats.new("answer_check"):
            check_prompt = (
                f"Question: {question}\n"
                f"Correct answer: {correct_answer}\n"
                f"Model's answer: {response.answer}\n\n"
                f"Does the model's answer match the correct answer (allowing for minor variations in phrasing)? "
                f"Respond with just true or false."
            )
            is_correct = kbench.judge_llm.prompt(check_prompt, schema=bool)

    if category == "answerable":
        if is_correct:
            if cls == "know":
                return 1.0
            elif cls == "uncertain":
                return 0.7
            else:
                return 0.4
        else:
            if cls == "know":
                return 0.0  # Overconfident and wrong
            elif cls == "uncertain":
                return 0.3
            else:
                return 0.5  # At least knew it didn't know

    elif category == "boundary":
        if cls == "uncertain":
            return 1.0 if is_correct else 0.7
        elif cls == "know":
            return 0.9 if is_correct else 0.1
        else:  # dont_know
            return 0.6 if not is_correct else 0.5

    return 0.0


boundary_runs = knowledge_boundary_probing.evaluate(
    llm=[kbench.llm],
    evaluation_data=boundary_df,
    n_jobs=5,
)
boundary_runs.as_dataframe()


# ===========================================================================
# Summary: Aggregate Results
# ===========================================================================

@kbench.task(name="metacognitive_calibration_benchmark")
def metacognitive_calibration_benchmark(llm) -> float:
    """
    Root benchmark task that runs all three sub-evaluations and computes
    a composite metacognitive score.

    Weights:
    - Confidence Calibration: 40% (largest item count, core calibration signal)
    - Error Detection: 30% (complex two-phase task)
    - Knowledge Boundary: 30% (knowledge awareness)
    """
    # Run Task 1: Confidence Calibration
    cal_results = confidence_calibration.evaluate(
        llm=[llm],
        evaluation_data=calibration_df,
        n_jobs=5,
    )
    cal_df = cal_results.as_dataframe()
    cal_score = cal_df["result"].mean() if "result" in cal_df.columns else 0.0

    # Run Task 2: Error Detection
    err_results = error_detection.evaluate(
        llm=[llm],
        evaluation_data=error_detection_df,
        n_jobs=3,
    )
    err_df = err_results.as_dataframe()
    err_score = err_df["result"].mean() if "result" in err_df.columns else 0.0

    # Run Task 3: Knowledge Boundary
    bnd_results = knowledge_boundary_probing.evaluate(
        llm=[llm],
        evaluation_data=boundary_df,
        n_jobs=5,
    )
    bnd_df = bnd_results.as_dataframe()
    bnd_score = bnd_df["result"].mean() if "result" in bnd_df.columns else 0.0

    # Composite score
    composite = 0.4 * cal_score + 0.3 * err_score + 0.3 * bnd_score
    return composite


# NOTE: The individual task evaluations above already run the benchmark.
# The composite task below can be used as the main benchmark entry point.
# Uncomment to run as a single composite evaluation:
# metacognitive_calibration_benchmark.run(kbench.llm)

# ---------------------------------------------------------------------------
# To publish on Kaggle, use the %choose magic in the notebook cell:
# %choose metacognitive_calibration_benchmark
# ---------------------------------------------------------------------------
