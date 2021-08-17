import cv2 as cv
import time
from os import remove

face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')


def get_video_frame_details(file_name):
    cap = cv.VideoCapture(file_name)

        # get height, width and frame count of the video
    width, height = (
            int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        )
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv.CAP_PROP_FPS))

    print("Video frame count = {}".format(frame_count))
    print("Video fps = {}".format(fps))
    print("Width = {}, Height = {}".format(width, height))

    return frame_count

def process_video():
    # Read video file
    cap = cv.VideoCapture(file_name)

    # get height, width and frame count of the video
    width, height = (
            int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        )
    fps = int(cap.get(cv.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv.VideoWriter()
    output_file_name = "output_single.mp4"
    out.open(output_file_name, fourcc, fps, (width, height), True)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            im = frame
            # Perform face detection of frame
            bboxes = face_cascade.detectMultiScale(im)

            # Loop through list (if empty this will be skipped) and overlay green bboxes
            for i in bboxes:
                cv.rectangle(im, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 3)
            
            # write the frame
            out.write(im)
    except:
        # Release resources
        cap.release()
        out.release()
        

    # Release resources
    cap.release()
    out.release()


def single_process():
    print("Video processing using single process...")
    start_time = time.time()
    process_video()
    end_time = time.time()
    total_processing_time = end_time - start_time
    print("Time taken: {}".format(total_processing_time))
    
file_name = "sample.mp4"
output_file_name = "output.mp4"
get_video_frame_details(file_name)
single_process()