from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

# 預設資料列
DownloadInfo=[['BCU Utility and Configure File - CPS', 'P00V2E-B2A', 100, 'Application', 'customer'], ['Dump BCU before and after downloading customer image Hook - CPS', 'P00PS9-B2D', 100, 'GBUHOOK', 'var'], ['Benny', 'P00000-000', 100, 'Application', 'customer'], ['MPM Unlock support flag for Diags - CPS', 'P00TKB-B2A', 100, 'DIAGS', 'diags'], ['MSC - NTFS (26GB / 1.5GB)', 'P00LWZ-B2A', 100, 'MSC', None], ['Windows Push Button Reset Recovery - CPS', 'P012LZ-B2D', 100, 'OS', 'customer'], ['Mia', 'P11111-111', 111, 'OS', 'customer'],['BCU Utility and Configure File - CPS', 'P00V2E-B2A', 100, 'Application', 'customer'], ['Dump BCU before and after downloading customer image Hook - CPS', 'P00PS9-B2D', 100, 'GBUHOOK', 'var'], ['Benny', 'P00000-000', 100, 'Application', 'customer'], ['MPM Unlock support flag for Diags - CPS', 'P00TKB-B2A', 100, 'DIAGS', 'diags'], ['MSC - NTFS (26GB / 1.5GB)', 'P00LWZ-B2A', 100, 'MSC', None], ['Windows Push Button Reset Recovery - CPS', 'P012LZ-B2D', 100, 'OS', 'customer'], ['Mia', 'P11111-111', 111, 'OS', 'customer'],['BCU Utility and Configure File - CPS', 'P00V2E-B2A', 100, 'Application', 'customer'], ['Dump BCU before and after downloading customer image Hook - CPS', 'P00PS9-B2D', 100, 'GBUHOOK', 'var'], ['Benny', 'P00000-000', 100, 'Application', 'customer'], ['MPM Unlock support flag for Diags - CPS', 'P00TKB-B2A', 100, 'DIAGS', 'diags'], ['MSC - NTFS (26GB / 1.5GB)', 'P00LWZ-B2A', 100, 'MSC', None], ['Windows Push Button Reset Recovery - CPS', 'P012LZ-B2D', 100, 'OS', 'customer'], ['Mia', 'P11111-111', 111, 'OS', 'customer']]


def Search():
	Search_string = sStr.get()
	selections = []
	for rowid in trv.get_children():
		if Search_string.lower() in trv.item(rowid)['values'][0].lower() or Search_string.lower() in trv.item(rowid)['values'][1].lower():   # compare strings in  lower cases.
			selections.append(rowid)
	trv.selection_set(selections)

def Unselect_All():
	print('Unselect All Components')
	for rowid in trv.get_children():
		if trv.item(rowid, 'tags')[0] == 'checked':
			trv.item(rowid, tags='unchecked')

def Select_All():
	print('Select All Components')
	for rowid in trv.get_children():
		if trv.item(rowid, 'tags')[0] == 'unchecked':
			trv.item(rowid, tags='checked')

def Download():
	downloadItemList=[]
	for rowid in trv.get_children():
		if trv.item(rowid, 'tags')[0] == 'checked':
			downloadItemList.append(trv.item(rowid)['values'])
	print(downloadItemList)

def togglecheck(event):
	rowid = trv.identify_row(event.y)
	if len(rowid) == 0:
		return
	tag = trv.item(rowid, 'tags')[0]
	tags = list(trv.item(rowid, 'tags'))
	print(trv.item(rowid)['values'][0])
	tags.remove(tag)
	# trv.item(rowid, tags=tags)
	if tag == 'checked':
		trv.item(rowid, tags='unchecked')
	else:
		trv.item(rowid, tags='checked')

# def getrow(event):
# 	rowid = trv.identify_row(event.y)
# 	tag = trv.item(rowid, 'tags')[0]
# 	print(tag)
# 	tags = list(trv.item(rowid, 'tags'))
# 	print(tags)
# 	tags.remove(tag)
# 	# print(tag)
# 	print(tags)
# 	print(tag)
# 	print(rowid)
# 	print(trv.item(rowid))

# def getcol(event):
# 	colid = trv.identify_column(event.x)
# 	item = trv.item(trv.focus())
# 	print(item['values'][2])
# 	print(colid)
# 	# print(trv.set(trv.identify_row(event.y)))



# 根UI宣告
root = Tk()

# 區塊宣告
section1 = LabelFrame(root, text='Component List')
section2 = LabelFrame(root, text='Actions')
section3 = LabelFrame(root, text='Process Log')
section1.pack(fill='both', expand='no', padx=20, pady=5, ipadx=10, ipady=3)
section2.pack(fill='both', expand='no', padx=20, pady=5, ipadx=10, ipady=3)
section3.pack(fill='both', expand='YES', padx=20, pady=5, ipadx=10, ipady=3)


# 其他變數宣告
sStr = StringVar()
im_checked = ImageTk.PhotoImage(Image.open('checked20.png'))
im_unchecked = ImageTk.PhotoImage(Image.open('unchecked20.png'))


# ================== 第一區塊 表格宣告 ==================
trv = ttk.Treeview(section1, height='15', columns=('ComponentName','PartNo','PrismVer','DownloadType'))
style = ttk.Style(trv)
trv.pack()

trv.tag_configure('checked', image=im_checked)
trv.tag_configure('unchecked', image=im_unchecked)

trv.heading('#0', text='Check')
trv.heading('ComponentName', text='Component Name')
trv.heading('PartNo', text='Part No')
trv.heading('PrismVer', text='Prism Ver')
trv.heading('DownloadType', text='Download Type')

trv.column('#0',width=45)
trv.column('ComponentName',width=400)
trv.column('PartNo',width=100, anchor='center')
trv.column('PrismVer',width=100, anchor='center')
trv.column('DownloadType',width=100, anchor='center')


# 將預設資料列輸進第一區塊裡面的表格
for i in range(0,len(DownloadInfo)):
	trv.insert('',i ,value=(DownloadInfo[i][0],DownloadInfo[i][1],DownloadInfo[i][2],DownloadInfo[i][4]), tags='checked')

trv.bind('<Button 1>', togglecheck)
# trv.bind('<Button 1>', getrow)
# trv.bind('<Button 1>', getcol)


# ================== 第二區塊 功能按鈕宣告 ==================
sLab = Label(section2, text='Search:')
sLab.grid(column=0, row=0)
sEnt = Entry(section2, textvariable=sStr)
sEnt.grid(column=1, row=0)
sBtn = Button(section2, text='Search', command=Search)
sBtn.grid(column=2, row=0, padx=10)
UnselAllBtn = Button(section2, text='Unselect All', command=Unselect_All)
UnselAllBtn.grid(column=0, row=1, padx=10)
selAllBtn = Button(section2, text='Select All', command=Select_All)
selAllBtn.grid(column=1, row=1, padx=10)
Download_Btn = Button(section2, text='Download', command=Download)
Download_Btn.grid(column=0, row=2, padx=10, pady=10)


# ================== 第三區塊 功能按鈕宣告 ==================
showLog = Label(section3, text='Log shows here', height=15, width=150,bg='white', anchor='nw', pady=10, relief="sunken")
showLog.pack()



# 根UI設定
root.title('CoreML Download Tool')
root.geometry('800x750')
root.resizable(0,0)
root.mainloop()