import cv2
import face_recognition
from app import app   # import Flask app from app.py

# Load known face
known_image = face_recognition.load_image_file("registered_face.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]
known_faces = [known_encoding]

video_capture = cv2.VideoCapture(0)
authenticated = False

while not authenticated:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Error: Couldn't access webcam.")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if not face_encodings:
        cv2.putText(frame, "⚠️ No face detected", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    else:
        for encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces, encoding)
            if True in matches:
                cv2.putText(frame, "✅ Access Granted", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                authenticated = True
                break
            else:
                cv2.putText(frame, "⛔ Access Denied", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow("Face Authentication", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()

if authenticated:
    print("🎙️ Face verified → Launching Arya Assistant at http://127.0.0.1:5000/")
    app.run(debug=True)
