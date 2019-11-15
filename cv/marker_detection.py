import cv2
from cv.cam_calib import *


def get_marker():
    marker_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    return cv2.aruco.drawMarker(marker_dict, 0, 200)


if __name__ == '__main__':
    cam_calib_w_i = CameraCalibrationWI((9, 6))
    cam_calib_w_i.load_camera_calibration('CamCalib.json')

    marker_dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

    cv2.namedWindow("Camera", cv2.WINDOW_AUTOSIZE)
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, marker_dictionary)
        if not ids is None:
            frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            rvecs, tvecs, _objPoints = cv2.aruco.estimatePoseSingleMarkers(corners, 0.05,
                                                                           cam_calib_w_i.camera_matrix,
                                                                           cam_calib_w_i.distortion_coefficients)
            frame = cv2.aruco.drawAxis(frame, cam_calib_w_i.camera_matrix, cam_calib_w_i.distortion_coefficients,
                                       rvecs, tvecs, 0.05)

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyWindow("Camera")
