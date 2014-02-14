import sys
sys.path.append('/home/glen/workspace/DataRobot')
from common.services.security import datarobot_crypt

print datarobot_crypt.encrypt(sys.argv[1])
