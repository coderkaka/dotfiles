Vim�UnDo� ���������,/8�M�kV\�����,�Y{�$   �                                   ^�t�    _�                             ����                                                                                                                                                                                                                                                                                                                                                             ^�t�     �              �   # encoding: utf-8   # owner: 张琼   9# X-Forwarded-EIP 中通路情况下的基本基本测试   # 测试点：   t#   server端使用tcpdump抓包保存到pcap文件中，然后直接grep二进制文件中的X-Forwarded-EIP: xxxx"   #   add test cases for rules           import time   import json   import string   import random   import pytest   import slbqat   import logging   import alitest   import threading   from slb_ops    import *   from slbqat     import api   from random     import randint   "from slbqat.api import db as apidb   *from alitest import http_util, system_util   (from slbqat.master import db as masterdb       $logger = logging.getLogger(__name__)   slb_obj = slb_ops()       __vport4__ = 60081   __bport4__ = 80   __persistence_timeout__ = 5   __loop_times__ = 10   __download_file__ = "file1k"   __pcap_file__ = "proxy.pcap"    __tcpdump_file__ = "tcpdump.txt"           def setup_module(module):        slb_obj.start_module(module)       def setup_function(function):       slb_obj.start_case()        def teardown_function(function):       slb_obj.end_case()       Ldef check_result(vms, client, eip, vport=__vport4__, in_vid=0, domain=None):   5    slb_obj.wait_lvs_config_ready(eip, vport, in_vid)       time.sleep(3)   7    resp = slb_obj.curl_status_code(client, eip, vport)       assert resp[0] == 0       assert resp[1] == '200'           for vm in vms:   C        slb_obj.execute_remote_cmd(vm['ALI_IP'], "killall tcpdump")           time.sleep(2)   0        slb_obj.execute_remote_cmd(vm['ALI_IP'],   T            "nohup tcpdump -i any -nn port 80 -w /tmp/%s 2>/dev/null >/tmp/%s &" % (   -            __pcap_file__, __tcpdump_file__))           if domain is None:           domain_param = ""           time.sleep(15)   	    else:   q        (ret, out, err) = slb_obj.execute_remote_cmd(client, 'echo "%s  %s" | tee -a /etc/hosts' % (eip, domain))   L        #print "\n---->ret:%s" % ret + "---->out:" + out + "---->err:" + err           time.sleep(35)   5        domain_param = '''-H "Host: %s"''' % (domain)       ]    slb_obj.execute_remote_cmd(client, "curl -v --connect-timeout 10 %s:%s/%s -o /tmp/%s" % (   ?        eip, __vport4__, __download_file__, __download_file__))           time.sleep(2)       for vm in vms:   C        slb_obj.execute_remote_cmd(vm['ALI_IP'], "killall tcpdump")           time.sleep(2)   9        result = slb_obj.execute_remote_cmd(vm['ALI_IP'],   B            'grep -i "X-Forwarded-EIP" /tmp/%s' % (__pcap_file__))   )        if result[1].find("matches") > 0:               return           #time.sleep(200)       assert False       &def clear_testcase_files(vms, client):       for vm in vms:   B        slb_obj.execute_remote_cmd(vm['ALI_IP'],"killall tcpdump")   S        slb_obj.execute_remote_cmd(vm['ALI_IP'],"rm -rf /tmp/%s" % (__pcap_file__))   V        slb_obj.execute_remote_cmd(vm['ALI_IP'],"rm -rf /tmp/%s" % (__tcpdump_file__))       M    slb_obj.execute_remote_cmd(client, "rm -f /tmp/%s" % (__download_file__))       >def clear_testcase_resource(lb_id, vms, rs_pool_name, client):   $   clear_testcase_files(vms, client)   	   # try:   *   #     clear_testcase_files(vms, client)      # finally:      #     try:   %   #         slb_obj.delete_lb(lb_id)      #     finally:   1   #         slb_obj.delete_rs_pool(rs_pool_name)       @marker.function   @pytest.mark.test_way('''   8    构建listen,验证X-Forwarded-EIP配置是否正确   ''')   @pytest.mark.test_points(   @    "验证通路配置，正常访问返回200，配置正确",   n    "配置X-Forwarded-EIP，server端使用tcpdump抓包，验证抓包文件中是否包含X-Forwarded-EIP",   )   *def test_06_classic_ip_vip_vpc_inner_ip():   8    client1 = slb_obj.get_classis_clients()[0]['ALI_IP']   '    vms = slb_obj.get_classis_servers()       in_vid = 0       3    rs_pool_name = data_generator.gen_str('<l,10>')   9    slb_obj.create_http_rs_pool(__bport4__, rs_pool_name)               wild_conf = {   '        "x_forwarded_eip": "127.1.1.1",   '        "x_forwarded_eip_switch": "on",   '        "backend_connect_retries": "2",   &        "backend_connect_timeout": "8"       }       all_config = {            "vip_config": wild_conf,   %        "rs_pool_name": rs_pool_name,           "vport": __vport4__,           "bport": __bport4__,    	    "servers": [vms[0], vms[1]]       }       2    ret = slb_obj.build_simple_service(all_config)       assert ret == True           eip = all_config["eip"]       lb_id = all_config["lb_id"]   H    #add_vip_and_config_vip(lb_id, __vport4__, __bport4__, rs_pool_name)               try:   ;        check_result(vms, client1, eip, __vport4__, in_vid)       finally:   B        clear_testcase_resource(lb_id, vms, rs_pool_name, client1)5�_�                             ����                                                                                                                                                                                                                                                                                                                                                             ^�t�    �                   5��