# -*- coding: utf-8 -*-
"""pictor_PPE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m2h6UdsyacplZpCu3keATcXVSp6xI-zJ
"""

# !git
# clone
# https: // github.com / ciber - lab / pictor - ppe

# Commented out IPython magic to ensure Python compatibility.
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib as mpl
import sqlite3, os, datetime
#from google.colab import drive
# %cd pictor-ppe

from tensorflow.python.keras.layers import Input

from src.yolo3.model import *
from src.yolo3.detect import *

# from src.utils.image import *
from src.utils.datagen import *
from src.utils.fixes import *

fix_tf_gpu()


def letterbox_image(image, size):
    '''
    Resize image with unchanged aspect ratio using padding
    '''

    # original image size
    ih, iw, ic = image.shape

    # given size
    h, w = size

    # scale and new size of the image
    scale = min(w / iw, h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)

    # placeholder letter box
    new_image = np.zeros((h, w, ic), dtype='uint8') + 128

    # top-left corner
    top, left = (h - nh) // 2, (w - nw) // 2

    # paste the scaled image in the placeholder anchoring at the top-left corner
    new_image[top:top + nh, left:left + nw, :] = cv2.resize(image, (nw, nh))

    return new_image


def draw_detection(
        img,
        boxes,
        class_names,
        # drawing configs
        font=cv2.FONT_HERSHEY_DUPLEX,
        font_scale=0.5,
        box_thickness=2,
        border=5,
        text_color=(255, 255, 255),
        text_weight=1
):
    '''
    Draw the bounding boxes on the image
    '''
    # generate some colors for different classes
    num_classes = len(class_names)  # number of classes
    colors = [mpl.colors.hsv_to_rgb((i / num_classes, 1, 1)) * 255 for i in range(num_classes)]

    # draw the detections
    for box in boxes:
        x1, y1, x2, y2 = box[:4].astype(int)
        score = box[-2]
        label = int(box[-1])

        clr = colors[label]

        # draw the bounding box
        img = cv2.rectangle(img, (x1, y1), (x2, y2), clr, box_thickness)

        # text: <object class> (<confidence score in percent>%)
        text = f'{class_names[label]} ({score * 100:.0f}%)'

        # get width (tw) and height (th) of the text
        (tw, th), _ = cv2.getTextSize(text, font, font_scale, 1)

        # background rectangle for the text
        tb_x1 = x1 - box_thickness // 2
        tb_y1 = y1 - box_thickness // 2 - th - 2 * border
        tb_x2 = x1 + tw + 2 * border
        tb_y2 = y1

        # draw the background rectangle
        img = cv2.rectangle(img, (tb_x1, tb_y1), (tb_x2, tb_y2), clr, -1)

        # put the text
        img = cv2.putText(img, text, (x1 + border, y1 - border), font, font_scale, text_color, text_weight, cv2.LINE_AA)

        # поиск рабочих без жилета и каски с функцией сохранения save_warning в БД
        if (class_names[label] == "W" or class_names[label] == "WH" or class_names[label] == "WV") and score > 0.9:
            save_warning(img, class_names[label], score)


    return img

def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(f"db_data/{filename}", 'rb') as file:
        blob_data = file.read()
    return blob_data

def insert_blob(name, img, dtime):
    try:
        sqlite_connection = sqlite3.connect('warn.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_blob_query = """INSERT INTO warlist
                                  (ttype, photo, dtime) VALUES (?, ?, ?)"""

        # Преобразование данных в формат кортежа
        photo = convert_to_binary_data("curentimg.jpg")
        data_tuple = (name, photo, dtime)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqlite_connection.commit()
        print("Изображение и файл успешно вставлены как BLOB в таблицу")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def save_warning(img, name, score):
    print(f'WARNING!!! {name} ({score * 100:.0f}%)')
    dtime = datetime.datetime.now()
    cv2.imwrite(os.path.join("db_data", "curentimg.jpg"), img)


    insert_blob(name, img, dtime)


#drive.mount('/content/drive')


def prepare_model(approach):
    '''
    Prepare the YOLO model
    '''
    global input_shape, class_names, anchor_boxes, num_classes, num_anchors, model

    # shape (height, width) of the imput image
    input_shape = (416, 416)

    # class names
    if approach == 1:
        class_names = ['H', 'V', 'W']

    elif approach == 2:
        class_names = ['W', 'WH', 'WV', 'WHV']

    elif approach == 3:
        class_names = ['W']

    else:
        raise NotImplementedError('Approach should be 1, 2, or 3')

    # anchor boxes
    if approach == 1:
        anchor_boxes = np.array(
            [
                np.array([[76, 59], [84, 136], [188, 225]]) / 32,  # output-1 anchor boxes
                np.array([[25, 15], [46, 29], [27, 56]]) / 16,  # output-2 anchor boxes
                np.array([[5, 3], [10, 8], [12, 26]]) / 8  # output-3 anchor boxes
            ],
            dtype='float64'
        )
    else:
        anchor_boxes = np.array(
            [
                np.array([[73, 158], [128, 209], [224, 246]]) / 32,  # output-1 anchor boxes
                np.array([[32, 50], [40, 104], [76, 73]]) / 16,  # output-2 anchor boxes
                np.array([[6, 11], [11, 23], [19, 36]]) / 8  # output-3 anchor boxes
            ],
            dtype='float64'
        )

    # number of classes and number of anchors
    num_classes = len(class_names)
    num_anchors = anchor_boxes.shape[0] * anchor_boxes.shape[1]

    # input and output
    input_tensor = Input(shape=(input_shape[0], input_shape[1], 3))  # input
    num_out_filters = (num_anchors // 3) * (5 + num_classes)  # output

    # build the model
    model = yolo_body(input_tensor, num_out_filters)

    # load weights
    if approach == 1:
        weight_path = 'yolo/pictor/pictor-ppe-v302-a1-yolo-v3-weights.h5'  # f'model-data\weights\pictor-ppe-v302-a{approach}-yolo-v3-weights.h5'
    elif approach == 2:
        weight_path = 'yolo/pictor/pictor-ppe-v302-a2-yolo-v3-weights.h5'
    elif approach == 3:
        weight_path = 'yolo/pictor/pictor-ppe-v302-a3-yolo-v3-weights.h5'
    model.load_weights(weight_path)


def get_detection(img):
    # save a copy of the img
    act_img = img.copy()

    # shape of the image
    ih, iw = act_img.shape[:2]

    # preprocess the image
    img = letterbox_image(img, input_shape)
    img = np.expand_dims(img, 0)
    image_data = np.array(img) / 255.

    # raw prediction from yolo model
    prediction = model.predict(image_data)

    # process the raw prediction to get the bounding boxes
    boxes = detection(
        prediction,
        anchor_boxes,
        num_classes,
        image_shape=(ih, iw),
        input_shape=(416, 416),
        max_boxes=10,
        score_threshold=0.3,
        iou_threshold=0.45,
        classes_can_overlap=False)

    # convert tensor to numpy
    boxes = boxes[0].numpy()

    # draw the detection on the actual image
    return draw_detection(act_img, boxes, class_names)


def plt_imshow(img):
    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.axis('off')

def main(cap):
    # prepare the model (1, 2, 3)
    prepare_model(approach=2)

    #cap = cv2.VideoCapture(path) #нужно сделать загрузку из кнопки будет браться путь
    if cap.isOpened():
        print("Видео загружено")
        fps = int(cap.get(5))
        frame_count = int(cap.get(5))
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        frame_size = (frame_width, frame_height)
    print(fps, frame_count, frame_size)

    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('yolo/examles_pictor/Video5.avi', fourcc, fps, frame_size)

    while True:
        ret, frame = cap.read()

        if ret:
            frame = cv2.resize(frame, input_shape)
            frame = get_detection(frame)
            frame = cv2.resize(frame, (frame_width, frame_height))
            # plt_imshow(frame[:, :, ::-1])
            out.write(frame)

        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()