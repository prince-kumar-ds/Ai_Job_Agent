from processing.skill_extractor import extract_keywords_with_scores

def match_job(resume_text, job_text, keywords, keyword_embeddings):
    
    resume_skills = extract_keywords_with_scores(
        resume_text, keywords, keyword_embeddings
    )

    job_skills = extract_keywords_with_scores(
        job_text, keywords, keyword_embeddings
    )

    # ✅ Convert to dict FIRST
    resume_dict = dict(resume_skills)
    job_dict = dict(job_skills)

    # ✅ THEN apply filter
    if len(job_dict) < 3:
        return {
            "score": 0,
            "matched": [],
            "missing": [],
            "note": "Too few skills detected"
        }

    matched = []
    missing = []

    score = 0
    total = 0

    for skill, job_score in job_dict.items():
        total += job_score

        if skill in resume_dict:
            matched.append(skill)
            score += min(resume_dict[skill], job_score)
        else:
            missing.append(skill)

    match_score = (score / total) * 100 if total > 0 else 0

    return {
        "score": round(min(match_score, 95), 2),
        "matched": matched,
        "missing": missing
    }