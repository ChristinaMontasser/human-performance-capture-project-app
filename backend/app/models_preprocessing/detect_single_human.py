import cv2
import torch
import argparse
import os
import sys


def detect_single_person_in_video(model, video_path, conf_threshold=0.5):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return False

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        results = model(frame)
        persons = [d for d in results.xyxy[0] if int(d[-1]) == 0 and d[4] > conf_threshold]
        if len(persons) != 1:
            cap.release()
            return False

    cap.release()
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Detect if a video contains a single person.')
    parser.add_argument('--model_path', type=str, required=True, help='Path to the .pt model file')
    parser.add_argument('--video_path', type=str, required=True, help='Path to the video file')
    parser.add_argument('--conf_threshold', type=float, default=0.5, help='Confidence threshold for detecting persons')

    args = parser.parse_args()

    model = torch.hub.load('ultralytics/yolov5', 'custom', path=args.model_path)

    is_single_person = detect_single_person_in_video(model, args.video_path, args.conf_threshold)
    print(f"Video {os.path.basename(args.video_path)} contains a single person: {is_single_person}")

    if is_single_person:
        sys.exit(0)
    else:
        sys.exit(1)


