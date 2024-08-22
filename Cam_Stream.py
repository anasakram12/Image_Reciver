from flask import Flask, Response
import cv2
import time

app = Flask(__name__)

def initialize_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while not cap.isOpened():
        print("Camera is not available, retrying in 2 seconds...")
        time.sleep(2)
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    return cap

# Initialize the camera with retry mechanism
cap = initialize_camera()

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

def gen():
    while True:
        success, frame = cap.read()
        while not success:  # Retry mechanism if frame grabbing fails
            print("Failed to grab frame, retrying...")
            time.sleep(1)  # Wait for 1 second before retrying
            success, frame = cap.read()
        
        # Resize the frame to the desired resolution
        frame = cv2.resize(frame, (1920, 1080))
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("Failed to encode frame, skipping...")
            continue  # Skip this frame and try the next one

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        # Release camera and destroy any OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
