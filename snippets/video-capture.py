import cv2, time

video = cv2.VideoCapture(0)



while(True):
    ret, frame = video.read()
    cv2.imshow("capturing", frame)
    print(frame)
    


    key = cv2.waitKey(1)
    if key == ord('q'): 
        break
   

video.release()

cv2.destroyAllWindows()
