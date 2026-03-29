import json

def process_jobs(raw_data):
    jobs = []

    for job in raw_data["data"]:
        jobs.append({
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "description": job.get("job_description") or "",
            "location": job.get("job_city"),
            "link": job.get("job_apply_link") or job.get("job_google_link") or None
        })

    # Save cleaned jobs
    with open("data/processed_jobs.json", "w") as f:
        json.dump(jobs, f, indent=4)

    return jobs