#!/usr/bin/env python3
import subprocess
import sys
import time

def get_latest_job_id():
    """Fetches the latest running or pending LSF job ID."""
    try:
        job_list_cmd = ["bjobs", "-o", "jobid", "-noheader"]
        job_list = subprocess.run(job_list_cmd, capture_output=True, text=True)

        if job_list.returncode != 0 or not job_list.stdout.strip():
            print("No running or pending jobs found.")
            return None

        # Get the most recent job (last in the list)
        job_ids = job_list.stdout.strip().split("\n")
        return job_ids[-1].strip()

    except Exception as e:
        print(f"Error fetching latest job ID: {e}")
        return None

def stream_lsf_output(job_id, interval=0.1):
    """
    Stream the output of an LSF job given its job ID.

    Parameters:
    - job_id (str): The LSF job ID.
    - interval (int): Time in seconds between checks.
    """
    try:
        print(f"Streaming output for job {job_id}...\n")
        seen_lines = set()

        while True:
            # Check job status
            job_status_cmd = ["bjobs", "-o", "stat", "-noheader", job_id]
            job_status = subprocess.run(job_status_cmd, capture_output=True, text=True)

            if job_status.returncode != 0:
                print(f"Error checking job status: {job_status.stderr.strip()}")
                break

            status = job_status.stdout.strip()
            if status in ["EXIT", "DONE"]:
                print(f"\nJob {job_id} has finished with status: {status}. Stopping output stream.")
                break

            # Fetch job output
            bpeek_cmd = ["bpeek", job_id]
            process = subprocess.Popen(bpeek_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            for line in iter(process.stdout.readline, ''):
                line = line.strip()
                if line and line not in seen_lines:
                    print(line)
                    seen_lines.add(line)
            process.stdout.close()

            for line in iter(process.stderr.readline, ''):
                line = line.strip()
                if line and line not in seen_lines:
                    print(line)
                    seen_lines.add(line)
            process.stderr.close()

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nStreaming interrupted by user.")

if __name__ == "__main__":
    job_id = sys.argv[1] if len(sys.argv) > 1 else None

    if not job_id:
        job_id = get_latest_job_id()
        if not job_id:
            sys.exit("No job ID provided and no running jobs found.")

    stream_lsf_output(job_id)