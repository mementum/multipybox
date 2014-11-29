#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
################################################################################
# 
#  Copyright (C) 2014 Daniel Rodriguez
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
import appconstants
import maingui
from utils.mvc import DynBind, DynamicClass
import wx

filemissing = ''' could not be opened.

That means it has been removed from the distribution package either running as an
installed/standalone application or running from source.

Please check the development site for it:

'''

@DynamicClass(moddirs=['views', 'controllers'])
class AboutDialog(maingui.AboutDialog):

    def __init__(self, parent):
        maingui.AboutDialog.__init__(self, parent)
        self.font = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.FillPanelAbout()
        self.AddDocuments()
        self.Fit() # Ensure the Dialog resizes to fit the added Panels
        self.Centre()

    def AddDocuments(self):
        for doc, srcdir in appconstants.about_datas:
            panel = maingui.PanelAboutDocument(self.m_notebookAbout)
            self.m_notebookAbout.AddPage(panel, text=doc, select=False)
            self.FillTextCtrl(panel.m_textCtrlDocument, doc, srcdir)
            panel.Layout()

    def FillTextCtrl(self, textctrl, fname, srcdir='appdir'):
        if srcdir == 'appdir':
            fpath = appconstants.getapppath(fname)
        else:
            fpath = appconstants.getdatapath(fname)
        try:
            f = open(fpath, 'r')
        except IOError:
            fcontent = fname + filemissing + appconstants.AppURL
        else:
            fcontent = f.read()
        textctrl.SetFont(self.font)
        textctrl.SetValue(fcontent)
        winDC = wx.ClientDC(textctrl)
        width, height = winDC.GetTextExtent('-' * 82)
        height *= 26
        textctrl.SetMinSize(wx.Size(width, height))

    def FillPanelAbout(self):
        # Application Name and Version
        appnameversion = appconstants.AppName + ' ' + appconstants.AppVersion
        self.m_staticTextAppNameVersion.SetLabel(appnameversion)

        # Copyright Year and Publisher
        appcopyright = '(C) ' + appconstants.AppYear + ' ' + appconstants.AppPublisher
        self.m_staticTextCopyright.SetLabel(appcopyright)

        # HyperLink URL
        self.m_hyperlinkURL.SetLabel(appconstants.AppURL)
        self.m_hyperlinkURL.SetURL(appconstants.AppURL)

        # Refresh panel Layout to ensure correct content and alignment of StaticText/HyperLinkURL controls
        self.m_panelAbout.Layout()

    @DynBind.EVT_BUTTON.Button.Close
    def OnButtonClickClose(self, event):
        event.Skip()
        self.EndModal(wx.ID_OK)
