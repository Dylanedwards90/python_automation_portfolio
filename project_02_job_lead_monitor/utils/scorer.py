# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 05:18:55 2026

@author: Dylan
"""


from config.settings import KEYWORDS, HIGH_FIT_THRESHOLD, MEDIUM_FIT_THRESHOLD

def score_job(title: str, skills: str, description: str) -> int:
    text = f"{title} {skills} {description}".lower()
    score = 0

    for keyword, points in KEYWORDS.items():
        if keyword in text:
            score += points

    return score


def recommend(score: int) -> str:
    if score >= HIGH_FIT_THRESHOLD:
        return "High Fit"
    if score >= MEDIUM_FIT_THRESHOLD:
        return "Medium Fit"
    return "Low Fit"