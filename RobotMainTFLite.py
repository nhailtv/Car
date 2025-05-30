import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import tensorflow as tf
import numpy as np
import MotorModule as Motor
import WebcamModule as Webcam
import cv2

interpreter = tf.lite.Interpreter(model_path='best-fp16.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_shape = input_details[0]['shape']
input_height = input_shape[1]
input_width = input_shape[2]

class_names = {
    0: "Cấm Dừng & Cấm Đỗ",
    1: "Cấm Dừng", 
    2: "Cấm Đỗ"
}

motor = Motor.Motor(27, 17, 18, 24, 22, 23)

print("Model loaded successfully!")
print(f"Input shape: {input_shape}")

while True:
    img = Webcam.getImg(False, size=[320, 320])
    
    if img is None:
        continue
    
    img_resized = cv2.resize(img, (input_width, input_height))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_normalized = img_rgb.astype(np.float32) / 255.0
    img_batch = np.expand_dims(img_normalized, axis=0)
    
    interpreter.set_tensor(input_details[0]['index'], img_batch)
    
    interpreter.invoke()
    
    output = interpreter.get_tensor(output_details[0]['index'])
    
    detections = output[0]  # Remove batch dimension
    
    target_detected = False
    for detection in detections:
        x1, y1, x2, y2 = detection[:4]
        confidence = detection[4]
        class_probs = detection[5:]
        
        class_id = np.argmax(class_probs)
        class_prob = class_probs[class_id]
        
        final_confidence = confidence * class_prob
        
        if final_confidence > 0.5:
            class_name = class_names.get(class_id, f"Class_{class_id}")
            target_detected = True
            print(f"Phát hiện: {class_name}, độ tin cậy: {final_confidence:.2f}")
            
            # if class_name == "Cấm Dừng & Cấm Đỗ":
            #     print("Phát hiện biển báo Cấm Dừng & Cấm Đỗ")
            #     motor.move(speed=0.2, turn=0)
            # elif class_name == "Cấm Dừng":
            #     print("Phát hiện biển báo Cấm Dừng")
            #     motor.move(speed=0.2, turn=0)
            # elif class_name == "Cấm Đỗ":
            #     print("Phát hiện biển báo Cấm Đỗ")
            #     motor.move(speed=0.2, turn=0)
            
            motor.move(speed=0.2, turn=0)
            break

    if not target_detected:
        motor.stop()
        continue