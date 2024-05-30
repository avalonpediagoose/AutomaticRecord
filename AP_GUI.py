# -*- coding: utf-8 -*-
"""
Created on Fri May 17 15:46:09 2024

@author: ginachen
"""
####################################################################################################
import wx 
####################################################################################################
class MyFrame(wx.Frame):
    """
    Frame class that holds all other widgets.
    """
    #-----------------------------------------------------------------------------------------------
    def __init__(self, title):
        super().__init__(parent = None, title = title, size = (420, 224)) 
        self.panel = wx.Panel(self)        

        PosX = 16
        PosY = 16
        self.stext_InputLabel = wx.StaticText(self.panel, wx.ID_ANY, 
        label = '請輸入總局數、湖中(ex:0湖4好，則打4o)、刺殺誰(沒有請按空白鍵)', 
        pos = (PosX, PosY), size = (400, 20))
        
        self.stext_Example_1 = wx.StaticText(self.panel, wx.ID_ANY, 
        label = '範例1 (3局3藍刺殺): 34o5', 
        pos = (PosX, PosY+24), size = (140, 20))       
        self.stext_Example_2 = wx.StaticText(self.panel, wx.ID_ANY, 
        label = '範例2 (5局3紅): 54o8o1x ', 
        pos = (PosX+180, PosY+24), size = (140, 20))
        
        self.stext_ActualCombat = wx.StaticText(self.panel, wx.ID_ANY, label = '實戰:', pos = (PosX, PosY+66), size = (38, 20))
        self.textc_ActualCombat = wx.TextCtrl(self.panel, wx.ID_ANY, value = '56o2x9o6', pos = (PosX+38, PosY+64), size = (86, 22))
        
        self.stext_DelaySel = wx.StaticText(self.panel, wx.ID_ANY, label = '延遲:', pos = (PosX, PosY+97), size = (38, 20))
        self.textc_DelaySel = wx.TextCtrl(self.panel, wx.ID_ANY, value = '5', pos = (PosX+38, PosY+94), size = (36, 22))
        self.stext_DelayUnit = wx.StaticText(self.panel, wx.ID_ANY, label = '秒(s)', pos = (PosX+80, PosY+97), size = (38, 20))
        self.stext_WaitSel = wx.StaticText(self.panel, wx.ID_ANY, label = 'CMD', pos = (PosX+150, PosY+97), size = (120, 20))
        self.stext_WaitSel.SetForegroundColour((0,0,255))
        
        self.stext_RecordName = wx.StaticText(self.panel, wx.ID_ANY, label = '紀錄者ID:', pos = (PosX, PosY+129), size = (62, 20))
        self.tctrl_RecordName = wx.TextCtrl(self.panel, wx.ID_ANY, value = '派票紀錄員', pos = (PosX+62, PosY+127), size = (96, 22))
        
        self.btnRecord = wx.Button(self.panel, wx.ID_ANY, label = '紀錄', pos = (PosX+166, PosY+127), size = (62, 22))
        self.btnRecord.Bind(wx.EVT_BUTTON, self.RecordEvent)                       
#---------------------------------------------------------------------------------------------------
#EOF 