import cv2
import pyrebase
import socket
import struct
import numpy as np
from tracker import CentroidTracker
import RPi.GPIO as GPIO

class MotorController:
    def __init__(self, pin, frequency):
        self.pin = pin
        self.frequency = frequency
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(50)

    def set_duty_cycle(self, duty_cycle):
        self.pwm.ChangeDutyCycle(duty_cycle)

def setup_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(33, GPIO.IN)
    GPIO.setup(34, GPIO.IN)

def establish_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print('HOST IP:', host_ip)
    port = 9999
    socket_address = (host_ip, port)
    server_socket.bind(socket_address)
    server_socket.listen(5)
    print("LISTENING AT:", socket_address)
    return server_socket

def establish_client_socket(rpi_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((rpi_ip, port))
    return client_socket

def initialize_tracker():
    return CentroidTracker(max_disappeared=80)

def initialize_firebase():
    firebase_config = {
        # Replace with your Firebase configuration details
    }
    return pyrebase.initialize_app(firebase_config).database()

def initialize_object_detection_model():
    config_path = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weights_path = 'frozen_inference_graph.pb'
    net = cv2.dnn_DetectionModel(weights_path, config_path)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    return net

def main():
    setup_gpio()
    server_socket = establish_server_socket()
    client_socket = establish_client_socket('192.168.137.33', 9000)
    data = b""
    payload_size = struct.calcsize("Q")

    tracker = initialize_tracker()
    database = initialize_firebase()
    roll_out_motor = MotorController(36, 300)
    pitch_out_motor = MotorController(37, 300)

    rpi_socket, address = server_socket.accept()
    print("Got connection from", address)

    while True:
        try:
            track_status = database.child("checkpoint").get().val()

            if track_status == "track_proceed":
                # Rest of the code remains unchanged for brevity
                pass

            elif track_status == "track_abort":
                success, img = cap.read()
                counter = 0

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Exception: {e}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
