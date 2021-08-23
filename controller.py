# -*- coding: UTF-8 -*-
'''
@Project -> File   ：pyCode -> controller
@Author ：ToualeCula
@Email ：1367642349@qq.com
@Date ：2021/8/23 22:33
@Desc ：
'''

from areaConfig import areaData
from core import Core
import os,time
from time import sleep
from tqdm import tqdm

class Controller:
    def __init__(self,limit = 50,TingyunId='',Identification='',Cookie=''):
        self.core = Core(
            TingyunId=TingyunId,
            Identification=Identification,
            Cookie=Cookie)
        self.limit = limit
        return

    def initFile(self,filename):

        if not os.path.exists(filename):
            os.makedirs(filename)

        if not os.path.exists(filename+"/文书/"):
            os.makedirs(filename+"/文书/")


    def runAllProvinces(self):
        for i,temp in tqdm(enumerate(areaData)):


            print(i,temp['areaName'],temp['nodeId'])

            self.initFile('downLoad/{}'.format(temp['areaName']))
            self.core.setNumAndProvince(i,temp['areaName'])

            page = 0
            zipPath, xlsPath, xlsData = 'downLoad/{}'.format(temp['areaName']) + "/文书/",'downLoad/{}'.format(temp['areaName']) + "/",''

            while 1:
                # as one page == 50 -> xxx.zip
                page += 1
                ids = self.core.search(self.limit,page,temp['nodeId'])

                if(ids == ''):break

                xlsData += ids
                title = '{}'.format(int(time.time()))
                key = self.core.initDownLoad(ids,title)
                self.core.downLoad(title, key,zipPath)

            # as all pages -> xxx.xls
            title = '{}'.format(int(time.time()))
            key = self.core.initExcel(xlsData,title)
            self.core.downLoadExcel(title,key,xlsPath)

            # there, i do not know the best value
            sleep(3)
            print()






