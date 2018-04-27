#/usr/bin/python


from email.mime.text import MIMEText
import smtplib, time
import requests
from requests.auth import HTTPBasicAuth
import time


def get_current_time():
    return time.ctime()

def cafe_logo(v, sv, sv2=0):
    logo = '''

    \033[1;34;40m    
                                                                                                                        
                                ##      ##               ##                                                             
                               ###   ## ##               ##                                                             
                               #### ###### ###  ######## ###### #####                                                   
                               #### ###### ############# ############                                                   
                              ## ##  ## ##   #####  ###  ##   #### ##                                                   
                              ###### ## ## #### #### ### ######### ##                                                   
                              ###### ## #### ##   ### ## #### #### ##                                                   
                             ##   ## ##### ############# ######### ##                                                   
         #######                                                                                                        
       ###########           #############  ####              #####           #############                             
     ###############         ############## #####             #####           #############                             
    #################        ############## #####             #####           #############                             
   ###################       ############## #####             #####           #############                             
  #####        ########      #####                            #####           ####                                      
 #####           ######      #####                            #####           ####                            ####      
 ###              ######     #####          #####  ########## #############   ####         ####      #####  ########    
 ###               #####     #####          ##### ##########  #############   ####         #####     ####  ##########   
###                 #####    #####          ##### ##########  #############   ###########   ####    ##### ############  
##                  #####    #############  ##### #####    #  ##############  ############  ####    ##### #####  #####  
##    ####           ####    #############  ##### ####        ######   #####  ############  #####   ####  ####    ####  
##   #######         ####    #############  ##### ######      #####    #####  ############   ####  #####  ####    ####  
     #########       ####    #############  ##### #########   #####    #####  ############   ##### #####  ############  
     ##########      ####    #####          #####  #########  #####    #####  ####            #### ####   ############  
     ##  #######     ####    #####          #####   ######### #####    #####  ####            #########   ############  
     ##   #######    ###     #####          #####       ##### #####    #####  ####            #########   ####          
     ##  ########    ###     #####          #####        #### #####    #####  ####             #######    ####          
     ###########    ###      #####          ##### ###   ##### #####    #####  #############    #######    #####    ###  
     ##########     ###      #####          ##### ########### #####    #####  #############    #######    ############  
     #########     ###       #####          ##### ##########  #####    #####  #############     #####      ###########  
     ########     ###        #####          ##### ##########  #####    #####  #############     #####       ##########  
      #####      ###                                                                            #####               
                                                                                                ####                    
                                                                                                ####                    
                                                                                               #####                    
                                                                                               ####                                                                                                     
                                                                                                 Verion: <version>.<sub_version1>.<sub_version2>
    '''
    return logo.replace('<version>', str(v)).replace('<sub_version1>', str(sv)).replace('<sub_version2>', str(sv2))

def send_mail(data):
    # with open("prober_msg.txt", 'rb') as fp:
    #     content = fp.read()
        # content = re.sub(r"ZZZZZZ\r", data['topo'], content)
        # content = re.sub(r"XXXXXX\r", data['ip_list'], content)
    print("%s : Sending email..." % get_current_time())
    msg = MIMEText(data["content"])
    msg['Subject'] = data["subject"]
    msg['From'] = data['from']
    msg['To'] = data["to"]

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('mail.calix.local')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    print('%s : Email has been sent to %s!' % (get_current_time(), data['to']))

def send_mail_html(data):
    # with open("prober_msg.txt", 'rb') as fp:
    #     content = fp.read()
        # content = re.sub(r"ZZZZZZ\r", data['topo'], content)
        # content = re.sub(r"XXXXXX\r", data['ip_list'], content)
    print("%s : Sending email..." % get_current_time())
    msg = MIMEText(data["content"], 'html', 'utf-8')
    msg['Subject'] = data["subject"]
    msg['From'] = data['from']
    msg['To'] = data["to"]

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('mail.calix.local')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    print('%s : Email has been sent to %s!' % (get_current_time(), data['to']))

def get_fisheye_json(url, reviewID, auth, headers):


    # ret = requests.request('GET', BASE_URL+'filter?project=CR-SQACAFE', auth=HTTPBasicAuth(auth['user'], auth['password']), headers=headers)
    print('%s : Collecting data from Fisheye <%s>......' % (get_current_time(), reviewID))
    ret = requests.get(url+reviewID+'/details', auth=HTTPBasicAuth(auth['user'], auth['password']), headers=headers)
    return ret
    # print(ret.json())

def get_all_reviews(url, auth, headers):
    # ret = requests.request('GET', BASE_URL+'filter?project=CR-SQACAFE', auth=HTTPBasicAuth(auth['user'], auth['password']), headers=headers)
    print(str(get_current_time()) + ': Collecting data from Fisheye......')
    ret = requests.get(url+'filter?project=CR-SQACAFE', auth=HTTPBasicAuth(auth['user'], auth['password']), headers=headers)
    return ret

def data_generator(source, reviewid, base='http://fisheye.calix.local/cru/'):

    table= {}
    table['reviewers'] = []
    try:

        if source.json()['state'] in ('Draft', 'Approval', 'Closed', 'Dead', 'Rejected', 'Unknown'):
            print('%s : %s is in %s.' % (get_current_time() , reviewid,source.json()['state']))
            return
    except KeyError:
        print('%s : ERROR: No such review ID!' % get_current_time())
        pass
    try:
        print('>>>%s : %s is in %s...' % (get_current_time(), reviewid, source.json()['state']))
    except Exception as e:
        raise KeyError('ERROR: No such key found!')
    try:
        table['reviewID'] = reviewid
        table['link'] = base + reviewid
        table['creator'] = source.json()['creator']['displayName']
        table['title'] = source.json()['name']
        for i in range(len(source.json()['reviewers']['reviewer'])):
            table['reviewers'].append((source.json()['reviewers']['reviewer'][i]['displayName'], source.json()['reviewers']['reviewer'][i]['completed']))
    except Exception as e:
        raise KeyError('ERROR: No such key found!')
    # for k, v in source.json().items():
    #
    #     if k.encode('utf-8') == 'creator':
    #         table['reviewID'] = reviewid
    #         table['link'] = base+reviewid
    #         table['creator'] = v['displayName']
    #     if k.encode('utf-8') == "reviewers":
    #         for i in range(len(v['reviewer'])):
    #             table['reviewers'].append((v['reviewer'][i]['displayName'], v['reviewer'][i]['completed']))
                # table['reviewers'+str(i)] = [v['reviewer'][i]['displayName'], v['reviewer'][i]['completed']]
    return table

def close_review(base, reviewid, user, password, close_xpath):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    browser = webdriver.PhantomJS('/home/jcao/sw/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    # browser = webdriver.Firefox()

    browser.get(base_url_+reviewid)
    # browser.find_element_by_id("username").text(user)
    browser.find_element_by_id("username").send_keys(user)
    browser.find_element_by_id("password").send_keys(password)
    browser.find_element_by_id("loginButton").click()
    browser.find_element_by_xpath('//*[@id="page-actions"]/div/a[4]').click()

    # time.sleep(5)
    m = browser.find_element_by_xpath('//*[@id="tools-dropdown"]/ul/li[2]/a').is_displayed()
    if m:
        time.sleep(5)
        browser.find_element_by_xpath('//*[@id="tools-dropdown"]/ul/li[2]/a').click()
    time.sleep(5)
    # browser.find_elements_by_link_text('Close')
    # browser.find_elements_by_class_name('action-closeReview').click()
    # browser.find_element_by_css_selector('.action-closeReview').click()
    # browser.find_element_by_css_selector('#tools-dropdown > ul > li:nth-child(2) > a').click()
    # browser.find_element_by_xpath('class="action-closeReview"').click()
    # browser.find_element_by_xpath('//*[@id="confirm-close-receipt-dialog"]/div/div[2]/a[2]').click()
    # browser.find_element_by_xpath(close_xpath).click()
    print('review %s is closed automatically!' % reviewid)
    browser.quit()



if __name__ == '__main__':

    print(cafe_logo(1,00,"Beta"))
    BASE_URL='http://fisheye.calix.local/rest-service/reviews-v1/'
    # BASE_URL='http://fisheye.calix.local/rest-service/reviews-v1/filter?project=CR-SQACAFE'

    headers = {
        'authorization': "Basic Y2RjY2FmZTpDYWxpeDEyMw==",
        'accept' : "application/json",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "6b9c2c43-a3af-690a-4380-1039d014f87d"
        }
    auth = {
        'user': 'cdccafe',
        'password': 'Calix123'
    }
    # ret = get_all_reviews(BASE_URL,auth, headers)
    # print ret.text
    HTML = ''
    ALL = ''
    cafeid = 900
    baristaid=0

    while True:
        cafeid += 1
        ReviewerID = "CR-SQACAFE-" + str(cafeid)
        if cafeid>1200:
            ReviewerID = 'CR-SQA-BARISTA-' +  str(baristaid)
            baristaid +=1
            if baristaid > 100:
                break

        ret = get_fisheye_json(BASE_URL,ReviewerID, auth, headers)
        try:
            table= data_generator(ret, ReviewerID)
        except Exception as e:
            continue
        # print(table)
        if not table:
            continue
        if len(table) < 3:
            continue

        content = [table['reviewID'], table['link'], table['title'], table['creator'],table['reviewers']]
        state = []
        #for c in table['reviewers']:
        #    state.append(c[1])
        #if len(set(state)) == 1:
            #base_url_ = 'http://fisheye.calix.local/cru/'
            ## xpath = '//*[@id="tools-dropdown"]/ul/li[2]/a'
            #xpath = "//div[@id='content']/header/div/div[3]"
            #with open('/home/jcao/sw/code.txt', 'r') as f:
            #    lines = f.readlines()
            #    # print type(lines[1]), type(lines[2])
            #    user = lines[1].replace('kk', 'j').strip()
            #    password = lines[2].replace('$!','diannao').strip()
            #    close_review(base_url_, ReviewerID, user, password, xpath)

        head ="""
        <table style="height: 240px; width: 533px;">
        <tbody>"""

        bottom = """
        </tbody>
        </table>"""

        template = """
        <tr style="height: 24px;">
        <td bgcolor="#cccccc" nowrap><strong><font color="#000001"> $key </td>
        <td bgcolor="#cccccc" nowrap><font color="#000000"> $value </td>
        </tr> """

        reviewers_ = """
        <tr style="height: 24px;"  >
        <td nowrap="nowrap" bgcolor="#cccccc" colspan=2><strong><span style="color: #000001;"> Reviewers </span></td>
        </tr>"""

        html = " "
        reviewID=template.replace('$key', 'Review ID').replace('$value', table['reviewID'])
        Link=template.replace('$key', 'Link').replace('$value', table['link'])
        Title = template.replace('$key', 'Title').replace('$value', table['title'])
        Creator=template.replace('$key', 'Creator').replace('$value', table['creator'])
        HTML += head + '\n' + reviewID + '\n' + Link +'\n' + Title+ '\n' + Creator +'\n' +reviewers_ +'\n'

        # print(type(table['reviewers']))
        for i in range(len(table['reviewers'])):
            if table['reviewers'][i][1] is False:
                reviewers = template.replace('$key', table['reviewers'][i][0]).replace('$value', 'Not Completed').replace('000000', 'ff3300').replace('><strong><', '><')
                HTML += reviewers
            else:
                reviewers = template.replace('$key', table['reviewers'][i][0]).replace('$value',' Completed').replace('000000', '006600').replace('><strong><', '><')
                HTML += reviewers

        HTML += bottom + '\n' + '#'*80 +'\n'

    data = {
                "from": "fisheyeBot@calix.com",
                # "to": "james.cao@calix.com",
                "to": "automation-dev-cdc@calix.com",
                "content": HTML,
                "subject": "[FisheyeBot]: Code review status summary!"
        }
    if data['content']:
        print(data['content'])
        send_mail_html(data)
