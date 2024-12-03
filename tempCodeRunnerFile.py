                    cv2.putText(img, key.text, (key.pos[0] + 10, key.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 2)

                    if length < 40:
                        keyboard.press(key.text)
                        cv2.rectangle(img, key.pos, (x + w, y + h), (0, 153, 0), cv2.FILLED)  # Pressed color
                        cv2.putText(img, key.text, (key.pos[0] + 10, key.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 2)
                        output_txt += key.text
                        sleep(0.25)

            # Backspace functionality
            if 1010 < lmList[8][0] < 1090 and 410 < lmList[8][1] < 500:
                cv2.rectangle(img, (1010, 410), (1090, 500), (255, 153, 51), cv2.FILLED)
                cv2.putText(img, "<-", (1015, 470), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 2)

                if length < 40:
                    keyboard.press(Key.backspace)
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
        file.write("Here is another line of text.")
    print(f"File '{file_path}' created successfully.")
