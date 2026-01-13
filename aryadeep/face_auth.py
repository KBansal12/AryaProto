# face_auth.py
import cv2
import face_recognition
import os

def authenticate_user():
    if not os.path.exists("registered_face.jpg"):
        print("⚠️ No registered face found! Run register_face.py first.")
        return False

    # Load registered face image and encode
    registered_img = face_recognition.load_image_file("registered_face.jpg")
    registered_encoding = face_recognition.face_encodings(registered_img)[0]

    cap = cv2.VideoCapture(0)
    print("🔒 Starting Face Authentication… Look at the camera.")

    authenticated = False
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            match = face_recognition.compare_faces([registered_encoding], face_encoding)[0]
            
            if match:
                label = "✅ Access Granted"
                color = (0, 200, 0)
                authenticated = True
            else:
                label = "❌ Unknown Face"
                color = (0, 0, 255)

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow("Arya — Face Authentication", frame)

        if authenticated:
            cv2.waitKey(1000)  # wait a second before closing
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return authenticated

if __name__ == "__main__":
    if authenticate_user():
        print("🎉 Welcome back!")
    else:
        print("❌ Access denied.")
