# Streaming Batch Job Outputs on an LSF Cluster

If you have experience running batch jobs on an LSF cluster, you may be familiar with constantly `bpeek`ing the job ID to monitor the job's progress. This is fine if you just want to periodically check it, but for scenarios like babysitting a deep learning training run, it can be horribly inefficient. Ideally, you could see the progress of the job in real-time, like you can in an interactive session.

This repository allows you to stream the outputs of the job's `stdout` and `stderr` at arbitrary time intervals. The default is to check for new outputs every 0.1 seconds, but you can modify this in the Python script `stream_bsub.py`.

## Setup

1. `git clone` this repository

2. Add the following line to your `~/.bashrc` (or `~/.zshrc`, or whatever shell config you use): 

`alias stream_bsub="/path/to/bsub_streaming/stream_bsub.py"`

for instance, if I clone the repository to the folder `/home/adam`, I would add to my `/home/adam/.bashrc` file:

`alias stream_bsub="/home/adam/bsub_streaming/stream_bsub.py"`

3. Run `source ~/.bashrc` (or whatever shell config you use)

Now you can use the command `stream_bsub`, demonstrated in the next section.

## Use

After setting up the tool and submitting a batch job, you can run 

`stream_bsub <JOB_ID>` 

in your bash/zsh/etc session, and it will stream all logging/print statements from your job.

If you don't provide a job ID as an argument to `bpeek`, it will show you a snapshot of the latest job submitted. In this spirit, the `stream_bsub.py` script also will stream the latest job if you don't explicitly provide a job ID. To stream the latest job, just enter in the shell

`stream_bsub`

It's that simple.