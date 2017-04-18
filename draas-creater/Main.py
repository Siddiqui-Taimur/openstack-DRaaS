
import subprocess
from Configurations import Configurations


def largescaledisaster():
    subprocess.call(['scripts/shutdown.sh'])

def networkdisaster():
    subprocess.call(['scripts/networkfailure.sh'])

def ftpdisaster():
    subprocess.call(['scripts/ftpfailure.sh'])

def keystonedisaster():
    subprocess.call(['scripts/keystonefailure.sh'])

def smallscaledisaster():
    subprocess.call(['scripts/smallscale.sh'])

if __name__ == '__main__':
    conf = Configurations()

    for disaster in conf.DISASTERS:
        if disaster == 'large_scale':
            largescaledisaster()
        elif disaster == 'network':
            networkdisaster()
        elif disaster == 'ftp_failure':
            ftpdisaster()
        elif disaster == 'keystone_failure':
            keystonedisaster()
        elif disaster == 'small_scale':
            smallscaledisaster()
