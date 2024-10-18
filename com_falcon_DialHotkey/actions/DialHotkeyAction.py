import os
import logging
from evdev import UInput, ecodes
from src.backend.PluginManager.ActionBase import ActionBase
from gi.repository import Gtk, Adw
from src.backend.DeckManagement.InputIdentifier import InputEvent, Input

class DialHotkeyAction(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.clockwise_hotkey = ""
        self.counterclockwise_hotkey = ""
        self.press_hotkey = ""

        # Initialize UInput with specified capabilities
        capabilities = {
            ecodes.EV_KEY: ecodes.keys.keys()
        }
        self.ui = UInput(capabilities)

        # Entry fields
        self.clockwise_hotkey_entry = Gtk.Entry()
        self.clockwise_hotkey_entry.set_placeholder_text("E.g., Ctrl+Alt+Del")
        self.clockwise_hotkey_entry.set_tooltip_text("Type the hotkey combination using '+' to separate keys.")

        self.counterclockwise_hotkey_entry = Gtk.Entry()
        self.counterclockwise_hotkey_entry.set_placeholder_text("E.g., Shift+F1")
        self.counterclockwise_hotkey_entry.set_tooltip_text("Type the hotkey combination using '+' to separate keys.")

        self.press_hotkey_entry = Gtk.Entry()
        self.press_hotkey_entry.set_placeholder_text("E.g., Ctrl+Shift+S")
        self.press_hotkey_entry.set_tooltip_text("Type the hotkey combination using '+' to separate keys.")

    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)
        self.load_hotkey_settings()
        self.connect_hotkey_entry_signals()
        self.logger.info("SimpleAction is ready and settings are loaded.")

    def get_config_rows(self) -> list:
        for entry in [self.clockwise_hotkey_entry, self.counterclockwise_hotkey_entry, self.press_hotkey_entry]:
            if entry.get_parent():
                entry.get_parent().remove(entry)

        config_rows = [
            Adw.ActionRow(title="Clockwise Hotkey", subtitle="Hotkey for clockwise turn"),
            Adw.ActionRow(title="Counterclockwise Hotkey", subtitle="Hotkey for counterclockwise turn"),
            Adw.ActionRow(title="Press Hotkey", subtitle="Hotkey for dial press")
        ]

        for row, entry in zip(config_rows, [self.clockwise_hotkey_entry, self.counterclockwise_hotkey_entry, self.press_hotkey_entry]):
            row.add_suffix(entry)

        return config_rows

    def connect_hotkey_entry_signals(self):
        for entry, hotkey_type in zip(
            [self.clockwise_hotkey_entry, self.counterclockwise_hotkey_entry, self.press_hotkey_entry],
            ["Clockwise Hotkey", "Counterclockwise Hotkey", "Press Hotkey"]
        ):
            entry.connect("changed", self.on_hotkey_text_changed, hotkey_type)

    def on_hotkey_text_changed(self, entry: Gtk.Entry, hotkey_type: str):
        value = entry.get_text()
        if self.validate_hotkey(value):
            # If valid, save the hotkey
            self.on_hotkey_change(entry, hotkey_type)
            entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)
            entry.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, None)
        else:
            # If invalid, show a warning icon
            entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, "dialog-warning")
            entry.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, "Invalid hotkey format")

    def validate_hotkey(self, hotkey: str) -> bool:
        if not hotkey:
            return True  # Allow empty hotkeys
        keys = hotkey.split('+')
        for key in keys:
            keycode = self.get_keycode(key.strip())
            if keycode is None:
                return False
        return True

    def on_hotkey_change(self, entry, hotkey_type):
        value = entry.get_text()
        settings = self.get_settings()

        if hotkey_type == "Clockwise Hotkey":
            self.clockwise_hotkey = value
            settings["clockwise_hotkey"] = value
        elif hotkey_type == "Counterclockwise Hotkey":
            self.counterclockwise_hotkey = value
            settings["counterclockwise_hotkey"] = value
        elif hotkey_type == "Press Hotkey":
            self.press_hotkey = value
            settings["press_hotkey"] = value

        self.set_settings(settings)
        self.logger.info(f"Updated {hotkey_type} to: {value}")

    def load_hotkey_settings(self):
        settings = self.get_settings()
        self.clockwise_hotkey = settings.get("clockwise_hotkey", "")
        self.counterclockwise_hotkey = settings.get("counterclockwise_hotkey", "")
        self.press_hotkey = settings.get("press_hotkey", "")

        self.clockwise_hotkey_entry.set_text(self.clockwise_hotkey)
        self.counterclockwise_hotkey_entry.set_text(self.counterclockwise_hotkey)
        self.press_hotkey_entry.set_text(self.press_hotkey)

        self.logger.info(f"Loaded hotkey settings: clockwise={self.clockwise_hotkey}, counterclockwise={self.counterclockwise_hotkey}, press={self.press_hotkey}")

    def event_callback(self, event: InputEvent, data: dict = None):
        if event == Input.Dial.Events.DOWN:
            if self.press_hotkey:
                self.trigger_hotkey(self.press_hotkey)
        elif event == Input.Dial.Events.TURN_CW:
            if self.clockwise_hotkey:
                self.trigger_hotkey(self.clockwise_hotkey)
        elif event == Input.Dial.Events.TURN_CCW:
            if self.counterclockwise_hotkey:
                self.trigger_hotkey(self.counterclockwise_hotkey)

    def trigger_hotkey(self, hotkey: str):
        if not hotkey:
            return
        self.logger.info(f"Triggering hotkey: {hotkey}")
        try:
            keys = hotkey.split('+')
            keycodes = []
            for key in keys:
                keycode = self.get_keycode(key.strip())
                if keycode is not None:
                    keycodes.append(keycode)
                else:
                    self.logger.warning(f"Invalid key in hotkey: {key}")
                    return  # Stop if any key is invalid

            # Press all keys
            for keycode in keycodes:
                self.ui.write(ecodes.EV_KEY, keycode, 1)
            self.ui.syn()

            # Release all keys in reverse order
            for keycode in reversed(keycodes):
                self.ui.write(ecodes.EV_KEY, keycode, 0)
            self.ui.syn()

            self.logger.info(f"Successfully triggered hotkey: {hotkey}")
        except Exception as e:
            self.logger.error(f"Failed to trigger hotkey {hotkey}: {e}")

    def get_keycode(self, key: str):
        key = key.strip().upper()
        keycode = None
        modifier_keys = {
            "CTRL": ecodes.KEY_LEFTCTRL,
            "ALT": ecodes.KEY_LEFTALT,
            "SHIFT": ecodes.KEY_LEFTSHIFT,
            "WIN": ecodes.KEY_LEFTMETA,
            "META": ecodes.KEY_LEFTMETA,
            "SUPER": ecodes.KEY_LEFTMETA,
        }

        function_keys = {f"F{i}": getattr(ecodes, f"KEY_F{i}", None) for i in range(1, 25)}

        special_keys = {
            "ENTER": ecodes.KEY_ENTER,
            "TAB": ecodes.KEY_TAB,
            "ESC": ecodes.KEY_ESC,
            "SPACE": ecodes.KEY_SPACE,
            "BACKSPACE": ecodes.KEY_BACKSPACE,
            "DELETE": ecodes.KEY_DELETE,
            "HOME": ecodes.KEY_HOME,
            "END": ecodes.KEY_END,
            "PAGEUP": ecodes.KEY_PAGEUP,
            "PAGEDOWN": ecodes.KEY_PAGEDOWN,
            "LEFT": ecodes.KEY_LEFT,
            "RIGHT": ecodes.KEY_RIGHT,
            "UP": ecodes.KEY_UP,
            "DOWN": ecodes.KEY_DOWN,
            "CAPSLOCK": ecodes.KEY_CAPSLOCK,
            "NUMLOCK": ecodes.KEY_NUMLOCK,
            "SCROLLLOCK": ecodes.KEY_SCROLLLOCK,
        }

        if key in modifier_keys:
            keycode = modifier_keys[key]
        elif key in function_keys:
            keycode = function_keys[key]
        elif key in special_keys:
            keycode = special_keys[key]
        elif len(key) == 1 and key.isalpha():
            keycode = getattr(ecodes, f"KEY_{key}", None)
        elif key.isdigit():
            keycode = getattr(ecodes, f"KEY_{key}", None)
        else:
            keycode = getattr(ecodes, f"KEY_{key}", None)

        if keycode is None:
            self.logger.warning(f"No keycode found for key '{key}'")
        return keycode

    def __del__(self):
        self.ui.close()
