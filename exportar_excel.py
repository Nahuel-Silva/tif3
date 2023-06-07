import pandas as pd
import datetime

class ExportExcel():

    def generate_csv(self, med_izq, med_der, c):
        
        
        data = {
            "numero imagen":c,
            "medida del lado izquierdo":f"{med_izq}cm",
            "medida del lado derecho":f"{med_der}cm",
            "fecha": datetime.datetime.now()
        }

        df = pd.DataFrame(data)
        with pd.ExcelWriter('./excel/paciente.xlsx', engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')