import cv2
import os
import argparse

def extract_frames(video_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f'Total frames in video {video_path}: {total_frames}')

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(video_path))[0]}_frame_{frame_count:04d}.jpg')
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    print(f'Total frames extracted from {video_path}: {frame_count}')

def main(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_path = os.path.join(input_dir, filename)
            extract_frames(video_path, output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from video files in a folder")
    parser.add_argument("--input_dir", type=str, required=True, help="Input directory containing video files")
    parser.add_argument("--output_dir", type=str, required=True, help="Output directory to save extracted frames")

    args = parser.parse_args()
    main(args.input_dir, args.output_dir)
