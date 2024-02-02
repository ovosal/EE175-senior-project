# server.py

import socket, pickle, struct
import cv2 as cv

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# # If you pass an empty string, the server will accept connections on all available IPv4 interfaces.
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

WIN_NAME = "SERVER"

def receive_video(client_socket, addr):
    try:
        print(f'Connected by {addr}')

        while True:
            data = b""
            payload_size = struct.calcsize("Q")

            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)
                if not packet:
                    break
                data += packet

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)

            cv.namedWindow(WIN_NAME, cv.WND_PROP_FULLSCREEN)
            cv.setWindowProperty(WIN_NAME, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
            cv.imshow(WIN_NAME, frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Keyboard interrupt. Closing connection.")
    finally:
        client_socket.close()
        cv.destroyAllWindows()

def main():
    HOST_IP = socket.gethostbyname(socket.gethostname())
    PORT = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST_IP, PORT))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        receive_video(client_socket, addr)

if __name__ == "__main__":
    main()
