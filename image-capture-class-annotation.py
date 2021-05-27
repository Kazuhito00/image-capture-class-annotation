#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
from collections import deque

import cv2
import numpy as np

click_points = deque(maxlen=4)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--crop_width", type=int, default=96)
    parser.add_argument("--crop_height", type=int, default=96)
    parser.add_argument("--extension", type=str, default='jpg')
    parser.add_argument("--start_count", type=int, default=0)

    args = parser.parse_args()

    return args


def mouse_callback(event, x, y, flags, param):
    global click_points
    if event == cv2.EVENT_LBUTTONDOWN:
        click_points.append([x, y])


def main():
    global click_points

    # コマンドライン引数
    args = get_args()
    cap_device = args.device

    cap_width = args.width
    cap_height = args.height
    crop_width = args.crop_width
    crop_height = args.crop_height

    extension = args.extension
    image_count = args.start_count

    # GUI準備
    window_name = 'Image Capture & Class Annotation'
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    # カメラ準備
    cap = cv2.VideoCapture(cap_device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

    # 認識対象座標 格納用
    click_points = deque(maxlen=4)

    while True:
        extract_image = None

        # カメラキャプチャ
        ret, frame = cap.read()
        if not ret:
            print('cap.read() error')
        resize_frame = cv2.resize(frame, (int(cap_width), int(cap_height)))

        # 指定領域抜き出し
        if len(click_points) == 4:
            # 射影変換
            pts1 = np.float32([
                click_points[0],
                click_points[1],
                click_points[2],
                click_points[3],
            ])
            pts2 = np.float32([
                [0, 0],
                [crop_width, 0],
                [crop_width, crop_height],
                [0, crop_height],
            ])
            M = cv2.getPerspectiveTransform(pts1, pts2)
            extract_image = cv2.warpPerspective(resize_frame, M,
                                                (crop_width, crop_height))

        # デバッグ情報描画
        for click_point in click_points:
            cv2.circle(resize_frame, (click_point[0], click_point[1]), 4,
                       (255, 255, 255), -1)
            cv2.circle(resize_frame, (click_point[0], click_point[1]), 2,
                       (0, 0, 0), -1)
        if len(click_points) >= 3:
            cv2.drawContours(resize_frame, [np.array(click_points)], -1,
                             (255, 255, 255), 2)
            cv2.drawContours(resize_frame, [np.array(click_points)], -1,
                             (0, 0, 0), 1)

        # GUI描画更新
        cv2.imshow(window_name, resize_frame)
        if extract_image is not None:
            cv2.imshow('Capture', extract_image)

        # キー入力
        key = cv2.waitKey(50)
        number = -1
        if 48 <= key <= 57:  # 0:48 ～ 9:57
            number = key - 48
        if 97 <= key <= 122:  # a:97～z：122
            number = key - 97
            number = number + 10
        if key == 27:  # ESC
            break

        if (extract_image is not None) and (number >= 0):
            save_dir = 'capture/' + '{:02}'.format(number)

            # 保存先ディレクトリ作成
            os.makedirs(save_dir, exist_ok=True)

            # 画像保存
            save_dir = os.path.join(save_dir,
                                    '{:08}.'.format(image_count) + extension)
            cv2.imwrite(save_dir, extract_image)
            print('{:08}'.format(image_count))

            image_count = image_count + 1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
