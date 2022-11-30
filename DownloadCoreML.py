import os
import xlrd
import time
import socket
from datetime import datetime

# 宣告log變數
logpath = 'process.log'
f = open(logpath, 'a')
result = 'NA'

# Function-判斷是否可以連到server
def Authorize():
	ip = socket.gethostbyname(socket.gethostname())
	iplist = ip.split(".")
	if iplist[0]=='10' and iplist[1]=='109':
		return True
	else:
		return False
# Function-設定一個包含switch case，把文件的"Deliverable Type"轉換成下載時會用到的downloadtype
def switch(switchType):
	match switchType:
		case "Application":
			return "customer"
		case "GBUHOOK":
			return "var"
		case "Driver":
			return "customer"
		case "DIAGS":
			return "diags"
		case "MSC":
			return None
		case "Factory Driver":
			return None
		case "OS":
			return "customer"
		case _:
			return "---fail----"
# Function-抓取當下時間，以便輸出至log
def GetNowTime():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# Function-用ExtractAssembly.exe去下載Component
def download(ComName, PN, DLtype):
	if DLtype == None:
		print('['+GetNowTime()+']'+' ExtractAssembly.exe --sserver 10.110.20.52 --assembly '+PN+' --localpath "%CD%\\Download\\'+ComName+'\\'+PN+'"', file=f)
		result = os.system('%CD%\\ExtractAssemblyKits\\ExtractAssembly.exe --sserver 10.110.20.52 --assembly '+PN+' --localpath "%CD%\\Download\\'+ComName+'\\'+PN+'"')
		return result
	else:
		print('['+GetNowTime()+']'+' ExtractAssembly.exe --sserver 10.110.20.52 --assembly '+PN+' --localpath "%CD%\\Download\\'+ComName+'\\'+PN+'"'+' --downloadtype '+DLtype, file=f)
		result = os.system('%CD%\\ExtractAssemblyKits\\ExtractAssembly.exe --sserver 10.110.20.52 --assembly '+PN+' --localpath "%CD%\\Download\\'+ComName+'\\'+PN+'"'+' --downloadtype '+DLtype)
		return result

print('******************* Start *******************', file=f)

# 檢查使否可以連線
if Authorize() == False:
	print('['+GetNowTime()+']'+' Connection is False', file=f)
	f.close()
	quit()

# 篩選檔案名稱為 .xls 或 .xlsx
for Allfiles in os.listdir(os.curdir):
        if '.xls' in Allfiles or '.xlsx' in Allfiles:
            xlPinCoreML_Name = Allfiles
            break

# 列印出檔案名稱
print('['+GetNowTime()+']'+' PIN Core ML: '+xlPinCoreML_Name, file=f)

xlPinCoreML_WB = xlrd.open_workbook(xlPinCoreML_Name)
xlPinCoreML_WS = xlPinCoreML_WB.sheets()[0]
xlPinCoreML_WSName = xlPinCoreML_WB.sheets()[0].name

# 預設只有第一個分頁會有資料，直接抓取第一個分頁的資料
print('['+GetNowTime()+']'+' Sheet Name: '+xlPinCoreML_WSName, file=f)
# Total的欄位數(有值的)
print('['+GetNowTime()+']'+' Total Col Amount: '+str(xlPinCoreML_WS.ncols), file=f)
# Total的列(行)數(有值的)
print('['+GetNowTime()+']'+' Total Row Amount: '+str(xlPinCoreML_WS.nrows), file=f)

# 抓取"Name", "PartNo", "PRISM Revision", "Deliverable Type"的欄位Index數
for i in range(0, xlPinCoreML_WS.ncols):
	if xlPinCoreML_WS.row(0)[i].value == "Name":
		Name_col = i
		print('['+GetNowTime()+']'+' \"Name\" Colume Index: '+str(Name_col), file=f)
	if xlPinCoreML_WS.row(0)[i].value == "PartNo":
		PartNo_col = i
		print('['+GetNowTime()+']'+' \"PartNo\" Colume Index: '+str(PartNo_col), file=f)
	if xlPinCoreML_WS.row(0)[i].value == "PRISM Revision":
		PrismVer_col = i
		print('['+GetNowTime()+']'+' \"PRISM Reversion\" Colume Index: '+str(PrismVer_col), file=f)
	if xlPinCoreML_WS.row(0)[i].value == "Deliverable Type":
		DeliverType_col = i
		print('['+GetNowTime()+']'+' \"Deliverable Type\" Colume Index: '+str(DeliverType_col), file=f)

# 宣告一個名稱叫做DownloadInfo的list
# 分別設定變數去抓去每一列(Row)中，特定欄位(Name, PartNo, PRISM Revision, Deliverable Type)的值
# 另外再針對"Deliverable Type"去用switch function去轉成我們要的downloadtype
# 轉成downloadtype之後在append到list的最後面
DownloadInfo = list([])
for i in range(1, xlPinCoreML_WS.nrows):
	name = (xlPinCoreML_WS.cell(i,Name_col)).value
	partNo = (xlPinCoreML_WS.cell(i,PartNo_col)).value
	prismVer = int((xlPinCoreML_WS.cell(i,PrismVer_col)).value)
	switchType = str.strip((xlPinCoreML_WS.cell(i,DeliverType_col)).value)
	downloadType = switch(switchType)
	DownloadInfo.append([name,partNo,prismVer,switchType,downloadType])

# 開始下載Component
for item in DownloadInfo:
	print('['+GetNowTime()+']'+' Downloading...', file=f)
	print('['+GetNowTime()+'] ', end='', file=f)
	print(item, file=f)
	if download(item[0],item[1],item[4]) == 0:
		print('['+GetNowTime()+']'+' PASS', file=f)
	else:
		print('['+GetNowTime()+']'+' FAIL', file=f)
		print('error code = '+str(result), file=f)