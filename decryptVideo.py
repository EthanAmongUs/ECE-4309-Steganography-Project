import cv2

def decode_message_from_video(video_path, start_location, end_location, message_length):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open the video file.")
        return None

    binary_message = ''
    start_row, start_pixel, start_channel = start_location
    end_row, end_pixel, end_channel = end_location

    # Decode binary message from video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        for row_idx, row in enumerate(frame):
            for pixel_idx, pixel in enumerate(row):
                for channel in range(3):  # Iterate over RGB channels
                    if (row_idx, pixel_idx, channel) >= start_location and (row_idx, pixel_idx, channel) <= end_location:
                        binary_message += str(pixel[channel] & 1)
                        if len(binary_message) == message_length * 8:
                            cap.release()
                            decoded_message = ''.join(chr(int(binary_message[i:i + 8], 2)) for i in range(0, len(binary_message), 8))
                            print(f"Decoded message: {decoded_message}")
                            return decoded_message

    cap.release()
    print("Decoding incomplete.")
    return None

if __name__ == "__main__":
    # Hardcoded file path and decoding values
    video_path = r"C:\Users\Ethan\Downloads\encoded_video_ffv1.avi"
    start_location = (0, 0, 0)  # Update based on encoding output
    end_location = (0, 143, 0)  # Update based on encoding output
    message_length = 23  # Length of the message

    # Decode message
    decode_message_from_video(video_path, start_location, end_location, message_length)
