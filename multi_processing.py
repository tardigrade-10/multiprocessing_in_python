import cv2 as cv
import time
import subprocess as sp
import multiprocessing as mp
from os import remove


face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')


def get_video_frame_details(file):
    cap = cv.VideoCapture(file)

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

def process_video_multiprocessing(group_number, video_file):
    # Read video file
    cap = cv.VideoCapture(video_file)

    cap.set(cv.CAP_PROP_POS_FRAMES, frame_jump_unit * group_number)

    # get height, width and frame count of the video
    width, height = (
            int(cap.get(cv.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        )
    no_of_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv.CAP_PROP_FPS))
    proc_frames = 0

    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv.VideoWriter()
    output_file_name = "output_multi1.mp4"
    out.open("output_{}.mp4".format(group_number), fourcc, fps, (width, height), True)
    try:
        while proc_frames < frame_jump_unit:
            ret, frame = cap.read()
            if not ret:
                break

            im = frame
            # Perform face detection on each frame
            bboxes = face_cascade.detectMultiScale(im)

            # Loop through list (if empty this will be skipped) and overlay green bboxes
            for i in bboxes:
                cv.rectangle(im, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 3)
            
            # write the frame
            out.write(im)

            proc_frames += 1
    except:
        # Release resources
        cap.release()
        out.release()

    # Release resources
    cap.release()
    out.release()

def combine_output_files(num_processes):
    # Create a list of output files and store the file names in a txt file
    list_of_output_files = ["output_{}.mp4".format(i) for i in range(num_processes)]
    with open("list_of_output_files.txt", "w") as f:
        for t in list_of_output_files:
            f.write("file {} \n".format(t))

    # use ffmpeg to combine the video output files
    ffmpeg_cmd = "ffmpeg -y -loglevel error -f concat -safe 0 -i list_of_output_files.txt -vcodec copy " + output_file_name
    sp.Popen(ffmpeg_cmd, shell=True).wait()

    # Remove the temporary output files
    for f in list_of_output_files:
        remove(f)
    remove("list_of_output_files.txt")

def multi_process(file):
    print("Video processing using {} processes...".format(num_processes))
    start_time = time.time()

    # Parallel execution of a function across multiple input values
    p = mp.Pool(num_processes)
    p.map(process_video_multiprocessing, (range(num_processes), file))

    combine_output_files(num_processes)

    end_time = time.time()

    total_processing_time = end_time - start_time
    print("Time taken: {}".format(total_processing_time))
    # print("FPS : {}".format(frame_count/total_processing_time))

file_name = "sample.mp4"
output_file_name = "output.mp4"
frame_count = get_video_frame_details(file_name)
num_processes = mp.cpu_count()
print("Number of CPU: " + str(num_processes))
frame_jump_unit =  frame_count// num_processes
multi_process(file_name)