import os
import pyautogui
import subprocess
from request_handler import mouse_script


def call_windows(allowed, command):
    """
    Windows-only method controlling OS work.
    :param allowed: instance of AllowedRequest model, created by default with running migrations.
    :param command: integer value interpreted as one of defined commands.
    :return: return value is none, each subsequent request call is executed as soon as possible.
    """

    if allowed.volume_louder is True and command == 1:
        subprocess.call(["nircmd", "changesysvolume", "3255"], stdout=open(os.devnull, 'wb'))

    if allowed.volume_lower is True and command == 2:
        subprocess.call(["nircmd", "changesysvolume", "-3255"], stdout=open(os.devnull, 'wb'))

    if allowed.volume_mute is True and command == 3:
        subprocess.call(["nircmd", "mutesysvolume", "2"], stdout=open(os.devnull, 'wb'))

    if allowed.system_monitor is True and command == 4:
        subprocess.call(["nircmd", "monitor", "off"], stdout=open(os.devnull, 'wb'))

    if allowed.system_reboot is True and command == 5:
        subprocess.call(["nircmd", "exitwin", "reboot"], stdout=open(os.devnull, 'wb'))

    if allowed.system_shutdown is True and command == 6:
        subprocess.call(["nircmd", "exitwin", "poweroff"], stdout=open(os.devnull, 'wb'))

    if allowed.system_logout is True and command == 7:
        subprocess.call(["nircmd", "exitwin", "logoff"], stdout=open(os.devnull, 'wb'))

    if allowed.system_recycle is True and command == 8:
        subprocess.call(["nircmd", "emptybin"], stdout=open(os.devnull, 'wb'))

    if allowed.mouse_left is True and command == 9:
        pyautogui.moveRel(-10, 0)

    if allowed.mouse_right is True and command == 10:
        pyautogui.moveRel(10, 0)

    if allowed.mouse_up is True and command == 11:
        pyautogui.moveRel(0, -10)

    if allowed.mouse_down is True and command == 12:
        pyautogui.moveRel(0, 10)

    if allowed.mouse_leftclick is True and command == 13:
        try:
            mouse_script._click(
                button='left',
                x=pyautogui.position()[0],
                y=pyautogui.position()[1]
            )
        except:
            pass

    if allowed.mouse_rightclick is True and command == 14:
        try:
            mouse_script._click(
                button='right',
                x=pyautogui.position()[0],
                y=pyautogui.position()[1]
            )
        except:
            pass
