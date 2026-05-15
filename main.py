"""
main.py — CLI entry point
Run: python main.py
"""

from core.recommender import TechStackRecommender
import os

DATASET = os.path.join(os.path.dirname(__file__), "data", "raw_skills.csv")


def main():
    engine = TechStackRecommender(DATASET)

    print("\n" + "═" * 60)
    print("  🎯  TECH STACK RECOMMENDER — DecodeLabs Project 3")
    print("═" * 60)
    print(f"\n  Dataset: {engine.role_count} roles | {engine.skill_count} unique skills\n")
    print("  Enter at least 3 skills (comma-separated):")

    raw = input("  > ").strip()
    skills = [s.strip().lower() for s in raw.split(",") if s.strip()]

    if len(skills) < 3:
        print(f"\n  ⚠️  Need at least 3 skills. You entered {len(skills)}.")
        return

    results = engine.recommend(skills, top_n=3)

    print(f"\n  Your profile: {skills}")
    print("\n" + "─" * 60)
    medals = ["🥇", "🥈", "🥉"]
    for r in results:
        print(f"\n  {medals[r.rank-1]}  {r.role}")
        print(f"      Score   : {r.score:.4f}  ({r.match_percent}% match)")
        print(f"      Matched : {', '.join(r.matched_skills) or 'indirect match'}")
        print(f"      Requires: {', '.join(r.role_skills[:5])}...")
    print("\n" + "═" * 60)


if __name__ == "__main__":
    main()
