import subprocess
import os


class Transcription:
    def __init__(self, transcriber, output_folder):
        self.transcriber = transcriber
        self.transcription_output_folder = output_folder

    def transcribe_audio_files(self, input_folder):
        if not os.path.exists(input_folder):
            print("Input folder not found.")
            return
        
        for file_name in os.listdir(input_folder):
            file_path = os.path.join(input_folder, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith(('.mp3', '.wav')):
                self.transcribe_audio_file(file_path)
            else:
                print(f"Skipping non-audio file: {file_name}")

    def transcribe_audio_file(self, audio_path):
        transcript = self.transcriber.transcribe(audio_path)
        file_path = os.path.join(self.transcription_output_folder, f"{os.path.basename(audio_path)}.txt")
        with open(file_path, "w") as f:
            f.write(transcript.text)

    def convert_video_to_audio_ffmpeg(self, video_file, output_ext="mp3", output_folder="extracted_audio"):
        """Converts video to audio directly using `ffmpeg` command
        with the help of subprocess module"""
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Get the filename without extension
        filename, _ = os.path.splitext(os.path.basename(video_file))

        # Define the full path to the output file in the subfolder
        output_path = os.path.join(output_folder, f"{filename}.{output_ext}")

        # Call ffmpeg to convert video to audio
        subprocess.call(["ffmpeg", "-y", "-i", video_file, output_path], 
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)

    def convert_videos(self, input_folder):
        # Check if the input folder exists
        if not os.path.exists(input_folder):
            print("Input folder not found.")
            return

        # Loop through files in the input folder
        for file_name in os.listdir(input_folder):
            file_path = os.path.join(input_folder, file_name)
            
            # Check if the file is a video file
            if os.path.isfile(file_path) and file_name.lower().endswith(('.mp4', '.avi', '.mov')):
                self.convert_video_to_audio_ffmpeg(file_path)
            else:
                print(f"Skipping non-video file: {file_name}")
