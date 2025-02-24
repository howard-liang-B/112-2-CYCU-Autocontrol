import cv2
from ultralytics import YOLO


if __name__ == "__main__":
    # 1. 載入模型 
    # 2. 建立相機物件
    model = YOLO(r'C:\Users\user\Desktop\112-2社課\weights\face_five.pt')
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        # 3. 讀取相機每一帪畫面
        success, frame = cap.read()

        # 4. 預測每一帪
        results = model(frame)
        
        # 5. 畫出預測的結果
        annotated_frame = results[0].plot()

        cv2.imshow("Camera", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


    cap.release()
    cv2.destroyAllWindows()