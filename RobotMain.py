import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import torch
import MotorModule as Motor
import WebcamModule as Webcam
import cv2

model = torch.hub.load(
    repo_or_dir='yolov5', 
    model='custom', 
    path='best.pt', 
    force_reload=False,
    trust_repo=True,
    verbose=True,
    source='local'
)
motor = Motor.Motor(27, 17, 18, 24, 22, 23)

# def preProcess(img):
#     # img = img[54:120, :, :]
#     # img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
#     # img = cv2.GaussianBlur(img, (3, 3), 0)
#     # img = cv2.resize(img, (200, 66))
#     # img = img / 255
#     img = cv2.resize(img, (320, 240))
#     return img

while True:
    img = Webcam.getImg(False, size=[320, 320])
    # img = preProcess(img)
    
    if img is None:
        continue
    
    results = model(img)
    detections = results.xyxy[0]
    
    target_detected = False
    for *box, conf, cls in detections:
        class_name = model.names[int(cls)]
        if conf > 0.5:
            target_detected = True
            print(f"Phát hiện: {class_name}, độ tin cậy: {conf:.2f}")
            # if class_name == "Cấm Dừng & Cấm Đỗ":
            #     print("Phát hiện biển báo Cấm Dừng & Cấm Đỗ")
            #     motor.move(speed=0.2, turn=0)
            # elif class_name == "Cấm Dừng":
            #     print("Phát hiện biển báo Cấm Dừng")
            #     motor.move(speed=0.2, turn=0)
            # elif class_name == "Cấm Đỗ":
            #     print("Phát hiện biển báo Cấm Đỗ")
            #     motor.move(speed=0.2, turn=0)
            # break
            motor.move(speed=0.2, turn=0)

    if not target_detected:
        motor.stop()
        # print("Không phát hiện đối tượng, tiếp tục di chuyển")
        continue