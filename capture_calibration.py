##
# cording:utf-8
##

import os
import numpy as np
import cv2
import json
import argparse
from glob import glob

debug = False


def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str, default='output')
    parser.add_argument('-s', '--square_size', type=float, default=25.0)
    parser.add_argument('-v', '--video_id', type=int, default=0)
    parser.add_argument('--pattern_size', type=str, default='9x6')
    parser.add_argument('--sleep', type=int, default=3)
    return parser.parse_args()


def main():
    args = argparser()

    debug_dir = args.output
    if debug_dir and not os.path.isdir(debug_dir):
        os.mkdir(debug_dir)
    square_size = args.square_size

    ph, pw = args.pattern_size.split('x')
    pattern_size = (int(ph), int(pw))
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []
    img_points = []

    if debug:
        img_names = glob('output/*.png')
        img = cv2.imread(img_names[0])
        sleep_time = 0
    else:
        cap = cv2.VideoCapture(args.video_id)
        if not cap.isOpened():
            return None
        ret, img = cap.read()
        sleep_time = cap.get(cv2.CAP_PROP_FPS) * args.sleep

    h, w = img.shape[:2]

    sleep_frame = 0
    counter = 0
    while True:
        if debug:
            if counter >= len(img_names):
                break
            img = cv2.imread(img_names[counter])
        else:
            ret, img = cap.read()
            if not ret:
                break

        viz = img.copy()
        found, corners = cv2.findChessboardCorners(img, pattern_size)
        if found:
            cv2.drawChessboardCorners(viz, pattern_size, corners, found)

        if found and sleep_frame >= sleep_time:
            print("Count:{}".format(counter))
            img_points.append(corners.reshape(-1, 2))
            obj_points.append(pattern_points)
            cv2.imwrite(os.path.join(debug_dir, '{:07d}.png'.format(counter)), img)
            counter += 1
            sleep_frame = 0

        sleep_frame += 1
        cv2.imshow('img', viz)
        if cv2.waitKey(3) == 27:
            break

    if not debug:
        cap.release()

    print("estimate... {}".format(len(img_points)))
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)

    print("\nRMS:", rms)
    print("camera matrix:\n", camera_matrix)
    print("distortion coefficients: ", dist_coefs.ravel())

    with open(os.path.join(debug_dir, 'calibrate.json'), 'w') as fp:
        param = {'RMS': rms,
                 'camera_matrix': camera_matrix.tolist(),
                 'distortion': dist_coefs.ravel().tolist()}
        json.dump(param, fp, indent=4)


if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()