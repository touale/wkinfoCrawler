# -*- coding: UTF-8 -*-
'''
@Project -> File   ：pyCode -> requestConfig
@Author ：ToualeCula
@Email ：1367642349@qq.com
@Date ：2021/8/23 21:28
@Desc ：
'''

import requests,json

class Core:
    def __init__(self,TingyunId='',Identification='',Cookie=''):
        self.TingyunId = TingyunId
        self.Identification = Identification
        self.Cookie = Cookie

    def setNumAndProvince(self,num,province):
        ''':cvar
        just used for printing ,and then,you can learn about which num and province is running!!!
        '''
        self.num,self.province = num,province

    def getHeaders(self):
        headers = {
            'DNT': "1",
            'sec-ch-ua-mobile': "?0",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73",
            'X-Tingyun-Id': self.TingyunId,
            'Identification': self.Identification,
            'Content-Type': "application/json;charset=UTF-8",
            'Accept': "application/json, text/plain, */*",
            'Cache-Control': "no-cache",
            'Appversion': "2021.03.17.1",
            'Origin': "https://law.wkinfo.com.cn",
            'Sec-Fetch-Site': "same-origin",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Dest': "empty",
            'Referer': "https://law.wkinfo.com.cn/judgment-documents/list?mode=advanced",
            'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            'Cookie': self.Cookie,
        }
        return headers

    def search(self,limit,page,count):
        ''':cvar
        :return isAgainst,ids
        '''


        url = 'https://law.wkinfo.com.cn/csi/search'
        offset = (page - 1) * limit

        data = {
            "indexId": "law.case",
            "query": {
                "queryString": "court:((" + count+ ")) AND courtLevel:((2)) AND typeOfCase:行政 AND typeOfDecision:((002))",
                "filterQueries": [],
                "filterDates": ["judgmentDate:[2018.01.01 TO 2018.01.31]"]
            },
            "searchScope": {
                "treeNodeIds": []
            },
            "relatedIndexQueries": [],
            "sortOrderList": [{
                "sortKey": "judgmentDate",
                "sortDirection": "DESC"
            }],
            "pageInfo": {
                "limit": "{}".format(limit),
                "offset": offset
            },
            "otherOptions": {
                "requireLanguage": "cn",
                "relatedIndexEnabled": False,
                "groupEnabled": False,
                "smartEnabled": True,
                "buy": False,
                "summaryLengthLimit": 100,
                "advanced": True,
                "synonymEnabled": True,
                "isHideBigLib": 0,
                "relatedIndexFetchRows": 5,
                "proximateCourtID": "",
                "module": ""
            },
            "chargingInfo": {
                "useBalance": True
            }
        }

        res = requests.request('POST', url, json=data,headers=self.getHeaders())

        js,ids = json.loads(res.text),''

        for i,list in enumerate(js['documentList']):
            ids += list['docId'] + ','
            # print('---> ',self.num,self.province,i,list['title'],list['docId'])

        return ids

    def initDownLoad(self,ids,title):
        url = 'https://law.wkinfo.com.cn/csi/document/downloadPath'
        data = {
          "indexId": "law.case",
          "fileType": "doc",
          "docId": ids,
          "showType": 0,
          "filename": "{}.zip".format(title),
          "module": ""
        }

        res = requests.request('POST', url, json=data, headers=self.getHeaders())
        print('     zipLink:',self.num,self.province,res.text)

        js = json.loads(res.text)

        try:
            return js['data']['key']
        except:
            print("         !!!!!! error: key == NULL")
            return ''

    def downLoad(self,title,key,path):
        url = 'https://law.wkinfo.com.cn/api/download?key=' + key
        down_res = requests.get(url=url)

        with open(path + title + '.zip', "wb") as code:
            code.write(down_res.content)

    def initExcel(self,ids,title):
        url = 'https://law.wkinfo.com.cn/csi/document/downloadPath'
        data = {
          "indexId": "law.case",
          "fileType": "excel",
          "docId": ids,
          "showType": 0,
          "filename": "{}.xls".format(title),
          "module": "",
          "cellList": "title,documentnumber,court,territory,typeofcase,causeofaction,judgmentdatestr,instance,typeofdecision,subjectFee,courtAcceptanceFee,judgmentReason,judgmentResult,judges"
        }

        res = requests.request('POST', url, json=data, headers=self.getHeaders())
        print('     xlsLink:',self.num,self.province,res.text)

        js = json.loads(res.text)

        try:
            return js['data']['key']
        except:
            print("         !!!!!! error: key == NULL")
            return ''

    def downLoadExcel(self,title,key,path):
        url = 'https://law.wkinfo.com.cn/api/download?key=' + key
        down_res = requests.get(url=url)

        with open(path + title + '.xls', "wb") as code:
            code.write(down_res.content)










