
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For static images:
IMAGE_FILES = []
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      print('hand_landmarks:', hand_landmarks)
      print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )
      mp_drawing.draw_landmarks(
          annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imwrite(
        '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))

# For webcam input:
plot_x = []
plot_y = []
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
        wanted_x = []
        wanted_y = []
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

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)



        if results.multi_hand_landmarks:

              x1 = []
              for hand_landmarks in results.multi_hand_landmarks:
                    x = []
                    y = []
                    t = str(list(hand_landmarks.landmark)).replace(':',' ').replace(',',' ').replace('\n',' ').split(' ')

                    for j in range(2,len(t),11):
                        x.append(float(t[j]))

                    for j in range(5,len(t),11):
                          y.append(float(t[j]))



                    if len(x1)==0:

                        x1 = x.copy()
                        y1 = y.copy()



              wanted_x.append(x1[8] )
              wanted_x.append(x1[4] )
              wanted_x.append(x[8])
              wanted_x.append(x[4])
              wanted_y.append(y1[8] )
              wanted_y.append(y1[4] )
              wanted_y.append(y[8])
              wanted_y.append(y[4])
              if len(wanted_x)>0:


                    xmin = np.min(np.array(wanted_x))
                    xmax = np.max(np.array(wanted_x))
                    ymin = np.min(np.array(wanted_y))
                    ymax = np.max(np.array(wanted_y))

                    cv2.rectangle(image, pt1=(int(xmin*image.shape[1]), int(ymin*image.shape[0])), pt2=(int(xmax*image.shape[1]), int(ymax*image.shape[0])), color=(0, 0, 255), thickness=-1)

                  #image = cv2.circle(image, (int(x[8]* image.shape[1]), int(y[8]*image.shape[0])), radius=10, color=(0, 0, 255), thickness=-1)

                  #plot_x.append(int(x[8]* image.shape[1]))
                  #plot_y.append(int(y[8]*image.shape[0]))

            #for i in range(len(plot_x)):
            #    image = cv2.circle(image, (plot_x[i], plot_y[i]), radius=10, color=(0, 0, 255), thickness=-1)

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
          break
cap.release()