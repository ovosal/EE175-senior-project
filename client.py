# client.py

# pickle - serialize frame to byte data
# struct - pack each frame data
import socket, pickle, struct
import cv2 as cv

HOST_IP = '169.235.86.66'
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST_IP, PORT))

WIN_NAME = "CLIENT"

def get_video_capture():
    camera = cv.VideoCapture(0)
    if camera.isOpened():
        camera.release()
        return cv.VideoCapture(0)
    else:
        return cv.VideoCapture('sample-media/sample-vid-1.mp4')


def send_video(client_socket):
    try:
        vid = get_video_capture()
        while vid.isOpened():
            ret, frame = vid.read()
            if not ret:
                print("Video finished.")
                break
            
            data = pickle.dumps(frame)
            size = struct.pack("Q", len(data))
            client_socket.sendall(size + data)

            cv.imshow(WIN_NAME, frame)
            if cv.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("Keyboard interrupt. Closing connection.")
    finally:
        client_socket.close()
        vid.release()
        cv.destroyAllWindows()

def main():
    send_video(client_socket)

if __name__ == "__main__":
    main()
