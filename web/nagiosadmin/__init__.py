#/usr/bin/env python
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
ini = os.path.join(BASE_DIR, 'nagiosadmin/modules/config.ini')
