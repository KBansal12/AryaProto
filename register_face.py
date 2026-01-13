# register_face.py
import cv2
import face_recognition
import pickle

def register_face():
    cap = cv2.VideoCapture(0)
    print("📸 Please look at the camera to register your face.")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            # Save the FIRST detected face encoding
            with open("face_data.pkl", "wb") as f:
                pickle.dump(face_encodings[0], f)
            print("✅ Face registered successfully!")
            break

        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    register_face()
