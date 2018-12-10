# -*- coding: utf-8 -*-
import os
from myflowlib import save_list,read_list

class NameGenerater(object):
    def __init__(self,num):
        self.num = num
        self.runDir = 'YOU RUN DIR'
        self.fileNameHead = 'tt'
        self.idlist = list(map(str,range(self.num)))

    def set_runDir(self,runDir):
        self.runDir = runDir

    def set_head(self,fileNameHead):
        self.fileNameHead = fileNameHead

    def Gen(self,itemDir,itemName):
        runDir = self.runDir
        newList = [self.fileNameHead + x + itemName for x in self.idlist]
        newList = list(map(os.path.join,
                           [runDir ] * self.num,
                           [itemDir] * self.num, newList))
        return newList

    def Generate(self,itemDir,head,itemName,num):
        runDir = self.runDir
        fileNameHead = head
        idlist = list(map(str,range(self.num)))
        newList = [fileNameHead + x + itemName for x in idlist]
        newList = list(map(os.path.join,
                           [runDir ] * num,
                           [itemDir] * num, newList))
        return newList

class ListsManager(object):
    def __init__(self,*invalues,**invaluesdicts):
        self.values = dict() 
        self.valuesDirs = dict()
        self.valuesShortNames= dict()
        self.valuesShortNamesExt= dict()
        self.txtFileNames = dict()
        self.runDir = 'YOU RUN DIR'
        self.txtsDir = 'txts'

        self._init_values(invalues,invaluesdicts)
        self._init_txtFileNames()

    def _init_values(self,lists,dicts):
        for key in lists:
            self.values[key] = [];
        for key,value in dicts.items():
            self.values[key] = value

    def _init_txtFileNames(self):
        for key in self.values:
            name = key
            self.txtFileNames[key] = ExtCheck(name,'.txt')

# ======= set ==================

    def set_value(self,*lists,**dicts):
        for key in lists:
            self.values[key] = [];
        for key,value in dicts.items():
            self.values[key] = value

    def set_runDir(self,runDir):
        self.runDir = runDir

    def set_txtsDir(self,txtsDir):
        self.txtsDir = txtsDir

    def set_txtNames(self,**dicts):
        for key,txtname in dicts.items():
            if key in self.values:
                self.txtFileNames[key] = ExtCheck(txtname,'.txt')
            else:
                print('WARRING set_txtNames: '+
                      str(key)+' is not in the listdicts')

    def _set_valuesDirs(self,dicts):
        for key,vdir in dicts.items():
            if key in self.values:
                self.valuesDirs[key] = vdir
            else:
                print('WARRING _set_valuesDirs: '+
                      str(key)+' is not in the listdicts')

    def set_valuesDirs(self,**dicts):
        self._set_valuesDirs(dicts)

    def set_allValuesDirs(self,vdir):
        self._set_valuesDirs(dict(zip(
                self.get_keys(),
                [vdir]*len(self.get_keys())
                )))

    def set_valuesShortNames(self,**dicts):
        for key,shortName in dicts.items():
            if key in self.values:
                if key in self.valuesShortNamesExt:
                    ext = self.valuesShortNamesExt[key]
                else:
                    ext = ''
                self.valuesShortNames[key] = ExtCheck(shortName,ext)
            else:
                print('WARRING set_valuesShortNames: '+
                      str(key)+' is not in the listdicts')

    def _set_valuesShortNamesExt(self,dicts):
        for key,shortNameExt in dicts.items():
            if key in self.values:
                self.valuesShortNamesExt[key] = shortNameExt
            else:
                print('WARRING _set_valuesShortNamesExt: '+
                      str(key)+' is not in the listdicts')

    def set_valuesShortNamesExt(self,**dicts):
        self._set_valuesShortNamesExt(dicts)

    def set_allValuesShortNamesExt(self,ext):
        self._set_valuesShortNamesExt(dict(zip(
                self.get_keys(),
                [ext]*len(self.get_keys())
                )))

    def set_extsAuto(self,*keys):
        self._set_extsAuto(keys)

    def set_allExtsAuto(self,*keys):
        self._set_extsAuto(self.get_keys())

    def _set_extsAuto(self,keys):
        for key in keys:
            if key in self.values:
                if len(self.values[key]):
                    example  = self.values[key][0]
                    _ , ext = os.path.splitext(example)
                    self.valuesShortNamesExt[key] = ext
                else:
                    print('WARRING set_namesExtAuto : key '+str(key)+' is empty')
            else:
                print('WARRING set_namesExtAuto: '+
                      str(key)+' is not in the listdicts')



    def __setitem__(self,key,value):
        if key in self.values:
            self.values[key] = value 
        else:
            raise KeyError(key)

# ========= get =============
    def get_listdicts(self):
        return self.values

    def get_keys(self):
        return [key for key in self.values]

    def get_lists(self):
        return [item[1] for item in self.values.items()]#历史原因，字典的名称就是values，不要弄混

    def get_saveDir(self):
        return os.path.join(self.runDir,self.txtsDir)

    def get_txtFileNames(self):
        for key in self.values:
            if key not in self.txtFileNames:
                name = key
                self.txtFileNames[key] = ExtCheck(name,'.txt')
        return self.txtFileNames

    def get_allSavetxtNames(self):
        self.savetxtNames = dict()
        sdir = self.get_saveDir()
        for key,txt in self.get_txtFileNames().items():
            self.savetxtNames[key] = os.path.join(sdir,txt)
        return self.savetxtNames

    def get_SavetxtNamesLists(self,*keys):
        SavetxtNames = self.get_allSavetxtNames()
        SavetxtNamesLists = []
        for key in keys:
            if key in SavetxtNames:
                SavetxtNamesLists.append(SavetxtNames[key])
            else:
                print('WARRING get_SavetxtNamesLists: '+
                      str(key)+' is not in the listdicts')
        return SavetxtNamesLists

    def __getitem__(self,key):
        if key in self.values:
            return self.values[key]
        else:
            return None

    def __len__(self):
        return len(self.__getitem__(self.get_keys()[0]))

# ================ get single ==================

    def get_valuesShortName(self,key):
        if key in self.valuesShortNames:
            ext = self.valuesShortNamesExt[key]
            self.valuesShortNames[key] = ExtCheck(self.valuesShortNames[key],ext)
            return self.valuesShortNames[key]
        else:
            print('WARRING get_valuesShortName: '+
                  str(key)+' is not in the listdicts')
            return None

    def get_valuesShortNamesExt(self,key):
        if key in self.valuesShortNamesExt:
            return self.valuesShortNamesExt[key]
        else:
            print('WARRING get_valuesShortNamesExt: '+
                  str(key)+' is not in the listdicts')

# ======== generate ===============

    def GenAllList(self,num,fileNameHead='nt'):
        self._GenList(num,self.get_keys(),fileNameHead)

    def GenList(self,num,*keys,fileNameHead='nt'):
        self._GenList(num,keys,fileNameHead)

    def _GenList(self,num,keys,fileNameHead='nt'):
        gen = NameGenerater(num)
        gen.set_runDir(self.runDir)
        gen.set_head(fileNameHead)
        for key in keys:
            if key in self.values:
                itemDir  = self.valuesDirs[key]
                itemName = self.get_valuesShortName(key)
                newList  = gen.Gen(itemDir,itemName)
                self.values[key] = newList
            else:
                print('WARRING GenList: '+
                      str(key)+' is not in the listdicts')

# ======== save ============

    def SaveAlltxts(self):
        self._Savetxts(self.get_keys())

    def Savetxts(self,*keys):
        self._Savetxts(keys)

    def _Savetxts(self,keys):
        print('Saveing   ' + ' , '.join([item[1] for item in self.txtFileNames.items()]))
        SavetxtNames = self.get_allSavetxtNames()
        for key in keys:
            if key in SavetxtNames:
                save_list(SavetxtNames[key],self.values[key])
                if(self.values[key]==[]):print("WARRING: List "+str(key)+' is empty')
            else:
                print('WARRING _Savetxts: '+
                      str(key)+' is not in the listdicts')

# ========read ==========

    def ReadAlltxts(self):
        self._Readtxts(self.get_keys())

    def Readtxts(self,*keys):
        self._Readtxts(keys)

    def _Readtxts(self,keys):
        print('Lording   ' + ' , '.join([item[1] for item in self.txtFileNames.items()]))
        SavetxtNames = self.get_allSavetxtNames()
        for key in keys:
            if key in SavetxtNames:
                self.values[key] = read_list(SavetxtNames[key])
                if(self.values[key]==[]):print("WARRING: File "+str(SavetxtNames[key])+' is empty')
            else:
                print('WARRING _Readtxts: '+
                      str(key)+' is not in the listdicts')

# ======== print ============

    def PrintAllvaluesNames(self):
        print (','.join([item[0] for item in self.values.items()]))

    def PrintAllValues(self):
        print ('\n'.join(['%s:%s' % item for item in self.values.items()]))

    def PrintAllNames(self):
        print (','.join([item[0] for item in self.__dict__.items()]))

    def PrintAll(self):
        print ('\n'.join(['%s:%s' % item for item in self.__dict__.items()]))

    def PrintInfo(self,name = ''):
        print('\nGROUP: ',name)
        print('%-15s'%'Lists||items:','%-10s'%'vLen','%-20s'%'vDirs',
              '%-20s'%'sNames','%-15s'%'nameExt','%-20s'%'txtName')
        for key in self.get_keys():
            print('%-15s'% key,
                  '%-10s'% len(self.values[key]),
                  '%-20s'% self.valuesDirs[key] ,
                  '%-20s'% self.get_valuesShortName(key),
                  '%-15s'% self.valuesShortNamesExt[key],
                  '%-20s'% self.txtFileNames[key])



# ========== Funtions ===============

def ExtCheck_old(name,ext):
    _,e = os.path.splitext(name)
    if(e):
        res = name
    else:
        res = name + ext
    return res

def ExtCheck(name,ext):
    n,e = os.path.splitext(name)
    if(e == ext):
        res = name
    else:
        res = n + ext
    return res


#A=['datasets/1A','datasets/2A','datasets/3A']
#B=['datasets/1B','datasets/2B','datasets/3B']

#pics = ListsManager('imgA','imgB')
#pics.set_runDir('./data/TESTNamesManager')
#pics.set_txtNames(imgA="img1.txt", imgB="img2.txt")
#pics.set_value(imgA = A ,imgB = B)
#pics.SaveAlltxts()

#pics = ListsManager('imgA','imgB')
#pics.set_runDir('./data/TESTNamesManager')
#pics.set_txtNames(imgA="img1.txt", imgB="img2.txt")
#pics.Readtxts('imgA')
#pics.PrintAll()

#flows = ListsManager('out',gt=A)
#flows.set_runDir('./data/TESTNamesManager')
#flows.set_txtNames(gt="groundtruth",out="out.txt")
#flows.set_valuesDirs()
#flows.set_allValuesShortNamesExt('.flo')
#flows.set_allValuesDirs('flow')
#flows.set_valuesShortNames(out='f',gt = 'gt')
#flows.GenList(4,'out')
#flows.SaveAlltxts()
#flows.PrintAll()
#NameGenerater