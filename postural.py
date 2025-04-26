# import cv2
# import numpy as np

# class Postural_change():

#     def shoulders_difference(self, list_mask, altura_objPix):

#         cord_centroide = []
#         mask_l = []

#         for mask in list_mask:

#             mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

#             contours, hierarchy = cv2.findContours(mask_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
#             # Calcula los centroides de los contornos y crea una lista de tuplas que los contiene junto con el índice del contorno
#             for i, contour in enumerate(contours):
#                 M = cv2.moments(contour)
#                 if M["m00"] != 0:
#                     cx = int(M["m10"] / M["m00"])
#                     cy = int(M["m01"] / M["m00"])
#                     cv2.circle(mask, (cx, cy), 5, (0, 0, 255), -1)
#                     cord_centroide.append((i, (cx, cy)))

#             # Ordena los contornos por su centroide en el eje x
#             sorted_centroids = sorted(cord_centroide, key=lambda c: c[0])

#             # Enumera los contornos en el orden de la lista ordenada de centroides
#             for i, (index, _) in enumerate(sorted_centroids):
#                 cv2.drawContours(mask, contours, index, (0, 255, 0), 2)
#                 cv2.putText(mask, str(i+1), sorted_centroids[i][1], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#             # Dibujo una linea de centroide a centroide de cada uno de los lados
#             cv2.line(mask, sorted_centroids[0][1], sorted_centroids[3][1], (255, 255, 255), 2)
#             cv2.line(mask, sorted_centroids[2][1], sorted_centroids[1][1], (255, 255, 255), 2)

#             dist_centroides_der = np.sqrt((sorted_centroids[3][1][0] - sorted_centroids[0][1][0])**2 + (sorted_centroids[3][1][1] - sorted_centroids[0][1][1])**2)
#             dist_centroides_izq = np.sqrt((sorted_centroids[2][1][0] - sorted_centroids[1][1][0])**2 + (sorted_centroids[2][1][1] - sorted_centroids[1][1][1])**2)

#             #Altura del objeto
#             altura_obj = 20

#             cm_distance_der = (dist_centroides_der*altura_obj)/altura_objPix
#             cm_distance_izq = (dist_centroides_izq*altura_obj)/altura_objPix

#             mask_l.append(mask)

#             if cm_distance_izq < (cm_distance_der - 1.5) or cm_distance_izq > (cm_distance_der + 1.5):
#                 # print(f"Distancia del hombro der a cirtura der: {cm_distance_der}cm")
#                 # print(f"Distancia del hombro izq a cirtura izq: {cm_distance_izq}cm")
#                 # print("Deteccion de posible diferencia de hombro")
#                 a = "deteccion de posible diferencia de hombro"
#                 return mask_l, cm_distance_der, cm_distance_izq, a
#             else:
#                 # print(f"Distancia del hombro der a cirtura der: {cm_distance_der}cm")
#                 # print(f"Distancia del hombro izq a cirtura izq: {cm_distance_izq}cm")
#                 # print("No se detecto diferencia de hombro")
#                 a = "no se detecto diferencia de hombro"
#                 return mask_l, cm_distance_der, cm_distance_izq, a
                

#             # cv2.namedWindow('Linea de contorno a contorno', cv2.WINDOW_NORMAL)
#             # cv2.imshow('Linea de contorno a contorno', mask)
#             # cv2.waitKey(0)
#             # cv2.destroyAllWindows()

import cv2
import numpy as np

class Postural_change():

    def shoulders_difference(self, list_mask, altura_objPix):

        cord_centroide = []
        mask_l = []

        for mask in list_mask:

            mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

            contours, hierarchy = cv2.findContours(mask_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Calcula los centroides de los contornos y crea una lista de tuplas que los contiene junto con el índice del contorno
            for i, contour in enumerate(contours):
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.circle(mask, (cx, cy), 5, (0, 0, 255), -1)
                    cord_centroide.append((i, (cx, cy)))

            # Ordena los contornos por su centroide en el eje x
            sorted_centroids = sorted(cord_centroide, key=lambda c: c[0])

            # Calcula un tamaño de fuente dinámico basado en la altura de la imagen
            font_scale = mask.shape[0] / 500  # Ajusta el divisor según lo que necesites
            font_thickness = int(font_scale * 2)  # Ajusta el grosor proporcionalmente

            # Enumera los contornos en el orden de la lista ordenada de centroides
            for i, (index, _) in enumerate(sorted_centroids):
                cv2.drawContours(mask, contours, index, (0, 255, 0), 2)
                cv2.putText(mask, str(i+1), sorted_centroids[i][1], cv2.FONT_HERSHEY_SIMPLEX, 
                            font_scale, (255, 255, 255), font_thickness)

            # Dibujo una linea de centroide a centroide de cada uno de los lados
            cv2.line(mask, sorted_centroids[0][1], sorted_centroids[3][1], (255, 255, 255), 2)
            cv2.line(mask, sorted_centroids[2][1], sorted_centroids[1][1], (255, 255, 255), 2)

            dist_centroides_der = np.sqrt((sorted_centroids[3][1][0] - sorted_centroids[0][1][0])**2 + (sorted_centroids[3][1][1] - sorted_centroids[0][1][1])**2)
            dist_centroides_izq = np.sqrt((sorted_centroids[2][1][0] - sorted_centroids[1][1][0])**2 + (sorted_centroids[2][1][1] - sorted_centroids[1][1][1])**2)

            #Altura del objeto
            altura_obj = 20

            cm_distance_der = (dist_centroides_der*altura_obj)/altura_objPix
            cm_distance_izq = (dist_centroides_izq*altura_obj)/altura_objPix

            mask_l.append(mask)

            if cm_distance_izq < (cm_distance_der - 1.5) or cm_distance_izq > (cm_distance_der + 1.5):
                # print(f"Distancia del hombro der a cirtura der: {cm_distance_der}cm")
                # print(f"Distancia del hombro izq a cirtura izq: {cm_distance_izq}cm")
                # print("Deteccion de posible diferencia de hombro")
                a = "deteccion de posible diferencia de hombro"
                return mask_l, cm_distance_der, cm_distance_izq, a
            else:
                # print(f"Distancia del hombro der a cirtura der: {cm_distance_der}cm")
                # print(f"Distancia del hombro izq a cirtura izq: {cm_distance_izq}cm")
                # print("No se detecto diferencia de hombro")
                a = "no se detecto diferencia de hombro"
                return mask_l, cm_distance_der, cm_distance_izq, a
                

            # cv2.namedWindow('Linea de contorno a contorno', cv2.WINDOW_NORMAL)
            # cv2.imshow('Linea de contorno a contorno', mask)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()