import cv2
import numpy as np

def encode_message_in_video(input_video, output_ffv1, output_xvid, message):
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'
    print(f"Binary message to encode: {binary_message}")
    message_idx = 0

    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print("Error: Cannot open the input video file.")
        return None

    # Initialize FFV1 and XVID video writers
    fourcc_ffv1 = cv2.VideoWriter_fourcc(*'FFV1')
    fourcc_xvid = cv2.VideoWriter_fourcc(*'XVID')
    frame_width, frame_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    out_ffv1 = cv2.VideoWriter(output_ffv1, fourcc_ffv1, fps, (frame_width, frame_height))
    out_xvid = cv2.VideoWriter(output_xvid, fourcc_xvid, fps, (frame_width, frame_height))

    start_location = None
    end_location = None

    # Process frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Encode binary message into the frame
        if message_idx < len(binary_message):
            for row_idx, row in enumerate(frame):
                for pixel_idx, pixel in enumerate(row):
                    for channel in range(3):  # Iterate over RGB channels
                        if message_idx < len(binary_message):
                            bit = int(binary_message[message_idx])
                            pixel[channel] = (pixel[channel] & ~1) | bit  # Set LSB
                            if start_location is None:
                                start_location = (row_idx, pixel_idx, channel)
                            message_idx += 1
                            if message_idx == len(binary_message):
                                end_location = (row_idx, pixel_idx, channel)
                                break
                    if message_idx == len(binary_message):
                        break
                if message_idx == len(binary_message):
                    break

        out_ffv1.write(frame)
        out_xvid.write(frame)

    cap.release()
    out_ffv1.release()
    out_xvid.release()

    if start_location and end_location:
        print(f"Message encoding started at {start_location} and ended at {end_location}.")
        return start_location, end_location, len(message)
    else:
        print("Message encoding failed.")
        return None

if __name__ == "__main__":
    # Hardcoded file paths and message
    input_video = r"C:\Users\Ethan\Downloads\Rick Rolled.avi"
    output_ffv1 = r"C:\Users\Ethan\Downloads\encoded_video_ffv1.avi"
    output_xvid = r"C:\Users\Ethan\Downloads\encoded_video_xvid.avi"
    message = "Never gonna give you up!"

    # Encode message
    result = encode_message_in_video(input_video, output_ffv1, output_xvid, message)
    if result:
        start_location, end_location, message_length = result
        print(f"Save these values for decoding:\nStart Location: {start_location}\nEnd Location: {end_location}\nMessage Length: {message_length}")
    else:
        print("Encoding failed.")
