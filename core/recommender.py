"""
core/recommender.py
────────────────────────────────────────────────────────────────
Content-Based Filtering Engine — DecodeLabs Project 3
Pure Python implementation: no sklearn, no external ML libs.

Pipeline:
  1. Ingestion  → load dataset, normalize vocabulary
  2. Scoring    → TF-IDF vectors + cosine similarity
  3. Sorting    → rank by similarity score
  4. Filtering  → return Top-N results
"""

import math
import csv
from collections import Counter
from dataclasses import dataclass, field


# ─────────────────────────────────────────────────────────────
# DATA MODELS
# ─────────────────────────────────────────────────────────────

@dataclass
class JobRole:
    name: str
    skills: list[str]
    vector: list[float] = field(default_factory=list)


@dataclass
class RecommendationResult:
    rank: int
    role: str
    score: float
    matched_skills: list[str]
    role_skills: list[str]

    @property
    def match_percent(self) -> float:
        return round(self.score * 100, 1)


# ─────────────────────────────────────────────────────────────
# DATASET LOADER
# ─────────────────────────────────────────────────────────────

def load_dataset(filepath: str) -> list[JobRole]:
    """
    Load job roles from a CSV file.
    Expected columns: role, skills (comma-separated inside quotes)
    """
    roles = []
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                skills = [s.strip().lower() for s in row["skills"].split(",")]
                roles.append(JobRole(name=row["role"], skills=skills))
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset not found at: {filepath}")
    return roles


# ─────────────────────────────────────────────────────────────
# VOCABULARY
# ─────────────────────────────────────────────────────────────

def build_vocabulary(roles: list[JobRole]) -> list[str]:
    """
    Create a sorted list of every unique skill term across all roles.
    This forms the shared vector space — every role and the user
    will be represented as a vector of this length.
    """
    vocab = set()
    for role in roles:
        vocab.update(role.skills)
    return sorted(vocab)


# ─────────────────────────────────────────────────────────────
# TF-IDF
# ─────────────────────────────────────────────────────────────

def compute_tf(skill_list: list[str]) -> dict[str, float]:
    """
    Term Frequency = count(term) / total_terms
    Normalizes raw counts so longer skill lists don't dominate.
    """
    counts = Counter(skill_list)
    total = len(skill_list)
    return {term: count / total for term, count in counts.items()}


def compute_idf(roles: list[JobRole]) -> dict[str, float]:
    """
    Inverse Document Frequency = log((N+1) / (df+1)) + 1  (smoothed)
    Penalizes terms that appear in many roles (generic),
    rewards terms appearing in only a few roles (specific).
    The +1 smoothing prevents division-by-zero and zero IDF.
    """
    N = len(roles)
    all_terms = set(term for role in roles for term in role.skills)
    idf = {}
    for term in all_terms:
        df = sum(1 for role in roles if term in role.skills)
        idf[term] = math.log((N + 1) / (df + 1)) + 1
    return idf


def build_tfidf_vector(
    skill_list: list[str],
    vocabulary: list[str],
    idf_scores: dict[str, float]
) -> list[float]:
    """
    Map a skill list → a TF-IDF weighted numerical vector.
    Each dimension = TF(term) × IDF(term), or 0 if term absent.
    """
    tf = compute_tf([s.lower() for s in skill_list])
    return [
        tf.get(term, 0.0) * idf_scores.get(term, 1.0)
        for term in vocabulary
    ]


# ─────────────────────────────────────────────────────────────
# COSINE SIMILARITY
# ─────────────────────────────────────────────────────────────

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    cos(θ) = (A · B) / (‖A‖ × ‖B‖)

    Measures angular alignment — invariant to vector magnitude.
    A user with 3 skills vs a role with 10 skills: still fair.
    Returns 0.0 for zero vectors (cold start protection).
    """
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a ** 2 for a in vec_a))
    mag_b = math.sqrt(sum(b ** 2 for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


# ─────────────────────────────────────────────────────────────
# MAIN RECOMMENDER
# ─────────────────────────────────────────────────────────────

class TechStackRecommender:
    """
    Content-Based Filtering recommender.
    Instantiate once, call recommend() on each user query.
    """

    def __init__(self, dataset_path: str):
        self.roles = load_dataset(dataset_path)
        self.vocabulary = build_vocabulary(self.roles)
        self.idf_scores = compute_idf(self.roles)

        # Pre-compute TF-IDF vectors for all roles (done once at startup)
        for role in self.roles:
            role.vector = build_tfidf_vector(
                role.skills, self.vocabulary, self.idf_scores
            )

    def recommend(
        self,
        user_skills: list[str],
        top_n: int = 3
    ) -> list[RecommendationResult]:
        """
        Full 4-step pipeline:
        1. Build user TF-IDF vector from input skills
        2. Score every role via cosine similarity
        3. Sort descending by score
        4. Return top_n results
        """
        # Step 1 — Ingestion: vectorize user profile
        user_vector = build_tfidf_vector(
            [s.lower() for s in user_skills],
            self.vocabulary,
            self.idf_scores
        )

        # Step 2 — Scoring
        scored = []
        for role in self.roles:
            score = cosine_similarity(user_vector, role.vector)
            matched = [
                s for s in user_skills
                if s.lower() in role.skills
            ]
            scored.append((role, score, matched))

        # Step 3 — Sorting
        scored.sort(key=lambda x: x[1], reverse=True)

        # Step 4 — Filtering
        results = []
        for rank, (role, score, matched) in enumerate(scored[:top_n], 1):
            results.append(RecommendationResult(
                rank=rank,
                role=role.name,
                score=score,
                matched_skills=matched,
                role_skills=role.skills
            ))

        return results

    @property
    def all_known_skills(self) -> list[str]:
        """Return all skills in the vocabulary (for UI autocomplete)."""
        return self.vocabulary

    @property
    def role_count(self) -> int:
        return len(self.roles)

    @property
    def skill_count(self) -> int:
        return len(self.vocabulary)
