# -*- coding: utf-8 -*-
import wx

app = wx.App()
frame = wx.Frame(
    None,
    title = 'Generator',
    size = (500,350))

panel = wx.Panel(frame)
count = 0


def openFile(evt):
    dlg = wx.FileDialog(
        frame,
        'Choose',
        '',
        '',
        'All Files (*.*)|*.*',
        wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
    filepath = []
    if dlg.ShowModal() == wx.ID_OK:
        filepath = dlg.GetPaths()
        pass
    else:
        return
    global count
    for x in filepath:
        filelist.InsertStringItem(count,x)
        count += 1


def writecode(l, filepath):
    code = u'''\
# -*- coding: utf-8 -*-
import win32api
l = ''' + str(l) + '''
for x in l:
    win32api.ShellExecute(0, 'open', x, '', '', 1)
'''
    f = open(filepath, 'w')
    f.write(code.encode('gbk'))
    f.close()


def saveFile(evt):
    dlg = wx.FileDialog(
        frame,
        'Save',
        '',
        '',
        'Python files(*.py)|*.py|Python files(*.pyw)|*.pyw',
        wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    filepath = ''
    if dlg.ShowModal() == wx.ID_OK:
        filepath = dlg.GetPath()
    else:
        return
    l = []
    global count
    for x in range(count):
        l.append(filelist.GetItemText(x))
    if l:
        writecode(l,filepath)
        savepath.SetValue(filepath)


def delItem(evt):
    global count
    id = filelist.GetFirstSelected()
    while id != -1:
        filelist.DeleteItem(id)
        count -= 1
        id = filelist.GetFirstSelected()


def turnUp(evt):
    id = filelist.GetFirstSelected()
    if id != -1 and id != 0:
        xpath = filelist.GetItemText(id)
        filelist.DeleteItem(id)
        filelist.InsertStringItem(id-1, xpath)
        filelist.Select(id-1)


def turnDown(evt):
    id = filelist.GetFirstSelected()
    global count
    if id != -1 and id != count-1:
        xpath = filelist.GetItemText(id)
        filelist.DeleteItem(id)
        filelist.InsertStringItem(id+1, xpath)
        filelist.Select(id+1)


choBtn = wx.Button(panel, label='Choose')
choBtn.Bind(wx.EVT_BUTTON, openFile)

bldBtn = wx.Button(panel, label='Build')
bldBtn.Bind(wx.EVT_BUTTON, saveFile)

savepath = wx.TextCtrl(panel, style=wx.TE_READONLY)
filelist = wx.ListCtrl(panel, -1, style=wx.LC_LIST)

delBtn = wx.Button(panel, label='Delete')
delBtn.Bind(wx.EVT_BUTTON, delItem)

upBtn = wx.Button(panel, label='Up')
upBtn.Bind(wx.EVT_BUTTON, turnUp)

downBtn = wx.Button(panel, label='Down')
downBtn.Bind(wx.EVT_BUTTON, turnDown)

fbox = wx.BoxSizer(wx.HORIZONTAL)
fbox.Add(choBtn, proportion=0, flag=wx.ALL, border = 5)
fbox.Add(savepath, proportion=1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
fbox.Add(bldBtn, proportion=0, flag=wx.ALL, border = 5)

sbox = wx.BoxSizer(wx.VERTICAL)
sbox.Add(delBtn, proportion=0, flag=wx.RIGHT | wx.TOP | wx.EXPAND, border = 5)
sbox.Add(upBtn, proportion=0, flag=wx.RIGHT | wx.TOP | wx.EXPAND, border = 5)
sbox.Add(downBtn, proportion=0,
         flag=wx.RIGHT | wx.TOP | wx.BOTTOM | wx.EXPAND, border = 5)

tbox = wx.BoxSizer(wx.HORIZONTAL)
tbox.Add(filelist, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
tbox.Add(sbox, proportion=0, flag=wx.EXPAND | wx.ALL)

fobox = wx.BoxSizer(wx.VERTICAL)
fobox.Add(fbox, proportion=0, flag=wx.EXPAND | wx.ALL)
fobox.Add(tbox, proportion=1, flag=wx.EXPAND | wx.ALL)

panel.SetSizer(fobox)

frame.Show()
app.MainLoop()
