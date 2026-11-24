# -*- coding: utf-8 -*-  
from Screens.Screen import Screen  
from Screens.MessageBox import MessageBox  
from Components.ActionMap import ActionMap  
from Components.Label import Label  
from Components.MenuList import MenuList  
from Components.PluginComponent import plugins  
from Plugins.Plugin import PluginDescriptor  
from Tools.Directories import resolveFilename, SCOPE_PLUGINS  
from enigma import eTimer  
import os  
import subprocess  
  
PLUGIN_NAME = "ARABY VU PANEL"  
VERSION = "1.0.0"  
  
class ArabyVUPanel(Screen):  
    skin = """  
    <screen name="ArabyVUPanel" position="center,center" size="1100,620"  
        title="ARABY VU PANEL" backgroundColor="#101010" flags="wfNoBorder">  
        <widget name="header" position="20,15" size="1060,70"  
            font="Regular;38" halign="center" valign="center"  
            foregroundColor="#D6AE45" backgroundColor="#101010" />  
        <widget name="subtitle" position="30,88" size="1040,38"  
            font="Regular;22" halign="center" valign="center"  
            foregroundColor="#FFFFFF" backgroundColor="#101010" />  
        <widget name="menu" position="70,150" size="960,340"  
            itemHeight="62" font="Regular;27"  
            foregroundColor="#FFFFFF" backgroundColor="#202020"  
            foregroundColorSelected="#101010" backgroundColorSelected="#D6AE45"  
            scrollbarMode="showOnDemand" />  
        <widget name="footer" position="30,520" size="1040,55"  
            font="Regular;20" halign="center" valign="center"  
            foregroundColor="#D6AE45" backgroundColor="#101010" />  
    </screen>  
    """  
  
    def __init__(self, session):  
        Screen.__init__(self, session)  
        self.session = session  
        self.arabic = True  
        self.setTitle(PLUGIN_NAME)  
        self["header"] = Label("ARABY VU PANEL  |  العربي فيو بانل")  
        self["subtitle"] = Label("Vu+ Zero 4K  •  OpenATV 8.x  •  v" + VERSION)  
        self["footer"] = Label("OK: اختيار   |   MENU: اللغة   |   EXIT: خروج")  
        self["menu"] = MenuList([])  
        self["actions"] = ActionMap(  
            ["OkCancelActions", "DirectionActions", "MenuActions"],  
            {  
                "ok": self.run_selected,  
                "cancel": self.close,  
                "menu": self.toggle_language,  
                "up": self["menu"].up,  
                "down": self["menu"].down,  
            }, -1  
        )  
        self.refresh_menu()  
  
    def refresh_menu(self):  
        if self.arabic:  
            self.items = [  
                ("معلومات الرسيفر  |  Receiver information", "info"),  
                ("إدارة الإضافات  |  Plugin manager", "plugins"),  
                ("تحديث قوائم النظام  |  Update package lists", "update"),  
                ("إعادة تشغيل الواجهة  |  Restart GUI", "restart"),  
                ("حول البانل  |  About", "about"),  
            ]  
            self["footer"].setText("OK: اختيار   |   MENU: English   |   EXIT: خروج")  
        else:  
            self.items = [  
                ("Receiver information  |  معلومات الرسيفر", "info"),  
                ("Plugin manager  |  إدارة الإضافات", "plugins"),  
                ("Update package lists  |  تحديث قوائم النظام", "update"),  
                ("Restart GUI  |  إعادة تشغيل الواجهة", "restart"),  
                ("About  |  حول البانل", "about"),  
            ]  
            self["footer"].setText("OK: Select   |   MENU: العربية   |   EXIT: Back")  
        self["menu"].setList([x[0] for x in self.items])  
  
    def toggle_language(self):  
        self.arabic = not self.arabic  
        self.refresh_menu()  
  
    def run_selected(self):  
        idx = self["menu"].getSelectionIndex()  
        if idx is None:  
            return  
        action = self.items[idx][1]  
        if action == "info":  
            self.show_info()  
        elif action == "plugins":  
            self.open_plugin_manager()  
        elif action == "update":  
            self.update_lists()  
        elif action == "restart":  
            self.confirm_restart()  
        elif action == "about":  
            self.session.open(  
                MessageBox,  
                "ARABY VU PANEL v%s\nVu+ Zero 4K / Enigma2 / OpenATV 8.x\n\n"  
                "A lightweight community panel. Use at your own risk."  
                % VERSION,  
                MessageBox.TYPE_INFO  
            )  
  
    def show_info(self):  
        def read(path, default="غير متاح"):  
            try:  
                with open(path, "r") as f:  
                    return f.read().strip()  
            except:  
                return default  
  
        model = read("/proc/stb/info/model")  
        image = read("/etc/image-version", "OpenATV (version file unavailable)")  
        try:  
            with open("/proc/uptime", "r") as f:  
                uptime = f.read().split(".")[0]  
            uptime = str(int(int(uptime) / 3600)) + " hours"  
        except:  
            uptime = "N/A"  
        msg = "Model: %s\nImage: %s\nUptime: %s\n\nPanel: %s" % (  
            model, image[:250], uptime, VERSION  
        )  
        self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)  
  
    def open_plugin_manager(self):  
        try:  
            from Screens.PluginBrowser import PluginBrowser  
            self.session.open(PluginBrowser)  
        except Exception as e:  
            self.session.open(  
                MessageBox, "Cannot open Plugin Manager:\n%s" % str(e),  
                MessageBox.TYPE_ERROR  
            )  
  
    def update_lists(self):  
        self.session.openWithCallback(  
            self.run_update,  
            MessageBox,  
            "Run 'opkg update' to refresh package lists?\\nThis requires internet and may take a few minutes.",  
            MessageBox.TYPE_YESNO,  
            title="ARABY VU PANEL"  
        )  
  
    def run_update(self, answer):  
        if not answer:  
            return  
        try:  
            from Screens.Console import Console  
            self.session.open(  
                Console,  
                title="ARABY VU PANEL - Package list update",  
                cmdlist=["opkg update"]  
            )  
        except Exception as e:  
            self.session.open(  
                MessageBox, "Could not start update:\\n%s" % str(e),  
                MessageBox.TYPE_ERROR  
            )  
  
    def confirm_restart(self):  
        self.session.openWithCallback(  
            self.restart_gui,  
            MessageBox,  
            "Restart Enigma2 GUI now? Any unsaved activity may be interrupted.",  
            MessageBox.TYPE_YESNO  
        )  
  
    def restart_gui(self, answer):  
        if answer:  
            try:  
                from Screens.Standby import TryQuitMainloop  
                self.session.open(TryQuitMainloop, 3)  
            except Exception as e:  
                self.session.open(MessageBox, str(e), MessageBox.TYPE_ERROR)  
  
  
def main(session, **kwargs):  
    session.open(ArabyVUPanel)  
  
  
def Plugins(**kwargs):  
    return [PluginDescriptor(  
        name=PLUGIN_NAME,  
        description="Arabic/English tools for Vu+ Zero 4K",  
        where=PluginDescriptor.WHERE_PLUGINMENU,  
        fnc=main  
    )]  
