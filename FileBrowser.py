from pandac.PandaModules import TextNode
from panda3d.core import TransparencyAttrib
from direct.showbase import DirectObject
from direct.gui.DirectGui import *

from toontown.toonbase import ToontownGlobals

from ctypes import windll
import os
import string


class FileBrowser(DirectObject.DirectObject):

    def __init__(self):
        self.dot = os.getcwd()

        self.prevdir = os.getcwd()

        self.selectedFile = ' '

        self.browserCreated = False
        self.browser = None
        self.fileList = None
        self.fileNameEntry = None

    def cleanup(self):
        self.dot = None
        self.prevdir = None
        self.selectedFile = None
        self.browserCreated = None
        self.fileList = None
        self.fileNameEntry = None

        if self.browser:
            self.browser.destroy()
        del self.browser

        self.ignoreAll()
        return

    def dirbuttonpushed(self, name, dirpath):
        self.selectedFile = ' '
        self.fileNameEntry.enterText('')
        self.cleanCanvas()
        self.dot = os.path.join(dirpath, name)
        self.createFileList(self.dot)

    def filebuttonpushed(self, name, dirpath):
        self.selectedFile = os.path.join(dirpath, name)
        self.dot = dirpath
        self.fileNameEntry.enterText(name)

    def upSelected(self):
        self.selectedFile = ' '
        self.fileNameEntry.enterText('')
        self.cleanCanvas()
        self.dot = os.path.dirname(self.dot)
        self.createFileList(self.dot)
        if len(self.dot) <= 3:
            self.dot = ''

    def entryCR(self, textentered):
        if os.path.isabs(textentered):
            words = os.path.split(textentered)
        else:
            words = (self.dot, textentered)

        if os.path.isdir(os.path.join(words[0], words[1])):
            self.dirbuttonpushed(words[1], words[0])
        else:
            self.filebuttonpushed(words[1], words[0])
            self.openSelected()

    def openSelected(self):
        temp = self.fileNameEntry.get()
        if not temp:
            messenger.send('selectionMade', [self.dot])
            self.closeFileBrowser()
            return

        if os.path.isabs(temp):
            words = os.path.split(temp)
        else:
            words = (self.dot, temp)

        if os.path.isdir(os.path.join(words[0], words[1])):
            self.dirbuttonpushed(words[1], words[0])
        else:
            self.selectedFile = os.path.join(words[0], words[1])
            messenger.send('selectionMade', [self.selectedFile])
            self.closeFileBrowser()

    def cancelSelected(self):
        self.selectedFile = ' '
        self.dot = self.prevdir
        self.fileNameEntry.enterText('')
        messenger.send('selectionMade', [self.selectedFile])
        self.closeFileBrowser()

    def showFileBrowser(self):
        self.browser.show()

    def closeFileBrowser(self):
        self.browser.hide()
        base.transitions.noTransitions()
        self.selectedFile = ' '
        self.fileNameEntry.enterText('')

    def openFileBrowser(self):
        self.prevdir = self.dot
        base.transitions.fadeScreen(0.5)
        if self.browserCreated:
            self.showFileBrowser()
        else:
            self.createFileBrowser()

    def cleanCanvas(self):
        canvas = self.fileList.getCanvas()
        kids = canvas.getChildren()
        for I in range(kids.getNumPaths()):
            temp = kids.getPath(I)
            if temp.getTag('mytype') == 'button':
                temp.removeNode()

    def createFileList(self, mydir):
        canvas = self.fileList.getCanvas()
        directoryInfo = os.walk(mydir)
        elispe = '...'

        if not mydir:
            drives = []
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.uppercase:
                if bitmask & 1:
                    drives.append(letter)
                bitmask >>= 1

            nextPos = (-.93, 0.95)
            drives.sort()
            for name in drives:
                cutoffName = name[0:21]
                if len(cutoffName) < len(name):
                    cutoffName += elispe
                dirbutton = DirectButton(text=cutoffName, text_scale=(0.05, 0.05), text_align=TextNode.ALeft,
                                         text_font=ToontownGlobals.getToonFont(), frameSize=(-.95, .6, -.01, .037),
                                         frameColor=(0.9414, 1.0, 0.9414, 1.0), relief=DGG.SUNKEN,
                                         borderWidth=(0.003, 0.003), command=self.dirbuttonpushed,
                                         extraArgs=[name + ":\\", mydir])
                dirbutton.reparentTo(canvas)
                dirbutton.setPos(nextPos[0], 0, nextPos[1])
                dirbutton.setTag('mytype', 'button')
                nextPos = (-.95, nextPos[1] - .06)

            self.fileList['canvasSize'] = (-1, 0, nextPos[1], 1)
            return

        for dirpath, dirnames, filenames in directoryInfo:
            nextPos = (-.93, 0.95)
            dirnames.sort()
            for name in dirnames:
                cutoffName = name[0:21]
                if len(cutoffName) < len(name):
                    cutoffName += elispe
                dirbutton = DirectButton(text=cutoffName, text_scale=(0.05, 0.05), text_align=TextNode.ALeft,
                                         text_font=ToontownGlobals.getToonFont(), frameSize=(-.95, .6, -.01, .037),
                                         frameColor=(0.9414, 1.0, 0.9414, 1.0), relief=DGG.SUNKEN,
                                         borderWidth=(0.003, 0.003), command=self.dirbuttonpushed,
                                         extraArgs=[name, dirpath])
                dirbutton.reparentTo(canvas)
                dirbutton.setPos(nextPos[0], 0, nextPos[1])
                dirbutton.setTag('mytype', 'button')
                nextPos = (-.95, nextPos[1] - .06)

            filenames.sort()
            for name in filenames:
                cutoffName = name[0:21]
                if len(cutoffName) < len(name):
                    cutoffName += elispe
                filebutton = DirectButton(text=cutoffName, text_scale=(0.05, 0.05), text_align=TextNode.ALeft,
                                          text_font=ToontownGlobals.getToonFont(), frameSize=(-.95, .6, -.01, .037),
                                          frameColor=(1.0, 0.9414, 0.96, 1.0), relief=DGG.SUNKEN,
                                          borderWidth=(0.003, 0.003), command=self.filebuttonpushed,
                                          extraArgs=[name, dirpath])
                filebutton.reparentTo(canvas)
                filebutton.setPos(nextPos[0], 0, nextPos[1])
                filebutton.setTag('mytype', 'button')
                nextPos = (-.95, nextPos[1] - .06)
            break
        self.fileList['canvasSize'] = (-1, 0, nextPos[1], 1)

    def createFileBrowser(self):
        self.browserCreated = True

        cdrGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_sbk_codeRedemptionGui')
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        circleModel = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_nameShop')

        scrollBkgd = OnscreenImage(image='phase_3/maps/slider.png')
        scrollBkgd.setTransparency(TransparencyAttrib.MAlpha)

        self.browser = DirectFrame(frameSize=(-0.6, 0.6, -0.8, 0.95), frameColor=(1.0, 0.98, 0.80, 1.0),
                                   relief=None, borderWidth=(0.01, 0.01), geom=DGG.getDefaultDialogGeom(),
                                   geom_scale=(1.3, 1, 1.8), geom_pos=(0, 0, 0.05),
                                   geom_color=ToontownGlobals.GlobalDialogColor, scale=0.85)
        self.browser.setBin('gui-popup', 0)

        self.fileList = DirectScrolledFrame(parent=self.browser, frameSize=(-0.55, 0.55, -0.4, 0.75), relief=DGG.SUNKEN,
                                            geom=scrollBkgd, geom_scale=(0.55, 1, 0.03), geom_pos=(0.5, 0, 0.175),
                                            geom_hpr=(0, 0, 90), borderWidth=(0.01, 0.01),
                                            frameColor=(0.85, 0.95, 1, 1), manageScrollBars=True,
                                            autoHideScrollBars=True, canvasSize=(-1, 0, -10, 1))

        self.fileList.verticalScroll['relief'] = None
        self.fileList.verticalScroll['frameTexture'] = None
        self.fileList.verticalScroll.incButton['relief'] = None
        self.fileList.verticalScroll.decButton['relief'] = None
        self.fileList.verticalScroll.thumb['geom'] = circleModel.find('**/tt_t_gui_mat_namePanelCircle')
        self.fileList.verticalScroll['resizeThumb'] = False
        self.fileList.verticalScroll.incButton.reparentTo(hidden)
        self.fileList.verticalScroll.decButton.reparentTo(hidden)

        self.fileNameBox = DirectFrame(parent=self.browser, relief=None,
                                       image=cdrGui.find('**/tt_t_gui_sbk_cdrCodeBox2'), pos=(0.1, 0, -0.525),
                                       scale=(1.0, 0.6, 0.6))

        self.fileNameEntry = DirectEntry(parent=self.browser, relief=None, borderWidth=(0.01, 0.01), text="",
                                         text_font = ToontownGlobals.getToonFont(), pos=(-0.23, 0, -0.53), scale=0.05,
                                         width=13, command=self.entryCR, numLines=1, focus=1, overflow=1)
        self.fileNameLabel = DirectLabel(parent=self.browser, text="File name:", text_scale=(0.05, 0.05),
                                         text_font=ToontownGlobals.getToonFont(), frameColor=(1.0, 0.98, 0.80, 1.0),
                                         pos=(-0.425, 0, -0.525))

        cancelButton = DirectButton(parent=self.browser, frameSize=(-0.11, 0.11, -0.05, 0.05), relief=None,
                                    image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'),
                                           guiButton.find('**/QuitBtn_RLVR')),
                                    borderWidth=(0.01, 0.01), pos=(-0.25, 0, -0.7),
                                    text="Cancel", text_pos=(0, -0.02), text_scale=(0.07, 0.07),
                                    text_font=ToontownGlobals.getToonFont(), command=self.cancelSelected)

        openButton = DirectButton(parent=self.browser, frameSize=(-0.11, 0.11, -0.05, 0.05), relief=None,
                                  image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'),
                                         guiButton.find('**/QuitBtn_RLVR')),
                                  borderWidth=(0.01, 0.01), pos=(0.25, 0, -0.7),
                                  text="Open", text_pos=(-0.01, -0.02), text_scale=(0.07, 0.07),
                                  text_font=ToontownGlobals.getToonFont(), command=self.openSelected)

        higherButton = DirectButton(parent=self.browser, frameSize=(-0.3, 0.3, -0.04, 0.04), relief=None,
                                    image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'),
                                           guiButton.find('**/QuitBtn_RLVR')),
                                    borderWidth=(0.01, 0.01), pos=(0, 0, 0.85),
                                    text="Go Up", text_pos=(-0.01, -0.015), text_scale=(0.05, 0.05),
                                    text_font=ToontownGlobals.getToonFont(), command=self.upSelected)

        self.createFileList(self.dot)

        cdrGui.removeNode()
        guiButton.removeNode()
        scrollBkgd.destroy()
