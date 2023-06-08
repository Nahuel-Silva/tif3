import pandas as pd
import datetime

class ExportExcel():

    def generate_csv(self, med_izq, med_der, c):
        
        
        data = {
            "numero imagen":c,
            "medida del lado izquierdo (cm)":med_izq,
            "medida del lado derecho (cm)":med_der,
            "fecha": datetime.datetime.now()
        }

        df = pd.DataFrame(data)
        with pd.ExcelWriter('./excel/paciente.xlsx', engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')