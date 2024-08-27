import os
import cv2
import argparse


def collect_hd_overlay_images(base_folder):
    image_list = []
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            hd_overlay_path = os.path.join(root, dir_name, 'hd_overlay.png')
            if os.path.isfile(hd_overlay_path):
                image_list.append(hd_overlay_path)
    return sorted(image_list)


def create_video_from_images(image_list, output_video_path, fps=30):
    if not image_list:
        print("No images to process.")
        return

    # Read the first image to get dimensions
    first_image = cv2.imread(image_list[0])
    height, width, layers = first_image.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    for image_path in image_list:
        img = cv2.imread(image_path)
        video.write(img)

    video.release()
    print(f"Video saved to {output_video_path}")


def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="Create a video from hd_overlay.png images in subfolders")

    # Add --input-folder argument
    parser.add_argument('--input-folder', type=str, required=True, help='Path to the input folder')

    # Add --output-folder argument
    parser.add_argument('--output-folder', type=str, required=True, help='Path to the output folder')

    # Parse command-line arguments
    args = parser.parse_args()

    # Collect images and create video
    image_list = collect_hd_overlay_images(args.input_folder)
    output_video_path = os.path.join(args.output_folder, 'video.mp4')
    create_video_from_images(image_list, output_video_path)


if __name__ == "__main__":
    main()
