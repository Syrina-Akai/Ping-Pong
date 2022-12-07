import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

radius = 20  # radius of the circle
# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)
    image_height, image_width, _ = image.shape    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # Here is How to Get All the Coordinates
        cx, cy = hand_landmarks.landmark[10].x * image_width, hand_landmarks.landmark[10].y*image_height
        print((cx, cy))
        cv2.circle(image, (abs(int(cx)), abs(int(cy))), 10, (0, 255, 0), 10)
        """    for ids, landmrk in enumerate(hand_landmarks.landmark):
                # print(ids, landmrk)
                cx, cy = landmrk.x * image_width, landmrk.y*image_height
                print((cx, cy))
                cv2.circle(image, (abs(int(cx)), abs(int(cy))), 10, (0, 255, 0), 10)
                cv2.circle(image, (cx, cy), 10, (0, 255, 0), 10)
                font = cv2.FONT_HERSHEY_SIMPLEX
                # fontScale
                fontScale = 0.5
                # Blue color in BGR
                color = (255, 0, 0)
                # Line thickness of 2 px
                thickness = 2
                # Using cv2.putText() method
                image = cv2.putText(image, str((cx, cy)), (cx, cy), font, 
                            fontScale, color, thickness, cv2.LINE_AA)
            # print (ids, cx, cy)        
                mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)"""

        # we draw the circle in the secondary interface
        img = cv2.imread('Test1/white_image.jpeg')

    
        cv2.circle(img, (abs(int(cx)), img.shape[1] // 2), radius, (0, 0, 255), thickness = 15)
        cv2.imshow('img', img)
        cv2.waitKey(100)
    
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()