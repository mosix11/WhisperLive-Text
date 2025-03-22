

from whisper_live.client import TranscriptionClient
import os
import datetime


last_text = ""

def sample_callback(text, is_final):
    global last_text
    global client

    # print(text[-1])
    if is_final and text != last_text:
        # print("\r" + text[-1], end='', flush=True)
        last_text = text
        client.paused = True
        # # Define the command to be run
        # command = f'echo "{text[-1]}" | piper --model en_US-lessac-medium --output-raw | aplay -r 22050 -f S16_LE -t raw -'
        # # Run the command
        # subprocess.run(command, shell=True, check=True)
        # print("\r" + text[-1], end='', flush=True)
        print(text[-1])


        client.paused = False
    #   else:
        # os.system("cls" if os.name == "nt" else "clear")
        # print(text[-1], end='', flush=True)

# def sample_callback(segments, is_final):
#     # Instead of clearing the terminal, print every segment with its timing.
#     for seg in segments:
#         start = seg.get("start", "N/A")
#         end = seg.get("end", "N/A")
#         try:
#             duration = float(end) - float(start)
#         except Exception:
#             duration = 0.0
#         print(f"[{start} - {end} (dur: {duration:.2f}s)] {seg['text']}")

last_printed_index = 0
recording_start_time = None

# def sample_callback(segments, is_final):
#     """
#     Callback that prints only the new segments with a formatted timestamp.
#     The format is: [YYYY-MM-DD, HH:MM:SS, (dur: x.xx s)] <text>
#     It appends only the new segments (avoiding duplicate prints) and does not clear the screen.
#     """
#     global last_printed_index, recording_start_time
#     global client


#     # On the very first callback, capture the current time as the recording start time.
#     if recording_start_time is None and segments:
#         recording_start_time = datetime.datetime.now()

#     # Only process segments that haven't been printed yet.
#     new_segments = segments[last_printed_index:]
#     for seg in new_segments:
#         try:
#             seg_start_offset = float(seg.get("start", "0.0"))
#             seg_end = float(seg.get("end", "0.0"))
#         except Exception:
#             seg_start_offset = 0.0
#             seg_end = 0.0
#         seg_duration = seg_end - seg_start_offset

#         # Calculate the absolute start time using the recording start time and the segment's offset.
#         abs_start_time = recording_start_time + datetime.timedelta(seconds=seg_start_offset)
#         date_str = abs_start_time.strftime("%Y-%m-%d")
#         time_str = abs_start_time.strftime("%H:%M:%S")

#         # Print in the desired format.
#         print(f"[{date_str}, {time_str}, (dur: {seg_duration:.2f}s)] {seg['text']}")
        
    
#     # Update the index so that next time only the new segments are printed.
#     last_printed_index = len(segments)


# def process_transcript_with_lm(transcript):
#     """
#     Placeholder function for processing the complete transcript with a language model.
#     Replace this with your actual language model integration.
#     """
#     # For demonstration, we simply return a dummy response.
#     return f"Processed transcript: {transcript}"

# def sample_callback(segments, is_final):
#     """
#     Callback function that:
#       - Appends only new transcript segments to the terminal.
#       - Prints each new segment with its start date/time and duration.
#       - When is_final is True (indicating the speaker stopped), it pauses the client,
#         passes the full transcript to a language model, and then resumes processing.
#     Output format: [YYYY-MM-DD, HH:MM:SS, (dur: x.xx s)] <transcribed text>
#     """
#     global last_printed_index, recording_start_time, client

#     # If the client is already paused, skip processing new segments.
#     if getattr(client, 'paused', False):
#         return

#     # Set recording start time on first callback.
#     if recording_start_time is None and segments:
#         recording_start_time = datetime.datetime.now()

#     # Process only the new segments (avoiding reprinting everything).
#     new_segments = segments[last_printed_index:]
#     for seg in new_segments:
#         try:
#             seg_start_offset = float(seg.get("start", "0.0"))
#             seg_end = float(seg.get("end", "0.0"))
#         except Exception:
#             seg_start_offset = 0.0
#             seg_end = 0.0
#         seg_duration = seg_end - seg_start_offset

#         # Calculate the absolute start time using the recording start time and the segment offset.
#         abs_start_time = recording_start_time + datetime.timedelta(seconds=seg_start_offset)
#         date_str = abs_start_time.strftime("%Y-%m-%d")
#         time_str = abs_start_time.strftime("%H:%M:%S")

#         # Print the segment in the desired format.
#         print(f"[{date_str}, {time_str}, (dur: {seg_duration:.2f}s)] {seg['text']}")
        
#     # If the speaker has finished speaking, pause the client, process the transcript with LM, then resume.
#     if is_final:
#         print('is final')
#         full_transcript = " ".join([seg["text"] for seg in new_segments])
#         if not len(full_transcript.strip()) <= 1:
            
#             client.paused = True
#             lm_response = process_transcript_with_lm(full_transcript)
#             print("LM Response:", lm_response)
#             client.paused = False

#     # Update the index so that next time only new segments are printed.
#     last_printed_index = len(segments)



client = TranscriptionClient(
  "localhost",
  9090,
  lang="en",
  translate=False,
  model="distil-large-v3",
  use_vad=True,
  max_clients=1,
  max_connection_time=600,
  mute_audio_playback=False,
  callback=sample_callback
)

client()
