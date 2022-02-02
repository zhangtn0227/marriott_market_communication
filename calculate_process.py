import pandas as pd
import numpy as np
import xlrd

#"ZKT.csv"
def calculate_ZKT(ZKT_input):
    
    ZKT_csv = pd.read_csv(ZKT_input)
    
    # data clean for ` and space 
    ZKT_csv["类型"]=ZKT_csv.apply(lambda row: row["类型"].replace("`",""),axis=1)
    ZKT_csv["产品名称"]=ZKT_csv.apply(lambda row: row["产品名称"].replace("`",""),axis=1)
    ZKT_csv["产品名称"]=ZKT_csv.apply(lambda row:row["产品名称"].strip(),axis=1)
    ZKT_csv["类型"]=ZKT_csv.apply(lambda row: row["类型"].strip(),axis=1)
    
    #calculate 现金账户进项	交易服务费	系统服务费	营销推广费	实际结算
    #only calculate those transaction under normal type 
    #create pivot table for ZKT for "现金账户进项","交易服务费","系统服务费","营销推广费","实际结算","售价"
    ZKT_pivot_table = pd.pivot_table(ZKT_csv,values=["现金账户进项","交易服务费","系统服务费","营销推广费","实际结算","售价"],columns=["产品名称","类型"],
                                     aggfunc={"现金账户进项":np.sum,"交易服务费":np.sum,"系统服务费":np.sum,"营销推广费":np.sum,"实际结算":np.sum,"售价":np.sum})
    #transpose the whole dataframe
    ZKT_pivot_table_transpose = pd.DataFrame(ZKT_pivot_table.values.T, index=ZKT_pivot_table.columns, columns=ZKT_pivot_table.index)
    ZKT_pivot_table_transpose["count"]=0
    #calculate count number of 
    for i in ZKT_pivot_table_transpose.index:
        if i[0] in list(ZKT_csv["产品名称"].values):
            txn_count = len(ZKT_csv[(ZKT_csv["产品名称"]==i[0])&(ZKT_csv["类型"]==i[1])])
            ZKT_pivot_table_transpose.loc[i,"count"] =str(txn_count)
    ZKT_output = ZKT_input.split(".")[0]+"_output"+ZKT_input.split(".")[1]
    ZKT_pivot_table_transpose.to_csv(ZKT_output)
    return ZKT_pivot_table_transpose
    
print(calculate_ZKT("ZKT.csv"))

workbook = xlrd.open_workbook('MiniApp.xls', ignore_workbook_corruption=True)  
MiniApp_df = pd.read_excel(workbook,skiprows=1,names=['订单号', '订单时间', '微信支付交易单号', '菜品券号', '菜品ID', '菜品名称', '菜品价格', '所属餐厅', '状态', '状态更新时间', '金额'])
MiniApp_df_pivot = pd.pivot_table(MiniApp_df,values=["菜品价格","金额"],columns=["菜品ID","菜品名称","所属餐厅","状态"] ,
                                     aggfunc={"菜品价格":np.sum,"金额":np.sum})
MiniApp_df_pivot

#MTDP.xlsx
#项目 原价	顾客实付	促销费	服务费	商家应得
MTDP_df = pd.read_excel('MTDP.xlsx')
MTDP_pivot_table = pd.pivot_table(MTDP_df,values=["原价","顾客实付","促销费","服务费","商家应得"],columns=["项目"],
                                     aggfunc={"原价":np.sum,"顾客实付":np.sum,"促销费":np.sum,"服务费":np.sum,"商家应得":np.sum})

MTDP_pivot_table_columns = MTDP_pivot_table.columns.to_list()
MTDP_pivot_table_index = MTDP_pivot_table.index.to_list()
MTDP_pivot_table_transpose = pd.DataFrame(MTDP_pivot_table.values.T,columns = MTDP_pivot_table_index, index = MTDP_pivot_table_columns)
