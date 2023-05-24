import os
import cv2

IMG_DIR = "./input_images"
VID_DIR = "./input_videos"
OUT_DIR = "./output_images"
if not os.path.isdir(OUT_DIR):
    os.makedirs(OUT_DIR)

def video_frame_generator(filename):
    """A generator function that returns a frame on each 'next()' call.

    Will return 'None' when there are no frames left.

    Args:
        filename (string): Filename.

    Returns:
        None.
    """

    filename = os.path.join(VID_DIR, filename)
    video = cv2.VideoCapture(filename)

    # Do not edit this while loop
    while video.isOpened():
        ret, frame = video.read()

        if ret:
            yield frame
        else:
            break

    # Close video (release) and yield a 'None' value. (add 2 lines)
    video.release()
    yield None


def mp4_video_writer(filename, frame_size, fps=20):
    """Opens and returns a video for writing.

    Use the VideoWriter's `write` method to save images.
    Remember to 'release' when finished.

    Args:
        filename (string): Filename for saved video
        frame_size (tuple): Width, height tuple of output video
        fps (int): Frames per second
    Returns:
        VideoWriter: Instance of VideoWriter ready for writing
    """
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    return cv2.VideoWriter(os.path.join(OUT_DIR, filename), fourcc, fps, frame_size)


def save_image(filename, image):
    """Convenient wrapper for writing images to the output directory."""
    cv2.imwrite(os.path.join(OUT_DIR, filename), image)

def read_image(filename):
    return cv2.imread(os.path.join(IMG_DIR, filename))