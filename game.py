import os
import app
import dbg
import grp
import item
import background
import chr
import chrmgr
import cw_player
import snd
import chat
import textTail
import snd
import net
import effect
import wndMgr
import fly
import systemSetting
import quest
import guild
import skill
import messenger
import localeInfo
import constInfo
import exchange
import ime
import ui
import serverInfo
import uiCommon
import uiPhaseCurtain
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget
import uiDeathCause
import uiauctionbuylink
import uiTeleport
import uiMobInfo
import uiProphecy
import cw_lootfilter
import localeString
import nonplayer
import uiCelestialPortal
import uiToolTip

# PRIVATE_SHOP_PRICE_LIST
import uiPrivateShopBuilder
# END_OF_PRIVATE_SHOP_PRICE_LIST

import mouseModule
import consoleModule

import playerSettingModule
import interfaceModule

import musicInfo
import debugInfo
import stringCommander


from _weakref import proxy





# TEXTTAIL_LIVINGTIME_CONTROL
#if localeInfo.IsJAPAN():
#	app.SetTextTailLivingTime(8.0)
# END_OF_TEXTTAIL_LIVINGTIME_CONTROL

# SCREENSHOT_CWDSAVE
SCREENSHOT_CWDSAVE = FALSE
SCREENSHOT_DIR = None

if localeInfo.IsEUROPE():
	SCREENSHOT_CWDSAVE = TRUE

if localeInfo.IsCIBN10():
	SCREENSHOT_CWDSAVE = FALSE
        SCREENSHOT_DIR = "YT2W"

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0

def GetLGInfo(id):
	table = {
		1	:	"Hallo, mein Name ist Celia. Ich werde deinen Weg in dieser Welt mitverfolgen und dir hilfreiche Tipps geben. Nun solltest du erst mal ein bisschen Erfahrung sammeln. Ich melde mich sp�ter wieder!",
		5	:	"Gl�ckwunsch, du hast Level 5 erreicht. Nun kannst du deine Ausbildung w�hlen. Wenn du etwas Yang angespart hast, kannst du zu Meister-Yi gehen, um deine Fertigkeiten zu erh�hen!",
		20	:	"Du machst gute Fortschritte, schau doch mal auf den anderen Niedrig-Level-Maps vorbei, du findest sie im Userpanel unter dem Menupunkt Sonstige Maps",
		65	:	"Sehr gut, du hast das Level 65 erreicht. Ich habe geh�rt, dass man in den verw�steten Landen sehr gut Austr�stung sammeln kann. Du findest sie im Userpanel unter dem Menupunkt Farm-Maps",
		75	:	"Mit dem Level 75 steht dir der Weg in die Grotte der Verbannung offen und ausserdem kannst du nun endlich die legend�ren Regenbogensteine sammeln!",
		90	:	"Na hast du endlich das Level 90 erreicht? Zeit der Grotte der Verbannung 2 einen Besuch abzustatten!",
		105	:	"Ich habe geh�rt, dass sich im Feuerland 2 ein paar fiese Gestalten befinden. Du hast hoffentlich keine Angst..",
		115	:	"Eine lang verschollene Stadt wurde wiederentdeckt! Begib dich zur Alten Stadt, wenn du antike Gegenst�nde sammeln willst!",
		120	:	"Hast du schon mal einen Zombie gesehen? Falls nicht besuche doch mal das Zombie-Land und dessen Zombieturm!",
		140	:	"Es wurden zwei neue L�nder offen gelegt, das Tal des Grauens und das Tal der aufgehenden Sonne.",
		150	:	"Du hast das Level 150 erreicht. Beachte bitte, dass du ab dem n�chsten Levelaufstieg deine Lehre bei den Lehrern nicht mehr wechseln kannst.",
		170	:	"Hall�le, ich habe wieder zwei neue L�nder entdeckt, Parricida Finis und das Vergessene K�nigreich.",
		210	:	"Es gibt nichts ekelhafteres als Spinnen, trotzdem kann ich dich leider nicht vor dem Spinnendungeon 3 bewahren.",
		230	:	"Kennst du schon meinen Lieblings Ort? Nein? Dann besuche doch mal das Kap des Drachenfeuers!",
		300	:	"Gl�ckwunsch, du hast das derzeitige Maximal-Level erreicht!",
		1000:	"GOTTA GO FAST BRO",
		1001:	"WAAAAAAAAZZZZZZZZZZZZZZZZUUUUUUUUUUP??"}

	if table.has_key(id):
		return table[id]
		
def GetGradeName(id):
	table = {
		1	:	localeInfo.TOOLTIP_GRADE1,
		2	:	localeInfo.TOOLTIP_GRADE2,
		3	:	localeInfo.TOOLTIP_GRADE3,
		4	:	localeInfo.TOOLTIP_GRADE4,
		5	:	localeInfo.TOOLTIP_GRADE5,
		6	:	localeInfo.TOOLTIP_GRADE6,
		7	:	localeInfo.TOOLTIP_GRADE7,
		8	:	localeInfo.TOOLTIP_GRADE8,
		9	:	localeInfo.TOOLTIP_GRADE9,
		10	:	localeInfo.TOOLTIP_GRADE10}

	if table.has_key(id):
		return table[id]

class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self, "GAME")
		self.SetWindowName("game")
		net.SetPhaseWindow(net.PHASE_WINDOW_GAME, self)
		cw_player.SetGameWindow(self)

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None

		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		self.console = None
		self.mapNameShower = None
		self.affectShower = None
		self.playerGauge = None
		self.confirmAHBuyDialog = None
		self.ahShopVnum = 0
		self.ahShopAuctionID = 0

		self.dlgCraftPowerstone = None
		
		self.ahLinkAttrSlot = []
		self.ahLinkMetinSlot = []
		self.ahLinkAscendanceSlot = []
		self.ahLinkAuctionID = 0
		self.ahLinkPricetype = 0
		self.ahLinkAscendance = 0
		self.ahLinkDlg = uiauctionbuylink.AuctionBuylinkDialog()
		
		self.hideAllWindows = 0


		self.stream=stream
		self.interface = interfaceModule.Interface()
		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()

		self.curtain = uiPhaseCurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()

		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
		self.targetBoard.BindGameClass(self)
		self.targetBoard.Hide()

		self.console = consoleModule.ConsoleWindow()
		self.console.BindGameClass(self)
		self.console.SetConsoleSize(wndMgr.GetScreenWidth(), 200)
		self.console.Hide()

		self.mapNameShower = uiMapNameShower.MapNameShower()
		self.affectShower = uiAffectShower.AffectShower()

		self.playerGauge = uiPlayerGauge.PlayerGauge(self)
		self.playerGauge.Hide()

		self.__SetQuickSlotMode()

		self.__ServerCommand_Build()
		self.__ProcessPreservedServerCommand()	
		
		self.DeathCauseDlg = None
		self.LootFilter = None

		self.dlgCelestialPortal = None

		self.coordinates = []
		self.numpad = [app.DIK_NUMPAD1, app.DIK_NUMPAD2, app.DIK_NUMPAD3, app.DIK_NUMPAD4, app.DIK_NUMPAD5, app.DIK_NUMPAD6, app.DIK_NUMPAD7, app.DIK_NUMPAD8]






	def __del__(self):
		cw_player.SetGameWindow(0)
		net.ClearPhaseWindow(net.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		app.SetFrameSkip(1)

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

		self.quickSlotPageIndex = 0
		self.PickingCharacterIndex = -1
		self.PickingItemIndex = -1
		self.consoleEnable = TRUE
		self.isShowDebugInfo = TRUE
		self.ShowNameFlag = FALSE

		self.enableXMasBoom = FALSE
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

		constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()
		constInfo.SET_DEFAULT_CHRNAME_COLOR()
		constInfo.SET_DEFAULT_FOG_LEVEL()
		constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
		constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()

		# TWO_HANDED_WEAPON_ATTACK_SPEED_UP
		constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()
		# END_OF_TWO_HANDED_WEAPON_ATTACK_SPEED_UP

		import event
		event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)

		textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)
		
		if systemSetting.GetDayTime()==1:
			background.SetEnvironmentData(0)
		elif systemSetting.GetDayTime()==2:
			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)

		if constInfo.PVPMODE_TEST_ENABLE:
			self.testPKMode = ui.TextLine()
			self.testPKMode.SetFontName(localeInfo.UI_DEF_FONT)
			self.testPKMode.SetPosition(0, 15)
			self.testPKMode.SetWindowHorizontalAlignCenter()
			self.testPKMode.SetHorizontalAlignCenter()
			self.testPKMode.SetFeather()
			self.testPKMode.SetOutline()
			self.testPKMode.Show()

			self.testAlignment = ui.TextLine()
			self.testAlignment.SetFontName(localeInfo.UI_DEF_FONT)
			self.testAlignment.SetPosition(0, 35)
			self.testAlignment.SetWindowHorizontalAlignCenter()
			self.testAlignment.SetHorizontalAlignCenter()
			self.testAlignment.SetFeather()
			self.testAlignment.SetOutline()
			self.testAlignment.Show()

		self.__BuildKeyDict()
		self.__BuildDebugInfo()

		# PRIVATE_SHOP_PRICE_LIST
		uiPrivateShopBuilder.Clear()
		# END_OF_PRIVATE_SHOP_PRICE_LIST

		# UNKNOWN_UPDATE
		exchange.InitTrading()
		# END_OF_UNKNOWN_UPDATE
		
		self.confirmAHBuyDialog = uiCommon.QuestionDialogNew()
		self.confirmAHBuyDialog.Open()
		self.confirmAHBuyDialog.SetText1(localeInfo.AH_SHOP_CONFIRM)
		self.confirmAHBuyDialog.SetText2(localeInfo.AH_SHOP_CONFIRM)
		self.confirmAHBuyDialog.SetAcceptEvent(self.AHItemBuyConfirm)
		self.confirmAHBuyDialog.SetCancelEvent(self.confirmAHBuyDialog.Hide)
		self.confirmAHBuyDialog.Hide()

		## Sound
		snd.SetMusicVolume(systemSetting.GetMusicVolume()*net.GetFieldMusicVolume())
		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		netFieldMusicFileName = net.GetFieldMusicFileName()
		if netFieldMusicFileName:
			snd.FadeInMusic("BGM/" + netFieldMusicFileName)
		elif musicInfo.fieldMusic != "":						
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		net.SendEnterGamePacket()

		# START_GAME_ERROR_EXIT
		try:
			self.StartGame()
		except:
			import exception
			exception.Abort("GameWindow.Open")
		# END_OF_START_GAME_ERROR_EXIT
		
		# NPC�� ť��ý������� ���� �� �ִ� �����۵��� ����� ĳ��
		# ex) cubeInformation[20383] = [ {"rewordVNUM": 72723, "rewordCount": 1, "materialInfo": "101,1&102,2", "price": 999 }, ... ]
		self.cubeInformation = {}
		self.currentCubeNPC = 0
		
		constInfo.ItemVnumList = []
		constInfo.mountSkinList = []
		item.LoadItemList()
		self.LootFilter = cw_lootfilter.LootFilter()
		self.LootFilter.LoadFilter()
		
	def Close(self):
		self.Hide()

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		self.onPressKeyDict = None
		self.onClickKeyDict = None

		chat.Close()
		snd.StopAllSound()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		skill.ClearSkillData()
		wndMgr.Unlock()
		mouseModule.mouseController.DeattachObject()

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()

		self.guildNameBoard = None
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None
		

		# UNKNOWN_UPDATE
		self.itemDropQuestionDialog = None
		# END_OF_UNKNOWN_UPDATE

		# QUEST_CONFIRM
		self.confirmDialog = None
		# END_OF_QUEST_CONFIRM

		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None
		self.confirmAHBuyDialog = None
		self.ahShopVnum = 0
		self.ahShopAuctionID = 0
		self.LootFilter = None

		self.ClearDictionary()

		self.playerGauge = None
		self.mapNameShower = None
		self.affectShower = None

		self.dlgCraftPowerstone = None

		if self.console:
			self.console.BindGameClass(0)
			self.console.Close()
			self.console=None
		
		if self.targetBoard:
			self.targetBoard.Destroy()
			self.targetBoard = None
	
		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			self.interface=None

		if self.DeathCauseDlg:
			self.DeathCauseDlg.Destroy()

		if self.dlgCelestialPortal:
			self.dlgCelestialPortal.Destroy()
			self.dlgCelestialPortal = None

		cw_player.ClearSkillDict()
		cw_player.ResetCameraRotation()

		self.KillFocus()
		app.HideCursor()

		print "---------------------------------------------------------------------------- CLOSE GAME WINDOW"

	def __BuildKeyDict(self):
		onPressKeyDict = {}

		##PressKey �� ������ �ִ� ���� ��� ����Ǵ� Ű�̴�.
		
		## ���� ����Ű �����Կ� �̿�ȴ�.(���� ���ڵ鵵 �� ���Կ� ����)
		## F12 �� Ŭ�� ����׿� Ű�̹Ƿ� ���� �ʴ� �� ����.
		onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)
		onPressKeyDict[app.DIK_F5]	= lambda : self.__PressF5()#packen
		onPressKeyDict[app.DIK_F6]	= lambda : self.__uiSwitchBot()#Switchbot
		onPressKeyDict[app.DIK_F7]	= lambda : self.__OpenAttrBoard()
		onPressKeyDict[app.DIK_F8]	= lambda : self.__PressF8()
		onPressKeyDict[app.DIK_F9]	= lambda : self.__PressF9()
		onPressKeyDict[app.DIK_F10]	= lambda : self.__PressF10()
		

		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
		onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

		#ĳ���� �̵�Ű
		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		#onPressKeyDict[app.DIK_F]			= lambda: app.ZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey

		#onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera() #
		#onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE) #
		#onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE) #
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		#onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE) #
		#onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE) #
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItemFast()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItemCW()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_P]			= lambda state = "BASE": self.interface.TogglePetWindow(state)
		onPressKeyDict[app.DIK_X]			= lambda state = "BASE": self.interface.ToggleParagonWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		#onPressKeyDict[app.DIK_B]			= lambda state = "EMOTICON": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
		onPressKeyDict[app.DIK_O]			= lambda : self.interface.ToggleDragonSoulWindowWithNoInfo()
		onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
		#onPressKeyDict[app.DIK_H]			= lambda : self.interface.OpenHelpWindow()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
		onPressKeyDict[app.DIK_COMMA]		= lambda : self.ShowConsole()		# "`" key #Modded by Jakrich
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()

		onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()
		

		onPressKeyDict[app.DIK_K]			= lambda : self.interface.ToggleMountWindow()

		self.onPressKeyDict = onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()

		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		#onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP) #
		#onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP) #
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		#onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP) #
		#onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP) #
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()

		onClickKeyDict[app.DIK_NUMPAD0] = lambda: self.__SaveCoordinate() #Modded by Jakrich
		onClickKeyDict[app.DIK_NUMPAD9] = lambda: self.__resetCoordinate()  #

		#if constInfo.PVPMODE_ACCELKEY_ENABLE:
		#	onClickKeyDict[app.DIK_B] = lambda: self.ChangePKMode()

		self.onClickKeyDict=onClickKeyDict

	def __Teleport(self, character_coordinate): #
		(x, y) = character_coordinate
		#net.SendChatPacket("ALERT: I am teleporting to: %d %d" % (x, y))
		net.SendChatPacket("/du %d %d" % (x, y))



	def __SaveCoordinate(self): #Modded by Jakrich
		if len(self.coordinates) >= 8:
			return
		else:
			(x, y, z) = cw_player.GetMainCharacterPosition()
			x = x / 100
			y = y / 100
			character_coordinate = (x, y)
			if character_coordinate in self.coordinates:
				return
			self.coordinates.append(character_coordinate)
			numpad_position = len(self.coordinates) -1
			self.onClickKeyDict[self.numpad[numpad_position]] = lambda: self.__Teleport(character_coordinate)
			#net.SendChatPacket("Coordinate Successfully Saved: %d %d" % (x, y))
			#for coordinate in self.coordinates:
				#net.SendChatPacket("%d %d Already saved" % (coordinate))


	def __resetCoordinate(self): #Modded by Jakrich
		self.coordinates = []
		for key in self.numpad:
			self.onClickKeyDict.pop(key)
		net.SendChatPacket("ALERT: Deleting coordinates %d")



	"""
	def __TeleportHere(self):
		(x, y, z) = cw_player.GetMainCharacterPosition()
		self.TeleportCoordX = x / 100
		self.TeleportCoordY = y / 100
		net.SendChatPacket("du %d %d" % (self.TeleportCoordX, self.TeleportCoordY))

	def __TeleportThere(self):
		net.SendChatPacket("/du %d %d" % (self.TeleportCoordX, self.TeleportCoordY))
	"""

	def __PressNumKey(self,num):




		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			
			if systemSetting.IsSpecialEmote():
				spclEmo = 12
			else:
				spclEmo = 0
				
			
			if num >= 1 and num <= 9:
				if(chrmgr.IsPossibleEmoticon(-1)):				
					chrmgr.SetEmoticon(-1,int(num)-1+spclEmo)
					# net.SendEmoticon(int(num)-1+spclEmo)
					net.SendChatPacket("/emoticon %d" % (int(num)-1+spclEmo))
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num-1)


	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constInfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()


	def	__PressJKey(self):
				if not uiPrivateShopBuilder.IsBuildingPrivateShop():
					for i in xrange(cw_player.INVENTORY_PAGE_SIZE*cw_player.INVENTORY_PAGE_COUNT):
						if cw_player.GetItemIndex(i) in (71114, 71116, 71118, 71120, 85268,85269,85270,85271,85272,85273,50053):
							net.SendItemUsePacket(i)
							break
	def	__PressHKey(self):
			if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
				if not uiPrivateShopBuilder.IsBuildingPrivateShop():
					for i in xrange(cw_player.INVENTORY_PAGE_SIZE*cw_player.INVENTORY_PAGE_COUNT):
						if cw_player.GetItemIndex(i) in (71114, 71116, 71118, 71120, 85268,85269,85270,85271,85272,85273,50053):
							net.SendItemUsePacket(i)
							break
			else:
				if app.IsPressed(app.DIK_LSHIFT):
					self.interface.OpenHelpWindow()

	def	__PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_back")
		else:
			state = "EMOTICON"
			self.interface.ToggleCharacterWindow(state)

	def	__PressFKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_feed")	
		else:
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)
			
	def __PressGKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
				if not uiPrivateShopBuilder.IsBuildingPrivateShop():
					for i in xrange(cw_player.INVENTORY_PAGE_SIZE*cw_player.INVENTORY_PAGE_COUNT):
						if cw_player.GetItemIndex(i) in (71114, 71116, 71118, 71120, 85268,85269,85270,85271,85272,85273,50053):
							net.SendItemUsePacket(i)
							break
		else:
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)


	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	def __SetQuickSlotMode(self):
		self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)


	def __SetQuickPageMode(self):
		self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)
	
	def __PressQuickSlot(self, localSlotIndex):
		if app.IsPressed(app.DIK_LSHIFT):
			self.HotkeyTeleport(55+localSlotIndex)
		else:
			cw_player.RequestUseLocalQuickSlot(localSlotIndex)			

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		cw_player.SetQuickPage(pageIndex)

	def ToggleDebugInfo(self):
		self.isShowDebugInfo = not self.isShowDebugInfo

		if self.isShowDebugInfo:
			self.PrintCoord.Show()
			self.FrameRate.Show()
			self.Pitch.Show()
			self.Splat.Show()
			self.TextureNum.Show()
			self.ObjectNum.Show()
			self.ViewDistance.Show()
			self.PrintMousePos.Show()
		else:
			self.PrintCoord.Hide()
			self.FrameRate.Hide()
			self.Pitch.Hide()
			self.Splat.Hide()
			self.TextureNum.Hide()
			self.ObjectNum.Hide()
			self.ViewDistance.Hide()
			self.PrintMousePos.Hide()

	def __BuildDebugInfo(self):
		## Character Position Coordinate
		self.PrintCoord = ui.TextLine()
		self.PrintCoord.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintCoord.SetPosition(wndMgr.GetScreenWidth() - 270, 0)
		
		## Frame Rate
		self.FrameRate = ui.TextLine()
		self.FrameRate.SetFontName(localeInfo.UI_DEF_FONT)
		self.FrameRate.SetPosition(wndMgr.GetScreenWidth() - 270, 20)

		## Camera Pitch
		self.Pitch = ui.TextLine()
		self.Pitch.SetFontName(localeInfo.UI_DEF_FONT)
		self.Pitch.SetPosition(wndMgr.GetScreenWidth() - 270, 40)

		## Splat
		self.Splat = ui.TextLine()
		self.Splat.SetFontName(localeInfo.UI_DEF_FONT)
		self.Splat.SetPosition(wndMgr.GetScreenWidth() - 270, 60)
		
		##
		self.PrintMousePos = ui.TextLine()
		self.PrintMousePos.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintMousePos.SetPosition(wndMgr.GetScreenWidth() - 270, 80)

		# TextureNum
		self.TextureNum = ui.TextLine()
		self.TextureNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.TextureNum.SetPosition(wndMgr.GetScreenWidth() - 270, 100)

		# ������Ʈ �׸��� ����
		self.ObjectNum = ui.TextLine()
		self.ObjectNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.ObjectNum.SetPosition(wndMgr.GetScreenWidth() - 270, 120)

		# �þ߰Ÿ�
		self.ViewDistance = ui.TextLine()
		self.ViewDistance.SetFontName(localeInfo.UI_DEF_FONT)
		self.ViewDistance.SetPosition(0, 0)

	def __NotifyError(self, msg):
		chat.AppendChat(chat.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):

		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if cw_player.GetStatus(cw_player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = cw_player.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == cw_player.PK_MODE_PROTECT:
			if 0 == cw_player.GetGuildID():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = cw_player.PK_MODE_GUILD

		elif nextPKMode == cw_player.PK_MODE_MAX_NUM:
			nextPKMode = 0

		net.SendChatPacket("/PKMode " + str(nextPKMode))
		print "/PKMode " + str(nextPKMode)

	def OnChangePKMode(self):

		self.interface.OnChangePKMode()

		try:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[cw_player.GetPKMode()])
		except KeyError:
			print "UNKNOWN PVPMode[%d]" % (cw_player.GetPKMode())

		if constInfo.PVPMODE_TEST_ENABLE:
			curPKMode = cw_player.GetPKMode()
			alignment, grade = chr.testGetPKData()
			self.pkModeNameDict = { 0 : "PEACE", 1 : "REVENGE", 2 : "FREE", 3 : "PROTECT", }
			self.testPKMode.SetText("Current PK Mode : " + self.pkModeNameDict.get(curPKMode, "UNKNOWN"))
			self.testAlignment.SetText("Current Alignment : " + str(alignment) + " (" + localeInfo.TITLE_NAME_LIST[grade] + ")")

	###############################################################################################
	###############################################################################################
	## Game Callback Functions

	# Start
	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()

	# Refresh
	def CheckGameButton(self):
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		self.CheckGameButton()
			
		if self.LootFilter:
			self.LootFilter.LootFilterPacket()
		
		if self.interface:	
			if self.LootFilter:
				self.LootFilter.LootFilterPacket()		
				
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()
		self.interface.RefreshGuildSafeboxGradePage()
		
	def RefreshGuildSafeboxPage(self):
		self.interface.RefreshGuildSafeboxPage()

	def RefreshMobile(self):
		if self.interface:
			self.interface.RefreshMobile()

	def OnMobileAuthority(self):
		self.interface.OnMobileAuthority()

	def OnBlockMode(self, mode):
		constInfo.SetBlockMode(mode)
		
	def OnDetailLogMode(self, mode):
		constInfo.SetDetailLogMode(mode)

	def OnDamageTextTailType(self, value):
		constInfo.SetDamageTextTailType(value)

	def OpenQuestWindow(self, skin, idx):
		if constInfo.INPUT_IGNORE == 1:
			return
		else:
			self.interface.OpenQuestWindow(skin, idx)

	def AskGuildName(self):

		guildNameBoard = uiCommon.InputDialog()
		guildNameBoard.SetTitle(localeInfo.GUILD_NAME)
		guildNameBoard.SetAcceptEvent(ui.__mem_func__(self.ConfirmGuildName))
		guildNameBoard.SetCancelEvent(ui.__mem_func__(self.CancelGuildName))
		guildNameBoard.Open()

		self.guildNameBoard = guildNameBoard

	def ConfirmGuildName(self):
		guildName = self.guildNameBoard.GetText()
		if not guildName:
			return

		if net.IsInsultIn(guildName):
			self.PopupMessage(localeInfo.GUILD_CREATE_ERROR_INSULT_NAME)
			return

		net.SendAnswerMakeGuildPacket(guildName)
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return TRUE

	def CancelGuildName(self):
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return TRUE

	## Refine
	def PopupMessage(self, msg, lockWindow = True):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.lockWindow = lockWindow
		self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

	def ClearRefineDialog(self):
		self.interface.ClearRefineDialog()

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, costType, cost, prob, type=0, sourceItemPos = 0):
		self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, costType, cost, prob, type, sourceItemPos)

	def AppendMaterialToRefineDialog(self, vnum, count, real_count):
		self.interface.AppendMaterialToRefineDialog(vnum, count, real_count)
	
	def AppendRequirementToRefineDialog(self, type, count):
		self.interface.AppendRequirementToRefineDialog(type, count)

	def AppendAttrToRefineDialog(self, type, value):
		self.interface.AppendAttrToRefineDialog(type, value)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	# UNKNOWN_UPDATE
	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration, spCost):
		if self.affectShower:
			self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration, spCost)
			if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
				self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)
			elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
				self.BINARY_DragonSoulGiveQuilification()

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		if self.affectShower:
			self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
			if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
				self.interface.DragonSoulDeactivate()
	
 
 
	# END_OF_UNKNOWN_UPDATE

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	def OnGameOver(self):
		self.CloseTargetBoard()
		self.OpenRestartDialog()

	def OpenRestartDialog(self):
		self.interface.OpenRestartDialog()

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	## TargetBoard
	def SetPCTargetBoard(self, vid, name):
		self.targetBoard.Open(vid, name)
		
		if app.IsPressed(app.DIK_LCONTROL):
			
			if not cw_player.IsSameEmpire(vid):
				return

			if cw_player.IsMainCharacterIndex(vid):
				return		
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return

			self.interface.OpenWhisperDialog(name)
			

	def RefreshTargetBoardByVID(self, vid):
		if self.targetBoard:
			self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		if self.targetBoard:
			self.targetBoard.RefreshByName(name)
		
	def __RefreshTargetBoard(self):
		self.targetBoard.Refresh()
		
	def SetHPTargetBoardCurHP(self, curHP):
		chat.AppendChat(chat.CHAT_TYPE_INFO,"curHP: %d" % (curHP))
		self.targetBoard.curHP = curHP
		
	def SetHPTargetBoardMaxHP(self, maxHP):
		chat.AppendChat(chat.CHAT_TYPE_INFO,"maxHP: %d" % (maxHP))
		self.targetBoard.maxHP = maxHP
	
	def SetHPTargetBoard(self, vid, hpPercentage , bLevel, RaceFlag, no_reset = False, addHPBars = 0):
		if not no_reset and vid != self.targetBoard.GetTargetVID():
			self.targetBoard.ResetTargetBoard()
			self.targetBoard.SetEnemyVID(vid,bLevel,RaceFlag)

		self.targetBoard.SetHP(hpPercentage, not no_reset, addHPBars)
		self.targetBoard.Show()

	def CloseTargetBoardIfDifferent(self, vid):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	def UpdateTargetBoardDPS(self):
		if self.targetBoard:
			self.targetBoard.UpdateDPS()

	def AppendTargetBountyObjective(self, bountyType, target, addTarget, addTarget2, count, countGoal):
		self.targetBoard.AppendBountyObjective(bountyType, target, addTarget, addTarget2, count, countGoal)

	def ClearTargetBoardAffects(self):
		self.targetBoard.ClearTargetAffects()

	def AppendTargetBoardAffect(self, affectType, affectCount):
		self.targetBoard.AppendTargetAffect(affectType, affectCount)
		
	## View Equipment
	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

	# SHOW_LOCAL_MAP_NAME
	def ShowMapName(self, mapName, x, y):

		if self.mapNameShower:
			self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)
	# END_OF_SHOW_LOCAL_MAP_NAME	

	def BINARY_OpenAtlasWindow(self):
		self.interface.BINARY_OpenAtlasWindow()

	## Chat
	def OnRecvWhisper(self, mode, name, line):
		if mode == chat.WHISPER_TYPE_ALERT:
			name = localeInfo.WHISPER_IMPORTANT
		elif mode == chat.WHISPER_TYPE_GM:
			self.interface.RegisterGameMasterName(name)
		
		chat.AppendWhisper(mode, name, line)
		self.interface.RecvWhisper(name)

	def AppendOnlineStatusMessage(self, type,name, message):
		if type == chat.WHISPER_TYPE_STATUS_MESSAGE:
			chat.AppendWhisper(chat.WHISPER_TYPE_STATUS_MESSAGE, name, localeInfo.WHISPER_ONLINE_STATUS_AFK_NOTICE % (name))
		else:
			chat.AppendWhisper(chat.WHISPER_TYPE_STATUS_MESSAGE, name, localeInfo.WHISPER_ONLINE_STATUS_DND_NOTICE % (name))
		if message:
			message = "%s : %s" % (localeInfo.WHISPER_ONLINE_STATUS_MESSAGE, message)
			chat.AppendWhisper(chat.WHISPER_TYPE_STATUS_MESSAGE, name, message)


	def OnRecvWhisperSystemMessage(self, mode, name, line):
		line = constInfo.ParseString(line)
		chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperError(self, mode, name, line):
		if localeInfo.WHISPER_ERROR.has_key(mode):
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name))
		else:
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		self.interface.RecvWhisper(name)

	def RecvWhisper(self, name):
		self.interface.RecvWhisper(name)

	def OnPickMoney(self, money):
		if not systemSetting.IsShowGoldText() & (1 << 0):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (money))
			
	def OnPickItem(self, vnum, count, toBag):				
		if not systemSetting.IsShowGoldText() & (1 << 1):
			if int(toBag):
				if int(count) > 1:
					chat.AppendChat(chat.CHAT_TYPE_INFO, "%s %s" % (localeInfo.GAME_PICK_ITEM % (int(count),item.GetNameByVnum(int(vnum))), localeInfo.GAME_PICK_ITEM_CRAFTING_BAG))
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, "%s %s" % (localeInfo.GAME_PICK_ITEM2 % (item.GetNameByVnum(int(vnum))), localeInfo.GAME_PICK_ITEM_CRAFTING_BAG))
			else:
				if int(count) > 1:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_ITEM % (int(count),item.GetNameByVnum(int(vnum))))
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_ITEM2 % (item.GetNameByVnum(int(vnum))))

	def OnShopError(self, type):
		try:
			self.PopupMessage(localeInfo.SHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeInfo.SAFEBOX_ERROR)

	def OnFishingSuccess(self, isFish, fishName):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)

	# ADD_FISHING_MESSAGE
	def OnFishingNotifyUnknown(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)
	# END_OF_ADD_FISHING_MESSAGE

	def OnFishingNotify(self, isFish, fishName):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)

	# MINING
	def OnCannotMining(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)
	# END_OF_MINING

	def OnCannotUseSkill(self, vid, type):
		if localeInfo.USE_SKILL_ERROR_TAIL_DICT.has_key(type):
			textTail.RegisterInfoTail(vid, localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])

		if localeInfo.USE_SKILL_ERROR_CHAT_DICT.has_key(type):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

	def	OnCannotShotError(self, vid, type):
		textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))

	## PointReset
	def StartPointReset(self):
		self.interface.OpenPointResetDialog()

	## Shop
	def StartShop(self, vid, size_x = 0, size_y = 0, isAHShop = 0, ownerName = ""):
		# chat.AppendChat(chat.CHAT_TYPE_INFO,"sizex: %d, sizey: %d"  % (size_x,size_y))
		self.interface.OpenShopDialog(vid,size_x, size_y, isAHShop, ownerName)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()

	def SetShopSellingPrice(self, Price):
		pass

	## Exchange
	def StartExchange(self):
		self.interface.StartExchange()

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
		self.interface.RefreshExchange()

	## Party
	def RecvPartyInviteQuestion(self, leaderVID, leaderName):
		partyInviteQuestionDialog = uiCommon.QuestionDialog()
		partyInviteQuestionDialog.SetText(leaderName + localeInfo.PARTY_DO_YOU_JOIN)
		partyInviteQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.Open()
		partyInviteQuestionDialog.partyLeaderVID = leaderVID
		self.partyInviteQuestionDialog = partyInviteQuestionDialog

	def AnswerPartyInvite(self, answer):

		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		distance = cw_player.GetCharacterDistance(partyLeaderVID)
		if distance < 0.0 or distance > 5000:
			answer = FALSE

		net.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None

	def AddPartyMember(self, pid, name):
		self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	def LinkPartyMember(self, pid, vid):
		self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		self.interface.ChangePartyParameter(distributionMode)

	## Messenger
	def OnMessengerAddFriendQuestion(self, name):
		messengerAddFriendQuestion = uiCommon.QuestionDialog2()
		messengerAddFriendQuestion.SetText1(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_1 % (name))
		messengerAddFriendQuestion.SetText2(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_2)
		messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
		messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
		messengerAddFriendQuestion.Open()
		messengerAddFriendQuestion.name = name
		self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return TRUE

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return TRUE

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return TRUE

	## SafeBox
	def OpenSafeboxWindow(self, size, pageCount):
		self.interface.OpenSafeboxWindow(size, pageCount)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	def RefreshSafeboxMoney(self):
		self.interface.RefreshSafeboxMoney()
		
	def ClearSafebox(self):
		self.interface.ClearSafebox()
		
	def AppendSafeboxPageName(self, pageName):
		self.interface.AppendSafeboxPageName(pageName)
		
	def AppendSafeboxPageType(self, pageName):
		self.interface.AppendSafeboxPageType(pageName)
		
	def AppendSafeboxPageButtonColor(self, r, g, b):
		self.interface.AppendSafeboxPageButtonColor(r, g, b)

	## GuildSafeBox
	def OpenGuildSafeboxWindow(self, size):
		self.interface.OpenGuildSafeboxWindow(size)

	def RefreshGuildSafebox(self):
		self.interface.RefreshGuildSafebox()

	# def RefreshGuildSafeboxMoney(self):
		# self.interface.RefreshGuildSafeboxMoney()

	def CloseGuildSafeboxWindow(self):
		self.interface.wndGuildSafebox.CommandCloseGuildSafebox()

	# ITEM_MALL
	def OpenMallWindow(self, size):
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
		self.interface.RefreshMall()
	# END_OF_ITEM_MALL

	## Guild
	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uiCommon.QuestionDialog()
		guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
		guildInviteQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.Open()
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):

		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		net.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None

	
	def DeleteGuild(self):
		self.interface.DeleteGuild()

	## Clock
	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	## Emotion
	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	###############################################################################################
	###############################################################################################
	## Keyboard Functions

	def CheckFocus(self):
		if FALSE == self.IsFocus():
			if TRUE == self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

	def SaveScreen(self):
		print "save screen"

		# SCREENSHOT_CWDSAVE
		if SCREENSHOT_CWDSAVE:
			if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
				os.mkdir(os.getcwd()+os.sep+"screenshot")

			(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)
		elif SCREENSHOT_DIR:
			(succeeded, name) = grp.SaveScreenShot(SCREENSHOT_DIR)
		else:
			(succeeded, name) = grp.SaveScreenShot()
		# END_OF_SCREENSHOT_CWDSAVE

		if succeeded:
			pass
			"""
			chat.AppendChat(chat.CHAT_TYPE_INFO, name + localeInfo.SCREENSHOT_SAVE1)
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE2)
			"""
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE_FAILURE)

	def ShowConsole(self):
		self.consoleDialog = consoleModule.ConsoleWindow()
		self.consoleDialog.OpenWindow()
		

	def ShowName(self):
		self.ShowNameFlag = TRUE
		self.playerGauge.EnableShowAlways()
		cw_player.SetQuickPage(self.quickSlotPageIndex+1)

	# ADD_ALWAYS_SHOW_NAME
	def __IsShowName(self):

		if systemSetting.IsAlwaysShowName():
			return TRUE

		if self.ShowNameFlag:
			return TRUE

		return FALSE
	# END_OF_ADD_ALWAYS_SHOW_NAME
	
	def HideName(self):
		self.ShowNameFlag = FALSE
		self.playerGauge.DisableShowAlways()
		cw_player.SetQuickPage(self.quickSlotPageIndex)

	def ShowMouseImage(self):
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		self.interface.HideMouseImage()

	def StartAttack(self):
		cw_player.SetAttackKeyState(TRUE)

	def EndAttack(self):
		cw_player.SetAttackKeyState(FALSE)

	def MoveUp(self):
		# import chat
		# chat.AppendChat(chat.CHAT_TYPE_INFO,"lol")
		cw_player.SetSingleDIKKeyState(app.DIK_UP, TRUE)

	def MoveDown(self):
		cw_player.SetSingleDIKKeyState(app.DIK_DOWN, TRUE)

	def MoveLeft(self):
		cw_player.SetSingleDIKKeyState(app.DIK_LEFT, TRUE)

	def MoveRight(self):
		cw_player.SetSingleDIKKeyState(app.DIK_RIGHT, TRUE)

	def StopUp(self):
		cw_player.SetSingleDIKKeyState(app.DIK_UP, FALSE)

	def StopDown(self):
		cw_player.SetSingleDIKKeyState(app.DIK_DOWN, FALSE)

	def StopLeft(self):
		cw_player.SetSingleDIKKeyState(app.DIK_LEFT, FALSE)

	def StopRight(self):
		cw_player.SetSingleDIKKeyState(app.DIK_RIGHT, FALSE)

	def PickUpItemCW(self):
		cw_player.PickCloseItem()

	def PickUpItemFast(self):
		cw_player.PickCloseItem()
		
	###############################################################################################
	###############################################################################################
	## Event Handler

	def OnKeyDown(self, key):
		if self.interface.wndWeb and self.interface.wndWeb.IsShow():
			return

		constInfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)

		try:
			self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return TRUE

	def OnKeyUp(self, key):
		if key == app.DIK_LSHIFT and mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()
			
		try:
			self.onClickKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return TRUE

	def OnMouseLeftButtonDown(self):
		if self.interface.BUILD_OnMouseLeftButtonDown():
			return

		if mouseModule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				cw_player.SetMouseState(cw_player.MBT_LEFT, cw_player.MBS_PRESS);

		return TRUE

	def OnMouseLeftButtonUp(self):

		if self.interface.BUILD_OnMouseLeftButtonUp():
			return

		if mouseModule.mouseController.isAttached():

			attachedType = mouseModule.mouseController.GetAttachedType()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()

			## QuickSlot
			if cw_player.SLOT_TYPE_QUICK_SLOT == attachedType:
				cw_player.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

			## Inventory
			elif cw_player.SLOT_TYPE_INVENTORY == attachedType:

				if cw_player.ITEM_MONEY == attachedItemIndex:
					self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## DragonSoul
			elif cw_player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)
			
			# if not app.IsPressed(app.DIK_LSHIFT):
			mouseModule.mouseController.DeattachObject()

		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.IsPressed(app.DIK_LALT):
					link = chat.GetLinkFromHyperlink(hyperlink)
					ime.PasteString(link)
				else:
					self.interface.MakeHyperlinkTooltip(hyperlink)
				return
			else:
				cw_player.SetMouseState(cw_player.MBT_LEFT, cw_player.MBS_CLICK)

		#cw_player.EndMouseWalking()
		return TRUE

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if cw_player.SLOT_TYPE_INVENTORY == attachedType or cw_player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
			attachedInvenType = cw_player.SlotTypeToInvenType(attachedType)
			if TRUE == chr.HasInstance(self.PickingCharacterIndex) and cw_player.GetMainCharacterIndex() != dstChrID:
				if cw_player.IsEquipmentSlot(attachedItemSlotPos):
					self.stream.popupWindow.Close()
					self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
				else:
					if chr.IsNPC(dstChrID) or constInfo.CanGiveToMob(attachedItemIndex):
						if app.IsPressed(app.DIK_LSHIFT):
							net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount, 1)
						else:
							net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount, 0)
					else:
						net.SendExchangeStartPacket(dstChrID)
						net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
			else:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

	def __PutMoney(self, attachedType, attachedMoney, dstChrID):
		if TRUE == chr.HasInstance(dstChrID) and cw_player.GetMainCharacterIndex() != dstChrID:
			net.SendExchangeStartPacket(dstChrID)
			net.SendExchangeElkAddPacket(attachedMoney)
		else:
			self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		# PRIVATESHOP_DISABLE_ITEM_DROP - ���λ��� ���� �ִ� ���� ������ ���� ����
		if uiPrivateShopBuilder.IsBuildingPrivateShop():			
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
		
		if attachedMoney>=1000:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = cw_player.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
		# PRIVATESHOP_DISABLE_ITEM_DROP - ���λ��� ���� �ִ� ���� ������ ���� ����
		if uiPrivateShopBuilder.IsBuildingPrivateShop():			
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
		
		if cw_player.SLOT_TYPE_INVENTORY == attachedType and cw_player.IsEquipmentSlot(attachedItemSlotPos):
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

		else:
			if cw_player.SLOT_TYPE_INVENTORY == attachedType:
				dropItemIndex = cw_player.GetItemIndex(attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				## Question Text
				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				## Dialog
				itemDropQuestionDialog = uiCommon.QuestionDialog()
				itemDropQuestionDialog.SetText(questionText)
				itemDropQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.RequestDropItem(arg))
				itemDropQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.RequestDropItem(arg))
				itemDropQuestionDialog.Open()
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(1)
			elif cw_player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				dropItemIndex = cw_player.GetItemIndex(cw_player.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)

				item.SelectItem(dropItemIndex)
				dropItemName = item.GetItemName()

				## Question Text
				questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

				## Dialog
				itemDropQuestionDialog = uiCommon.QuestionDialog()
				itemDropQuestionDialog.SetText(questionText)
				itemDropQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.RequestDropItem(arg))
				itemDropQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.RequestDropItem(arg))
				itemDropQuestionDialog.Open()
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog = itemDropQuestionDialog

				constInfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(1)

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if cw_player.SLOT_TYPE_INVENTORY == dropType:
				if dropNumber == cw_player.ITEM_MONEY:
					net.SendGoldDropPacketNew(dropCount)
					snd.PlaySound("sound/ui/money.wav")
				else:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
			elif cw_player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount, cw_player.DRAGON_SOUL_INVENTORY)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_DROP_QUESTION_DIALOG_STATUS(0)

	# PRIVATESHOP_DISABLE_ITEM_DROP
	def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = cw_player.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)
	# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

	def OnMouseRightButtonDown(self):

		self.CheckFocus()

		if TRUE == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			cw_player.SetMouseState(cw_player.MBT_RIGHT, cw_player.MBS_PRESS)

		return TRUE
		
	# def OnMouseOverIn(self):
		# chat.AppendChat(chat.CHAT_TYPE_INFO,"LUL")
		# hyperlink = ui.GetHyperlink()
		# if hyperlink:
			# self.interface.MakeHyperlinkTooltip(hyperlink)

	def OnMouseRightButtonUp(self):
		if TRUE == mouseModule.mouseController.isAttached():
			return TRUE

		cw_player.SetMouseState(cw_player.MBT_RIGHT, cw_player.MBS_CLICK)
		return TRUE

	def OnMouseMiddleButtonDown(self):
		cw_player.SetMouseMiddleButtonState(cw_player.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		cw_player.SetMouseMiddleButtonState(cw_player.MBS_CLICK)

	def OnUpdate(self):	
		app.UpdateGame()
		
		if self.mapNameShower.IsShow():
			self.mapNameShower.Update()

		if self.isShowDebugInfo:
			self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()

		self.interface.BUILD_OnUpdate()
		uiPrivateShopBuilder.UpdateADBoard()
		
		if cw_player.GetStatus(cw_player.PET_HUNGRY)==10 and constInfo.PET_HUNGRY_PM==0:
			constInfo.PET_HUNGRY_PM = 1
			chat.AppendWhisper(chat.WHISPER_TYPE_CHAT, "Celia","Celia : Dein Pet ist hungrig! Bitte f�ttere es oder bin ich gezwungen die PETA dar�ber zu informieren. :)")
			self.interface.RecvWhisper("Celia")
		
		if systemSetting.IsToggleSprint()==1:	
			if app.IsPressed(app.DIK_LSHIFT):
				cw_player.SetToggleSprint(1)
			else:
				cw_player.SetToggleSprint(0)
		

	def UpdateDebugInfo(self):
		#
		# ĳ���� ��ǥ �� FPS ���
		(x, y, z) = cw_player.GetMainCharacterPosition()
		nUpdateTime = app.GetUpdateTime()
		nUpdateFPS = app.GetUpdateFPS()
		nRenderFPS = app.GetRenderFPS()
		nFaceCount = app.GetFaceCount()
		fFaceSpeed = app.GetFaceSpeed()
		nST=background.GetRenderShadowTime()
		(fAveRT, nCurRT) =  app.GetRenderTime()
		(iNum, fFogStart, fFogEnd, fFarCilp) = background.GetDistanceSetInfo()
		(iPatch, iSplat, fSplatRatio, sTextureNum) = background.GetRenderedSplatNum()
		if iPatch == 0:
			iPatch = 1

		#(dwRenderedThing, dwRenderedCRC) = background.GetRenderedGraphicThingInstanceNum()

		self.PrintCoord.SetText("Coordinate: %.2f %.2f %.2f ATM: %d" % (x, y, z, app.GetAvailableTextureMemory()/(1024*1024)))
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.PrintMousePos.SetText("MousePosition: %d %d" % (xMouse, yMouse))			

		self.FrameRate.SetText("UFPS: %3d UT: %3d FS %.2f" % (nUpdateFPS, nUpdateTime, fFaceSpeed))

		if fAveRT>1.0:
			self.Pitch.SetText("RFPS: %3d RT:%.2f(%3d) FC: %d(%.2f) " % (nRenderFPS, fAveRT, nCurRT, nFaceCount, nFaceCount/fAveRT))

		self.Splat.SetText("PATCH: %d SPLAT: %d BAD(%.2f)" % (iPatch, iSplat, fSplatRatio))
		#self.Pitch.SetText("Pitch: %.2f" % (app.GetCameraPitch())
		#self.TextureNum.SetText("TN : %s" % (sTextureNum))
		#self.ObjectNum.SetText("GTI : %d, CRC : %d" % (dwRenderedThing, dwRenderedCRC))
		self.ViewDistance.SetText("Num : %d, FS : %f, FE : %f, FC : %f" % (iNum, fFogStart, fFogEnd, fFarCilp))

	def OnRender(self):
		app.RenderGame()
		
		if self.console.Console.collision:
			background.RenderCollision()
			chr.RenderCollision()

		(x, y) = app.GetCursorPosition()

		########################
		# Picking
		########################
		textTail.UpdateAllTextTail()

		if TRUE == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			# ADD_ALWAYS_SHOW_NAME
			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)
			# END_OF_ADD_ALWAYS_SHOW_NAME
			
		## Show all name in the range
		
		# ADD_ALWAYS_SHOW_NAME
		if self.__IsShowName():
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)
		# END_OF_ADD_ALWAYS_SHOW_NAME

		textTail.UpdateShowingTextTail()
		textTail.ArrangeTextTail()
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		textTail.Render()
		textTail.HideAllTextTail()

	def OnPressEscapeKey(self):
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif TRUE == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			self.interface.OpenSystemDialog()

		return TRUE

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
			
		# if self.interface.wndTeleportMenu:
			# if self.interface.wndTeleportMenu.IsShow():
				# self.interface.wndTeleportMenu.Warp()
		return TRUE

	def OnPressExitKey(self):
		self.interface.ToggleSystemDialog()
		return TRUE

	## BINARY CALLBACK
	######################################################################################
	
	# WEDDING
	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)
	# END_OF_WEDDING
	
	# QUEST_CONFIRM
	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
		confirmDialog.Open(msg, timeout)
		confirmDialog.SetAcceptEvent(lambda answer=TRUE, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelEvent(lambda answer=FALSE, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		self.confirmDialog = confirmDialog
    # END_OF_QUEST_CONFIRM

    # GIFT command
	def Gift_Show(self):
		self.interface.ShowGift()

	 # CelestialPortalPopUp command
	def ShowCelestialPortalButton(self, bIsBoss = False):
		self.interface.ShowCelestialPortalButton(bIsBoss)

	def ShowLeaveDungeonButton(self):
		self.interface.ShowLeaveDungeonButton()

	def ShowSkipWaveCountdownButton(self):
		self.interface.ShowSkipWaveCountdownButton()

	def HideSkipWaveCountdownButton(self):
		self.interface.HideSkipWaveCountdownButton()
		
	def UpdateLootFilterTime(self, LootFilterTime, LootFilterLastUse):
		constInfo.LOOTFILTER_TIME = LootFilterTime
		constInfo.LOOTFILTER_LAST_USE = LootFilterLastUse
	

	# CUBE
	def BINARY_Cube_Open(self, npcVNUM):
		self.currentCubeNPC = npcVNUM
		
		self.interface.OpenCubeWindow()

		
		if npcVNUM not in self.cubeInformation:
			net.SendChatPacket("/cube r_info")
		else:
			cubeInfoList = self.cubeInformation[npcVNUM]
			
			i = 0
			for cubeInfo in cubeInfoList:								
				self.interface.wndCube.AddCubeResultItem(cubeInfo["vnum"], cubeInfo["count"])
				
				j = 0				
				for materialList in cubeInfo["materialList"]:
					for materialInfo in materialList:
						itemVnum, itemCount = materialInfo
						self.interface.wndCube.AddMaterialInfo(i, j, itemVnum, itemCount)
					j = j + 1						
						
				i = i + 1
				
			self.interface.wndCube.Refresh()

	def BINARY_Cube_Close(self):
		self.interface.CloseCubeWindow()

	# ���ۿ� �ʿ��� ���, ����Ǵ� �ϼ�ǰ�� VNUM�� ���� ���� update
	def BINARY_Cube_UpdateInfo(self, gold, itemVnum, count):
		self.interface.UpdateCubeInfo(gold, itemVnum, count)
		
	def BINARY_Cube_Succeed(self, itemVnum, count):
		print "ť�� ���� ����"
		self.interface.SucceedCubeWork(itemVnum, count)
		pass

	def BINARY_Cube_Failed(self):
		print "ť�� ���� ����"
		self.interface.FailedCubeWork()
		pass

	def BINARY_Cube_ResultList(self, npcVNUM, listText):
		# ResultList Text Format : 72723,1/72725,1/72730.1/50001,5  �̷������� "/" ���ڷ� ���е� ����Ʈ�� ��
		#print listText
		
		if npcVNUM == 0:
			npcVNUM = self.currentCubeNPC
		
		self.cubeInformation[npcVNUM] = []
		
		try:
			for eachInfoText in listText.split("/"):
				eachInfo = eachInfoText.split(",")
				itemVnum	= int(eachInfo[0])
				itemCount	= int(eachInfo[1])

				self.cubeInformation[npcVNUM].append({"vnum": itemVnum, "count": itemCount})
				self.interface.wndCube.AddCubeResultItem(itemVnum, itemCount)
			
			resultCount = len(self.cubeInformation[npcVNUM])
			requestCount = 7
			modCount = resultCount % requestCount
			splitCount = resultCount / requestCount
			for i in xrange(splitCount):
				#print("/cube r_info %d %d" % (i * requestCount, requestCount))
				net.SendChatPacket("/cube r_info %d %d" % (i * requestCount, requestCount))
				
			if 0 < modCount:
				#print("/cube r_info %d %d" % (splitCount * requestCount, modCount))				
				net.SendChatPacket("/cube r_info %d %d" % (splitCount * requestCount, modCount))

		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0
			
		pass
		
	def BINARY_Cube_MaterialInfo(self, startIndex, listCount, listText):
		# Material Text Format : 125,1|126,2|127,2|123,5&555,5&555,4/120000
		try:
			#print listText
			
			if 3 > len(listText):
				dbg.TraceError("Wrong Cube Material Infomation")
				return 0

			
			
			eachResultList = listText.split("@")

			cubeInfo = self.cubeInformation[self.currentCubeNPC]			
			
			itemIndex = 0
			for eachResultText in eachResultList:
				cubeInfo[startIndex + itemIndex]["materialList"] = [[], [], [], [], []]
				materialList = cubeInfo[startIndex + itemIndex]["materialList"]
				
				gold = 0
				splitResult = eachResultText.split("/")
				if 1 < len(splitResult):
					gold = int(splitResult[1])
					
				#print "splitResult : ", splitResult
				eachMaterialList = splitResult[0].split("&")
				
				i = 0
				for eachMaterialText in eachMaterialList:
					complicatedList = eachMaterialText.split("|")
					
					if 0 < len(complicatedList):
						for complicatedText in complicatedList:
							(itemVnum, itemCount) = complicatedText.split(",")
							itemVnum = int(itemVnum)
							itemCount = int(itemCount)
							self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)
							
							materialList[i].append((itemVnum, itemCount))
							
					else:
						itemVnum, itemCount = eachMaterialText.split(",")
						itemVnum = int(itemVnum)
						itemCount = int(itemCount)
						self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)
						
						materialList[i].append((itemVnum, itemCount))
						
					i = i + 1
					
					
					
				itemIndex = itemIndex + 1
				
			self.interface.wndCube.Refresh()
			
				
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0
			
		pass
	
	# END_OF_CUBE
	
	# ��ȥ��	
	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		self.interface.Highligt_Item(inven_type, inven_pos)
	
	def BINARY_DragonSoulGiveQuilification(self):
		self.interface.DragonSoulGiveQuilification()
		
	def BINARY_DragonSoulRefineWindow_Open(self):
		self.interface.OpenDragonSoulRefineWindow()

	def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
		self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

	def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
		self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)
	
	# END of DRAGON SOUL REFINE WINDOW
	
	def BINARY_SetBigMessage(self, message):
		if self.interface.bigBoard:
			self.interface.bigBoard.SetTip(message)

	def	BigMsg(self, msg):
		if self.interface.bigBoard:
			self.interface.bigBoard.SetTip(msg.replace("##"," "))

	def BINARY_SetTipMessage(self, message):
		if self.interface and self.interface.tipBoard:
			self.interface.tipBoard.SetTip(message)		

	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeInfo.NOTIFY_MESSAGE:
			return
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
		mainCharacterName = cw_player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()
		if mainCharacterName == masterName:
			self.__GuildWar_OpenAskDialog(guildID, warType)

	def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
		self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)	

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)

	def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
		self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_OpenAskDialog(self, guildID, warType):

		guildName = guild.GetGuildName(guildID)

		# REMOVED_GUILD_BUG_FIX
		if "Noname" == guildName:
			return
		# END_OF_REMOVED_GUILD_BUG_FIX

		import uiGuild
		questionDialog = uiGuild.AcceptGuildWarDialog()
		questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
		questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
		questionDialog.Open(guildName, warType)

		self.guildWarQuestionDialog = questionDialog

	def __GuildWar_CloseAskDialog(self):
		self.guildWarQuestionDialog.Close()
		self.guildWarQuestionDialog = None

	def __GuildWar_OnAccept(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/war " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __GuildWar_OnDecline(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/nowar " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1
	## BINARY CALLBACK
	######################################################################################

	def __ServerCommand_Build(self):
		serverCommandList={
			"ConsoleEnable"			: self.__Console_Enable,
			"DayMode"				: self.__DayMode_Update, 
			"PRESERVE_DayMode"		: self.__PRESERVE_DayMode_Update, 
			"CloseRestartWindow"	: self.__RestartDialog_Close,
			"OpenPrivateShop"		: self.__PrivateShop_Open,
			"PartyHealReady"		: self.PartyHealReady,
			"ShowMeSafeboxPassword"	: self.AskSafeboxPassword,
			"CloseSafebox"			: self.CommandCloseSafebox,
			"OpenUserpanel"			: self.CommandOpenUserpanel,
			"SetCSQid"			: self.CommandSetCSQid,			
			"SetCSDisable"			: self.CommandSetCSDisable,
			"cwDaytime"			: self.CommandCwDaytime,
			"ds_environment"			: self.CommandDsEnvironment,
			"set_texture"				: self.CommandSetTexture,
			"replace_texture_by_idx"				: self.CommandReplaceTextureByIDX,
			"shuffle_textures"				: self.CommandShuffleTextures,
			"ds_textureset"				: self.CommandDSTextureSet,
			"ds_water_texture"			: self.CommandDSSetWaterTexture,
			"ds_snow"			: self.CommandDsSnow,
			"GetDayTime"		: self.GetDayTime,
			"HasGuildSafebox"	: self.CommandHasGuildSafebox,
			##TEAM_LOGIN_WITH_LIST
			"CheckTeamOnline"		: self.__CheckTeamOnline,
			"ReloadPanel"			: self.__ReloadPanel,
			"SetTeamOnline"			: self.__TeamLogin,
			"SetTeamOffline"		: self.__TeamLogout,
			##END_OF_TEAM_LOGIN_WITH_LIST
			"MessengerLogin"		: self.OnMsgLogin,
			"MessengerLogout"		: self.OnMsgLogout,
			##RANKSYSTEM##
			"LOAD_RANK"		: self.__LoadRank,
			"get_input_value"				: self.GetInputValue,
			"get_input_start"				: self.GetInputOn,
			"get_input_end"					: self.GetInputOff,
			"get_rank_info"				: self.GetRankInfo,
			##END_OF_RANK_SYSTEM##
			"Load_Safebox"		: self.__LoadSafebox,
			# CW_LEVELGUIDE
			"LG_SendTip"	: self.__cwLevelGuide,
			#END_OF_CW_LEVELGUIDE
			"UpdatePetName"	: self.__UpdatePetName,

			"search_item"	: self.SearchItem,

			"CloseShopAttrWindow"	:	self.CloseShopAttrWindow,
			
			"OpenAmuletFusion"	: self.OpenAmuletFusion,
			"add_amulet_fusion_result_slot"	: self.AddAmuletFusionResultSlot,

			"OpenAmuletCraft"	: self.OpenAmuletCraftDialog,
			"AppendAmuletCraft"	: self.AppendAmuletCraftDialog,
			"ClearAmuletCraft"	: self.ClearAmuletCraftDialog,
			
			"OpenCraftPowerstone"	: self.OpenCraftPowerstone,

			#PresetMap
			"ClearPresetMap"		: self.ClearPresetMap,
			"ClearPresetMapChallenge"	: self.ClearPresetMapChallenge,
			"AppendPresetMapChallenge"	: self.AppendPresetMapChallenge,
			"AppendPresetMapChallengePortals"	: self.AppendPresetMapChallengePortals,
			"SetPresetMapRitualCount"	: self.SetPresetMapRitualCount,
			"AppendPresetMapField"	: self.AppendPresetMapField,
			"AppendPresetMapPortal"	: self.AppendPresetMapPortal,
			"OpenPresetMap"			: self.OpenPresetMap,

			#LocaleString
			"append_locale_string"	:	self.AppendLocaleString,
			
			"AHItemBuy"			: self.AHItemBuy,
			#Auktionshaus
			"Auktionshausdialog"				: self.Auktionshausdialog,
			"Auktionshausbutton"				: self.Auktionshausbutton,
			"AuktionshausCMD"					: self.AuktionshausCMD,
			"Auktionshaus"						: self.Auktionshaus,
			"AuktionshausSetMoney"				: self.AuktionshausSetMoney,
			"AuktionshausSetLager"				: self.AuktionshausSetLager,
			"ClearAHItems"						: self.AuktionshausClearAHItems,
			"ClearAHSellingItems"				: self.AuktionshausClearAHItems,
			"AddAHSellingItem"					: self.AuktionshausAddAHSellingItem,
			"AddAHHistory"						: self.AuktionshausAddAHHistory,
			"AddAHItem"							: self.AuktionshausAddAHItem,
			"LoadAHSuccess"						: self.AuktionshausLoadAHSuccess,
			"RemoveAHSuccess"					: self.AuktionshausRemoveAHSuccess,
			"AuktionshausSetAvgPrice"					: self.AuktionshausSetAvgPrice,
			"RemoveItemComplete"	: self.AuktionhouseRemoveItemComplete,
			"BigMsg"				: self.BigMsg,
			# ITEM_MALL
			"CloseMall"				: self.CommandCloseMall,
			"ShowMeMallPassword"	: self.AskMallPassword,
			"item_mall"				: self.__ItemMall_Open,
			# END_OF_ITEM_MALL
			"update_language"				: self.__UpdateLanguage,
			"RefineSuceeded"		: self.RefineSuceededMessage,
			"RefineFailed"			: self.RefineFailedMessage,
			"xmas_snow"				: self.__XMasSnow_Enable,
			"xmas_boom"				: self.__XMasBoom_Enable,
			"xmas_song"				: self.__XMasSong_Enable,
			"xmas_tree"				: self.__XMasTree_Enable,
			"newyear_boom"			: self.__XMasBoom_Enable,
			"PartyRequest"			: self.__PartyRequestQuestion,
			"PartyRequestDenied"	: self.__PartyRequestDenied,
			"set_prophecy_obj_count": self.__SetProphecyObjCount,
			"OpenRingSwitchDialog"	: self.OpenRingSwitchDialog,
			"AddRingSwitchAttr"		: self.AddRingSwitchAttr,
			"ClearRingSwitchDialog"		: self.ClearRingSwitchDialog,
			"ClearRingSwitchLists"		: self.ClearRingSwitchLists,
			"UpdateRingSwitchSlot"		: self.UpdateRingSwitchSlot,
			"horse_state"			: self.__Horse_UpdateState,
			"hide_horse_state"		: self.__Horse_HideState,
			"WarUC"					: self.__GuildWar_UpdateMemberCount,
			"test_server"			: self.__EnableTestServerFlag,
			"mall"			: self.__InGameShop_Show,
			"refresh_channel"			: self.RefreshChannel,
			"refresh_map"			: self.RefreshMap,

			"RefreshBlockDropListItem"			: self.RefreshBlockDropListItem,

			#Portals
			"SetDungeonPerc"		: self.SetDungeonPointsPercentage,

			"update_dungeon_task"		: self.UpdateDungeonTask,
			
			"OnPickItem"			: self.OnPickItem,

			"UpdateServerInfo"		: self.UpdateServerInfo,
			# WEDDING
			"lover_login"			: self.__LoginLover,
			"lover_logout"			: self.__LogoutLover,
			"lover_near"			: self.__LoverNear,
			"lover_far"				: self.__LoverFar,
			"lover_divorce"			: self.__LoverDivorce,
			"PlayMusic"				: self.__PlayMusic,
			# END_OF_WEDDING

			# PRIVATE_SHOP_PRICE_LIST
			"MyShopPriceList"		: self.__PrivateShop_PriceList,
			# END_OF_PRIVATE_SHOP_PRICE_LIST
			
			"InitMountSkinWindow"	: self.InitMountSkinWindow,
			"AppendMountSkin"		: self.AppendMountSkin,
			"OpenMountSkinWindow"	: self.OpenMountSkinWindow,

			"RefreshMailWindow"	: self.ForceRefreshMailWindow,
			"MailLoginNotice"	: self.MailLoginNotice,
			"MailSendSuccess"	: self.MailSendSuccess,

			"OpenBountyHuntSetup"	: self.OpenBountyHuntSetup,
		}

		self.serverCommander=stringCommander.Analyzer()
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)

	def BINARY_ServerCommand_Run(self, line):
		#dbg.TraceError(line)
		try:
			#print " BINARY_ServerCommand_Run", line
			return self.serverCommander.Run(line)
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = net.GetPreservedServerCommand()
			while command:
				print " __ProcessPreservedServerCommand", command
				self.serverCommander.Run(command)
				command = net.GetPreservedServerCommand()
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def PartyHealReady(self):
		self.interface.PartyHealReady()

	def AskSafeboxPassword(self):
		self.interface.AskSafeboxPassword()

	# ITEM_MALL
	def AskMallPassword(self):
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		self.interface.OpenItemMall();
		
	def __UpdateLanguage(self):
		net.SendChatPacket("/set_language %d" % (systemSetting.GetLanguage()))

	def CommandCloseMall(self):
		self.interface.CommandCloseMall()
	# END_OF_ITEM_MALL

	def RefineSuceededMessage(self):
		snd.PlaySound("sound/ui/make_soket.wav")
		self.PopupMessage(localeInfo.REFINE_SUCCESS, False)

	def RefineFailedMessage(self):
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		self.PopupMessage(localeInfo.REFINE_FAILURE, False)

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()

	# PRIVATE_SHOP_PRICE_LIST
	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
		uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)	
	# END_OF_PRIVATE_SHOP_PRICE_LIST

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		self.affectShower.SetHorseState(int(level), int(health), int(battery))

	def __IsXMasMap(self):
		mapDict = ( "metin2_map_n_flame_01",
					"metin2_map_n_desert_01",
					"metin2_map_spiderdungeon",
					"metin2_map_deviltower1", )

		if background.GetCurrentMapName() in mapDict:
			return FALSE

		return TRUE

	def __XMasSnow_Enable(self, mode):

		if systemSetting.GetWeather()!=3:
			return
	
		self.__XMasSong_Enable(mode)

		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_SNOW ON"
			background.EnableSnow(1)

		else:
			print "XMAS_SNOW OFF"
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		
		if systemSetting.GetDayTime()!=3:
			return
		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_BOOM ON"
			self.__DayMode_Update("dark")
			self.enableXMasBoom = TRUE
			self.startTimeXMasBoom = app.GetTime()
		else:
			print "XMAS_BOOM OFF"
			self.__DayMode_Update("light")
			self.enableXMasBoom = FALSE

	def __XMasTree_Enable(self, grade):

		print "XMAS_TREE ", grade
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1"==mode:
			print "XMAS_SONG ON"

			XMAS_BGM = "xmas.mp3"

			if app.IsExistFile("BGM/" + XMAS_BGM)==1:
				if musicInfo.fieldMusic != "":
					snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

				musicInfo.fieldMusic=XMAS_BGM
				snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		else:
			print "XMAS_SONG OFF"

			if musicInfo.fieldMusic != "":
				snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

			musicInfo.fieldMusic=musicInfo.METIN2THEMA
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def __RestartDialog_Close(self):
		self.interface.CloseRestartDialog()

	def __Console_Enable(self):
		constInfo.CONSOLE_ENABLE = TRUE
		self.consoleEnable = TRUE
		app.EnableSpecialCameraMode()
		ui.EnablePaste(TRUE)

	## PrivateShop
	def __PrivateShop_Open(self, isAHShop = 0):
		# import chat
		# chat.AppendChat(chat.CHAT_TYPE_INFO,"isAHShop %s" % (isAHShop))
		self.interface.OpenPrivateShopInputNameDialog(int(isAHShop))

	def BINARY_PrivateShop_Appear(self, vid, text, fontColor, fontName):
		self.interface.AppearPrivateShop(vid, text, fontColor, fontName)

	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)

	## DayMode
	def __PRESERVE_DayMode_Update(self, mode):
		if "light"==mode:
			background.SetEnvironmentData(0)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)

	def __DayMode_Update(self, mode):
		if "light"==mode:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

	def __DayMode_OnCompleteChangeToLight(self):
		background.SetEnvironmentData(0)
		self.curtain.FadeIn()

	def __DayMode_OnCompleteChangeToDark(self):
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)
		self.curtain.FadeIn()

	## XMasBoom
	def __XMasBoom_Update(self):

		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return

		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

		if app.GetTime() - self.startTimeXMasBoom > boomTime:

			self.indexXMasBoom += 1

			for i in xrange(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = cw_player.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)

		snd.PlaySound3D(x+randX, -y+randY, z, "sound/common/etc/salute.mp3")

	def __PartyRequestQuestion(self, vid):
		vid = int(vid)
		partyRequestQuestionDialog = uiCommon.QuestionDialog()
		partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
		partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
		partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
		partyRequestQuestionDialog.SetAcceptEvent(lambda arg=TRUE: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.SetCancelEvent(lambda arg=FALSE: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.Open()
		partyRequestQuestionDialog.vid = vid
		self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			net.SendChatPacket("/party_request_accept " + str(vid))
		else:
			net.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

	def __EnableTestServerFlag(self):
		app.EnableTestServerFlag()

	def __InGameShop_Show(self, url):
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.interface.OpenWebWindow(url)
			
	def RefreshChannel(self, ch):
		constInfo.gChannel = int(ch)
		
	def RefreshMap(self, map):
		constInfo.gMap = int(map)

	# WEDDING
	def __LoginLover(self, status):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover(int(status))

	def __LogoutLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverDivorce(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
		if self.affectShower:
			self.affectShower.ClearLoverState()

	def AppendPortalInfo(self, type):
		if self.affectShower:
			self.affectShower.SetDungeonInfo()
			self.affectShower.ShowDungeonInfo(type)

	def __PlayMusic(self, flag, filename):
		flag = int(flag)
		if flag:
			snd.FadeOutAllMusic()
			musicInfo.SaveLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + filename)
		else:
			snd.FadeOutAllMusic()
			musicInfo.LoadLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)
			
	def Auktionshausdialog(self, itemslot):
		self.interface._AuktionshausdialogWindow(itemslot)
		
	def Auktionshausbutton(self,qid):
		constInfo.AUKTIONSHAUSBUTTON = int(qid)

	def Auktionshaus(self):
		self.interface.AuktionshausWindow.Open()
		
	def AuktionshausSetMoney(self, money):
		self.interface.AuktionshausWindow.SetMoney(money)
		
	def AuktionshausSetLager(self, lager):
		self.interface.AuktionshausWindow.SetLager(lager)
		
	def AuktionshausSetAvgPrice(self, price, pricetype):
		self.interface.AuktionshausdialogWindow.SetAvgPrice(price,pricetype)
		
	def AuktionshausClearAHItems(self):
		# self.SendSystemChat('clear')
		constInfo.AUKTIONSHAUSITEMS = []
		
	def SendSystemChat(self, text):
		chat.AppendChat(chat.CHAT_TYPE_INFO, "<System>: "+str(text))
		
	def AuktionshausAddAHItem(self,auctionId, playerName, vnum, grade, count, price,socket,attr,pricetype,ascendance, influence, uniqueFlag, unidentified, ascendanceSlots):
		self.AHType = 0
		self.AddAHitems(auctionId, playerName, vnum, grade, count, price,socket,attr,pricetype,ascendance,ascendanceSlots, influence, uniqueFlag, unidentified)
		# self.SendSystemChat("append items: "+auctionId+" "+playerName+" "+vnum+" "+grade+" "+count+" "+price+" "+socket+" "+attr)
		
	def AuktionshausAddAHSellingItem(self,auctionId, vnum, grade, count, price,socket,attr,pricetype,ascendance, influence, uniqueFlag, unidentified, ascendanceSlots):
		self.AHType = 1
		self.AddAHitems(auctionId, "Ich", vnum, grade, count, price,socket,attr,pricetype,ascendance,ascendanceSlots, influence, uniqueFlag, unidentified)
		
	def AuktionshausAddAHHistory(self,auctionId, vnum, grade, count, price,socket,attr,pricetype,ascendance, influence, uniqueFlag, unidentified, ascendanceSlots):
		self.AHType = 2
		# chat.AppendChat(chat.CHAT_TYPE_INFO, "%s %s %s %s %s %s %s %s %s %s" % (auctionId, vnum, grade, count, price,socket,attr,pricetype,ascendance,ascendanceSlots))
		self.AddAHitems(auctionId, "Ich", vnum, grade, count, price,socket,attr,pricetype,ascendance,ascendanceSlots, influence, uniqueFlag, unidentified)
		
	def AuktionshausRemoveAHSuccess(self):
		self.SendSystemChat('Item wurde aus dem Verkauf genommen.')
	
	def AuktionhouseRemoveItemComplete(self):
		self.interface.AuktionshausWindow.RemoveItemComplete()
		
	def AuktionshausCMD(self):
		net.SendQuestInputStringPacket(str(constInfo.AUKTIONSHAUSCMD))
		constInfo.AUKTIONSHAUSCMD = "NULL#"
		
	def AddAHitems(self,auctionId, playerName, vnum, grade, count, price,socket,attr,pricetype,ascendance,ascendanceSlots, influence, uniqueFlag, unidentified):
		socket = socket.split(":")
		attr = attr.split(":")
		ascendanceSlots = ascendanceSlots.split(":")
		constInfo.AUKTIONSHAUSITEMS.append([int(auctionId),playerName,int(vnum),int(grade),int(count),int(price),int(socket[0]),int(socket[1]),int(socket[2]),int(attr[0]),int(attr[1]),int(attr[2]),int(attr[3]),int(attr[4]),int(attr[5]),int(attr[6]),int(attr[7]),int(attr[8]),int(attr[9]),int(attr[10]),int(attr[11]),int(attr[12]),int(attr[13]),int(attr[14]),int(attr[15]),int(attr[16]),int(attr[17]),int(pricetype),int(socket[3]),int(ascendance),int(socket[4]),int(socket[5]), int(ascendanceSlots[0]),int(ascendanceSlots[1]),int(ascendanceSlots[2]),int(ascendanceSlots[3]),int(ascendanceSlots[4]),int(ascendanceSlots[5]),int(ascendanceSlots[6]),int(ascendanceSlots[7]),int(ascendanceSlots[8]),int(ascendanceSlots[9]),int(ascendanceSlots[10]),int(ascendanceSlots[11]),int(ascendanceSlots[12]),int(ascendanceSlots[13]),int(ascendanceSlots[14]),int(ascendanceSlots[15]),int(ascendanceSlots[16]),int(ascendanceSlots[17]),int(ascendanceSlots[18]),int(ascendanceSlots[19]),int(ascendanceSlots[20]),int(ascendanceSlots[21]),int(ascendanceSlots[22]),int(ascendanceSlots[23]),int(ascendanceSlots[24]),int(ascendanceSlots[25]),int(ascendanceSlots[26]),int(ascendanceSlots[27]),int(ascendanceSlots[28]),int(ascendanceSlots[29]), int(influence),int(uniqueFlag), int(socket[6]), int(socket[7]), int(socket[8]), int(socket[9]), int(socket[10]), int(unidentified)])
		
	def AuktionshausLoadAHSuccess(self):
		# self.SendSystemChat('success')
		items = constInfo.AUKTIONSHAUSITEMS
		if not items:
			self.interface.AuktionshausWindow.HideAllItemBox()
			self.SendSystemChat(localeInfo.HC_NO_ITEMS)
			return
		self.interface.AuktionshausWindow.scrollbar.SetPos(0)
		self.interface.AuktionshausWindow.LoadItems(0,self.AHType)
		# for i in range(len(items)):
			# self.SendSystemChat("IN: "+str(items[i]))
		## FILL FUNCTION

	def AHNothingFound(self):
		self.interface.AuktionshausWindow.HideAllItemBox()
		self.SendSystemChat(localeInfo.HC_NO_ITEMS)

	# END_OF_WEDDING
	def CommandOpenUserpanel(self, qid):
		constInfo.LOAD_USERPANEL = int(qid)
		
	def CommandSetCSQid(self,qid):
		constInfo.CSQID = int(qid)
	
	def CommandHasGuildSafebox(self, c):
		constInfo.HasGuildSafebox = int(c)
	
	def	CommandSetCSDisable(self,flag):
		constInfo.CSDisable = int(flag)

	def CommandCwDaytime(self, qid):
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.RegisterEnvironmentData(2, constInfo.ENVIRONMENT_CAPE)
		background.SetEnvironmentData(int(qid))
		
	def CommandDsEnvironment(self, id):
		if int(id) == 0:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif int(id) == 1:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)
		else:
			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_DICT[int(id)])
			background.SetEnvironmentData(1)
		

	def CommandSetTexture(self, ulIndex, szFileName, fuScale, fvScale, fuOffset, fvOffset, bSplat, usBegin, usEnd):
		fileName = "d:\\ymir work\\terrainmaps\\"+ szFileName
		background.SetTexture(int(ulIndex), fileName, float(fuScale), float(fvScale), float(fuOffset), float(fvOffset), int(bSplat), int(usBegin), int(usEnd))

	def CommandReplaceTextureByIDX(self, destIdx, sourceIdx):
		background.ReplaceTextureByIDX(int(destIdx), int(sourceIdx))

	def CommandDSTextureSet(self, str):
		background.SetTextureSet(str)

	def CommandShuffleTextures(self):
		background.ShuffleTextures()
	
	def CommandDSSetWaterTexture(self, str):
		waterTexturePathList = [
								"d:/ymir Work/special/water/",
								"d:/ymir Work/special/lava/",
								"d:/ymir Work/special/green_water/"
								]
		background.SetWaterTexture(waterTexturePathList[int(str)])
		
	def CommandDsSnow(self, id):
		background.EnableSnow(int(id))
		
	def GetDayTime(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, "test")
		background.EnableNight(1)

	def __CheckTeamOnline(self, qid):
		constInfo.LOAD_TEAMLIST = int(qid)
		
	def __ReloadPanel(self, qid):
		constInfo.LOAD_GUILDSTORAGE = int(qid)
		
	def AppendItemVnumList(self, vnum):
		constInfo.ItemVnumList.append(vnum)
	
	def AppendMountSkinList(self, vnum):
		constInfo.mountSkinList.append(vnum)

	def SearchItem(self, term):
		vnumList = constInfo.ItemVnumList
		vnumList.sort()
		for vnum in vnumList:
			if vnum:
				name = item.GetNameByVnum(int(vnum))
				if term.lower() in name.lower():
					chat.AppendChat(chat.CHAT_TYPE_INFO,"%s: %d" % (name, vnum))
				

	def __PressF5(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.HotkeyTeleport(63)
	
	def __PressF8(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.HotkeyTeleport(66)
		else:
			if self.hideAllWindows:
				self.interface.ShowAllWindowsNew()
				self.interface.wndChat.Show()
				self.affectShower.Show()
				self.hideAllWindows = 0
			else:
				self.interface.HideAllWindowsNew()
				self.interface.wndChat.Hide()
				self.affectShower.Hide()
				self.hideAllWindows = 1
		
	def __PressF9(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.HotkeyTeleport(67)
		else:
			net.SendChatPacket("/open_safebox")
			
	def __PressF10(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.HotkeyTeleport(68)
			
	def __uiSwitchBot(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.HotkeyTeleport(64)
		else:
			self.interface.ToggleSwitchbot()

	def __OpenAttrBoard(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.HotkeyTeleport(65)
		else:
			if self.interface.wndCharacter:
				self.interface.wndCharacter.ToggleAttrBoard()
			
	def __LoadSafebox(self, qid):
		constInfo.SAFEBOX_QID = int(qid)
		
	# CW-Levelguide
	
	def __cwLevelGuide(self, data):
		LG_DATA = data.split("|")
		chat.AppendWhisper(chat.WHISPER_TYPE_CHAT, LG_DATA[0],LG_DATA[0] + " : " + str(GetLGInfo(int(LG_DATA[1]))))
		self.interface.RecvWhisper(LG_DATA[0])

	# END_OF_CW_LEVELGUIDE
	
	def __UpdatePetName(self, name, vnum):
		constInfo.PET_NAME = name
		constInfo.PET_VNUM = int(vnum)
	# RANK_SYSTEM
	def __LoadRank(self, qid):
		constInfo.LOAD_RANK = int(qid)

	def GetInputOn(self):
		constInfo.INPUT_IGNORE = 1

	def GetInputOff(self):
		constInfo.INPUT_IGNORE = 0
			
	def GetInputValue(self):
		net.SendQuestInputStringPacket(str(constInfo.VID))
		
	def GetRankInfo(self, data):
		rank_data = data.split("|")
		constInfo.RANK_NAME = str(rank_data[0])
		constInfo.RANK_GRADE = str(rank_data[1])
		constInfo.RANK_MONSTER = int(rank_data[2])
		constInfo.RANK_METIN = int(rank_data[3])
		constInfo.RANK_DRAGON = int(rank_data[4])
		constInfo.RANK_PLAYER = int(rank_data[5])
		constInfo.RANK_DAILY = int(rank_data[6])
		constInfo.RANK_JOB = int(rank_data[7])
		
	def HotkeyTeleport(self, key):
		import pickle
		map_id = 0
		channel = 0
		with open("%s\Celestial World\config\\warp_menu_hotkeys.cw" % (os.getenv('APPDATA'))) as f:
			while True:
				try:
					ln = pickle.load(f)
					if ln["hotkey"] == key:
						map_id = int(ln["map_id"])
						channel = int(ln["channel"])
				except EOFError:
					break
		
		if map_id > 0:
			if self.interface.wndTeleportMenu:
				self.interface.wndTeleportMenu.Warp(map_id,channel)
		
					
		

	#END_OF_RANK_SYSTEM			
	# TEAM_LIST
	def __TeamLogin(self, name, status):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogin(0, name, status)

	def __TeamLogout(self, name):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogout(0, name)
	# END_OF_TEAM_LIST
	
	def OpenKillerInfo(self):		
		if not self.DeathCauseDlg:
			self.DeathCauseDlg = uiDeathCause.DeathCauseDialog()

		self.DeathCauseDlg.Show(cw_player.GetKillerName(),cw_player.GetKillerDamage(),cw_player.GetKillerDamageType(),cw_player.GetKillerSkillVnum(),cw_player.IsKillerCrit(),cw_player.IsKillerPene(),cw_player.GetKillerLevel(),cw_player.GetKillerJob())
		
	def SetDungeonPointsPercentage(self, Percentage):
		pass
		
	def ClearMobInfo(self):
		if not self.interface.wndMobinfo:
			self.interface.InitMobInfoWindow()

		if self.interface.wndMobinfo:
			self.interface.wndMobinfo.Clear()
		
	def OpenMobInfo(self, mobVnum, bLevel, race, diff, mapid):		
		if self.interface.wndMobinfo:
			self.interface.OpenMobInfo(mobVnum, cw_player.GetMobInfoHP(), bLevel, race, diff, mapid)
	
	def AppendMobInfoDrops(self, itemVnum):
		if self.interface.wndMobinfo:
			if not itemVnum in self.interface.wndMobinfo.itemListVnums:
				self.interface.wndMobinfo.itemListVnums.append(itemVnum)
				
				
	def AppendItemList(self, itemVnum):
		if self.interface.wndTeleportMenu:
			if not itemVnum in self.interface.wndTeleportMenu.itemListVnums:
				self.interface.wndTeleportMenu.itemListVnums.append(itemVnum)		
				self.interface.wndTeleportMenu.AppendToItemListStack(itemVnum)		
				self.interface.wndTeleportMenu.itemList.AppendItem(uiTeleport.MonsterItem(item.GetNameByVnum(itemVnum),itemVnum,0xffFFFFFF,True))
			
			if self.interface.wndTeleportMenu.itemList.GetItemCount() <= 8:
				self.interface.wndTeleportMenu.itemListScrollbar.Hide()
			else:
				self.interface.wndTeleportMenu.itemListScrollbar.Show()
				self.interface.wndTeleportMenu.itemListScrollbar.SetMiddleBarSize(float(self.interface.wndTeleportMenu.itemList.GetViewItemCount())/self.interface.wndTeleportMenu.itemList.GetItemCount())
	
	def ClearItemInfo(self):
		if not self.interface.wndItemInfo:
			self.interface.InitItemInfo()
		self.interface.wndItemInfo.Clear()
		
	def AppendItemInfoMonster(self, vnum):
		if self.interface.wndItemInfo:
			if not vnum in self.interface.wndItemInfo.monsterListVnums:
				self.interface.wndItemInfo.monsterListVnums.append(vnum)
				
	def AppendItemInfoAltDrop(self, rank, minLevel, maxLevel):
		if self.interface.wndItemInfo:
			self.interface.wndItemInfo.altDropList.append([rank,minLevel,maxLevel])
			
	def AppendItemInfoCrafters(self, vnum):
		if self.interface.wndItemInfo:
			self.interface.wndItemInfo.crafterList.append(vnum)
			
	def AppendSpecialItemDrop(self, vnum):
		if self.interface.wndItemInfo:
			if not vnum in self.interface.wndItemInfo.specialItemDropList:
				self.interface.wndItemInfo.specialItemDropList.append(vnum)
				
	def AppendItemInfoChests(self, vnum):
		if self.interface.wndItemInfo:
			if not vnum in self.interface.wndItemInfo.chestList:
				self.interface.wndItemInfo.chestList.append(vnum)
				
	def AppendItemInfoRefinedFrom(self, vnum):
		if self.interface.wndItemInfo:
			self.interface.wndItemInfo.refinedFrom = vnum
				
	def OpenItemInfo(self, itemVnum, canRefine):
		if self.interface.wndItemInfo:
			self.interface.OpenItemInfo(itemVnum,canRefine)
	
	def ClearRefineSystemWindow(self):
		if self.interface.wndRefineInfo:
			self.interface.wndRefineInfo.ClearWindow()
			
	def ClearRefineInfo(self):
		if self.interface.wndRefineInfo:
			self.interface.wndRefineInfo.ClearRefineInfo()
			
	def AppendRefineInfoMaterials(self, vnum, count):
		if self.interface.wndRefineInfo:
			self.interface.wndRefineInfo.AppendRefineMaterials(vnum,count)
			
	def AppendRefineItem(self, vnum, result, cost, costType, requirementType, requirement):
		if self.interface.wndRefineInfo:
			self.interface.wndRefineInfo.AppendRefineItem(vnum, result, cost, costType, requirementType, requirement)
		
	def ClearBlockDropList(self):
		self.interface.ClearBlockDropList()
		
	def AppendToBlockDropList(self, vnum):
		self.interface.AppendToBlockDropList(vnum)
		
	def OpenBlockDropList(self):
		self.interface.OpenBlockDropList()

	def RefreshBlockDropListItem(self, vnum):
		self.interface.RefreshBlockDropListItem(int(vnum))
		
	def OnMsgLogin(self, name, msg_id):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogin(int(msg_id), name, 0)
			
	def OnMsgLogout(self, name, msg_id):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogout(int(msg_id), name)
	
	def AppendRiftstoneHyperlink(self, link, name, level, vnum):
		if vnum == 85719:
			keyRank = (level-(level%50)) / 50
			if level%50 == 0:
				keyRank = keyRank - 1
			ime.PasteString("|cfff1e6c0|H%s|h[%s (%s %d, %s %d)]|h|r" % (link,name,localeInfo.RIFTSTONE_LEVEL,level-(keyRank*50),localeInfo.RIFTSTONE_RANK,keyRank+1))
		else:
			ime.PasteString("|cfff1e6c0|H%s|h[%s (%s %d)]|h|r" % (link,name,localeInfo.RIFTSTONE_LEVEL,level))
			
	def OpenAmuletFusion(self):	
		self.interface.OpenAmuletFusionWindow()

	def AddAmuletFusionResultSlot(self, vnum, soulLevel, slot1, slot2, slot3):
		self.interface.AddAmuletFusionResultSlot(int(vnum), int(soulLevel), int(slot1), int(slot2), int(slot3))

	def ClearFragmentPortalDialog(self):
		self.interface.ClearFragmentPortalDialog()

	def FragmentPortalDialogAppendPerk(self, slotID, perkID, level):
		self.interface.FragmentPortalDialogAppendPerk(int(slotID), int(perkID), int(level))

	def OpenFragmentPortalDialog(self, fragmentID, perkPoints):
		self.interface.OpenFragmentPortalDialog(int(fragmentID), int(perkPoints))

	def ClearGameEventDialog(self):
		self.interface.ClearGameEventDialog()

	def OpenGameEventDialog(self, eventID, level, xp, xpRequirement, nextReset, openDialog):
		self.interface.OpenGameEventDialog(int(eventID), int(level), int(xp), int(xpRequirement), int(nextReset), int(openDialog))

	def UpdateGameEventDialog(self, level, xp, xpRequirement):
		self.interface.UpdateGameEventDialog(int(level), int(xp), int(xpRequirement))

	def AppendChallengeToGameEventDialog(self, challengeID, challenge, goal, xp, rewardVnum, rewardCount):
		self.interface.AppendChallengeToGameEventDialog(int(challengeID), int(challenge), int(goal), int(xp), int(rewardVnum), int(rewardCount))

	def AppendLevelRewardToGameEventDialog(self, level, type, isClaimed, values): 
		self.interface.AppendLevelRewardToGameEventDialog(int(level), int(type), int(isClaimed), values)

	def OpenCraftPowerstone(self):
		if not self.dlgCraftPowerstone:
			import uiCraftPowerstone
			self.dlgCraftPowerstone = uiCraftPowerstone.CraftPowerstoneDialog()
		self.dlgCraftPowerstone.Show()
		
	def OpenRuneSystemWindow(self):
		import uiRuneSystem
		self.runeSystemDialog = uiRuneSystem.RuneSystemWindow()
		self.runeSystemDialog.Show()

	def AHItemBuy(self,auction_id,vnum,pos,price,pricetype):
		import shop
		metinSlot = []
		for i in xrange(cw_player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(int(pos), i))
	
		attrSlot = []
		for i in xrange(cw_player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(int(pos), i))
		
		item.SelectItem(int(vnum))
		self.__SetItemTitle(int(vnum), metinSlot, attrSlot, shop.GetItemGrade(int(pos)), item.GetItemType(), item.GetItemSubType())
		self.confirmAHBuyDialog.SetText2(localeInfo.AH_SHOP_CONFIRM3 % (localeInfo.NumberToMoneyString(int(price),shop.GetItemPricetype(int(pos)))))
		self.confirmAHBuyDialog.Show()
		self.ahShopVnum = int(vnum)
		self.ahShopAuctionID = int(auction_id)
		
		
	def AHItemBuyConfirm(self):
		import event
		constInfo.AUKTIONSHAUSCMD = "LINK_BUY#"+str(self.ahShopAuctionID)
		event.QuestButtonClick(int(constInfo.AUKTIONSHAUSBUTTON))
		self.confirmAHBuyDialog.Hide()

	def __SetNormalItemTitle(self,grade,itemType,metinSlot,itemVnum,itemSubType = 0):
		if itemType == item.ITEM_TYPE_AMULET or itemType == item.ITEM_TYPE_PET_TALISMAN:
			if grade>0:
				itemName = "%s+%s (%s)" % (item.GetItemName(),metinSlot[3],GetGradeName(grade))
			else:
				itemName = "%s+%s" % (item.GetItemName(),metinSlot[3])
		elif itemType == item.ITEM_TYPE_MOUNT_EQUIPMENT:
			if grade>0:
				itemName = "%s+%s (%s)" % (item.GetItemName(),metinSlot[0],GetGradeName(grade))
			else:
				itemName = "%s+%s" % (item.GetItemName(),metinSlot[0])
		elif itemType == item.ITEM_TYPE_RUNE and itemSubType == item.RUNE_SPIRIT:
			if metinSlot[1] == 1337:
				if grade>0:
					itemName = "%s %s+%s (%s)" % (localeInfo.TOOLTIP_LEGENDARY_SPIRIT_RUNE,item.GetItemName(),metinSlot[0],GetGradeName(grade))
				else:
					itemName = "%s %s+%s" % (localeInfo.TOOLTIP_LEGENDARY_SPIRIT_RUNE,item.GetItemName())
			else:
				if grade>0:
					itemName = "%s+%s (%s)" % (item.GetItemName(),metinSlot[0],GetGradeName(grade))
				else:
					itemName = "%s+%s" % (item.GetItemName(),metinSlot[0])
		elif constInfo.IS_AUTO_POTION_HPSP(itemVnum):
			itemName = item.GetItemName()
		else:
			if grade>0:
				itemName = "%s (%s)" % (item.GetItemName(),GetGradeName(grade))
			else:
				itemName = item.GetItemName()
		
		self.confirmAHBuyDialog.SetText1(localeInfo.AH_SHOP_CONFIRM2 % (itemName))

	def __SetSpecialItemTitle(self,itemType,metinSlot,itemSubType = 0):
		if itemType == item.ITEM_TYPE_AMULET or itemType == item.ITEM_TYPE_PET_TALISMAN:
			itemName = "%s+%s" %(item.GetItemName(),metinSlot[3])
		elif itemType == item.ITEM_TYPE_MOUNT_EQUIPMENT:
			itemName = "%s+%s" %(item.GetItemName(),metinSlot[0])	
		elif itemType == item.ITEM_TYPE_RUNE and itemSubType == item.RUNE_SPIRIT:
			if metinSlot[1] == 1337:
				itemName = "%s %s+%s" %(localeInfo.TOOLTIP_LEGENDARY_SPIRIT_RUNE,item.GetItemName(),metinSlot[0])
			else:
				itemName = "%s+%s" % (item.GetItemName(),metinSlot[0])			
		else:
			itemName = item.GetItemName()
		
		self.confirmAHBuyDialog.SetText1(localeInfo.AH_SHOP_CONFIRM2 % (itemName))

	def __SetPetSkinItemTitle(self, petskin):
		item.SelectItem(petskin)
		itemName = item.GetItemName()
		itemName+= " Skin"
		self.confirmAHBuyDialog.SetText1(localeInfo.AH_SHOP_CONFIRM2 % (itemName))		
		
	def __SetPolymorphItemTitle(self, monsterVnum):
		if localeInfo.IsVIETNAM():
			itemName =item.GetItemName()
			itemName+=" "
			itemName+=nonplayer.GetMonsterName(monsterVnum)
		else:
			itemName =nonplayer.GetMonsterName(monsterVnum)
			itemName+=" "
			itemName+=item.GetItemName()
		self.confirmAHBuyDialog.SetText(localeInfo.AH_SHOP_CONFIRM2 % (itemName))
	
	def __IsAttr(self, attrSlot):
		if not attrSlot:
			return FALSE

		for i in xrange(cw_player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			if 0 != type:
				return TRUE

		return FALSE
		
	def __SetItemTitle(self, itemVnum, metinSlot, attrSlot, grade, itemType = 0, itemSubType = 0):			
		if itemVnum >= 70103 and itemVnum <= 70106:
			self.__SetPolymorphItemTitle(metinSlot[0])
		elif itemVnum==85477 and metinSlot[0]>1:
			self.__SetPetSkinItemTitle(metinSlot[0])
		else:
			if self.__IsAttr(attrSlot) and grade == 0:
				self.__SetSpecialItemTitle(itemType,metinSlot,itemSubType)
				return
			if 	itemVnum==85719:
				keyRank = (metinSlot[0]-(metinSlot[0]%50)) / 50 
				if metinSlot[0]%50 == 0:
					keyRank = keyRank - 1
				itemName = "%s (%s %s, %s %s)" % (item.GetItemName(),localeInfo.RIFTSTONE_LEVEL,str(metinSlot[0]-keyRank*50),localeInfo.RIFTSTONE_RANK,str(keyRank+1))
				self.confirmAHBuyDialog.SetText1(localeInfo.AH_SHOP_CONFIRM2 % (itemName))
				return
			if itemVnum==85593 or itemVnum==85555 or itemVnum==85721 or itemVnum==85727 or itemVnum == 86284 or itemVnum == 86489:
				itemName = "%s (%s %s)" % (item.GetItemName(),localeInfo.RIFTSTONE_LEVEL,str(metinSlot[0]))
				self.confirmAHBuyDialog.SetText1(localeInfo.AH_SHOP_CONFIRM2 % (itemName))
				return
			if itemVnum==85627:
				itemName = "%s (%s %s)" % (item.GetItemName(),localeInfo.TOOLTIP_PARGONSOULD_LEVEL,str(metinSlot[3]))
				self.confirmAHBuyDialog.SetText1(localeInfo.AH_SHOP_CONFIRM2 % (itemName))
				return
			if itemVnum==85280:
				self.__SetSpecialItemTitle(itemType,metinSlot)
				return

			self.__SetNormalItemTitle(grade,itemType,metinSlot,itemVnum,itemSubType)
		
	
	def ClearAHLink(self):
		del self.ahLinkAttrSlot[:]
		del self.ahLinkMetinSlot[:]
		del self.ahLinkAscendanceSlot[:]
		self.ahLinkAuctionID = 0
		self.ahLinkPricetype = 0
		self.ahLinkAscendance = 0

	def AppendAHLinkAttrSlot(self,type,value):
		self.ahLinkAttrSlot.append((type, value))
		
	def AppendAHAscendanceSlot(self, id, tier, quality):
		self.ahLinkAscendanceSlot.append((id, tier, quality))
		
	def SetAHLinkAddInformations(self, itemIndex, pricetype, itemAscendance):
		self.ahLinkAuctionID = itemIndex
		self.ahLinkPricetype = pricetype
		self.ahLinkAscendance = itemAscendance
		
	def OpenAHLink(self, itemVnum, itemGrade, itemInfluence, itemUniqueFlag, itemUnidentified, sellName, itemCount, price):
		for i in xrange(cw_player.METIN_SOCKET_MAX_NUM):
			self.ahLinkMetinSlot.append(cw_player.GetAHLinkSocket(i))
			
		self.ahLinkDlg.toolTip.ClearToolTip()
		self.ahLinkDlg.toolTip.AddRefineItemData(itemVnum, self.ahLinkMetinSlot, self.ahLinkAttrSlot, itemGrade,0,self.ahLinkAscendance, self.ahLinkAscendanceSlot, itemInfluence, itemUniqueFlag, itemUnidentified)
		self.ahLinkDlg.Show(itemVnum, self.ahLinkMetinSlot , self.ahLinkAttrSlot, itemGrade, sellName, itemCount, price, self.ahLinkPricetype, self.ahLinkAuctionID , self.ahLinkAscendance, self.ahLinkAscendanceSlot, itemInfluence, itemUniqueFlag)
		
	def AppendChat(self,type,msg):
		new_msg = constInfo.ParseString(msg)	
		chat.AppendChat(type,new_msg)
		
	def SetPQTarget(self,target,mode):
		constInfo.SetPQTarget(target)
		constInfo.SetPQMode(mode)
		
	def ClearProphecy(self):
		self.interface.InitProphecyMenu()
		self.interface.wndProphecyMenu.Clear()
		
		
	def AppendProphecy(self, slotID, prophecyID, objectiveCount, targetCount, releasePrice, xp):
		if self.interface.wndProphecyMenu:
			# chat.AppendChat(chat.CHAT_TYPE_INFO,"%s %s %s %s %s %s" % (slotID, prophecyID, objectiveCount, targetCount, releasePrice, xp))
			self.interface.wndProphecyMenu.AppendProphecy(slotID, prophecyID, objectiveCount, targetCount, releasePrice, xp)
			
	def OpenProphecyMenu(self,showUI):
		if self.interface.wndProphecyMenu:
			self.interface.wndProphecyMenu.Show(showUI)
	
	def RefreshProphecy(self):
		if self.interface.wndProphecyMenu:
			self.interface.wndProphecyMenu.Refresh()
			
	def AppendProphecyItem(self, link, prophecyID):
		name = uiProphecy.GetProphecyName(prophecyID).strip()
		ime.PasteString("|cfff6c7e3|H%s|h[%s]|h|r" % (link,name))
		
	def __SetProphecyObjCount(self, slot, value):
		if self.interface.wndProphecyMenu:
			self.interface.wndProphecyMenu.UpdateProphecyItem(slot, value)
			
	def OpenRingSwitchDialog(self,invPos):
		if self.interface.wndSwitchRing:
			self.interface.wndSwitchRing.Show(int(invPos))
			
	def AddRingSwitchAttr(self,pos,type,value):
		if self.interface.wndSwitchRing:
			self.interface.wndSwitchRing.SetAttributeName(int(pos),int(type),int(value))
			
	def ClearRingSwitchDialog(self):
		if self.interface.wndSwitchRing:
			self.interface.wndSwitchRing.Clear()
			
	def ClearRingSwitchLists(self):
		if self.interface.wndSwitchRing:
			self.interface.wndSwitchRing.ClearLists()
	
	def UpdateRingSwitchSlot(self):
		if self.interface.wndSwitchRing:
			self.interface.wndSwitchRing.UpdateSlot()
			
	def OpenAmuletCraftDialog(self):
		if self.interface.wndAmuletCraft:
			self.interface.wndAmuletCraft.Show()
			
	def ClearAmuletCraftDialog(self):
		if self.interface.wndAmuletCraft:
			self.interface.wndAmuletCraft.Clear()
	
	def AppendAmuletCraftDialog(self,vnum,count):
		if self.interface.wndAmuletCraft:
			self.interface.wndAmuletCraft.AppendCoin(int(vnum),int(count))
		
	def ClearPresetMap(self):
		if not self.interface.wndPresetMap:
			self.interface.InitPresetMapDialog()
		self.interface.wndPresetMap.Clear()
		
	def SetPresetMapRitualCount(self, count):
		if self.interface.wndPresetMap:
			self.interface.wndPresetMap.SetRitualCount(int(count))
			
	def ClearPresetMapChallenge(self):
		if self.interface.wndPresetMap:
			self.interface.wndPresetMap.ClearChallengeDialog()
			
	def AppendPresetMapChallenge(self, island, curType, type1, type2, rank1, rank2):
		if self.interface.wndPresetMap:
			types = [int(type1), int(type2)]
			ranks = [int(rank1), int(rank2)]
			self.interface.wndPresetMap.AppendChallenge(int(island), int(curType), types, ranks)
			
	def AppendPresetMapChallengePortals(self, status):		
		if self.interface.wndPresetMap:
			self.interface.wndPresetMap.AppendChallengePortal(int(status))
			
	def AppendPresetMapField(self, type, preset, rank):
		if self.interface.wndPresetMap:
			self.interface.wndPresetMap.AppendField(int(type),int(preset),int(rank))
			
	def AppendPresetMapPortal(self, status):
		if self.interface.wndPresetMap:
			self.interface.wndPresetMap.AppendPortal(int(status))
			 
	def OpenPresetMap(self):
		if self.interface.wndPresetMap:
			self.interface.wndPresetMap.Show()
			
	def InitMountSkinWindow(self):
		if not self.interface.wndMountSkins:
			self.interface.InitMountSkinWindow()
		self.interface.wndMountSkins.Clear()
	
	def AppendMountSkin(self, vnum, is_favorite):
		if self.interface.wndMountSkins:
			self.interface.wndMountSkins.AppendMountSkin(int(vnum), int(is_favorite))
			
	# def OpenMountSkinWindow(self, skinVnum = 0, attrType = 0, attrValue = 0):
	def OpenMountSkinWindow(self, cell):
		if self.interface.wndMountSkins:
			# self.interface.wndMountSkins.Show(int(skinVnum), int(attrType), int(attrValue))
			self.interface.wndMountSkins.Show(int(cell))

	def AppendLocaleString(self, nId, chatType, args):
		args = args.split(",")
		for i in xrange(len(args)):
			if len(args[i]) > 5 and args[i][:5] == "#VNUM":
				args[i] = nonplayer.GetMonsterName(int( args[i][5:]))

		nId = int(nId)	
		if nId == 33:
			vid = int(args[1])
			args = [nonplayer.GetMonsterName(9000000 + int(args[2])), localeString.DIR_NAMES[int(args[0])]]
			textTail.RegisterChatTail(vid, localeString.GetLocaleString(nId, args))
		else:
			if nId == 77:
				args[0] = uiToolTip.ItemToolTip().GetAffectString(int(args[0]), int(args[1]))
				args.pop(1)

			chat.AppendChat(int(chatType), localeString.GetLocaleString(nId, args))

	def ClearCelestialPortalDialog(self):
		if not self.dlgCelestialPortal:
			self.dlgCelestialPortal = uiCelestialPortal.CelestialPortalDialog()
		self.dlgCelestialPortal.Clear()

	def CelestialPortalAppendGlobalAttributeToList(self, type, value):
		self.dlgCelestialPortal.AppendGlobalAttributeToList(int(type), int(value))

	def CelestialPortalAppendLocalAttributeToList(self, type, value):
		self.dlgCelestialPortal.AppendLocalAttributeToList(int(type), int(value))

	def CelestialPortalAppendRates(self, sExpRateLocal, sExpRateGlobal, sDropRateLocal, sDropRateGlobal, sBossDropRateLocal, sBossDropRateGlobal):
		self.dlgCelestialPortal.AppendRates(int(sExpRateLocal), int(sExpRateGlobal), int(sDropRateLocal), int(sDropRateGlobal), int(sBossDropRateLocal), int(sBossDropRateGlobal))

	def ShowCelestialPortalDialog(self, bPortalID, lMapIndex, bSpecialAttr):
		self.dlgCelestialPortal.Show(int(bPortalID), int(lMapIndex), int(bSpecialAttr))

	def ClearShopAttrWindow(self):
		if not self.interface.wndShopAttr:
			self.interface.InitShopAttrWindow()
		else:
			self.interface.wndShopAttr.Clear()
	
	def AppendShopAttr(self, type, value):
		if self.interface.wndShopAttr:
			self.interface.wndShopAttr.AppendShopAttr(type, value)

	def OpenShopAttrWindow(self, shop_vnum):
		if self.interface.wndShopAttr:
			self.interface.wndShopAttr.Open(shop_vnum)
	
	def CloseShopAttrWindow(self):
		if self.interface.wndShopAttr and self.interface.wndShopAttr.IsShow():
			self.interface.wndShopAttr.Hide()

	def AttrBoardRegister(self, pid, timestamp, name):
		self.interface.RegisterAttrBoard(int(pid), int(timestamp), name)

	def AttrBoardAppendPoint(self, pid, timestamp, point, value):
		self.interface.UpdateAttrBoardAttr(int(pid), int(timestamp), int(point), int(value))

	def ClearMailWindow(self):
		self.interface.ClearMailWindow()

	def AppendToMailList(self, name, title, mailID, flags, time):
		#chat.AppendChat(chat.CHAT_TYPE_INFO,"AppendToMailList: %s %s %d %d" % (name, title, int(mailID), int(time)))
		self.interface.AppendToMailList(name, title, int(mailID), int(flags), int(time))

	def RefreshMailWindow(self, sent):
		self.interface.RefreshMailWindow(int(sent))

	def LoadMail(self, mailID, name, title, msg, time):
		self.interface.LoadMail(int(mailID), name, title, msg, int(time))

	def LoadMailItem(self, mailID, vnum, count, grade, ascendance, influence, uniqueFlag, unidentified):
		self.interface.LoadMailItem(int(mailID), int(vnum), int(count), int(grade), int(ascendance), int(influence), int(uniqueFlag), int(unidentified))

	def LoadMailItemSocket(self, mailID, socket):
		self.interface.LoadMailItemSocket(int(mailID), int(socket))

	def LoadMailItemAttr(self, mailID, type, value):
		self.interface.LoadMailItemAttr(int(mailID), int(type), int(value))

	def LoadMailItemAscendanceSlot(self, mailID, id, tier, quality):
		self.interface.LoadMailItemAscendanceSlot(int(mailID), int(id), int(tier), int(quality))

	def ForceRefreshMailWindow(self, sent, unreadCount):
		self.interface.ForceRefreshMailWindow(int(sent), int(unreadCount))

	def MailLoginNotice(self, mails):
		if self.interface:
			self.interface.MailLoginNotice(int(mails))

	def MailSendSuccess(self, mailID):
		self.interface.MailSendSuccess(int(mailID))

	def ClearBountyHuntSetup(self, onlyBounties = False):
		if self.interface:
			self.interface.ClearBountyHuntSetup(onlyBounties)

	def OpenBountyHuntSetup(self):
		if self.interface:
			self.interface.OpenBountyHuntSetup()

	def AppendBountyHuntBounties(self, bountyType, target, addTarget, addTarget2, countGoal, count):
		if self.interface:
			self.interface.AppendBountyHuntBounties(int(bountyType), int(target), int(addTarget), int(addTarget2), int(countGoal), int(count))

	def AppendBountyHuntModToken(self, index, vnum):
		if self.interface:
			self.interface.AppendBountyHuntModToken(int(index), int(vnum))

	def AppendBountyHuntModTokenAttr(self, index, attrType, attrValue):
		if self.interface:
			self.interface.AppendBountyHuntModTokenAttr(int(index), int(attrType), int(attrValue))

	def SetBountyHuntInfo(self, reward, rewardCount, rerollPrice, status, flags, difficulty, maxDifficulty, playerFlags):
		if self.interface:
			self.interface.SetBountyHuntInfo(int(reward), int(rewardCount), int(rerollPrice), int(status), int (flags), int(difficulty), int(maxDifficulty), int(playerFlags))

	def BountyHuntSetupLoadBounties(self):
		if self.interface:
			self.interface.BountyHuntSetupLoadBounties()


	def BountyHuntIconShow(self, status = 1, name = ""):
		if self.affectShower:
			self.affectShower.SetBountyHuntImage(status, name)

	def BountyHuntIconAppendBounty(self, bountyType, target, addTarget, addTarget2, count, countGoal):
		if self.affectShower and self.affectShower.bountyHuntImage:
			self.affectShower.bountyHuntImage.AppendBounty(int(bountyType), int(target), int(addTarget), int(addTarget2), int(count), int(countGoal))

	def BountyHuntIconAppendReward(self, vnum, count, difficulty):
		if self.affectShower and self.affectShower.bountyHuntImage:
			self.affectShower.bountyHuntImage.BountyHuntIconAppendReward(int(vnum), int(count), int(difficulty))

	def ClearRewardWindow(self):
		if self.interface:
			self.interface.ClearRewardWindow()

	def RewardWindowAppendItem(self, vnum, count):
		if self.interface:
			self.interface.RewardWindowAppendItem(int(vnum), int(count))

	def OpenRewardWindow(self, gridX, gridY):
		if self.interface:
			self.interface.OpenRewardWindow(int(gridX), int(gridY))

	def RefreshTitleList(self):
		if self.interface:
			self.interface.RefreshTitleList()

	def SetOnlineStatus(self, status, message):
		if self.interface:
			self.interface.SetMessengerOnlineStatus(status, message)

	def ClearDungeonTask(self):
		self.interface.ClearDungeonTask()

	def AppendDungeonTask(self, taskID, target, count, countGoal, x, y):
		self.interface.AppendDungeonTask(taskID, target, count, countGoal, x, y)

	def SetupDungeonTask(self, dungeonID, remainingTime = 0, startTime = 0, finishTime = 0, flags = 0):
		self.interface.SetupDungeonTask(dungeonID, remainingTime, startTime, finishTime, flags)

	def UpdateDungeonTask(self, taskID, count):
		self.interface.UpdateDungeonTask(int(taskID), int(count))

	def EnableBigNotice(self):
		self.interface.MakeTipBoard()
	
	def DisableBigNotice(self):
		self.interface.bigBoard = None

	def ClearHighscoreWindow(self):
		self.interface.ClearHighscoreWindow()

	def AppendHighscore(self, name, charClass, score1, score2, score3):
		self.interface.AppendHighscore(name, charClass, score1, score2, score3)

	def OpenHighscore(self, id, difficulty, category, isParty, charClass, ownRank, ownScore1, ownScore2, ownScore3, page, maxPages):
		self.interface.OpenHighscore(id, difficulty, category, isParty, charClass, ownRank, ownScore1, ownScore2, ownScore3, page, maxPages)

	def OpenGameStatistic(self, id, charClass, ownRank, ownScore1, ownScore2, page, maxPages):
		self.interface.OpenGameStatistic(id, charClass, ownRank, ownScore1, ownScore2, page, maxPages)

	def UpdateServerInfo(self, channel):
		serverName = serverInfo.REGION_DICT[0][1]["name"]
		channelName = serverInfo.REGION_DICT[0][1]["channel"][int(channel)]["name"]
		net.SetServerInfo(("%s, %s " % (serverName, channelName)).strip())