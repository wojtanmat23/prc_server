from django.db import models


class Signal(models.Model):
    """
    Database model created for convenience of using drf ViewSet,
    describes types of requests that can be executed.
    """

    LOUDER = 1
    LOWER = 2
    MUTE = 3
    MONITOR = 4
    REBOOT = 5
    SHUTDOWN = 6
    LOGOUT = 7
    RECYCLE = 8
    LEFT = 9
    RIGHT = 10
    UP = 11
    DOWN = 12
    LEFTCLICK = 13
    RIGHTCLICK = 14

    signals = ((LOUDER, 'volume_louder'),
               (LOWER, 'volume_lower'),
               (MUTE, 'volume_mute'),
               (MONITOR, 'system_monitor'),
               (REBOOT, 'system_reboot'),
               (SHUTDOWN, 'system_shutdown'),
               (LOGOUT, 'system_logout'),
               (RECYCLE, 'system_recycle'),
               (LEFT, 'mouse_left'),
               (RIGHT, 'mouse_right'),
               (UP, 'mouse_up'),
               (DOWN, 'mouse_down'),
               (LEFTCLICK, 'mouse_leftclick'),
               (RIGHTCLICK, 'mouse_rightclick'),

               )

    value = models.IntegerField(choices=signals)


class ExternalRequest(models.Model):
    """
    Database model describing python code that can be run.
    """
    external = models.TextField()


class AllowedRequest(models.Model):
    """
    Database model storing user preferred settings, describes allowed (customizable)
    requests that can be called fromhandheld device.
    """

    # voice settings
    volume_louder = models.BooleanField(
        default=True, help_text="Turn volume up.")
    volume_lower = models.BooleanField(
        default=True, help_text="Turn volume down.")
    volume_mute = models.BooleanField(
        default=True, help_text="Mute speakers.")

    # power settings
    system_monitor = models.BooleanField(
        default=True, help_text="Turn on/off screen.")
    system_reboot = models.BooleanField(
        default=True, help_text="Reboot system.")
    system_shutdown = models.BooleanField(
        default=True, help_text="System shutdown.")
    system_logout = models.BooleanField(
        default=True, help_text="System logout.")
    system_recycle = models.BooleanField(
        default=True, help_text="Recycle bin.")

    # mouse settings
    mouse_left = models.BooleanField(
        default=True, help_text="Move cursor to the left.")
    mouse_right = models.BooleanField(
        default=True, help_text="Move cursor to the right.")
    mouse_up = models.BooleanField(
        default=True, help_text="Move cursor up.")
    mouse_down = models.BooleanField(
        default=True, help_text="Move cursor down.")
    mouse_leftclick = models.BooleanField(
        default=True, help_text="Perform left mouse click.")
    mouse_rightclick = models.BooleanField(
        default=True, help_text="Perform right mouse click.")

    # other
    python_external = models.BooleanField(
        default=True, help_text="Call python code to run in the console.")
