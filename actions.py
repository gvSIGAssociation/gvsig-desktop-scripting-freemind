# encoding: utf-8

import gvsig
from gvsig import getResource

import thread
from java.io import File
from org.gvsig.andami import PluginsLocator
from org.gvsig.app import ApplicationLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.swing.api import ToolsSwingLocator

from addons.freemind.freemind import launchFreeMind

class FreeMindExtension(ScriptingExtension):
  def __init__(self):
    pass

  def canQueryByAction(self):
    return False

  def isEnabled(self,action=None):
    return True

  def isVisible(self,action=None):
    return True
    
  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "freemind-launch":
      thread.start_new_thread(launchFreeMind,tuple())
        
def selfRegister():
  application = ApplicationLocator.getManager()

  #
  # Registramos los iconos en el tema de iconos
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  icon = File(getResource(__file__,"images","freemind.png")).toURI().toURL()
  iconTheme.registerDefault("scripting.FreeMindExtension", "action", "freemind-launch", None, icon)

  #
  # Creamos la accion 
  actionManager = PluginsLocator.getActionInfoManager()
  extension = FreeMindExtension()
  
  action = actionManager.createAction(
    extension, 
    "freemind-launch", # Action name
    "FreeMind", # Text
    "freemind-launch", # Action command
    "freemind-launch", # Icon name
    None, # Accelerator
    650700600, # Position 
    "_Show_the_FreeMind" # Tooltip
  )
  action = actionManager.registerAction(action)
  application.addMenu(action, "tools/FreeMind")
