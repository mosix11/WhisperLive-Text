from whisper_live.client import TranscriptionClient
import os
import time
import subprocess
import torch


def my_transcription_handler(transcript):
    print("Final text received:", transcript)

client = TranscriptionClient(
  "localhost",
  9090,
  lang="en",
  translate=False,
  model="distil-large-v3",
  use_vad=True,
  max_clients=1,
  max_connection_time=600,
  save_output_recording=False,
  mute_audio_playback=False,
  log_transcription=False,
  on_final_transcription=my_transcription_handler
)

client()

