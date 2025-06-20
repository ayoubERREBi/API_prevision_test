import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt



class forcasting():
    def __init__(self):
        pass
    
    
    def read_data(self):
        df21=pd.read_csv("2021.csv",parse_dates=["Date"],dtype={"Item Code": str})
        df22=pd.read_csv("2022.csv",parse_dates=["Date"],dtype={"Item Code": str})
        df23=pd.read_csv("2023.csv",parse_dates=["Date"],dtype={"Item Code": str})
        df24=pd.read_csv("2024.csv",parse_dates=["Date"],dtype={"Item Code": str})

        daily_sales_21 = df21.groupby(["Item Code","Date"])["Delivered Qty"].sum().reset_index()
        daily_sales_22 = df22.groupby(["Item Code","Date"])["Delivered Qty"].sum().reset_index()
        daily_sales_23 = df23.groupby(["Item Code","Date"])["Delivered Qty"].sum().reset_index()
        daily_sales_24 = df24.groupby(["Item Code","Date"])["Delivered Qty"].sum().reset_index()

        daily_sales_21 = daily_sales_21.sort_values(by="Date")
        daily_sales_22 = daily_sales_22.sort_values(by="Date")
        daily_sales_23 = daily_sales_23.sort_values(by="Date")
        daily_sales_24 = daily_sales_24.sort_values(by="Date")

        daily_sales_23 = daily_sales_23[daily_sales_23["Date"]>="2023-01"]
        daily_sales_24 = daily_sales_24[daily_sales_24["Date"]>="2024-01"]

        all_sales = pd.concat([daily_sales_21,daily_sales_22,daily_sales_23,daily_sales_24],ignore_index=True)
        
        return all_sales
    
    
    def choose_prod(self,prod_id):
        all_sales = self.read_data()
        prod = all_sales[all_sales["Item Code"]==prod_id]
        #prod = prod.set_index('Date').asfreq('D').reset_index()
        #prod['Delivered Qty'] = prod['Delivered Qty'].fillna(prod['Delivered Qty'].rolling(window=7, min_periods=1).mean())
        return prod


    def detect_outliers_iqr(self,data):
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 2.5 * iqr
        upper_bound = q3 + 2.5 * iqr
        return data[(data < lower_bound) | (data > upper_bound)]
    
    def correct_outliers(self,prod):
        outliers_iqr = self.detect_outliers_iqr(prod["Delivered Qty"])

        prod["Delivered Qty_NonOutliers"] = prod["Delivered Qty"]
        prod.loc[outliers_iqr.index, "Delivered Qty_NonOutliers"] = np.nan
        prod["Delivered Qty_NonOutliers"] = prod["Delivered Qty_NonOutliers"].interpolate(method='linear')
        #prod.drop(columns='Delivered Qty',inplace=True)
        
        return prod
    
f= forcasting()  
s=f.read_data()
prod_75135_2 =  f.choose_prod('75497') 
prod_75135_2 = f.correct_outliers(prod_75135_2)
print(prod_75135_2.head())
    




        


