import cv2
from time import sleep
from cvzone.HandTrackingModule import HandDetector
from flask import Flask, Response
import threading
import os

print("Current working directory:", os.getcwd())

# Initialize Flask
app = Flask(__name__)

# Initialize OpenCV Video Capture and the HandDetector
cap = cv2.VideoCapture(0)
cap.set(3, 1200)  # Width
cap.set(4, 800)  # Height

detector = HandDetector(detectionCon=0.8)

# Keyboard layout and keys (without pynput integration)
class Keys:
    def __init__(self, pos, text, size=[80, 80]):
        self.pos = pos
        self.text = text
        self.size = size

    def draw(self, img):
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, self.pos, (x + w, y + h), (204, 0, 0), cv2.FILLED)
        cv2.putText(img, self.text, (self.pos[0] + 20, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 2)
        return img

keyboard_layout = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ','],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '.', '?', ' ']
]

key_lst = []
for row_idx, row in enumerate(keyboard_layout):
    for col_idx, char in enumerate(row):
        key_lst.append(Keys((80 * col_idx + col_idx * 10 + 200, 50 + row_idx * 90), char))

output_txt = ""

# Function to handle webcam feed and hand tracking
def capture_frames():
    global output_txt
    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        for key in key_lst:
            key.draw(img)

        # Backspace button
        cv2.rectangle(img, (1010, 410), (1090, 500), (234, 0, 0), cv2.FILLED)
        cv2.putText(img, "<-", (1015, 470), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 2)

        if hands:
            hand = hands[0]
            lmList = hand["lmList"]
            length, _, _ = detector.findDistance(lmList[8][0:2], lmList[4][0:2], img)

            for key in key_lst:
                x, y = key.pos
                w, h = key.size
                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, key.pos, (x + w, y + h), (255, 153, 51), cv2.FILLED)  # Highlighted color
                    cv2.putText(img, key.text, (key.pos[0] + 10, key.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 2)

                    if length < 40:
                        # Removed the keyboard press functionality as it's not needed on EC2
                        output_txt += key.text
                        sleep(0.25)

            # Backspace functionality
            if 1010 < lmList[8][0] < 1090 and 410 < lmList[8][1] < 500:
                cv2.rectangle(img, (1010, 410), (1090, 500), (255, 153, 51), cv2.FILLED)
                cv2.putText(img, "<-", (1015, 470), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 2)

                if length < 40:
                    if output_txt:
                        output_txt = output_txt[:-1]
                    sleep(0.2)

        cv2.rectangle(img, (200, 410), (1000, 500), (234, 0, 0), cv2.FILLED)
        cv2.putText(img, output_txt, (210, 470), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 2)

        # Encode the frame for streaming
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/")
def home():
    return """
    <!doctype html>
    <html lang="en">
    <head>
        <title>Virtual Keyboard</title>
    </head>
    <body style="text-align: center; font-family: Arial, sans-serif;">
        <h1>Virtual Keyboard</h1>
        <p>The video feed from your webcam will appear below:</p>
        <div>
            <img src="/video_feed" style="border: 2px solid black; width: 80%; height: auto;" />
        </div>
    </body>
    </html>
    """

@app.route("/video_feed")
def video_feed():
    return Response(capture_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Code to create a .txt file
def create_text_file():
    file_path = "EaEcEhE_EEstWeWp.txt"  # File name
    with open(file_path, "w") as file:
        file.write("Hello! This is a custom text file.\n")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

