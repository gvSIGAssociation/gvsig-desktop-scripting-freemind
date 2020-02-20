# encoding: utf-8

import gvsig
from gvsig import getResource

import thread
import os.path
import subprocess
import shutil

from java.lang import System
from java.io import File
from java.io import FileInputStream
from java.io import FileOutputStream
from java.util import Properties

from org.apache.commons.io import FileUtils
from org.gvsig.andami import PluginsLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.scripting.swing.api import ScriptingSwingLocator, JScriptingComposer
from org.gvsig.tools import ToolsLocator

import javax.swing.ImageIcon
import javax.imageio.ImageIO
from javax.swing import AbstractAction, Action
from org.gvsig.scripting import ScriptingLocator

def getDataFolder():
  return ScriptingLocator.getManager().getDataFolder("hexeditor").getAbsolutePath()

def launchFreeMind():
  pluginsManager = PluginsLocator.getManager()
  appfolder = pluginsManager.getApplicationFolder().getAbsolutePath()
  
  java = os.path.join( System.getProperties().getProperty("java.home"), "bin", "java")

  installDir = getResource(__file__, "app").replace("\\","/")

  CP = installDir+"/squirrel-sql.jar"
  for fname in os.listdir(installDir+"/lib"):
    CP += ":"+installDir+"/lib/"+fname
 
  cmd = [
    java,
    "-Xmx256M",
    "-Dfreemind.base.dir="+installDir,
    "-cp",CP,
    "freemind.main.FreeMindStarter"
  ]
  print cmd
  subprocess.call(cmd)


class FreeMindAction(AbstractAction):

  def __init__(self):
    AbstractAction.__init__(self,"FreeMind")
    self.putValue(Action.ACTION_COMMAND_KEY, "FreeMind");
    self.putValue(Action.SMALL_ICON, self.load_icon(getResource(__file__,"images","freemind.png")));
    self.putValue(Action.SHORT_DESCRIPTION, "FreeMind");

  def load_icon(self, afile):
    if not isinstance(afile,File):
      afile = File(str(afile))
    return javax.swing.ImageIcon(javax.imageio.ImageIO.read(afile))

  def actionPerformed(self,e):
    composer = e.getSource().getContext()
    thread.start_new_thread(launchFreeMind,tuple())

def selfRegister():
  i18nManager = ToolsLocator.getI18nManager()
  manager = ScriptingSwingLocator.getUIManager()
  action = FreeMindAction()
  #manager.addComposerTool(action)
  manager.addComposerMenu(i18nManager.getTranslation("Tools"),action)

def main(*args):
  thread.start_new_thread(launchFreeMind,tuple())
