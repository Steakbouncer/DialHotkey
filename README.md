# DialHotkey
StreamController plugin for assigning hotkeys to Stream Deck dials

User Instructions for Assigning Hotkeys

The application allows you to assign custom hotkey combinations to specific dial actions: clockwise turn, counterclockwise turn, and dial press. You can define these hotkeys by typing them directly into the input fields.

How to Assign Hotkeys:
    Select the Entry Field:
        Click on the entry field corresponding to the action you want to assign a hotkey to:
            Clockwise Hotkey
            Counterclockwise Hotkey
            Press Hotkey
    Type the Hotkey Combination:
        Enter your desired hotkey combination using the following format:
            Use the '+' symbol to separate multiple keys.
            Example: Ctrl+Alt+Del

Hotkey Format Guidelines
    Modifiers First:
        Start with modifier keys if used (e.g., Ctrl, Alt, Shift, Win).
    Key Names:
        Use the exact key names as listed in the supported key list.
        Key names are not case-sensitive.
    No Spaces:
        Do not include spaces in the hotkey combination.
        Correct: Ctrl+Shift+A
        Incorrect: Ctrl + Shift + A

Input Validation
    The application will validate your input as you type.
    If the hotkey combination is valid:
        It will be saved automatically.
        No warning icons will be displayed.
    If the hotkey combination is invalid:
        A warning icon will appear in the entry field.
        Hover over the icon to see the error message.
        Correct the hotkey according to the guidelines.

Supported Key List

You can use the following keys in your hotkey combinations:
Modifier Keys

    Ctrl (Control)
    Alt (Alternate)
    Shift
    Win (Windows key)
        Also recognized as Meta or Super

Function Keys

    F1 to F24

Special Keys

    Enter
    Tab
    Esc (Escape)
    Space (Spacebar)
    Backspace
    Delete
    Home
    End
    PageUp
    PageDown
    Left (Left Arrow Key)
    Right (Right Arrow Key)
    Up (Up Arrow Key)
    Down (Down Arrow Key)
    CapsLock
    NumLock
    ScrollLock

Alphanumeric Keys

    Letters: A to Z
    Numbers: 0 to 9

Examples of Valid Hotkeys

    Ctrl+Alt+Del
    Shift+F5
    Ctrl+Shift+S
    Win+D
    Alt+F4
    Ctrl+C
    Ctrl+Shift+Esc
    Ctrl+Alt+Enter
    Ctrl+Shift+Left
    Shift+F13
    Ctrl+F24

Examples of Invalid Hotkeys

    Ctrl++A (Extra '+')
    Ctrl+Alt+UnknownKey (Unsupported key)
    Ctrl+Alt+ (Incomplete combination)
    Ctrl + Alt + Del (Contains spaces)

Using the Assigned Hotkeys
Dial Actions
    Clockwise Turn:
        When you turn the dial clockwise, the assigned "Clockwise Hotkey" will be triggered.
    Counterclockwise Turn:
        When you turn the dial counterclockwise, the assigned "Counterclockwise Hotkey" will be triggered.
    Dial Press:
        When you press the dial, the assigned "Press Hotkey" will be triggered.

Testing Your Hotkeys
    After assigning a hotkey, perform the corresponding dial action to test if the hotkey works as expected.
    Ensure that the application or system responds to the hotkey as intended.

Important Notes
System Reserved Hotkeys
    Some hotkeys are reserved by the operating system and may not be intercepted by the application.
        Avoid using system-reserved hotkeys to prevent conflicts and ensure reliable operation.

Conflict with Other Applications
    If a hotkey is already in use by another application, triggering it may result in unexpected behavior.
    Choose unique hotkey combinations to avoid conflicts.

Hotkey Limitations
    The application may not support certain multimedia keys or custom hardware keys.
    Stick to the supported key list for reliable operation.

Troubleshooting
Hotkey Not Triggering
    Check Hotkey Assignment:
        Ensure the hotkey is correctly entered and saved in the settings.
    Validate Hotkey Format:
        Make sure there are no typos or unsupported keys in the combination.
    Test in Another Application:
        Verify if the hotkey works outside the application to rule out system-level issues.

Warning Icon Appears

   Invalid Format:
        The hotkey may have an incorrect format or unsupported key.
    Solution:
        Edit the hotkey to match the supported keys and format guidelines.

Dial Actions Not Responding
    Hardware Connection:
        Ensure the dial device is properly connected and recognized by the application.
    Application Status:
        Restart the application to reset any potential issues.
