# multiprocessing_in_python

I first read video from the disk, perform face detection, and write the video with output of face detection (bounding boxes) back to the disk.

Started with defining a method to process video using single process. 
This is the way how we would normally read a video file, process each frame and write the output frames back to the disk.

In multi file, the video processing job, that is normally done using one process, 
is now divided equally amongst the total number of processors available on the executing device.

https://github.com/tardigrade-10/multiprocessing_in_python/blob/main/multi_processing.mp4
