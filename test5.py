import cv2
vidcap = cv2.VideoCapture('https://s3.amazonaws.com/vibbidi-us/videos/video_9857BEF2AD46441A896C49F723DEE157.mp4')
vidcap.set(cv2.CAP_PROP_POS_MSEC,3000)      # just cue to 20 sec. position
success,image = vidcap.read()
if success:
    cv2.imwrite("frame3sec.jpg", image)     # save frame as JPEG file
    cv2.imshow('joy',image)
    cv2.waitKey()