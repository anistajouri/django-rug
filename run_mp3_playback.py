"""
This script is used to start a mp3 playback from its database ID passed as argument.
The script can also handle the automatic stop with a second argument.

How to use: python run_mp3_playback.py <id_mp3_playback> [<seconds_before_auto_stop>]
E.g: python run_mp3_playback.py 12 20
"""
import inspect
import os
import sys
import django
from webapi.Utils.PlayerManager import CallbackPlayer, ThreadTimeout, PlayerManager

def is_mp3_path_valid(mp3_path):
    """
    :param mp3_path: mp3_path to check
    :return: True if the metode can connect to the URL
    """
    return (os.path.exists(mp3_path))
    # try:
    #     print("Try to connect to the URL: %s" % mp3_path)
    #     connection = requests.get(mp3_path)
    #     #print("URL status code: %s " % connection.getcode())
    #     #connection.close()
    #     return True
    # except ConnectionError as e:
    #     print("Failed to connect")
    #     return False
    # except URLError:
    #     print("Failed to connect (timeout)")
    #     return False


# load django models
project_path = os.path.dirname(os.path.realpath(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangorug.settings")
sys.path.append(project_path)
django.setup()
from webapi.models import MP3Playback, BackupMusic

# get the ID of the mp3playback to play from the argument
id_mp3_playback_to_play = sys.argv[1]
print("Id of the mp3 playback to play: %s" % id_mp3_playback_to_play )
# get the time in second before auto kill
second_before_auto_kill = None
try:
    second_before_auto_kill = sys.argv[2]
    print("Auto kill the mp3 playback in %s seconds" % second_before_auto_kill)
except IndexError:
    print( "No seconds for auto kill" )

# get the real mp3 playback object to play
try:
    mp3_playback_to_play = MP3Playback.objects.get(id=id_mp3_playback_to_play)
except MP3Playback.DoesNotExist:
    print("The mp3 playback id %s does not exist, cannot launch")
    sys.exit()

# get the current script path
current_script_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# try to get a backup mp3 if exists
backup_mp3_list = BackupMusic.objects.all()
backup_mp3_path = None
backup_mp3_callback = None
if backup_mp3_list is not None:
    if len(backup_mp3_list) == 1:
        backup_mp3_path = backup_mp3_list[0].backup_file.url
        print("Path to the backup MP3: %s" % backup_mp3_path)
        if backup_mp3_path is not None:
            backup_mp3_path = current_script_path + os.sep + backup_mp3_path
            backup_mp3_callback = CallbackPlayer(mp3_path=backup_mp3_path)



# test the URL, if this one is not valid, we start the backup
if is_mp3_path_valid(mp3_path=mp3_playback_to_play.mp3_path):
    print("valid mp3")
    # start the thread that will play the mp3 playback, check that the mp3 playback is playing, and auto kill it if needed  
    mp3_playback_callback = CallbackPlayer(mp3_path=mp3_playback_to_play.mp3_path)
    # the following thread will start to play the mp3 playback and then check if the player is still alive after 35 seconds
    # this to prevent the case where the URL is valid and is answering request but no stream is present inside
    command = ThreadTimeout(callback_instance=mp3_playback_callback,
                            backup_instance=backup_mp3_callback,
                            timeout=35,
                            time_before_auto_kill=second_before_auto_kill)
    command.run()
else:
    PlayerManager.play(mp3_path=current_script_path + os.sep + "sounds/cannot_play_mp3_playback.mp3", blocking_thread=True)
    # the URL is not valid, start the backup MP3 if exist
    if backup_mp3_callback is not None:
        PlayerManager.play(mp3_path=current_script_path + os.sep + "sounds/playing_backup_file.mp3", blocking_thread=True)
        backup_mp3_callback.start()
    else:
        PlayerManager.play(mp3_path=current_script_path + os.sep + "sounds/no_backup_file.mp3", blocking_thread=True)
