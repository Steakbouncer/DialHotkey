# Import StreamController modules
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from .actions.DialHotkeyAction import DialHotkeyAction

class PluginTemplate(PluginBase):
    def __init__(self):
        super().__init__()

        # Register the dial hotkey action
        self.dial_hotkey_action_holder = ActionHolder(
        plugin_base=self,
        action_base=DialHotkeyAction,
        action_id="com_falcon_DialHotkey::DialHotkeyAction",
        action_name="Dial Hotkey Action"
        )
        self.add_action_holder(self.dial_hotkey_action_holder)

        # Register plugin
        self.register(
            plugin_name = "Dial Hotkey",
            github_repo = "https://github.com/Steakbouncer/DialHotkey",
            plugin_version = "1.0.0",
            app_version = "1.1.1-alpha"
        )