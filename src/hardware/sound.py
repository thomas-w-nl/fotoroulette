import vlc
import time
from src.common.log import *

love = vlc.MediaPlayer("assets/sound/dingDong.mp3")
finishHim = vlc.MediaPlayer("assets/sound/finishHim.mp3")
mortalKombat = vlc.MediaPlayer("assets/sound/mortalKombat.mp3")
heroes = vlc.MediaPlayer("assets/sound/heroes.mp3")


if __name__ == "__main__":
    log.debug("sound running as main")
    mortalKombat.play()
    time.sleep(60)
