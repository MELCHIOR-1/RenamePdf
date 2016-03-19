# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 23:42:27 2016

@author: gxy
"""


from PyQt4 import QtGui
from ui_rename import *
from PyQt4.QtCore import *
from thesis import *
import os
import shutil

class MainWindow(QtGui.QDialog): 

    def __init__(self,parent=None):

        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_Dialog()# Ui_Dialog为.ui产生.py文件中窗体类名，经测试类名以Ui_为前缀，加上UI窗体对象名（此处为Dialog，见上图）
        self.ui.setupUi(self)
        self.thesisDict = {}
        self.fileNames = []
        self.connect(self.ui.ChooseFileBtn,QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("browse()"))
        self.connect(self.ui.RenameBtn,QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("rename()"))
        self.connect(self.ui.ExportInfoBtn,QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("exportInfo()"))
        self.ui.FileListView.clicked.connect(self.indexMove)
        
    def formatFileName(self,filename):
        if (isinstance(filename, str)):
            tuple=('?','╲','*','/',',','"','<','>','|','“','"','，','‘','”',',','/',':')
            for char in tuple:
                if (filename.find(char)!=-1):
                    filename=filename.replace(char," ")
            return filename
        else:
            return 'None'
        
    @QtCore.pyqtSlot()
    def rename(self):
        if len(self.thesisDict):
            for (fileName,thesis) in self.thesisDict.items():
                temp = os.path.split(fileName)
                folder = temp[0]
                ext = (os.path.splitext(temp[1]))[1]
                fname = self.formatFileName(thesis.title)
                if fname:
                    newPath = os.path.join(folder,fname+ext)
                    #newPath = os.path.join(folder,'【%s】'%thes.info.year+fname+ext)
                    shutil.copy(fileName,newPath)
            QtGui.QMessageBox.information(self,"Info","Convert Complete!",QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
    @QtCore.pyqtSlot()
    def exportInfo(self):
        infoList = []
        if len(self.thesisDict):
            for (fileName,thesis) in self.thesisDict.items():
                thesis.getInfo()
                infoList.append(thesis.printInfo())
            QtGui.QMessageBox.information(self,"Info",'\n'.join(infoList),QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                
    @QtCore.pyqtSlot() 
    def browse(self):
        self.fileNames = QtGui.QFileDialog.getOpenFileNames(self,self.tr('choose one or more pdf file'),'','PDF(*.pdf)',None,QtGui.QFileDialog.DontUseNativeDialog)
        if len(self.fileNames):
            self.thesisDict.clear()
            for fName in self.fileNames:
                fileName = str(fName)
                fileHandle = file(fileName,'rb')
                self.thesisDict.update({fileName:Thesis(fileHandle)})
                fileHandle.close()        
        self.lm = MyListMode(self.fileNames)
        self.ui.FileListView.setModel(self.lm)
        
    
    def indexMove(self,text):
        pass
        #print u'你选择的是{0}'.format(text.row())
        #print dir(text)
#        if text.row()==0:#obj.row()指定的项
#            print 'select 0'
        
class MyListMode(QtCore.QAbstractListModel):
    def __init__(self,datain,parnet=None,*args):
        """数据：一列表中的每个项目是一个行"""
        super(MyListMode,self).__init__(parnet,*args)
        self.listdata=datain
    #这2个方法是规定好的
    def rowCount(self,parent=QtCore.QModelIndex()):
        return len(self.listdata)

    def data(self,index,row):#isValid()是否有效的
        if index.isValid() and row==Qt.DisplayRole:#关键数据以文本的形式呈现
            return QVariant(self.listdata[index.row()])#QVariant类就像一个最常见的Qt联盟数据类型
        else:
            return QVariant()        

if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    myapp=MainWindow()
    myapp.show()
    app.exec_()