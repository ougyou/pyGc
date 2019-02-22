#!/usr/bin/env python
# coding=utf-8

import os, re, time, sys, commands, fileinput, shutil
##########调试开关##########
LOG_DEBUG = True
###########开发要替换的配置文件###########
DEVELOPER_CONFIG_DIR = "webapps/conftest/"
###########牧场源码主路径###########
MUCHANG_PATH = "/data/HY_MOCHANG"
##########发布路径##########
DEPLOY_FROM_WAR = "target/muchang-0.0.1-SNAPSHOT.war"
###########接口相关文件###########
MACHINE_IP = "117.34.98.20"
MACHINE_HOST = "mnshoptest.hylinkad.com"
ALIPAY_PATH = "src/net/jeeshop/core/payment/alipay"
ALIPAY_WAP_CONFIG_PATH = "wap/config/AlipayConfig.java"
ALIPAY_WAP_SUBMIT_PATH = "wap/config/util/AlipaySubmit.java"
ALIPAY_SERVICE_PATH = "services/AlipayService.java"
ORDER_QUERY_PATH = "src/net/jeeshop/mn/util/OrderQueryUtils.java"
SYSTEM_PROPERTIES = "src/system.properties"
##################################################################

# 启动tomcat
def start_tomcat(tomcat_home):
    try:
        catalina_dir = os.path.join(tomcat_home, "work/Catalina")
        if os.path.isdir(catalina_dir):
            delete_dir(catalina_dir)
        cmd = "cd %s\n./startup.sh" % os.path.join(tomcat_home, "bin")
        if LOG_DEBUG:
            print ' please wait :  starting tomcat ......'
        time.sleep(3)
        (status, out) = commands.getstatusoutput(cmd)
        # if LOG_DEBUG:
        #    print 'exec command : ', cmd
        if status != 0:
            return "%s fail : " % cmd, out
        if LOG_DEBUG:
            print 'tomcat started: ', tomcat_home
        return 'ok'
    except Exception, e:
        return 'start_tomcat() exception : ', str(e)
    
# 停止tomcat
def stop_tomcat(tomcat_home):
    try:
        cmd = "ps -ef | grep .*java.*%s.*" % tomcat_home
        # if LOG_DEBUG:
        #    print 'exec command : ', cmd
        (status, out) = commands.getstatusoutput(cmd)
        if status != 0:
            return "%s fail : " % cmd, out
        procs = out.split("\n")
        for p in procs:
            if 'grep .*java.*%s.*' % tomcat_home in p:
                continue
            if re.sub("\s+", "", p) == '':
                continue
            ps = re.split("\s+", p)
            if len(ps) < 2:
                continue
            pid = ps[1]
            if not re.match("\d+$", pid):
                continue
            cmd = "kill %s" % pid
            # if LOG_DEBUG:
            #    print 'exec command : ', cmd
            (status, out) = commands.getstatusoutput(cmd)
            if status != 0:
                if LOG_DEBUG:
                    print "%s fail : " % cmd, out
                continue
        if LOG_DEBUG:
            print ' stop tomcat : ', cmd
        return 'ok'
    except Exception, e:
        return 'stop_tomcat() exception : ', str(e)

# hg update到指定的branch，若branch为None，更新到最新tag    
def update_hg(branch=None): 
    try:
        cmd = "cd " + MUCHANG_PATH + "\nhg pull"
        if LOG_DEBUG:
            print 'exec command : ', cmd.replace("\n", ", ")
        (status, out) = commands.getstatusoutput(cmd)
        time.sleep(3)
        if status != 0:
            return "hg pull fail : ", out
        if branch == None:
            branch = get_latest_tag()
            if not branch.startswith("tag_"):
                return branch
        cmd = "cd " + MUCHANG_PATH + "\nhg update --clean " + branch
        if LOG_DEBUG:
            print 'exec command : ', cmd.replace("\n", ", ")
        (status, out) = commands.getstatusoutput(cmd)
        time.sleep(1)
        if status != 0:
            return 'hg update fail : ', out
        (status, out) = commands.getstatusoutput("cd " + MUCHANG_PATH + "\nhg id")
        if(status != 0):
            return 'get hg id fail : ', out
        else:
            if LOG_DEBUG:
                print 'current hg id: ', out
        return 'ok'
    except Exception, e:
        return 'update_hg(%s) exception : ' % branch, str(e)

# 获取最新tag
def get_latest_tag():
    try:
        (status, out) = commands.getstatusoutput("cd " + MUCHANG_PATH + "\nhg tags | head -2")
        if status != 0:
            return 'get hg tags fail : ', out
        tags = out.split("\n")
        if len(tags) < 2:
            return u'get latest hg tag fail: ' + tags[0]
        return tags[1].split(" ")[0]
    except Exception, e:
        return 'get_first_tag() exception : ', str(e)

# 修改工程代码中接口相关配置
def change_config():
    try:
        # 物流配置修改
        order_query_file = os.path.join(MUCHANG_PATH, ORDER_QUERY_PATH)
        for line in fileinput.input(order_query_file, inplace=1):
            if "PropertiesUtil.getInstance().get(\"mn_order_query_path\")" in line:
                line = line.replace('));', ') + \"&response=application/json\");')  
            if "JSONObject.parseObject(result)" in line:
                line = '            result = result.replaceAll("^\\\\{\\"expressstatusResponse\\":\\\\{\\"return\\":", "").replaceAll("}}}$", "}");' + "\n" + line
            print line,
        if LOG_DEBUG:
            print "replace over : ", order_query_file
            
        # pc端支付接口修改
        pc_alipay_file = os.path.join(MUCHANG_PATH, ALIPAY_PATH, ALIPAY_SERVICE_PATH)
        for line in fileinput.input(pc_alipay_file, inplace=1):
            if "private static final String ALIPAY_GATEWAY_NEW" in line:
                line = 'private static final String ALIPAY_GATEWAY_NEW = "http://117.34.98.20:8088/axis2/services/alipay/pay/gateway?";';    
            print line,
        if LOG_DEBUG:
            print "replace over : ", pc_alipay_file
        # wap端支付接口修改
        wap_alipay_file = os.path.join(MUCHANG_PATH, ALIPAY_PATH, ALIPAY_WAP_SUBMIT_PATH)
        for line in fileinput.input(wap_alipay_file, inplace=1):
            if "private static final String ALIPAY_GATEWAY_NEW" in line:
                line = 'private static final String ALIPAY_GATEWAY_NEW = "http://117.34.98.20:8088/axis2/services/alipay/pay/gateway?";';    
            print line,
        if LOG_DEBUG:
            print "replace over : ", wap_alipay_file
        # wap端公私钥修改
        from_file = os.path.basename(ALIPAY_WAP_CONFIG_PATH)
        to_file = os.path.join(MUCHANG_PATH, ALIPAY_PATH, ALIPAY_WAP_CONFIG_PATH)
        shutil.copyfile(from_file, to_file)
        if LOG_DEBUG:
            print "replace over : ", to_file
                
        # 修改system.properties
        system_prop_file = os.path.join(MUCHANG_PATH, SYSTEM_PROPERTIES)
        for line in fileinput.input(system_prop_file, inplace=1): 
            if line.startswith("mn_order_query_path="):
                line = line.replace("https://occ.mall.mengniu.com.cn/", "http://117.34.98.20:8088/axis2/services/")
            if (line.startswith("alipay_return_url=")  or line.startswith("alipay_return_url_wap=") or line.startswith("alipay_notify_url=")  or line.startswith("alipay_notify_url_wap=")) and MACHINE_IP in line:
                line = line.replace(MACHINE_IP, MACHINE_HOST)
                line = line.replace(MACHINE_HOST + "/web", MACHINE_HOST + "/test")
            print line,
        if LOG_DEBUG:
            print "replace over : ", system_prop_file
        return 'ok'
    except Exception, e:
        return 'change_config() exception : ', str(e)

# 开发文件替换
def change_config_for_dev(tomcat_home):
    try:
        from_dir = os.path.join(tomcat_home , DEVELOPER_CONFIG_DIR)
        if not os.path.isdir(from_dir):
            return 'ok'
        to_dir = os.path.join(MUCHANG_PATH, "src/")
        for f in os.listdir(from_dir):
            from_file = os.path.join(from_dir, f)
            to_file = os.path.join(to_dir, f)
            shutil.copyfile(from_file, to_file)
            if LOG_DEBUG:
                print '   copy file : ', from_file
        return 'ok'
    except Exception, e:
        return 'change_config_for_dev() exception : ', str(e)
    
# 执行mvn clean package
def build_project(branch=None):
    try:
        target = os.path.join(MUCHANG_PATH, "target")
        if os.path.isdir(target):
            delete_dir(target)
        cmd = "cd " + MUCHANG_PATH + "\nmvn clean package"
        if LOG_DEBUG:
            print ' please wait :  do building ............'
        (status, out) = commands.getstatusoutput(cmd)
        time.sleep(5)
        if(status != 0):
            return out
        if LOG_DEBUG:
            print 'build success: ', cmd.replace("\n", ", ")
        return 'ok'
    except Exception, e:
        return 'build_project(%s) exception : ' % branch, str(e)


# 发布工程到指定的deploy_dir下 
def deploy_project(deploy_dir, branch=None, do_replace=False):
    if deploy_dir.endswith("/"):
        deploy_dir = deploy_dir[:-1]
    if not "/" in deploy_dir or not "webapps" in deploy_dir:
        return 'error :', deploy_dir, 'is not a tomcat directory!'
    webapps = os.path.dirname(deploy_dir)
    tomcat_home = os.path.dirname(webapps)
    if not os.path.isdir(webapps): 
        return 'error :', deploy_dir, 'is not a tomcat directory!'
    # bak_deploy_dir = os.path.abspath(os.path.join(".", os.path.basename(deploy_dir) + "-bak-" + time.strftime("%Y%m%d")))
    try:
        update = update_hg(branch)
        if not 'ok' == update:
            return update
        change_config_for_dev(tomcat_home)
        if do_replace:
            change = change_config()
            if not 'ok' == change:
                return change
        build = build_project(branch)
        if not 'ok' == build:
            return build
        stop = stop_tomcat(tomcat_home)
        if not 'ok' == stop:
            return stop
        from_war_file = os.path.join(MUCHANG_PATH, DEPLOY_FROM_WAR)
        to_war_file = deploy_dir + ".war"
        delete_file(to_war_file)
        # if os.path.isdir(deploy_dir):
        #    if os.path.isdir(bak_deploy_dir):
        #        delete_dir(bak_deploy_dir)
        #    shutil.move(deploy_dir, bak_deploy_dir)
        #    time.sleep(2)
        #    if LOG_DEBUG:
        #        print '  backup dir :  %s to %s' % (deploy_dir, bak_deploy_dir) 
        delete_dir(deploy_dir)
        shutil.copyfile(from_war_file, to_war_file)
        if LOG_DEBUG:
            print 'deploy success:  %s to %s' % (from_war_file, to_war_file)
        start_tomcat(tomcat_home)
        return "ok"
    except Exception, e:
        # if os.path.isdir(bak_deploy_dir):
        #    delete_dir(deploy_dir)
        #    shutil.copytree(bak_deploy_dir, deploy_dir)
        #    if LOG_DEBUG:
        #        print 'recover dir :  %s to %s' % (bak_deploy_dir, deploy_dir) 
        return 'deploy_project() exception : ', str(e)
    # finally:
        # if os.path.isdir(bak_deploy_dir):
        #    delete_dir(bak_deploy_dir)
        # start_tomcat(tomcat_home)


def delete_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        if os.path.isdir(path):
            print ' delete FAIL : ', path
        else:
            if LOG_DEBUG:
                print '  delete dir : ', path

def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)
        # cmd = "rm -rf %s" % path
        # (status, out) = commands.getstatusoutput(cmd)
        if os.path.isfile(path):
            if LOG_DEBUG:
                print ' delete FAIL : ', path
        else:
            if LOG_DEBUG:
                print ' delete file : ', path
            
      
def print_usage():
    print 'usage: python build_muchang.py [-R] arg1 [arg2]'
    print u'       -R   -- 选配,修改支付宝及物流接口为模拟接口, 不加-R则不修改'
    print u'       arg1 -- 必配,工程发布路径,例如: /data/tomcat-7.0.61/webapps/test'
    print u'       arg2 -- 选配,要发布版本对应的分支号或标签,例如: tag_muchang_1.3.3_test_rev14'
    print u'               不配置arg2则默认更新代码到最新的tag版本'
            
if __name__ == '__main__':
    args = sys.argv[1:]
    deploy_dir = None
    branch = None
    do_replace = False
    can_deploy = True
    if args:
        arg0 = args[0]
        len_args = len(args)
        if len_args == 1:
            deploy_dir = arg0
        if len_args == 2:
            if "-R" == arg0:
                do_replace = True
                deploy_dir = args[1]
            else:
                deploy_dir = arg0
                branch = args[1]
        if len_args == 3:
            if "-R" == arg0:
                do_replace = True
                deploy_dir = args[1]
                branch = args[2]
            else:
                can_deploy = False
                print 'error : wrong args!'
                print_usage()
        if can_deploy:
            print '------------------------------------'
            print '    start at : ', time.strftime("%Y-%m-%d %H:%M:%S")
            print deploy_project(deploy_dir, branch, do_replace)
            print '       end at: ', time.strftime("%Y-%m-%d %H:%M:%S")
            print '------------------------------------'
    else:
        print_usage()
        

    
