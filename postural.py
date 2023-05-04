import cv2
import numpy as np

class Postural_change():

    def shoulders_difference(self, list_mask, altura_objPix):

        cord_centroide = []
        mask_l = []

        for mask in list_mask:

            mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

            contours, hierarchy = cv2.findContours(mask_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for i in range(len(contours)):
                cv2.drawContours(mask, contours, i, (0, 255, 0), 3)
                cv2.putText(mask, str(i), tuple(contours[i][0][0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            for cnt in contours:
                #Dibujo los centroides y agrego las coordenadas a una lista
                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                cv2.circle(mask, (cx, cy), 5, (0, 0, 255), -1)
                cord_centroide.append((cx,cy))

            # Dibujo una linea de centroide a centroide de cada uno de los lados
            cv2.line(mask, cord_centroide[0], cord_centroide[2], (255, 255, 255), 2)
            cv2.line(mask, cord_centroide[1], cord_centroide[3], (255, 255, 255), 2)
            
            dist_centroides_der = np.sqrt((cord_centroide[2][0] - cord_centroide[0][0])**2 + (cord_centroide[2][1] - cord_centroide[0][1])**2)
            dist_centroides_izq = np.sqrt((cord_centroide[3][0] - cord_centroide[1][0])**2 + (cord_centroide[3][1] - cord_centroide[1][1])**2)

            #Altura de la persona
            altura_obj = 168 #centimetros de la regla

            cm_distance_der = (dist_centroides_der*altura_obj)/altura_objPix
            cm_distance_izq = (dist_centroides_izq*altura_obj)/altura_objPix

            mask_l.append(mask)

            if cm_distance_izq < (cm_distance_der - 1.5) or cm_distance_izq > (cm_distance_der + 1.5):
                print(f"Distancia del hombro der a cirtura der: {cm_distance_der}cm")
                print(f"Distancia del hombro izq a cirtura izq: {cm_distance_izq}cm")
                print("Deteccion de posible diferencia de hombro")
                a = "deteccion de posible diferencia de hombro"
                return mask_l, cm_distance_der, cm_distance_izq, a
            else:
                print(f"Distancia del hombro der a cirtura der: {cm_distance_der}cm")
                print(f"Distancia del hombro izq a cirtura izq: {cm_distance_izq}cm")
                print("No se detecto diferencia de hombro")
                a = "no se detecto diferencia de hombro"
                return mask_l, cm_distance_der, cm_distance_izq, a
                

            # cv2.namedWindow('Linea de contorno a contorno', cv2.WINDOW_NORMAL)
            # cv2.imshow('Linea de contorno a contorno', mask)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()