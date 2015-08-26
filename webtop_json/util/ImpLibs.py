import sys, platform, os
sys.path.append(os.path.join('..', 'reqbuilder'))
sys.path.append(os.path.join('..', 'baseapi'))
sys.path.append(os.path.join('..', 'util'))
sys.path.append(os.path.join('..', 'const'))
sys.path.append(os.path.join('..', 'exception'))

#switch to json
import JSONUtils as utils
import JSONReqConsts as consts
from MsgConsts import MsgConsts as msgconsts
import JSONReqBuilder as reqbuilder
from APIException import APIException
from TestCodeException import TestCodeException