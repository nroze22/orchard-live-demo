
import os
from openclaw.tools import cron

cron_job_name = "X Bookmark Monitor for @nroze22"
user_discord_id = "854932071196393472" # Nathan's Discord ID

# Check if job already exists (for idempotency)
status = cron(action="list", includeDisabled=True)
job_exists = False
if status and "jobs" in status:
    for job in status["jobs"]:
        if job.get("name") == cron_job_name:
            job_exists = True
            print(f"Cron job \'{cron_job_name}\\' already exists. Skipping add.")
            break

if not job_exists:
    print(f"Adding cron job \'{cron_job_name}\'...")
    cron_res = cron(
        action="add",
        job={
            "name": cron_job_name,
            "schedule": {"kind": "every", "everyMs": 28800000}, # Every 8 hours
            "payload": {
                "kind": "agentTurn",
                "message": "python3 skills/x-monitor/main.py nroze22", # Command to execute the script
                "model": "kimi-k2.5", # Use Kimi 2.5 for cron execution
                "thinking": "low",
                "deliver": True, 
                "channel": "discord", 
                "to": user_discord_id 
            },
            "sessionTarget": "isolated",
            "enabled": True
        }
    )
    print(f"Cron job add response: {cron_res}")
