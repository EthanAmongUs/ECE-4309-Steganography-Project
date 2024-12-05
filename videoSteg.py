import cv2
import numpy as np

def encode_message_in_video(input_video, output_ffv1, output_xvid, message):
    # Convert the message to binary format with an end flag
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'
    print(f"Binary message to encode: {binary_message}")
    message_idx = 0

    # Open input video
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
    # Hardcoded file paths and message
    input_video = r"C:\Users\Ethan\Downloads\Rick Rolled.avi"
    output_ffv1 = r"C:\Users\Ethan\Downloads\encoded_video_ffv1.avi"
    output_xvid = r"C:\Users\Ethan\Downloads\encoded_video_xvid.avi"
    message = "ECE 4309: Fundamentals of Cybersecurity is the best!"

    # Encode or decode
    choice = input("Do you want to encode or decode a message? (encode/decode): ").strip().lower()
    if choice == "encode":
        result = encode_message_in_video(input_video, output_ffv1, output_xvid, message)
        if result:
            start_location, end_location, message_length = result
            print(f"Save these values for decoding:\nStart Location: {start_location}\nEnd Location: {end_location}\nMessage Length: {message_length}")
        else:
            print("Encoding failed.")
    elif choice == "decode":
        # Use hardcoded locations from the encoding step
        video_path = output_ffv1  # Always decode from FFV1
        start_location = (0, 0, 0)  # Update based on encoding output
        end_location = (0, 143, 0)  # Update based on encoding output
        message_length = len(message)
        decode_message_from_video(video_path, start_location, end_location, message_length)
    else:
        print("Invalid choice. Please select 'encode' or 'decode'.")
