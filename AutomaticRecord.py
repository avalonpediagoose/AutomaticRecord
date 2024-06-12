# -*- coding: utf-8 -*-
"""
Created on Fri May 17 15:49:34 2024

@author: ginachen
"""

import AP_GUI
import datetime
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import wx
#---------------------------------------------------------------------------------------------------
""" Global variables """
now = datetime.datetime.now()
data = now.strftime('%m%d')
titleStr = data+' 一般場'
####################################################################################################
""" Class Definition """ 
class APFrame(AP_GUI.MyFrame):    
    #""" Frame Event """----------------------------------------------------------------------------            
    def __init__(self,title):       
        AP_GUI.MyFrame.__init__(self, title)
        
        APFrame.SettingINI(self)
        print('AutomaticRecord.exe Loaded.')
            
    def OnClose(self, event):
        self.Destroy()
        app.ExitMainLoop() # Exit the main event loop
        
    def RecordEvent(self, event):       
        self.btnRecord.Enable(False)
        
        nowRecord = datetime.datetime.now()
        timestamp = nowRecord.strftime('_%m%d_%H%M%S')
        path = timestamp+'_AutoRecord.txt'
        screenpath = timestamp+'_screen.png'
        
        ll = self.textc_ActualCombat.GetValue()
        lake_lady = [i for i in ll]
        r = int(lake_lady[0])
        
        #開始跑網頁
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(options = options)
        ult = "https://avalon.signage-cloud.org/" #可改
        driver.get(ult)
        username=driver.find_element(By.CLASS_NAME,"form-control")
        TempName = self.tctrl_RecordName.GetValue()
        username.send_keys(TempName) #輸入玩家名字
        btn=driver.find_element(By.CLASS_NAME,"btn-block") #定義button
        btn.click() #點擊進入頁面
        self.stext_WaitSel.SetForegroundColour((255,0,0))
        print("請自行點擊需要的房間")
        self.stext_WaitSel.SetLabel("請自行點擊需要的房間")
        time.sleep(int(self.textc_DelaySel.GetValue()))
        
        # 在進入房間後保存螢幕截圖
        screenshot_filename = screenpath
        driver.save_screenshot(screenshot_filename)
        
        btn = driver.find_element(By.CSS_SELECTOR, 'button[data-toggle="modal"].btn.btn-primary')
        btn.click()
        time.sleep(3)        
              
        #定義變數
        i = 0
        a = 0
        ticket = []
        white = []
        black = []
        cup = []
        player_list = []
        btn = driver.find_element(By.XPATH, '//a[text()="第二局"]')
        
        #遊戲玩家
        p = driver.find_elements(By.CSS_SELECTOR,"[align=center]")
        for player in p:
            player_list.append(player.text)                    
            
        # 打開文件以寫入模式
        with open(path, "w", encoding = "utf-8") as file:
            #定義局數、黑白球、好壞杯
            for round_number in range(1,r+1):
                round_id = f"round_{round_number}"
                round = driver.find_element(By.ID,round_id)#定義第幾局
                round_tds = round.find_elements(By.TAG_NAME,"td")#派票黑白球
                round_cups = round.find_elements(By.CLASS_NAME,"col-sm-2")#好壞杯
                
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
                all_cup = ''.join(map(str,cup))
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
            print("刺客刺殺：",lake_lady[-1],sep = "")
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
        self.stext_WaitSel.SetForegroundColour((0,0,255))
        self.stext_WaitSel.SetLabel("完成紀錄")
        
        self.btnRecord.Enable(True)

    def SettingINI(self):
        IniBuf = {}
        PosIndex = 0
        path = 'Setting.ini'
        try:
            with open(path, 'r') as f:
                for line in f:
                    PosIndex+=1                                                      
                    if line != None: 
                        IniBuf[PosIndex] = line 
              
            for IndexExe in range(1,PosIndex+1):
                if IniBuf != None:
                    SplitExe = re.split(' |,', IniBuf[IndexExe])
                    
                    match SplitExe[0]:                                                                                    
                        case 'Config':
                            self.textc_ActualCombat.SetValue(SplitExe[1])
                            self.textc_DelaySel.SetValue(SplitExe[2])
                            self.tctrl_RecordName.SetValue(SplitExe[3])                     
                        #case _:
                            #print('Default')           
        except FileNotFoundError:
            APFrame.SaveAPSetting(self) 
            
    def SaveAPSetting(self):
        IniBuf = {}
        path = 'Setting.ini'
        
        IniBuf[0]='CONFIG,'\
            +self.textc_ActualCombat.GetValue()+','\
            +self.textc_DelaySel.GetValue()+','\
            +self.tctrl_RecordName.GetValue()
            
        try:
            file = open(path, "w")  
            for x in range(1):
                print(IniBuf[x], end="\n", file=file)
            file.close()            
        except IOError:
            print("[Error] Unable to write file.")                              
####################################################################################################
# Run the program
if __name__ == "__main__":               
    app = wx.App() 
    frame = APFrame(titleStr)
    frame.SetIcon(wx.Icon('gameboid.ico')) 
    frame.Show()
    app.MainLoop() #start the applications
#------------------------------------------------------------------------------------------
#EOF