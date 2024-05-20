# -*- coding: utf-8 -*-
"""
Created on Wed May 15 15:57:54 2024

@author: ginachen
"""

import wx
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

now = datetime.datetime.now()
timestamp = now.strftime('_%m%d_%H%M%S')
path = timestamp+'_AutoRecord.txt'
data = now.strftime('%m%d')
titleStr = data+' 一般場'

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw, size=(438, 300))
        
        # 創建面板
        panel = wx.Panel(self)
        
        # 創建垂直佈局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加變數1的文本框
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label="輸入:")
        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        self.var1 = wx.StaticText(panel, label="請輸入總局數、湖中(ex:0湖4好，則打4o)、刺殺誰(沒有請按空白鍵)")
        hbox1.Add(self.var1, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        # 添加變數2的文本框
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(panel, label="範例1 (3局3藍刺殺):")
        hbox2.Add(st2, flag=wx.RIGHT, border=8)
        self.var2 = wx.StaticText(panel, label="34o5")
        hbox2.Add(self.var2, flag=wx.RIGHT, border=8)
        st3 = wx.StaticText(panel, label=", 範例2 (5局3紅):")
        hbox2.Add(st3, flag=wx.RIGHT, border=8)
        self.var3 = wx.StaticText(panel, label="54o8o1x ")
        hbox2.Add(self.var3, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        # 添加變數3的文本框
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(panel, label="實戰:")
        hbox3.Add(st4, flag=wx.RIGHT, border=8)
        self.record_input = wx.TextCtrl(panel, value="56o2x9o6")
        hbox3.Add(self.record_input, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        # 添加變數4的文本框
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        st5 = wx.StaticText(panel, label="延遲:")
        hbox4.Add(st5, flag=wx.RIGHT, border=8)
        self.SelRoomTime = wx.TextCtrl(panel, value="5")
        hbox4.Add(self.SelRoomTime, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        st6 = wx.StaticText(panel, label="秒(s)")
        hbox4.Add(st6, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        self.WaitSel = wx.StaticText(panel, label="")
        self.WaitSel.SetForegroundColour(wx.Colour(255, 0, 0))
        hbox4.Add(self.WaitSel, proportion=1)
        vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
        # 添加記錄按鈕
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        st5 = wx.StaticText(panel, label="紀錄者ID:")
        hbox5.Add(st5, flag=wx.RIGHT, border=8)
        self.record_output = wx.TextCtrl(panel, size=(200, -1), value="派票紀錄員")  # 設置文本框初始大小
        hbox5.Add(self.record_output, proportion=1, flag=wx.RIGHT, border=8)
        self.btnRecord = wx.Button(panel, label="記錄")
        hbox5.Add(self.btnRecord, flag=wx.ALIGN_CENTER)
        vbox.Add(hbox5, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=10)
        self.btnRecord.Bind(wx.EVT_BUTTON, self.on_submit)
        
        # 設置面板佈局
        panel.SetSizer(vbox)
        
        # 設置框架屬性
        self.SetTitle(titleStr)
        self.Centre()

    def on_submit(self, event):
        self.btnRecord.Enable(False)
        
        ll = self.record_input.GetValue()
        lake_lady=[i for i in ll]
        r=int(lake_lady[0])
        #開始跑網頁
        options=webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        driver=webdriver.Chrome(options=options)
        ult="https://avalon.signage-cloud.org/" #可改
        driver.get(ult)
        username=driver.find_element(By.CLASS_NAME,"form-control")
        username.send_keys("派票紀錄員") #輸入玩家名字
        btn=driver.find_element(By.CLASS_NAME,"btn-block") #定義button
        btn.click() #點擊進入頁面
        print("請自行點擊需要的房間")
        self.WaitSel.SetLabel("請自行點擊需要的房間")
        time.sleep(int(self.SelRoomTime.GetValue()))
        btn = driver.find_element(By.CSS_SELECTOR, 'button[data-toggle="modal"].btn.btn-primary')
        btn.click()
        time.sleep(3)        
        
        #定義變數
        i=0
        a=0
        ticket=[]
        white=[]
        black=[]
        cup=[]
        player_list = []
        btn = driver.find_element(By.XPATH, '//a[text()="第二局"]')
        
        #遊戲玩家
        p=driver.find_elements(By.CSS_SELECTOR,"[align=center]")
        for player in p:
            player_list.append(player.text)
            
        # 打開文件以寫入模式
        with open(path, "w", encoding="utf-8") as file:
            #定義局數、黑白球、好壞杯
            for round_number in range(1,r+1):
                round_id = f"round_{round_number}"
                round=driver.find_element(By.ID,round_id)#定義第幾局
                round_tds=round.find_elements(By.TAG_NAME,"td")#派票黑白球
                round_cups=round.find_elements(By.CLASS_NAME,"col-sm-2")#好壞杯
                
                #紀錄派票黑白球
                for round_td in round_tds:
                    if "正常黑"in round_td.text or"場外白"in round_td.text or"場內黑"in round_td.text or"正常白"in round_td.text or"抗議黑"in round_td.text:
                        i+=1
                        if i==10:
                            i=0
                            a=99
                        if "場外白"in round_td.text:
                            white.append(i)
                        if "抗議黑"in round_td.text or"場內黑"in round_td.text:
                            black.append(i)
                        if "image/mission.jpg" in round_td.get_attribute("innerHTML"):
                            ticket.append(i)
                    if a==99:
                        all_white=''.join(map(str,white))
                        all_black=''.join(map(str,black))
                        all_ticket=''.join(map(str,ticket))
                        if white or black:
                            if white and black:
                                print(all_ticket+' '+all_white+'+'+all_black+'-')
                                file.write(f"{all_ticket} {all_white}+{all_black}-\n")                           
                            elif white:
                                print(all_ticket+' '+all_white+'+')
                                file.write(f"{all_ticket} {all_white}+\n")
                            elif black:
                                print(all_ticket+' '+all_black+'-')
                                file.write(f"{all_ticket} {all_black}-\n")
                        else:
                            print(all_ticket)
                            file.write(f"{all_ticket}\n")
                            
                        i=0
                        a=0
                        ticket=[]
                        white=[]
                        black=[]
                        
                #紀錄好壞杯
                for round_cup in round_cups:
                    if "image/good_cup.jpg" in round_cup.get_attribute("innerHTML"):
                        cup.append("o")
                    elif "image/bad_cup.jpg" in round_cup.get_attribute("innerHTML"):
                        cup.append("x")
                all_cup=''.join(map(str,cup))
                print(all_cup)
                file.write(f"{all_cup}\n")
                cup=[]
                if round_number==r:
                    break
                if round_number==1:
                    btn.click()       
                    btn = driver.find_element(By.XPATH, '//a[text()="第三局"]')
                if round_number==2:
                    print("0",">",lake_lady[1]," ",lake_lady[2],sep="")
                    file.write(f"0>{lake_lady[1]} {lake_lady[2]}\n")
                    btn.click()
                    btn = driver.find_element(By.XPATH, '//a[text()="第四局"]')
                if round_number==3:
                    print(lake_lady[1],">",lake_lady[3]," ",lake_lady[4],sep="")
                    file.write(f"{lake_lady[1]}>{lake_lady[3]} {lake_lady[4]}\n")
                    btn.click()
                    btn = driver.find_element(By.XPATH, '//a[text()="第五局"]')
                if round_number==4:
                    print(lake_lady[3],">",lake_lady[5]," ",lake_lady[6],sep="")
                    file.write(f"{lake_lady[3]}>{lake_lady[5]} {lake_lady[6]}\n")
                    btn.click()
                time.sleep(3)
                
            #刺客刺殺
            print("刺客刺殺：",lake_lady[-1],sep="")
            file.write(f"刺客刺殺：{lake_lady[-1]}\n")
            
            #角色位置
            i=0
            rl=[0,0,0,0,0,0]
            roles=driver.find_elements(By.CLASS_NAME,"col-sm-12")
            for role in roles:
                i+=1
                role=role.get_attribute("innerHTML")
                if i<7:
                    if "image/Q_刺客.jpg" in role:
                        rl[0]=i
                    if "image/Q_莫甘娜.jpg" in role:
                        rl[1]=i
                    if "image/Q_莫德雷德.jpg" in role:
                        rl[2]=i
                    if "image/Q_奧伯倫.jpg" in role:
                        rl[3]=i
                    if "image/Q_派西維爾.jpg" in role:
                        rl[4]=i
                    if "image/Q_梅林.jpg" in role:
                        rl[5]=i
                if i==7:
                    i=0
                    if "image/Q_刺客.jpg" in role:
                        rl[0]=i
                    if "image/Q_莫甘娜.jpg" in role:
                        rl[1]=i
                    if "image/Q_莫德雷德.jpg" in role:
                        rl[2]=i
                    if "image/Q_奧伯倫.jpg" in role:
                        rl[3]=i
                    if "image/Q_派西維爾.jpg" in role:
                        rl[4]=i
                    if "image/Q_梅林.jpg" in role:
                        rl[5]=i
                    i=7
                if i==8:
                    if "image/Q_刺客.jpg" in role:
                        rl[0]=i+1
                    if "image/Q_莫甘娜.jpg" in role:
                        rl[1]=i+1
                    if "image/Q_莫德雷德.jpg" in role:
                        rl[2]=i+1
                    if "image/Q_奧伯倫.jpg" in role:
                        rl[3]=i+1
                    if "image/Q_派西維爾.jpg" in role:
                        rl[4]=i+1
                    if "image/Q_梅林.jpg" in role:
                        rl[5]=i+1
                if i==9 or i==10:
                    if "image/Q_刺客.jpg" in role:
                        rl[0]=i-2
                    if "image/Q_莫甘娜.jpg" in role:
                        rl[1]=i-2
                    if "image/Q_莫德雷德.jpg" in role:
                        rl[2]=i-2
                    if "image/Q_奧伯倫.jpg" in role:
                        rl[3]=i-2
                    if "image/Q_派西維爾.jpg" in role:
                        rl[4]=i-2
                    if "image/Q_梅林.jpg" in role:
                        rl[5]=i-2
            print(''.join(map(str,rl)))#輸出角色位置
            file.write(''.join(map(str, rl)) + '\n')
            
            #房間玩家名字
            print("1",player_list[0],sep=".")
            file.write(f"1.{player_list[0]}\n")
            print("2",player_list[1],sep=".")
            file.write(f"2.{player_list[1]}\n")
            print("3",player_list[2],sep=".")
            file.write(f"3.{player_list[2]}\n")
            print("4",player_list[3],sep=".")
            file.write(f"4.{player_list[3]}\n")
            print("5",player_list[4],sep=".")
            file.write(f"5.{player_list[4]}\n")
            print("6",player_list[5],sep=".")
            file.write(f"6.{player_list[5]}\n")
            print("7",player_list[8],sep=".")
            file.write(f"7.{player_list[8]}\n")
            print("8",player_list[9],sep=".")
            file.write(f"8.{player_list[9]}\n")
            print("9",player_list[7],sep=".")
            file.write(f"9.{player_list[7]}\n")
            print("0",player_list[6],sep=".")
            file.write(f"0.{player_list[6]}\n")
            driver.quit()
            
        self.btnRecord.Enable(True)            

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    frame.SetIcon(wx.Icon('gameboid.ico'))
    frame.Show()
    app.MainLoop()
