# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 05:18:55 2026

@author: Dylan
"""


from config.settings import KEYWORDS, HIGH_FIT_THRESHOLD, MEDIUM_FIT_THRESHOLD

def get_matched_keywords(title: str, skills: str, description: str) -> list[str]:
    text = f"{title} {skills} {description}".lower()
    matched = []

    for keyword in KEYWORDS:
        if keyword in text:
            matched.append(keyword)

    return matched

def score_job(title: str, skills: str, description: str) -> int:
    matched = get_matched_keywords(title, skills, description)
    score = sum(KEYWORDS[keyword] for keyword in matched)
    return score


def recommend(score: int) -> str:
    if score >= HIGH_FIT_THRESHOLD:
        return "High Fit"
    if score >= MEDIUM_FIT_THRESHOLD:
        return "Medium Fit"
    return "Low Fit"