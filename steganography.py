from PIL import Image
import wave

def genData(data):
    newd = [format(ord(i), '08b') for i in data]
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
                        imdata.__next__()[:3] +
                        imdata.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode_pixel(img, data, new_img_name):
    image = Image.open(img, 'r')
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

def decode_pixel(img):
    image = Image.open(img, 'r')
    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def autism_function(autism_audiofile):
    autism_audio = wave.open(autism_audiofile, mode='rb')
    autism_frame_bytes = bytearray(list(autism_audio.readframes(autism_audio.getnframes())))
    extracted = [autism_frame_bytes[i] & 1 for i in range(len(autism_frame_bytes))]
    string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
    msg = string.split("###")[0]
    autism_audio.close()
    return msg

def autism_is_power(autism_audio_file, string, output):
    autism_audio = wave.open(autism_audio_file, mode='rb')
    autism_frame_bytes = bytearray(list(autism_audio.readframes(autism_audio.getnframes())))
    string = string + int((len(autism_frame_bytes)-(len(string)*8*8))/8) *'#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
    for i, bit in enumerate(bits):
        autism_frame_bytes[i] = (autism_frame_bytes[i] & 254) | bit
    frame_modified = bytes(autism_frame_bytes)
    with wave.open(output, 'wb') as fd:
        fd.setparams(autism_audio.getparams())
        fd.writeframes(frame_modified)
    autism_audio.close()

import base64

def base64_encode_string(s):
    return base64.b64encode(s.encode()).decode()

def base64_encode_file(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

from random import randint

def create_image(width, height, output_image_name):
    img = Image.new('RGB', (width, height))
    pixels = []

    for _ in range(width * height):
        pixels.append((randint(0, 255), randint(0, 255), randint(0, 255)))

    img.putdata(pixels)
    img.save(output_image_name)

def encode_file_in_image(file_path, output_image_name):
    encoded_string = base64_encode_file(file_path)
    width = height = int(len(encoded_string) ** 0.5) + 1

    create_image(width, height, output_image_name)
    encode_pixel(output_image_name, encoded_string, output_image_name)

def encode_file_in_audio(input_audio_file, file_path, output_audio_name):
    encoded_string = base64_encode_file(file_path)
    autism_is_power(input_audio_file, encoded_string, output_audio_name)
