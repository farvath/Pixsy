import random

import numpy as np
import pandas as pand
import os
import cv2
from cryptography.fernet import Fernet
import base64
from ImageSteg import ImageSteg

def creating_key(keys):
    # Convert the input to bytes using UTF-8 encoding
    key_bytes =keys.encode('utf-8')

    # Pad or truncate the key bytes to 32 bytes
    key_bytes = key_bytes[:32].ljust(32, b'\x00')

    # Encode the key bytes to URL-safe base64 format
    key = base64.urlsafe_b64encode(key_bytes)
    return key

def msgtobinary(msg):
    if type(msg) == str:
        result = ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result = [format(i, "08b") for i in msg]
    elif type(msg) == int or type(msg) == np.uint8:
        result = format(msg, "08b")
    else:
        raise TypeError("Input type is not supported in this function")
    return result


def substitution_embed(frame, data):
    data += '*^*^*'
    binary_data = msgtobinary(data)
    length_data = len(binary_data)
    index_data = 0

    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)

            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data >= length_data:
                break

    return frame


def substitution_extract(frame):
    data_binary = ""
    final_decoded_msg = ""

    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]

            total_bytes = [data_binary[i: i + 8] for i in range(0, len(data_binary), 8)]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))

                if decoded_data[-5:] == "*^*^*":
                    for i in range(0, len(decoded_data) - 5):
                        final_decoded_msg += decoded_data[i]

                    ciphertext = final_decoded_msg.encode('UTF-8')
                    output_keys = input("enter the key to decrpyt : ")
                    output_key = creating_key(output_keys)
                    cipher = Fernet(output_key)
                    try:
                        decrypted_text = cipher.decrypt(ciphertext).decode('UTF-8')
                        print("Decrypted Text from the video is :", decrypted_text)
                    except:
                        print("Invalid key! Decryption failed.")
                    return


def embed(frame):
    while True:
        string_key = input("Enter the key (not more than 32 bytes): ")
        key_bytes = string_key.encode('utf-8')

        if len(key_bytes) <= 32:
            break
        else:
            print("Input exceeds 32 bytes. Please try again.")

    key = creating_key(string_key)

    data = input("enter the text to encrypted : ")

    no_of_bytes = (frame.shape[0] * frame.shape[1] * 3) // 8
    print("\t\nMaximum bytes to encode in Image :", no_of_bytes)
    if (len(data) > no_of_bytes):
        raise ValueError("Insufficient bytes Error, Need Bigger Image or give Less Data !!")

    print("\nThe Length of Binary data", len(data))

    cipher = Fernet(key)
    ciphertext = cipher.encrypt(data.encode('UTF-8'))


    frame_ = substitution_embed(frame,ciphertext.decode('UTF-8'))
    return frame_




def encode_vid_data(input_video_path):
    cap = cv2.VideoCapture(input_video_path)
    vidcap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))

    size = (frame_width, frame_height)
    out = cv2.VideoWriter('output_video/stego_video.mp4', fourcc, 25.0, size)
    max_frame = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame += 1

    cap.release()
    print("Total number of Frames in selected Video:", max_frame)
    n =random.randint(1,max_frame)
    frame_number = 0

    while vidcap.isOpened():
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:
            frame_ = embed(frame)
            frame = frame_
        out.write(frame)

    print("\nEncoded the data successfully in the video file.")
    return frame_


def decode_vid_data(frame_):
    cap = cv2.VideoCapture('output_video/stego_video.mp4')
    max_frame = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame += 1

    print("Total number of Frames in selected Video:", max_frame)
    n =random.randint(1,max_frame)
    vidcap = cv2.VideoCapture('output_video/stego_video.mp4')
    frame_number = 0

    while vidcap.isOpened():
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:
            substitution_extract(frame_)
            return


def vid_steg():
    while True:
        print("\n\t\tVIDEO STEGANOGRAPHY OPERATIONS")
        print("1. Encode the Text message")
        print("2. Decode the Text message")
        print("3. Exit")
        choice1 = int(input("Enter the Choice:"))

        if choice1 == 1:
            input_video_path = input("Enter the video path  : ")
            a = encode_vid_data(input_video_path)
        elif choice1 == 2:
            decode_vid_data(a)
        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")


def image_steg():
    while True:
        print("\n\t\tIMAGE STEGANOGRAPHY OPERATIONS")
        print("1. Encode the Text message")
        print("2. Decode the Text message")
        print("3. Exit")
        choice1 = int(input("Enter the Choice:"))

        if choice1 == 1:
            img = ImageSteg()
            while True:
                string_key = input("Enter the key (not more than 32 bytes): ")
                key_bytes = string_key.encode('utf-8')

                if len(key_bytes) <= 32:
                    break
                else:
                    print("Input exceeds 32 bytes. Please try again.")

            key = creating_key(string_key)
            input_image_path = input("Enter the image path : ")
            msg = input("enter the text to encrypted : ")
            cipher = Fernet(key)
            ciphertext = cipher.encrypt(msg.encode('UTF-8'))

            res =img.encrypt_text_in_image(input_image_path,ciphertext.decode('UTF-8'),"output_image/")

            print("------------------ENCRYPTION SUCCESFULL--------------------------")
        elif choice1 == 2:
            img = ImageSteg()

            output_image_path = input("Enter the image path to be decrypted: ")
            res=img.decrypt_text_in_image(output_image_path)

            ciphertext=res.encode('UTF-8')

            output_keys = input("enter the key to decrpyt : ")
            output_key = creating_key(output_keys)
            cipher = Fernet(output_key)

            try:
                decrypted_text = cipher.decrypt(ciphertext).decode('UTF-8')
                print("Decrypted Text:", decrypted_text)
            except:
                print("Invalid key! Decryption failed.")

        elif choice1 == 3:
            break
        else:
            print("Incorrect Choice")
        print("\n")

def main():
    print("\n")
    print("\t\t  STEGANOGRAPHY")

    while True:
        print("\n\t\t\tMAIN MENU\n")
        print("1. VIDEO STEGANOGRAPHY {Hiding Text in Video cover file}")
        print("2. IMAGE STEGANOGRAPHY {Hiding Text in Image cover file}")
        print("3. Exit\n")
        choice1 = int(input("Enter the Choice: "))

        if choice1 == 1:
            vid_steg()
        elif choice1 == 2:
            image_steg()
            break
        else:
            exit()



if __name__ == "__main__":
    main()
