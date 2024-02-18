import cv2
import moviepy.editor as mp
import speech_recognition as sr
from moviepy.editor import VideoFileClip, concatenate_videoclips, clips_array
import os
import tempfile

def merge_letter_videos(word, assets_folder):
    letter_clips = []
    for letter in word:
        letter_lower = letter.lower()
        letter_video_path = os.path.join(assets_folder, f'{letter_lower}.mp4')
        if os.path.isfile(letter_video_path):
            letter_clip = VideoFileClip(letter_video_path)
            letter_clips.append(letter_clip)
        else:
            print(f"No video found for letter: {letter_lower}")
    if not letter_clips:
        print("No valid videos found for the word.")
        return None
    final_clip = concatenate_videoclips(letter_clips)
    return final_clip

def merge_word_videos(words, assets_folder):
    video_clips = []
    for word in words:
        word_lower = word.lower()
        word_video_path = os.path.join(assets_folder, f'{word_lower}.mp4')
        if os.path.isfile(word_video_path):
            video_clip = VideoFileClip(word_video_path)
            video_clips.append(video_clip)
        else:
            print(f"No video found for word: {word_lower}")
            print(f"Splitting '{word}' into letters...")
            letter_video = merge_letter_videos(word, assets_folder)
            if letter_video is not None:
                video_clips.append(letter_video)
    if not video_clips:
        print("No valid videos found.")
        return None
    final_clip = concatenate_videoclips(video_clips)
    return final_clip

def extract_audio_as_text(video_path):
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    temp_audio_path = "temp_audio.wav"
    audio.write_audiofile(temp_audio_path)
    r = sr.Recognizer()
    with sr.AudioFile(temp_audio_path) as source:
        audio_data = r.record(source)
        audio_text = r.recognize_google(audio_data)
    return audio_text

def generate_combined_video(extracted_text, video_path):
    words = extracted_text.split()
    assets_folder = 'assets'
    if not words:
        print("Please enter a sentence.")
    else:
        print(f"Generating combined video for text: {extracted_text}...")
        video = merge_word_videos(words, assets_folder)
        if video is not None:
            print("Combined video generated successfully!")
            continuous_video_path = "output_continuous_video.mp4"
            video.write_videofile(continuous_video_path, codec="libx264")
            uploaded_video = VideoFileClip(video_path)
            uploaded_video = uploaded_video.resize(height=video.h)
            final_video = clips_array([[uploaded_video, video]])
            final_video_path = "final_combined_video.mp4"
            final_video.write_videofile(final_video_path, codec="libx264")
            os.remove(continuous_video_path)
            os.remove(video_path)
            return final_video_path

def main():
    video_path = "your_video_path.mp4"  # Provide the path to your video
    extracted_text = extract_audio_as_text(video_path)
    print("Extracted Text from Uploaded Video:")
    print(extracted_text)
    final_video_path = generate_combined_video(extracted_text, video_path)
    if final_video_path:
        cap = cv2.VideoCapture(final_video_path)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow('Frame',frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
