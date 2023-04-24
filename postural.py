import cv2
import numpy as np


class Postural_change():

    def shoulders_difference(self, list_mask):

        for mask in list_mask:

            mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

            contours, hierarchy = cv2.findContours(mask_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for i in range(len(contours)):
                cv2.drawContours(mask, contours, i, (0, 255, 0), 3)
                cv2.putText(mask, str(i), tuple(contours[i][0][0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            

            start_point1 = tuple(contours[0][0][0])
            end_point1 = tuple(contours[3][0][0])
            cv2.line(mask, start_point1, end_point1, (255, 255, 255), 2)

            start_point2 = tuple(contours[1][0][0])
            end_point2 = tuple(contours[2][0][0])
            cv2.line(mask, start_point2, end_point2, (255, 255, 255), 2)

            cv2.imshow('Linea de contorno a contorno', mask)
            cv2.waitKey(0)
            cv2.destroyAllWindows()