from flask import Flask, render_template, request,send_file,send_from_directory,url_for,jsonify
import pandas as pd
import xlrd
import olefile
import xlwings as xw
import numpy as np
from datetime import timedelta

App_dic = {
            "MiniApp_df": pd.DataFrame(),
            "ZKT_df": pd.DataFrame(),
            "MTDP_df": pd.DataFrame(),
            "MiniApp_total_revenue":str(0),
            "MiniApp_total_volume":str(0),
            "MiniApp_total_order":str(0),
            "MiniApp_total_Mgmtfee":str(0),
            "MiniApp_total_AssociatesIncentive":str(0),
            "MiniApp_total_profit":str(0),
           #"顾客实付","促销费","服务费","商家应得" MTDP
           "MTDP_total_revenue":str(0),
           "MTDP_total_service_fee":str(0),
           "MTDP_total_order":str(0),
           "MTDP_total_profit":str(0),
           
           #ZKT "交易服务费","系统服务费","营销推广费"
           "ZKT_total_revenue":str(0),
            "ZKT_total_mgmt_fee":str(0),
            "ZKT_total_associates_incentive":str(0),
            "ZKT_total_profits":str(0),
            "ZKT_total_order":str(0)
           }



def analyze_miniApp(MiniApp_url):
    #the input url of MiniApp_url
    MiniApp_workbook = xlrd.open_workbook(MiniApp_url, ignore_workbook_corruption=True)  
    MiniApp_df = pd.read_excel(MiniApp_workbook,skiprows=1,names=['订单号', '订单时间', '微信支付交易单号', '菜品券号', '菜品ID', '菜品名称', '菜品价格', '所属餐厅', '状态', '状态更新时间', '金额'])
    MiniApp_df["order"] = 1
    MiniApp_df["Mgmt_Fee"] = MiniApp_df.apply(lambda row: 0.006*float(row["金额"]),axis=1)
    MiniApp_df["profit"] = MiniApp_df.apply(lambda row: 0.994*float(row["金额"]),axis=1)
    App_dic["MiniApp_df"] = MiniApp_df
    MiniApp_df_pivot = pd.pivot_table(MiniApp_df,values=["菜品价格","金额","order","Mgmt_Fee","profit"],columns=["菜品ID","菜品名称","所属餐厅","状态"] ,
                                        aggfunc={"菜品价格":np.sum,"金额":np.sum,"order":np.sum, "Mgmt_Fee":np.sum,"profit":np.sum})

    
    MiniApp_df_pivot_transpose = pd.DataFrame(MiniApp_df_pivot.values.T, index=MiniApp_df_pivot.columns, columns=MiniApp_df_pivot.index)
    #add_dic ={"菜品ID":"total","菜品名称":"total",	"所属餐厅":"total",	"状态":"total",	"菜品价格":str(sum(MiniApp_df["菜品价格"])),"金额":str(sum(MiniApp_df["金额"])),"order":str(sum(MiniApp_df["order"]))}
    #MiniApp_df_pivot_transpose.append(add_dic,ignore_index=True)
    MiniApp_df_pivot_transpose.loc["Total",:] = MiniApp_df_pivot_transpose.sum().values
    return MiniApp_df_pivot_transpose


def zkt_valid_order(input_type):
    if "正常" in input_type:
        return 1
    else:
        return -1

def analyze_zkt(ZKT_url):
    
    ZKT_csv = pd.read_csv(ZKT_url)
    # data clean for ` and space 
    ZKT_csv["类型"]=ZKT_csv.apply(lambda row: row["类型"].replace("`",""),axis=1)
    ZKT_csv["产品名称"]=ZKT_csv.apply(lambda row: row["产品名称"].replace("`",""),axis=1)
    ZKT_csv["产品名称"]=ZKT_csv.apply(lambda row:row["产品名称"].strip(),axis=1)
    ZKT_csv["类型"]=ZKT_csv.apply(lambda row: row["类型"].strip(),axis=1)
    ZKT_csv["order"] = ZKT_csv.apply(lambda row: zkt_valid_order(row["类型"]),axis=1)
    App_dic["ZKT_df"] = ZKT_csv
    #calculate 现金账户进项	交易服务费	系统服务费	营销推广费	实际结算
    #only calculate those transaction under normal type 
    #create pivot table for ZKT for "现金账户进项","交易服务费","系统服务费","营销推广费","实际结算","售价"
    ZKT_pivot_table = pd.pivot_table(ZKT_csv,values=["现金账户进项","交易服务费","系统服务费","营销推广费","实际结算","售价","order"],columns=["产品名称","类型"],
                                     aggfunc={"现金账户进项":np.sum,"交易服务费":np.sum,"系统服务费":np.sum,"营销推广费":np.sum,"实际结算":np.sum,"售价":np.sum,"order":np.sum})
    #transpose the whole dataframe
    ZKT_pivot_table_transpose = pd.DataFrame(ZKT_pivot_table.values.T, index=ZKT_pivot_table.columns, columns=ZKT_pivot_table.index)
    
    ZKT_pivot_table_transpose.loc["Total",:] = ZKT_pivot_table_transpose.sum().values
    return ZKT_pivot_table_transpose

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',App_dic=App_dic)


def trim_date(input_date):
    input_date = input_date.replace("`","")
    trime_date = input_date[0:11].replace(" ","")
    return trime_date

@app.route('/get_ZKT_piechart_data')
def get_ZKT_piechart_data():
    tmp_ZKT_raw_df = App_dic["ZKT_df"]
    ZKT_df_pivot_table = pd.DataFrame()
    while len(tmp_ZKT_raw_df) > 0:
        tmp_ZKT_raw_df["date"] = tmp_ZKT_raw_df.apply(lambda row: trim_date(row["结算日期"]),axis=1)
        tmp_ZKT_raw_df["revenue"] = tmp_ZKT_raw_df["实际结算"]
        tmp_ZKT_raw_df_update = tmp_ZKT_raw_df[["产品一级分类名称","revenue"]]
        tmp_ZKT_raw_pivot_df = tmp_ZKT_raw_df_update.groupby(by="产品一级分类名称").sum()
        tmp_ZKT_raw_pivot_df = tmp_ZKT_raw_pivot_df.reset_index()
        output_list = []
        output_item_list = list(tmp_ZKT_raw_pivot_df["产品一级分类名称"])
        output_revenue_list = list(tmp_ZKT_raw_pivot_df["revenue"])
        for i in range(len(output_item_list)):
            tmp_dic = {}
            tmp_revenue = output_revenue_list[i]
            tmp_item = output_item_list[i]
            tmp_dic["item"] =  tmp_item
            tmp_dic["revenue"] = tmp_revenue
            output_list.append(tmp_dic)

        return jsonify(output_list)

@app.route('/get_ZKT_linechart_data')
def get_ZKT_linechart_data():
    tmp_ZKT_raw_df = App_dic["ZKT_df"]
    while len(tmp_ZKT_raw_df)>0:
    
        tmp_ZKT_raw_df["date"] = tmp_ZKT_raw_df.apply(lambda row: trim_date(row["结算日期"]),axis=1)
        tmp_ZKT_raw_df["revenue"] = tmp_ZKT_raw_df["实际结算"]
        output_raw_data = tmp_ZKT_raw_df[["date","revenue"]]

        output_data = output_raw_data.groupby(by="date").sum()
       
        output_data = output_data.reset_index()
        output_date_list = list(output_data["date"])
        output_revenue_list = list(output_data["revenue"])
        output_list = []
        for i in range(len(output_date_list)):
            tmp_dic = {}
            tmp_date = output_date_list[i]
            tmp_revenue = output_revenue_list[i]
            tmp_dic["date"] = tmp_date
            tmp_dic["revenue"] = tmp_revenue
            output_list.append(tmp_dic)
        
        return jsonify(output_list)

@app.route('/get_MTDP_piechart_data')
def get_MTDP_piechart_data():
    tmp_MTDP_raw_df = App_dic["MTDP_df"]
    MTDP_df_pivot_table = pd.DataFrame()
    while len(tmp_MTDP_raw_df) > 0:
        tmp_MTDP_raw_df["date"] = tmp_MTDP_raw_df.apply(lambda row: trim_date(row["消费|撤销时间"]),axis=1)
        tmp_MTDP_raw_df["revenue"] = tmp_MTDP_raw_df["商家应得"]
        tmp_MTDP_raw_df_update = tmp_MTDP_raw_df[["项目","revenue"]]
        tmp_MTDP_raw_pivot_df = tmp_MTDP_raw_df_update.groupby(by="项目").sum()
        tmp_MTDP_raw_pivot_df = tmp_MTDP_raw_pivot_df.reset_index()
        output_list = []
        output_item_list = list(tmp_MTDP_raw_pivot_df["项目"])
        output_revenue_list = list(tmp_MTDP_raw_pivot_df["revenue"])
        for i in range(len(output_item_list)):
            tmp_dic = {}
            tmp_revenue = output_revenue_list[i]
            tmp_item = output_item_list[i]
            tmp_dic["item"] =  tmp_item
            tmp_dic["revenue"] = tmp_revenue
            output_list.append(tmp_dic)

        return jsonify(output_list)

@app.route('/get_MTDP_linechart_data')
def get_MTDP_linechart_data():
    tmp_MTDP_raw_df = App_dic["MTDP_df"]
    while len(tmp_MTDP_raw_df)>0:
    
        tmp_MTDP_raw_df["date"] = tmp_MTDP_raw_df.apply(lambda row: trim_date(row["消费|撤销时间"]),axis=1)
        tmp_MTDP_raw_df["revenue"] = tmp_MTDP_raw_df["顾客实付"]
        output_raw_data = tmp_MTDP_raw_df[["date","revenue"]]

        output_data = output_raw_data.groupby(by="date").sum()
       
        output_data = output_data.reset_index()
        output_date_list = list(output_data["date"])
        output_revenue_list = list(output_data["revenue"])
        output_list = []
        for i in range(len(output_date_list)):
            tmp_dic = {}
            tmp_date = output_date_list[i]
            tmp_revenue = output_revenue_list[i]
            tmp_dic["date"] = tmp_date
            tmp_dic["revenue"] = tmp_revenue
            output_list.append(tmp_dic)
        
        return jsonify(output_list)





@app.route('/get_MiniApp_piechart_data')
def get_MiniApp_piechart_data():
    tmp_MiniApp_raw_df = App_dic["MiniApp_df"]
    MiniApp_df_pivot_table = pd.DataFrame()
    while len(tmp_MiniApp_raw_df) > 0:
        tmp_MiniApp_raw_df["date"] = tmp_MiniApp_raw_df.apply(lambda row: trim_date(row["订单时间"]),axis=1)
        tmp_MiniApp_raw_df["revenue"] = tmp_MiniApp_raw_df["金额"]
        tmp_MiniApp_raw_df_update = tmp_MiniApp_raw_df[["菜品名称","revenue"]]
        tmp_MiniApp_raw_pivot_df = tmp_MiniApp_raw_df_update.groupby(by="菜品名称").sum()
        tmp_MiniApp_raw_pivot_df = tmp_MiniApp_raw_pivot_df.reset_index()
        output_list = []
        output_item_list = list(tmp_MiniApp_raw_pivot_df["菜品名称"])
        output_revenue_list = list(tmp_MiniApp_raw_pivot_df["revenue"])
        for i in range(len(output_item_list)):
            tmp_dic = {}
            tmp_revenue = output_revenue_list[i]
            tmp_item = output_item_list[i]
            tmp_dic["item"] =  tmp_item
            tmp_dic["revenue"] = tmp_revenue
            output_list.append(tmp_dic)

        return jsonify(output_list)

@app.route('/get_MiniApp_linechart_data')
def get_MiniApp_linechart_data():
    tmp_MiniApp_raw_df = App_dic["MiniApp_df"]
    while len(tmp_MiniApp_raw_df)>0:
    
        tmp_MiniApp_raw_df["date"] = tmp_MiniApp_raw_df.apply(lambda row: trim_date(row["订单时间"]),axis=1)
        tmp_MiniApp_raw_df["revenue"] = tmp_MiniApp_raw_df["金额"]
        output_raw_data = tmp_MiniApp_raw_df[["date","revenue"]]

        output_data = output_raw_data.groupby(by="date").sum()
       
        output_data = output_data.reset_index()
        output_date_list = list(output_data["date"])
        output_revenue_list = list(output_data["revenue"])
        output_list = []
        for i in range(len(output_date_list)):
            tmp_dic = {}
            tmp_date = output_date_list[i]
            tmp_revenue = output_revenue_list[i]
            tmp_dic["date"] = tmp_date
            tmp_dic["revenue"] = tmp_revenue
            output_list.append(tmp_dic)
        
        return jsonify(output_list)
    



@app.route('/Minidata', methods=[ 'POST'])
def Minidata():
    if request.method == 'POST':
        MiniApp_name = request.files['upload-file']
        #workbook = xlrd.open_workbook(MiniApp_name, ignore_workbook_corruption=True)
        MiniApp_name_string = "./"+str(MiniApp_name.filename)
        MiniApp_result = analyze_miniApp(MiniApp_name_string)
        MiniApp_output_path = "MiniApp_output.csv"
        MiniApp_result.to_csv(MiniApp_output_path,encoding='utf-8_sig')
        MiniApp_result_copy = MiniApp_result
        MiniApp_total_revenue = str(MiniApp_result_copy.loc[('Total','','',''),"金额"])
        #output at the same path
        App_dic["MiniApp_total_revenue"]="￥"+str(MiniApp_total_revenue)
        App_dic["MiniApp_total_order"] = str(MiniApp_result_copy.loc[('Total','','',''),"order"])
        App_dic["MiniApp_total_Mgmtfee"] = str(MiniApp_result_copy.loc[('Total','','',''),"Mgmt_Fee"])
        App_dic["MiniApp_total_AssociatesIncentive"] =  str(0)
        MiniApp_total_profit = float(MiniApp_total_revenue) - float(MiniApp_result_copy.loc[('Total','','',''),"Mgmt_Fee"])
        App_dic["MiniApp_total_profit"] = str(MiniApp_total_profit)

        return render_template('miniapp_box.html',App_dic=App_dic)

@app.route('/ZKTdata', methods=['POST'])
def ZKTdata():
    if request.method == 'POST':
        zkt_name = request.files['upload-file']
        zkt_name_string = "./"+str(zkt_name.filename)
        zkt_result = analyze_zkt(zkt_name_string)
        zkt_output_path = "ZKT_output.csv"
        zkt_result.to_csv(zkt_output_path,encoding='utf-8_sig')
        zkt_result_copy = zkt_result
        zkt_total_revenue= str(zkt_result_copy.loc[("Total",""),"现金账户进项"])
        App_dic["ZKT_total_revenue"]="￥"+str(zkt_total_revenue)
        ZKT_total_mgmt_fee = float(zkt_result_copy.loc[("Total",""),"交易服务费"]) + float(zkt_result_copy.loc[("Total",""),"系统服务费"])
        ZKT_total_associates_incentive = float(zkt_result_copy.loc[("Total",""),"营销推广费"])
        App_dic["ZKT_total_mgmt_fee"] = "￥"+str(ZKT_total_mgmt_fee)
        App_dic["ZKT_total_associates_incentive"] = "￥"+str(ZKT_total_associates_incentive)
        App_dic["ZKT_total_profits"] =  "￥"+str(zkt_result_copy.loc[("Total",""),"实际结算"])
        App_dic["ZKT_total_order"] = str(zkt_result_copy.loc[("Total",""),"order"])
        return render_template('ZKT_box.html',App_dic=App_dic)


def analyze_mtdp(MTDP_url):

    MTDP_df = pd.read_excel(MTDP_url)
    MTDP_df["order"] = 1
    MTDP_pivot_table = pd.pivot_table(MTDP_df,values=["原价","顾客实付","促销费","服务费","商家应得","order"],columns=["项目"],
                                        aggfunc={"原价":np.sum,"顾客实付":np.sum,"促销费":np.sum,"服务费":np.sum,"商家应得":np.sum,"order":np.sum})
    App_dic["MTDP_df"] = MTDP_df
    MTDP_pivot_table_columns = MTDP_pivot_table.columns.to_list()
    MTDP_pivot_table_index = MTDP_pivot_table.index.to_list()
    MTDP_pivot_table_transpose = pd.DataFrame(MTDP_pivot_table.values.T,columns = MTDP_pivot_table_index, index = MTDP_pivot_table_columns)
    MTDP_pivot_table_transpose.loc["Total",:] = MTDP_pivot_table_transpose.sum().values
    return MTDP_pivot_table_transpose

@app.route('/MTDPdata', methods=['POST'])
def MTDPdata():
    #项目 原价	顾客实付	促销费	服务费	商家应得
    if request.method == 'POST':
        mtdp_name = request.files['upload-file']
        mtdp_name_string = "./"+str(mtdp_name.filename)

        MTDP_df = analyze_mtdp(mtdp_name_string)
        MTDP_df_copy = MTDP_df
        #print(MTDP_df_copy.index)
        App_dic["MTDP_total_revenue"] = str(MTDP_df_copy.loc["Total","顾客实付"])
        MTDP_df.to_csv("MTDP_output.csv",encoding='utf-8_sig')
        MTDP_mgmt_fee = float(MTDP_df_copy.loc[["Total"],"促销费"])+float(MTDP_df_copy.loc[["Total"],"服务费"])
        App_dic["MTDP_total_mgmt_fee"] = MTDP_mgmt_fee
        App_dic["MTDP_total_order"] = float(MTDP_df_copy.loc[["Total"],"order"])
        App_dic["MTDP_total_profit"] = float(MTDP_df_copy.loc[["Total"],"商家应得"])
        return render_template('MTDP_box.html',App_dic=App_dic)

@app.route('/download')
def download_file():
    ZKT_summary_name ="ZKT_summary.xlsx"
    ZKT_workbook(ZKT_summary_name)
    ZKT_file.to_excel("download_output",'utf-8_sig')
    #return send_file(ZKT_file, as_attachment = True)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['JSON_AS_ASCII'] = False
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
    app.run(debug=True)
