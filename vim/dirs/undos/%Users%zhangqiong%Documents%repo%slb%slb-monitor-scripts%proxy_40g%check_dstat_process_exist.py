Vim�UnDo� ���X/$E��`�fM����Әo�O�Q?(I����   H   &        cmd = 'rm /tmp/dstat.restart*'   6   $                       ^!��    _�                             ����                                                                                                                                                                                                                                                                                                                                                             ^!�     �               �               �                  5�_�                           ����                                                                                                                                                                                                                                                                                                                                                             ^!�1     �                  5�_�                            ����                                                                                                                                                                                                                                                                                                                                                             ^!�4     �                 #!/usr/bin/env python5�_�                            ����                                                                                                                                                                                                                                                                                                                                                             ^!�4    �                 # coding=utf-85�_�                            ����                                                                                                                                                                                                                                                                                                                                                             ^!��     �                 #!/usr/bin/env python   	import os   
import sys   import json   import time   import commands       hc_path = "/tmp/last_hc_stats"   >result = {"collection_flag": 0, "error_info": '', "MSG": None}       def exec_local_cmd(cmd):   '    ret = commands.getstatusoutput(cmd)       return ret[0], ret[1]       if __name__ == '__main__':   S    cmd = 'ps aux | grep "python slbdstat.py --all-plugins" | grep -v grep | wc -l'   "    ret, out = exec_local_cmd(cmd)       count = int(out.strip())       dict = {}       dict['process_num'] = count       data = []       data.append(dict)       result['MSG'] = data   6    print json.dumps(result, sort_keys=True, indent=2)5�_�                            ����                                                                                                                                                                                                                                                                                                                                                             ^!��    �                   5�_�      	                      ����                                                                                                                                                                                                                                                                                                                                                             ^!��     �                *#风险，如何删除dstat的错误日志5�_�      
           	   6       ����                                                                                                                                                                                                                                                                                                                                                             ^!��     �   5   7   H              cmd = 'rm %s' % RESTART5�_�   	              
   6       ����                                                                                                                                                                                                                                                                                                                                                             ^!��     �   5   7   H              cmd = 'rm 5�_�   
                 6   %    ����                                                                                                                                                                                                                                                                                                                                                             ^!�     �   5   7   H      %        cmd = 'rm /tmp/dstat.restart*5�_�                    6   %    ����                                                                                                                                                                                                                                                                                                                                                             ^!�     �   5   7   H      '        cmd = 'rm /tmp/dstat.restart*""5�_�                    6   %    ����                                                                                                                                                                                                                                                                                                                                                             ^!�     �   5   7   H      &        cmd = 'rm /tmp/dstat.restart*"5�_�                    6   %    ����                                                                                                                                                                                                                                                                                                                                                             ^!�     �   5   7   H      %        cmd = 'rm /tmp/dstat.restart*5�_�                    "        ����                                                                                                                                                                                                                                                                                                                                                             ^!�G     �   !   #   H      I        cmd = 'cp %s /tmp/dstat.`date +%%Y%%m%%d%%H%%M%%S`.log' % RUNTIME5�_�                    6   $    ����                                                                                                                                                                                                                                                                                                                                                             ^!�X    �   5   7   H      &        cmd = 'rm /tmp/dstat.restart*'5�_�                     6   $    ����                                                                                                                                                                                                                                                                                                                                                             ^!��    �   5   7   H      '        cmd = 'rm /tmp/dstat.restart.*'5�_�                            ����                                                                                                                                                                                                                                                                                                                                                             ^!�     �                #!/usr/bin/env python   	import os   
import sys   import json   import time   import commands       hc_path = "/tmp/last_hc_stats"   >result = {"collection_flag": 0, "error_info": '', "MSG": None}       def exec_local_cmd(cmd):   '    ret = commands.getstatusoutput(cmd)       return ret[0], ret[1]       if __name__ == '__main__':   S    cmd = 'ps aux | grep "python slbdstat.py --all-plugins" | grep -v grep | wc -l'   "    ret, out = exec_local_cmd(cmd)       count = int(out.strip())       dict = {}       dict['process_num'] = count       data = []       data.append(dict)       result['MSG'] = data   6    print json.dumps(result, sort_keys=True, indent=2)5��