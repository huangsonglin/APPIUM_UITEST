#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/1/31 16:03'

import os,sys
import time
import re, string
from Until.YamlRead import *
from Driver.Driver import *
from Command.command import command as cmd
from appium.webdriver.common import mobileby
from Driver.Driver import *
from selenium.webdriver.common.by import By
from API.new_500 import *
from API.Order500 import *
from API.BBS500 import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from Page.AboutLogin import *
from Until.YamlRead import *
from Page.AboutLogin import *
from API.LZshop import *
from Page.PulicClass import *
from Until.DB import *
from Page.MyProduct import *

class TestMine:

    username = Config(CONFIG_FILE).get('username')
    password = Config(CONFIG_FILE).get('password')
    host = Config(CONFIG_FILE).get('host')
    headers = Config(CONFIG_FILE).get('headers')


    # 进入我的页面
    def Into_MimePage(self, driver):
        try:
            loc = (By.ID, (Config(HomePage).get('mine_RadioButton')))
            Mime = WebDriverWait(driver, 3).until\
                (EC.visibility_of_element_located(loc))
            Mime.click()
        except:
            raise '进入个人中心界面失败'


    # 个人信息板块验证
    def personal_information(self, driver):
        PulicClass().Login(driver)
        ele_nikename = Config(MinePage).get('user_nickname')
        ele_realname = (By.ID, (Config(MinePage).get('user_realname_icon')))
        ele_dcnum = Config(MinePage).get('user_dcnum')
        ele_lznum = Config(MinePage).get('my_lz')
        ele_money = Config(MinePage).get('my_money')
        req = v5().getMemberDetailInfo_112()
        monerreq = V5_ORDER().getAccountInfo_230()
        assert req.status_code == 200
        assert monerreq.status_code == 200
        try:
            nikename = driver.find_element_by_id(ele_nikename).text
            dcnum = driver.find_element_by_id(ele_dcnum).text
            lznum = driver.find_element_by_id(ele_lznum).text
            moneynum = driver.find_element_by_id(ele_money).text
            assert req.json()['name'] == nikename
            assert req.json()['zangNum'] == str(dcnum).split(':')[1].strip()
            assert int(float(req.json()['credit'])) == int(lznum)
            assert (float(monerreq.json()['balanceAccount']['totalAmount'])) + \
                   (float(monerreq.json()['bidBondAccount']['totalAmount'])) == float(moneynum)
            try:
                realname = WebDriverWait(driver, timeout=3).until(EC.visibility_of_element_located(ele_realname))
                realname_isdisplay = True
            except:
                realname_isdisplay = False
            if req.json()['realNameAuth']:
                assert realname_isdisplay == True
            else:
                assert realname_isdisplay == False
        except:
            assert True == False

    # 查看个人钱包信息
    def into_myburse(self, driver):
        try:
            PulicClass().Login(driver)
            ele_nikename = Config(MinePage).get('user_nickname')
            ele_realname = (By.ID, (Config(MinePage).get('user_realname_icon')))
            ele_my_wallet = Config(MinePage).get('my_wallet')
            PulicClass().Login(driver)
            mywallet_button = driver.find_element_by_id(ele_my_wallet)
            mywallet_button.click()
            driver.implicitly_wait(2)
            assert driver.current_activity == '.activity.MyAssetsActivity', u'我的钱包界面activity正常'
            account_button = driver.find_elements_by_id('cn.dcpai.auction:id/tv_tab_title')[0] # 账户按钮
            bidBond_button = driver.find_elements_by_id('cn.dcpai.auction:id/tv_tab_title')[1]
            drow_button = driver.find_elements_by_id('cn.dcpai.auction:id/tv_tab_title')[2]
            lz_button = driver.find_elements_by_id('cn.dcpai.auction:id/tv_tab_title')[3]
            ACtotalMoney = driver.find_element_by_id('cn.dcpai.auction:id/tv_money_1').text
            ACcanuseMoney = driver.find_element_by_id('cn.dcpai.auction:id/tv_money_2').text
            getreq = V5_ORDER().getAccountInfo_230()
            assert getreq.status_code == 200
            canUseAmount = getreq.json()['balanceAccount']['canUseAmount']  # 可用余额
            waitInAmount = getreq.json()['balanceAccount']['waitInAmount']  # 待入账金额
            ACtotalAmount = getreq.json()['balanceAccount']['totalAmount']  # 总共可用余额
            BindtotalAmount = getreq.json()['bidBondAccount']['totalAmount']  # 总保证金
            BindfrozenAmount = getreq.json()['bidBondAccount']['frozenAmount']  # 冻结的保证金
            BindcanUseAmount = getreq.json()['bidBondAccount']['canUseAmount']  # 解冻的保证金
            getlz = LZShop().findMemberCredit_220()
            assert getlz.status_code == 200
            NumLz = int(float(getlz.json()['result']))
            realnamereq = v5().getMemberDetailInfo_112()
            assert realnamereq.status_code == 200
            realname = realnamereq.json()['realNameAuth']
            assert float(ACcanuseMoney[1:]) == float(canUseAmount)
            assert float(ACtotalMoney[1:]) == float(ACtotalAmount) + float(BindtotalAmount)
            WaitInAccount = driver.find_element_by_id('cn.dcpai.auction:id/tv_wait_in_amount').text
            WaitInAccount = float(str(WaitInAccount).split('¥')[1])
            assert WaitInAccount == float(waitInAmount)
            bidBond_button.click()
            BidBondTotal = driver.find_element_by_id('cn.dcpai.auction:id/tv_bid_bond').text
            BidBondTotal = float(BidBondTotal[1:])
            assert float(BindtotalAmount) == BidBondTotal
            BidBondCansue = driver.find_element_by_id('cn.dcpai.auction:id/tv_money_1').text
            BidBondCansue = float(BidBondCansue[6:])
            assert BidBondCansue == float(BindcanUseAmount)
            switch_to_AC = driver.find_element_by_id('cn.dcpai.auction:id/btn_turn')
            if BidBondCansue > 0:
                assert switch_to_AC.is_enabled() == True
            else:
                assert switch_to_AC.is_enabled() == False
            BidBondFrozen = driver.find_element_by_id('cn.dcpai.auction:id/tv_money_2').text
            assert float(BidBondFrozen[6:]) == float(BindfrozenAmount)
            lz_button.click()
            lznum = driver.find_element_by_id('tv_loong_num').text
            assert int(lznum) == NumLz
            goto_lzshop = driver.find_element_by_id('cn.dcpai.auction:id/tv_loong_go')
            assert goto_lzshop.is_displayed() == True
            goto_lzshop.click()
            driver.implicitly_wait(1)
            assert driver.current_activity == '.loong.LoongMallActivity'
            driver.back()
            drow_button.click()
            time.sleep(1)
            if realname == False:
                assert driver.find_element_by_id('message').is_displayed() == True
                assert driver.find_element_by_id('message').text == '您尚未实名认证，请前往认证'
                EscButton = driver.find_element_by_name('取消')
                SureButton = driver.find_element_by_name('前往')
                assert EscButton.is_enabled() == SureButton.is_enabled() == True
                SureButton.click()
                driver.implicitly_wait(2)
                assert driver.current_activity == '.activity.RealNameAuthActivity'
                assert driver.find_element_by_id('et_real_name').text == '请输入真实姓名'
                assert driver.find_element_by_id('tv_card_type').text == '请选择证件类型'
                assert driver.find_element_by_id('et_card_num').text == '请输入证件号码'
                assert driver.find_element_by_id('tv_title').text == '实名认证'
                assert driver.find_element_by_id('iv_auth_file2').is_displayed() == True
                assert driver.find_element_by_id('iv_auth_file1').is_displayed() == True
                print(f'当前用户{self.username}未进行实名认证。提现需要实名认证后方可执行')
            else:
                assert driver.find_element_by_id('et_name').is_enabled() == True
                assert driver.find_element_by_id('tv_bank_name').is_enabled() == True
                assert driver.find_element_by_id('et_card_num').is_enabled() == True
                assert driver.find_element_by_id('tv_select_area').is_enabled() == True
                assert driver.find_element_by_id('et_bank_address').is_enabled() == True
                assert driver.find_element_by_id('et_input_money').is_enabled() == True
                assert driver.find_element_by_id('et_input_pay_pwd').is_enabled() == True
                assert driver.find_element_by_id('et_input_code').is_enabled() == True
                assert driver.find_element_by_id('btn_get_code').is_enabled() == True
            driver.back()
            assert driver.current_activity == '.MainActivity'
        except:
            assert True == False

    # 个人资料信息
    def into_myinformation(self, driver):
        try:
            PulicClass().Login(driver)
            getreq = v5().getMemberDetailInfo_112()
            assert getreq.status_code == 200
            zangNum = getreq.json()['zangNum']
            name = getreq.json()['name']
            getAddress = V5_ORDER().doGetAddress_112()
            assert getAddress.status_code == 200
            AddrTotal = len(getAddress.json())
            ele_userinfo = Config(MinePage).get('money_manager')
            UserInfoButton = driver.find_element_by_id(ele_userinfo)
            UserInfoButton.click()
            driver.implicitly_wait(2)
            assert driver.current_activity == '.activity.MyInfoActivity'
            assert driver.find_element_by_id('tv_title').text == '我的资料'
            APP_Username = driver.find_element_by_id('tv_nickname')
            assert APP_Username.text == name
            APP_Username.click()
            assert driver.current_activity == '.activity.NickNameModifyActivity'
            assert driver.find_element_by_id('tv_title').text == '修改昵称'
            assert driver.find_element_by_id('et_nickname').text == name
            driver.back()
            assert driver.find_element_by_id('tv_user_id').text == zangNum
            sexButton = driver.find_element_by_id('rl_sex_type')
            sexButton.click()
            assert sexButton.is_enabled() == False
            SecondText = driver.find_elements_by_class_name('android.widget.TextView')[1]
            Man = driver.find_element_by_name('男')
            Women = driver.find_element_by_name('女')
            if SecondText.text != '女':
                driver.drag_and_drop(Man, Women)
                driver.find_element_by_name('确定').click()  # 修改性别
                time.sleep(1)
                assert driver.find_element_by_id('tv_sex').text == '男'
            else:
                driver.drag_and_drop(Women, Man)
                driver.find_element_by_name('确定').click()  # 修改性别
                time.sleep(1)
                assert driver.find_element_by_id('tv_sex').text == '女'
            AreaButton = driver.find_element_by_id('rl_area')
            AreaButton.click()
            driver.implicitly_wait(1)
            assert driver.current_activity == '.activity.CityPickerActivity'
            assert driver.find_element_by_id('tv_title').text == '城市选择'
            serachText = driver.find_element_by_id('et_search')
            assert serachText.text == '请输入城市名或拼音', u'进入修改城区界面后页面默认值'
            AreaText = random.choice(['成都', '北京', '上海'])
            serachText.clear()
            serachText.send_keys(AreaText)
            serachResult = driver.find_element_by_id('tv_item_result_listview_name')
            assert serachResult.text == AreaText
            serachResult.click()
            assert driver.find_element_by_id('tv_area').text == AreaText, u'地区修改后展示成功'
            driver.find_element_by_id('rl_interest_hobby').click()     # 点击修改收藏爱好
            driver.implicitly_wait(2)
            assert driver.current_activity == '.activity.InterestHobbyModifyActivity'
            assert driver.find_element_by_id('tv_title').text == '收藏爱好'
            TextBox = driver.find_element_by_id('et_interest_hobby')
            TextBox.clear()
            InterestText = '古玉、珠宝'
            TextBox.send_keys(InterestText)
            driver.find_element_by_id('btn_right').click()     # 点击保存
            assert driver.current_activity == '.activity.MyInfoActivity'
            assert driver.find_element_by_id('tv_interest_hobby').text == InterestText
            driver.find_element_by_id('rl_diy_sign').click()   # 点击个性签名
            assert driver.current_activity == '.activity.DiySignModifyActivity'
            assert driver.find_element_by_id('tv_title').text == '个性签名'
            SignTextBox = driver.find_element_by_id('et_diy_sign')
            SignTextBox.clear()
            InputText = '如果不爱了就不要勉为其难'
            SignTextBox.send_keys(InputText)
            driver.find_element_by_id('btn_right').click()  # 点击保存
            assert driver.current_activity == '.activity.MyInfoActivity'
            assert driver.find_element_by_id('tv_diy_sign').text == InputText
            driver.find_element_by_id('rl_address_manager').click()    # 点击进入地址管理界面
            assert driver.current_activity == '.activity.AddressManagerActivity'
            assert driver.find_element_by_id('tv_title').text == '地址管理'
            if AddrTotal > 0:
                AdddrList = driver.find_elements_by_xpath\
                    ('//*[contains(@resource-id, "lv_address_list")]/android.widget.LinearLayout')
                assert len(AdddrList) <= AddrTotal
                for i in range(len(AdddrList)-1):
                    EveryAddrList = AdddrList[i]
                    Name_Tel = EveryAddrList.find_element_by_id('tv_contact_us').text
                    Name_Tel = str(Name_Tel).replace(' ', '')
                    ApiName_Tel = getAddress.json()[i]['receiverName'] + getAddress.json()[i]['receiverPhone']
                    assert Name_Tel == ApiName_Tel
                    DetailAddr = EveryAddrList.find_element_by_id('tv_address').text.split(':')[1].replace(' ', '')
                    ApiDetailAddr = (getAddress.json()[i]['strucAddr'] + getAddress.json()[i]['detailAddr']).replace(' ', '')
                    assert DetailAddr == ApiDetailAddr
                    if getAddress.json()[i]['defaultOne']:
                        assert EveryAddrList.find_element_by_id('cb_default_one').is_enabled() == False
                    else:
                        assert EveryAddrList.find_element_by_id('cb_default_one').is_enabled() == True
                    assert EveryAddrList.find_element_by_id('btn_edit').is_enabled() == True
                    assert EveryAddrList.find_element_by_id('btn_delete').is_enabled() == True
            driver.find_element_by_id('btn_right').click()             # 点击新增地址
            assert driver.current_activity == '.activity.NewAddressActivity'
            assert driver.find_element_by_id('tv_title').text == '添加地址'
            NewUserName = ''.join(random.sample(string.ascii_letters, 4))
            NewTel = random.randint(13855550000, 13855559999)
            NewPost = ''.join(random.sample(string.digits, 6))
            NewDetailAddr = '中央路%d号' %random.randint(1, 100)
            UserName_TextBox = driver.find_element_by_id('et_username')
            UserName_TextBox.clear()
            UserName_TextBox.send_keys(NewUserName)
            UserTel_TextBox = driver.find_element_by_id('et_mobile')
            UserTel_TextBox.clear()
            UserTel_TextBox.send_keys(NewTel)
            UserPostCode_TextBox = driver.find_element_by_id('et_zip_code')
            UserPostCode_TextBox.clear()
            UserPostCode_TextBox.send_keys(NewPost)
            UserArea_TextBox = driver.find_element_by_id('et_address_area')
            UserArea_TextBox.click()
            ScrollView1 = driver.find_elements_by_xpath('//*[@class="android.widget.ScrollView"]')[0]   # 省~直辖市
            ScrollView2 = driver.find_elements_by_xpath('//*[@class="android.widget.ScrollView"]')[1]   # 区~地级市
            ScrollView3 = driver.find_elements_by_xpath('//*[@class="android.widget.ScrollView"]')[2]   # 区
            ScrollView1_List = ScrollView1.find_elements_by_class_name('android.widget.TextView')
            ScrollView1_Text1 = ScrollView1_List[0]
            ScrollView1_Text2 = ScrollView1_List[-1]
            [driver.drag_and_drop(ScrollView1_Text1, ScrollView1_Text2) for i in range(random.randint(2,5))]
            time.sleep(1)
            ScrollView1_Text3 = ScrollView1_List[int(len(ScrollView1_List) / 2)].text
            ScrollView2_List = ScrollView2.find_elements_by_class_name('android.widget.TextView')
            ScrollView2_Text1 = ScrollView2_List[0]
            ScrollView2_Text2 = ScrollView2_List[-1]
            [driver.drag_and_drop(ScrollView2_Text1, ScrollView2_Text2) for i in range(random.randint(1, 3))]
            time.sleep(1)
            ScrollView2_Text3 = ScrollView2_List[int(len(ScrollView2_List) / 2)].text
            ScrollView3_List = ScrollView3.find_elements_by_class_name('android.widget.TextView')
            ScrollView3_Text1 = ScrollView3_List[0]
            ScrollView3_Text2 = ScrollView3_List[-1]
            [driver.drag_and_drop(ScrollView3_Text1, ScrollView3_Text2) for i in range(random.randint(1, 3))]
            time.sleep(1)
            ScrollView3_Text3 = ScrollView3_List[int(len(ScrollView3_List) / 2)].text
            driver.find_element_by_name('确定').click()
            print(ScrollView1_Text3, ScrollView2_Text3, ScrollView3_Text3)
            assert str(driver.find_element_by_id('et_address_area').text).strip().replace(' ','') == \
                   str(ScrollView1_Text3 + ScrollView2_Text3 + ScrollView3_Text3).strip()
            UserDetaile_TextBox = driver.find_element_by_id('et_address_desc')
            UserDetaile_TextBox.clear()
            UserDetaile_TextBox.send_keys(NewDetailAddr)
            driver.find_element_by_name('保存').click()
            [cmd(driver).up_swipe() for i in range(int(AddrTotal/7)*5)]
            NewAdddrList = driver.find_elements_by_xpath\
                    ('//*[contains(@resource-id, "lv_address_list")]/android.widget.LinearLayout')
            LastAddr = NewAdddrList[-1]
            Last_Name_Tel = LastAddr.find_element_by_id('tv_contact_us').text
            Last_Name_Tel = str(Last_Name_Tel).replace(' ', '')
            assert Last_Name_Tel == NewUserName + str(NewTel)
            LastDetailAddr = LastAddr.find_element_by_id('tv_address').text.split(':')[1].replace(' ', '')
            assert LastDetailAddr == ScrollView1_Text3 + ScrollView2_Text3 + ScrollView3_Text3 +  NewDetailAddr
            LastAddr.find_element_by_id('btn_delete').click()       # 删除最后一个地址信息
            assert driver.find_elements_by_xpath(
                '//*[contains(@resource-id, "lv_address_list")]/android.widget.LinearLayout')[-1].text != Last_Name_Tel
            driver.back()
            driver.find_element_by_id('rl_password_manager').click()
            assert driver.current_activity == '.activity.PasswordManagerActivity'
            assert driver.find_element_by_id('tv_title').text == '密码管理'
            driver.back()
            driver.back()
        except:
            assert True == False

    # 我的门派信息查看
    def into_myschool(self, dirver):
        try:
            PulicClass().Login(driver)
            ele_my_forum = Config(MinePage).get('my_forum')
            driver.find_element_by_id(ele_my_forum).click()
            driver.implicitly_wait(2)
            assert driver.current_activity == '.activity.MySchoolListActivity'
            assert driver.find_element_by_name('我的门派').is_displayed() == True
            assert driver.find_element_by_id('school_set').is_displayed() == True
            SchoolList = driver.find_elements_by_xpath('//*[contains(@resource-id, "school_list_Recycler")]')
            Num = 0
            getschool = V5_BBS().findMyForumPage_300()
            assert getschool.status_code == 200
            Total = getschool.json()['total']
            for EverySchool in SchoolList:
                API_Reputation = getschool.json()['rows'][Num]['reputation']
                API_postCount = getschool.json()['rows'][Num]['postCount']
                API_memberCount = getschool.json()['rows'][Num]['memberCount']
                API_Name = getschool.json()['rows'][Num]['declaration']
                SchoolName = EverySchool.find_element_by_id('item_school_name')
                SchoolText = SchoolName.text
                SchoolName.click()
                driver.implicitly_wait(2)
                assert driver.current_activity == '.activity.SchoolInfoActivity'
                assert driver.find_element_by_id('title_txt').text == SchoolText == API_Name
                School_Detaile_Page_reputationPost = driver.find_element_by_id('school_describe_tv').text
                assert ''.join(re.findall('\d',School_Detaile_Page_reputationPost)) == API_Reputation+API_postCount
                School_Detaile_Page_MemberTotal = driver.find_element_by_id('school_member_tv').text
                assert ''.join(re.findall('\d', School_Detaile_Page_MemberTotal)) == API_memberCount
                driver.back()
                SchoolInfo = EverySchool.find_element_by_id('item_school_info')
                SchoolInfoNumText = ''.join(re.findall('\d', SchoolInfo.text))
                assert SchoolInfoNumText == API_Reputation+API_postCount+API_memberCount
                Num += 1
            SetButton = driver.find_element_by_id('school_set')
            assert SetButton.text == '设置'
            SetButton.click()
            assert SetButton.text == '完成'
            try:
                QuitButton = WebDriverWait(driver, timeout=5).until\
                    (EC.visibility_of_element_located((By.XPATH, '//*[contains(@resource-id, "school_quit_tv")]')))
                QuitButton.click()
                driver.implicitly_wait(1)
                Notice = WebDriverWait(driver, timeout=5).until\
                    (EC.visibility_of_element_located((By.XPATH, '//*[contains(@resource-id, "alertTitle")]')))
                Message = WebDriverWait(driver, timeout=5).until\
                    (EC.visibility_of_element_located((By.XPATH, '//*[contains(@resource-id, "message")]')))
                assert '大侠您是否要退出' in Message.text
                GroupName = Message.text.strip('大侠您是否要退出').strip('?')
                SureDelete = WebDriverWait(driver, timeout=5).until\
                    (EC.visibility_of_element_located((By.NAME, '确定')))
                SureDelete.click()
                driver.implicitly_wait(1)
                SetButton.click()
                try:
                    APPGroupName = WebDriverWait(driver,timeout=5).until\
                        (EC.visibility_of_element_located((By.NAME, GroupName)))
                    print(f'退出门派功能存在问题')
                except:
                    print(f'退出门派功能正常')
            except:
                SetButton.click()
            driver.back()
        except Exception as e:
            assert True == False

    # 我的江湖信息查看
    def into_myRuneScape(self, driver):
        try:
            PulicClass().Login(driver)
            UnreadReq = V5_BBS().getUnReadMsgCount_201()
            assert UnreadReq.status_code == 200
            UnreadTotal = int(UnreadReq.json()['upvoteMsgCount']) + int(UnreadReq.json()['commentMsgCount']) + \
                          int(UnreadReq.json()['fansMsgCount']) + int(UnreadReq.json()['sysMsgCount']) + \
                          int(UnreadReq.json()['focusMsgCount']) + int(UnreadReq.json()['forumMsgCount'])
            MyFocusMemberPostPage = V5_BBS().findMyFocusMemberPostPage_300()
            assert MyFocusMemberPostPage.status_code == 200
            MxgCount = V5_BBS().findCount_500()
            assert MxgCount.status_code == 200
            MemberInfo = v5().getMemberDetailInfo_112()
            MemberLevel = MemberInfo.json()['level']
            MyJH = driver.find_element_by_id(Config(MinePage).get('my_jianghu'))
            MyJH.click()
            driver.implicitly_wait(5)
            assert driver.current_activity == '.activity.JiangHuActivity'
            assert driver.find_element_by_id('level_tv').text == 'V'+MemberLevel    # 会员等级
            MsgButton = driver.find_element_by_id('title_right')
            if UnreadTotal > 0:
                assert driver.find_element_by_id('message_txt').text == str(UnreadTotal)   # 未读信息
            MsgButton.click()
            driver.implicitly_wait(2)
            assert driver.current_activity == '.fragment.MessageActivity'
            assert driver.find_element_by_id('tv_title').text == '消息'
            if int(UnreadReq.json()['sysMsgCount']) != 0:
                assert driver.find_element_by_id('tv_sys_count').text == UnreadReq.json()['sysMsgCount']
            driver.find_element_by_id('rl_sys').click()    # 点击进入未读消息列表页
            driver.implicitly_wait(2)
            assert driver.current_activity == '.activity.ClickLikeListActivity'
            EditButton = driver.find_element_by_id('btn_right')
            driver.implicitly_wait(1)
            EditButton.click()
            driver.implicitly_wait(2)
            assert driver.find_element_by_id('btn_right').text == '取消'
            driver.find_element_by_id('btn_right').click()
            driver.back()
            driver.find_element_by_id('rl_forum').click()
            assert driver.find_element_by_id('tv_title').text == '门派'
            EditButton1 = driver.find_element_by_id('btn_right')
            EditButton1.click()
            driver.implicitly_wait(2)
            assert EditButton1.text == '取消'
            driver.back()
            driver.back()
            assert driver.find_element_by_id('topic_txt').text == MxgCount.json()['postCount']
            assert driver.find_element_by_id('comment_txt').text == MxgCount.json()['commentCount']
            assert driver.find_element_by_id('follow_txt').text == MxgCount.json()['focusCount']
            assert driver.find_element_by_id('fans_txt').text == MxgCount.json()['fansCount']
            assert driver.find_element_by_id('good_txt').text == MxgCount.json()['voteCount']
            assert driver.find_element_by_id('fanctions_txt').text == MxgCount.json()['forumCount']
            assert driver.find_element_by_id('collect_txt').text == MxgCount.json()['favoriteCount']
            assert driver.find_element_by_id('intergal_txt').text == MxgCount.json()['creditCount']
            if int(MyFocusMemberPostPage.json()['total']) >= 2:
                NUMBER = 2
            else:
                NUMBER == int(MyFocusMemberPostPage.json()['total'])
            for i in range(NUMBER):
                INfoName = driver.find_elements_by_id('info_name')[i]
                INfoLev = driver.find_elements_by_id('info_level')[i]
                INfoSeeButtom = driver.find_elements_by_id('info_see')[i]
                INfoCommentButtom = driver.find_elements_by_id('info_comment')[i]
                INfoLikeButtom = driver.find_elements_by_id('info_fabulous')[i]
                originalnum = INfoLikeButtom.text
                assert INfoName.text == \
                       MyFocusMemberPostPage.json()['rows'][i]['memberNickname']
                assert INfoLev.text == \
                       'V' + MyFocusMemberPostPage.json()['rows'][i]['memberLevel']
                INfoName.click()
                assert driver.current_activity == '.activity.MyJiangHuActivity'
                assert driver.find_element_by_id('tv_nickname').text == INfoName.text
                driver.back()
                INfoSeeButtom.click()
                driver.implicitly_wait(2)
                assert driver.current_activity == '.activity.RiversLakesTopicDetailActivity'
                assert driver.find_element_by_id('tv_title').text == '话题详情'
                try:
                    PlayerButton = WebDriverWait(driver, timeout=5).until\
                        (EC.visibility_of_element_located((By.ID, "topic_detail_header_play")))
                    PlayerButton.click()
                    time.sleep(10)
                    assert driver.current_activity == '.activity.VideoPlayActivity'
                except:
                    try:
                        ImgPlayerButton = WebDriverWait(driver, timeout=5).until\
                            (EC.visibility_of_element_located((By.ID, "topic_detail_header_attachments_imageView")))
                        ImgPlayerButton.click()
                        driver.implicitly_wait(5)
                        assert driver.current_activity == '.activity.ImagePagerActivity'
                    except:
                        ShareButton = WebDriverWait(driver, timeout=5).until\
                            (EC.visibility_of_element_located
                             ((By.XPATH, "//*[contains(@resource-id, 'exquitste_topic_detail_share')]")))
                        ShareButton.click()
                        driver.implicitly_wait(5)
                finally:
                    driver.back()
                    PulicClass().WBShare(driver)
                    PulicClass().WXShare(driver)
                    PulicClass().WXQShare(driver)
                driver.back()
                INfoCommentButtom.click()
                driver.implicitly_wait(2)
                assert driver.current_activity == '.activity.RiversLakesTopicDetailActivity'
                assert driver.find_element_by_id('tv_title').text == '话题详情'
                ContentText = PulicClass().Chinese(8)
                TextBox = driver.find_element_by_id('rivers_lakesdetail_comment_input_view')
                TextBox.send_keys(ContentText)
                driver.find_element_by_id('topic_detail_send_reply_button').click()
                TextBox.click()
                driver.find_element_by_id('topic_detail_emotion_button').click()
                driver.find_elements_by_id('iv_emotion')[random.randint(0,5)].click()
                driver.find_element_by_id('topic_detail_send_reply_button').click()
                # 尝试测试删除信息
                try:
                    ContentTotalPAGE = driver.find_element_by_id('river_lake_topic_detail_total_comment_tv')
                    ContentTotalPAGE = ''.join(re.findall('\d', ContentTotalPAGE.text))
                    for i in range(int(ContentTotalPAGE)):
                        cmd(driver).up_swipe()
                    assert driver.find_elements_by_id('river_lakes_comment_content_tv')[-1].text == ContentText
                    driver.find_elements_by_id('topic_detail_comment_delete_tv')[-2].click()   # 删除倒数第二条评论
                    driver.implicitly_wait(2)
                    NOTICE = driver.find_element_by_id('exquisite_announcement_content_tv')
                    assert NOTICE.text == '提示'
                    SUREDELETE = driver.find_element_by_id('dialog_sure_tv')
                    assert SUREDELETE.text == '删除评论'
                    SUREDELETE.click()
                    driver.implicitly_wait(2)
                    assert driver.find_elements_by_id('river_lakes_comment_content_tv')[-1].text != ContentText
                    driver.back()
                except:
                    print(f'删除评论可能存在问题，请手动验证')
                    driver.back()
                INfoLikeButtom.click()
                driver.implicitly_wait(5)
                Nownum = INfoLikeButtom.text
                assert int(originalnum) + 1 == int(Nownum)
            driver.back()
        except:
            assert True == False

    # 进入待付款页面--且判断首页显示的几个订单是否正确
    def into_waitpayOrder(self, driver):
        PulicClass().Login(driver)
        waitreq = V5_ORDER().findBuyerWaitPayPage_500()
        assert waitreq.status_code == 200
        ele_waitorder = Config(MinePage).get('my_order_obligation')
        ele_title = Config(BuyOrderPage).get('orderTitle')
        ele_display_area = Config(BuyOrderPage).get('display_area')
        try:
            driver.find_element_by_id(ele_waitorder).click()
            time.sleep(1)
            assert driver.current_activity == Config(ActivityPath).get('BuyOrder')
            assert driver.find_element_by_name('待付款').is_displayed() == True
            assert driver.find_element_by_id(ele_title).text == '我的订单'
            SUM = 0
            length = int(waitreq.json()['total'])
            if length > 0:
                if length >= 3:
                    ftemp = 3
                else:
                    ftemp = length
                for i in range(ftemp):
                    Temp = SUM
                    OrderNum = len(waitreq.json()['rows'][i]['orderItemList'])  # 当前订单商品总数
                    SUM = SUM + OrderNum
                    countDownTime = waitreq.json()['rows'][i]['countDownTime']  # 剩余发货时间
                    bidModel = waitreq.json()['rows'][i]['bidModel']
                    App_shopname = driver.find_elements_by_id('order_item_name')[i]
                    if bidModel == 'PRODUCT_SHOP':
                        for j in range(Temp, SUM):
                            lotname = waitreq.json()['rows'][i]['orderItemList'][j - Temp]['lotName']  # 商品名称
                            num = waitreq.json()['rows'][i]['orderItemList'][j - Temp]['quantity']  # 商品购买数量
                            salesprice = waitreq.json()['rows'][i]['orderItemList'][j - Temp]['salesPrice']
                            App_productName = driver.find_elements_by_id('order_item_good_name')[j]
                            # 商品名字
                            assert str(App_productName.text).replace('   ', '') == lotname + 'x%s' % num
                            App_proudctPrice = driver.find_elements_by_id('order_item_good_price')[j]
                            APP_every_productPrice = int(float(''.join(re.findall('\d', App_proudctPrice.text))))
                            # 成交价
                            assert APP_every_productPrice == int(float(salesprice))
                            # 成交时间
                            sellDate = waitreq.json()['rows'][i]['orderItemList'][j - Temp]['sellDate']
                            App_sellDate = driver.find_elements_by_id('order_item_good_time')[j]
                            assert App_sellDate.text[5:] == sellDate[0:-3]
                        sellerShopName = waitreq.json()['rows'][i]['sellerShopName'][0:10]  # 店铺名称
                        assert App_shopname.text == sellerShopName
                        App_Order = driver.find_elements_by_id('order_item_state_money')[i]
                        App_Order_Price = ''.join(re.findall('\d', App_Order.text.split('/')[0]))
                        App_Order_Postage = ''.join(re.findall('\d', App_Order.text.split('/')[1]))
                        hammerPrice = waitreq.json()['rows'][i]['hammerPrice']
                        postage = waitreq.json()['rows'][i]['postage']
                        assert int(float(App_Order_Price)) == int(float(hammerPrice))
                        assert float(App_Order_Postage) == float(postage)
                    else:
                        sum_price = 0
                        for j in range(Temp, SUM):
                            lotname = waitreq.json()['rows'][i]['orderItemList'][j - Temp]['lotName']  # 商品名称
                            App_productName = driver.find_elements_by_id('order_item_good_name')[j]
                            assert str(App_productName.text) == lotname
                            salesprice = waitreq.json()['rows'][i]['orderItemList'][j - Temp]['hammerPrice']
                            App_proudctPrice = driver.find_elements_by_id('order_item_good_price')[j]
                            App_everorder_price = int(float(''.join(re.findall('\d', App_proudctPrice.text))))
                            assert App_everorder_price == int(float(salesprice))
                            sum_price += App_everorder_price
                            lotBuyerCommissionPercent = waitreq.json()['rows'][i]['lotBuyerCommissionPercent']
                            sellDate = waitreq.json()['rows'][i]['orderItemList'][j - Temp]['sellDate']
                            App_sellDate = driver.find_elements_by_id('order_item_good_time')[j]
                            assert App_sellDate.text[5:] == sellDate[0:-3]
                        sellerName = waitreq.json()['rows'][i]['sellerNickname'][0:10]
                        assert App_shopname.text == sellerName or sellerName in App_shopname.text
                        App_Order = driver.find_elements_by_id('order_item_state_money')[i]
                        App_Order_Price = ''.join(re.findall('\d', App_Order.text.split('/')[0]))
                        App_Order_Postage = ''.join(re.findall('\d', App_Order.text.split('/')[2]))
                        App_Order_YJ = float(str(App_Order.text.split('/')[1]).split('¥')[1].strip())
                        hammerPrice = waitreq.json()['rows'][i]['hammerPrice']
                        postage = waitreq.json()['rows'][i]['postage']
                        buyerCommission = waitreq.json()['rows'][i]['buyerCommission']
                        assert int(float(App_Order_Price)) == int(float(hammerPrice)) == sum_price
                        assert float(App_Order_Postage) == float(postage)
                        assert float(App_Order_YJ) == float(buyerCommission) == \
                               float(sum_price * float(lotBuyerCommissionPercent)) / 100
                    App_remindtime = driver.find_elements_by_id('order_item_state_time')[i]
                    remindtime = ''.join(re.findall('\d', App_remindtime.text))
                    # assert remindtime not in ['00', '000'], u'倒计时都为0时还再前端显示，则存在bug'
                    pay_button = driver.find_elements_by_id('buyers_payment')[i]
                    assert pay_button.is_enabled() == pay_button.is_displayed() == True
            else:
                print(f'当前账号无待付款的订单')
        except:
            assert True == False

    # 返回到主界面
    def buyorder_reback_mine(self, driver):
        try:
            if '.shop.order.ui.OrderActivity' in driver.current_activity:
                backbutton = driver.find_element_by_id(Config(BuyOrderPage).get('backButton'))
                backbutton.click()
                assert driver.current_activity == '.MainActivity'
        except Exception as e:
            raise e

    # 进入待发货界面--验证其相关内容
    def into_waitsendOrder(self, driver):
        PulicClass().Login(driver)
        waitsendreq = V5_ORDER().findBuyerWaitSendPage_500()
        assert waitsendreq.status_code == 200
        ele_waitsendorder = Config(MinePage).get('my_order_waitsend')
        ele_title = Config(BuyOrderPage).get('orderTitle')
        ele_display_area = Config(BuyOrderPage).get('display_area')
        try:
            driver.find_element_by_id(ele_waitsendorder).click()
            time.sleep(1)
            assert driver.current_activity == Config(ActivityPath).get('BuyOrder')
            assert driver.find_element_by_name('待发货').is_displayed() == True
            assert driver.find_element_by_id(ele_title).text == '我的订单'
            SUM = 0
            length = int(waitsendreq.json()['total'])
            if length > 0:
                if length >= 3:
                    ftemp = 3
                else:
                    ftemp = length
                for i in range(ftemp):
                    Temp = SUM
                    OrderNum = len(waitsendreq.json()['rows'][i]['orderItemList'])  # 当前订单商品总数
                    SUM = SUM + OrderNum
                    countDownTime = waitsendreq.json()['rows'][i]['countDownTime']  # 剩余发货时间
                    bidModel = waitsendreq.json()['rows'][i]['bidModel']
                    App_shopname = driver.find_elements_by_id('order_item_name')[i]
                    if bidModel == 'PRODUCT_SHOP':
                        for j in range(Temp, SUM):
                            lotname = waitsendreq.json()['rows'][i]['orderItemList'][j-Temp]['lotName']  # 商品名称
                            num = waitsendreq.json()['rows'][i]['orderItemList'][j-Temp]['quantity']  # 商品购买数量
                            salesprice = waitsendreq.json()['rows'][i]['orderItemList'][j-Temp]['salesPrice']
                            App_productName = driver.find_elements_by_id('order_item_good_name')[j]
                            # 商品名字
                            assert str(App_productName.text).replace('   ', '') == lotname + 'x%s' % num
                            App_proudctPrice = driver.find_elements_by_id('order_item_good_price')[j]
                            APP_every_productPrice = int(float(''.join(re.findall('\d', App_proudctPrice.text))))
                            # 成交价
                            assert APP_every_productPrice == int(float(salesprice))
                            # 成交时间
                            sellDate = waitsendreq.json()['rows'][i]['orderItemList'][j-Temp]['sellDate']
                            App_sellDate = driver.find_elements_by_id('order_item_good_time')[j]
                            assert App_sellDate.text[5:] == sellDate[0:-3]
                        sellerShopName = waitsendreq.json()['rows'][i]['sellerShopName'][0:10]  # 店铺名称
                        assert App_shopname.text == sellerShopName
                        App_Order = driver.find_elements_by_id('order_item_state_money')[i]
                        App_Order_Price = ''.join(re.findall('\d', App_Order.text.split('/')[0]))
                        App_Order_Postage = ''.join(re.findall('\d', App_Order.text.split('/')[1]))
                        hammerPrice = waitsendreq.json()['rows'][i]['hammerPrice']
                        postage = waitsendreq.json()['rows'][i]['postage']
                        assert int(float(App_Order_Price)) == int(float(hammerPrice))
                        assert float(App_Order_Postage) == float(postage)
                    else:
                        sum_price = 0
                        for j in range(Temp, SUM):
                            lotname = waitsendreq.json()['rows'][i]['orderItemList'][j-Temp]['lotName']  # 商品名称
                            App_productName = driver.find_elements_by_id('order_item_good_name')[j]
                            assert str(App_productName.text) == lotname
                            salesprice = waitsendreq.json()['rows'][i]['orderItemList'][j-Temp]['hammerPrice']
                            App_proudctPrice = driver.find_elements_by_id('order_item_good_price')[j]
                            App_everorder_price = int(float(''.join(re.findall('\d', App_proudctPrice.text))))
                            assert App_everorder_price == int(float(salesprice))
                            sum_price += App_everorder_price
                            lotBuyerCommissionPercent = waitsendreq.json()['rows'][i]['lotBuyerCommissionPercent']
                            sellDate = waitsendreq.json()['rows'][i]['orderItemList'][j - Temp]['sellDate']
                            App_sellDate = driver.find_elements_by_id('order_item_good_time')[j]
                            assert App_sellDate.text[5:] == sellDate[0:-3]
                        sellerName = waitsendreq.json()['rows'][i]['sellerNickname'][0:10]
                        assert App_shopname.text == sellerName or sellerName in App_shopname.text
                        App_Order = driver.find_elements_by_id('order_item_state_money')[i]
                        App_Order_Price = ''.join(re.findall('\d', App_Order.text.split('/')[0]))
                        App_Order_Postage = ''.join(re.findall('\d', App_Order.text.split('/')[2]))
                        App_Order_YJ = float(str(App_Order.text.split('/')[1]).split('¥')[1].strip())
                        hammerPrice = waitsendreq.json()['rows'][i]['hammerPrice']
                        postage = waitsendreq.json()['rows'][i]['postage']
                        buyerCommission = waitsendreq.json()['rows'][i]['buyerCommission']
                        assert int(float(App_Order_Price)) == int(float(hammerPrice)) == sum_price
                        assert float(App_Order_Postage) == float(postage)
                        assert float(App_Order_YJ) == float(buyerCommission) == \
                               float(sum_price * float(lotBuyerCommissionPercent))/100
                    App_remindtime = driver.find_elements_by_id('order_item_state_time')[i]
                    remindtime = ''.join(re.findall('\d', App_remindtime.text))
                    # assert remindtime != '00'
                    buyers_refund_button = driver.find_elements_by_id('buyers_refund')[i]
                    assert buyers_refund_button.is_displayed() == True
                    remind_send_button = driver.find_elements_by_id('buyers_deliver_goods')[i]
                    assert remind_send_button.is_displayed() == True
            else:
                print(f'当前买家账号{self.username}不存在待发货的订单')
        except:
            assert True == False

    # 进入待收货订单界面，如果存在订单验证前三个订单信息是否正确
    def into_Receiving_Order(self, driver):
        PulicClass().Login(driver)
        wait_reciving = V5_ORDER().findBuyerWaitReceivePage_500()
        assert wait_reciving.status_code == 200
        ele_receiving = Config(MinePage).get('my_order_waittake')
        ele_title = Config(BuyOrderPage).get('orderTitle')
        try:
            driver.find_element_by_id(ele_receiving).click()
            time.sleep(1)
            assert driver.current_activity == Config(ActivityPath).get('BuyOrder')
            assert driver.find_element_by_name('待收货').is_displayed() == True
            assert driver.find_element_by_id(ele_title).text == '我的订单'
            SUM = 0
            length = int(wait_reciving.json()['total'])
            if length > 0:
                if length >=3:
                    ftemp = 3
                else:
                    ftemp = length
                for i in range(ftemp):
                    Temp = SUM
                    OrderNum = len(wait_reciving.json()['rows'][i]['orderItemList'])  # 当前订单商品总数
                    SUM = SUM + OrderNum
                    countDownTime = wait_reciving.json()['rows'][i]['countDownTime']  # 订单最迟自动收货时间
                    bidModel = wait_reciving.json()['rows'][i]['bidModel']
                    App_shopname = driver.find_elements_by_id('order_item_name')[i]
                    if bidModel == 'PRODUCT_SHOP':
                        for j in range(Temp, SUM):
                            lotname = wait_reciving.json()['rows'][i]['orderItemList'][j - Temp]['lotName']  # 商品名称
                            num = wait_reciving.json()['rows'][i]['orderItemList'][j - Temp]['quantity']  # 商品购买数量
                            salesprice = wait_reciving.json()['rows'][i]['orderItemList'][j - Temp]['salesPrice']
                            App_productName = driver.find_elements_by_id('order_item_good_name')[j]
                            # 商品名字
                            assert str(App_productName.text).replace('   ', '') == lotname + 'x%s' % num
                            App_proudctPrice = driver.find_elements_by_id('order_item_good_price')[j]
                            APP_every_productPrice = int(float(''.join(re.findall('\d', App_proudctPrice.text))))
                            # 成交价
                            assert APP_every_productPrice == int(float(salesprice))
                            # 成交时间
                            sellDate = wait_reciving.json()['rows'][i]['orderItemList'][j - Temp]['sellDate']
                            App_sellDate = driver.find_elements_by_id('order_item_good_time')[j]
                            assert App_sellDate.text[5:] == sellDate[0:-3]
                        sellerShopName = wait_reciving.json()['rows'][i]['sellerShopName'][0:10]  # 店铺名称
                        assert App_shopname.text == sellerShopName
                        App_Order = driver.find_elements_by_id('order_item_state_money')[i]
                        App_Order_Price = ''.join(re.findall('\d', App_Order.text.split('/')[0]))
                        App_Order_Postage = ''.join(re.findall('\d', App_Order.text.split('/')[1]))
                        hammerPrice = wait_reciving.json()['rows'][i]['hammerPrice']
                        postage = wait_reciving.json()['rows'][i]['postage']
                        assert int(float(App_Order_Price)) == int(float(hammerPrice))
                        assert float(App_Order_Postage) == float(postage)
                    else:
                        sum_price = 0
                        for j in range(Temp, SUM):
                            lotname = wait_reciving.json()['rows'][i]['orderItemList'][j - Temp]['lotName']  # 商品名称
                            App_productName = driver.find_elements_by_id('order_item_good_name')[j]
                            assert str(App_productName.text) == lotname
                            salesprice = wait_reciving.json()['rows'][i]['orderItemList'][j - Temp]['hammerPrice']
                            App_proudctPrice = driver.find_elements_by_id('order_item_good_price')[j]
                            App_everorder_price = int(float(''.join(re.findall('\d', App_proudctPrice.text))))
                            assert App_everorder_price == int(float(salesprice))
                            sum_price += App_everorder_price
                            lotBuyerCommissionPercent = wait_reciving.json()['rows'][i]['lotBuyerCommissionPercent']
                            App_sellDate = driver.find_elements_by_id('order_item_good_time')[j]
                            sellDate = waitreq.json()['rows'][i]['orderItemList'][j - Temp]['sellDate']
                            assert App_sellDate.text[5:] == sellDate[0:-3]
                        sellerName = wait_reciving.json()['rows'][i]['sellerNickname'][0:10]
                        assert sellerName in App_shopname.text
                        App_Order = driver.find_elements_by_id('order_item_state_money')[i]
                        App_Order_Price = ''.join(re.findall('\d', App_Order.text.split('/')[0]))
                        App_Order_Postage = ''.join(re.findall('\d', App_Order.text.split('/')[2]))
                        App_Order_YJ = float(str(App_Order.text.split('/')[1]).split('¥')[1].strip())
                        hammerPrice = wait_reciving.json()['rows'][i]['hammerPrice']
                        postage = wait_reciving.json()['rows'][i]['postage']
                        buyerCommission = wait_reciving.json()['rows'][i]['buyerCommission']
                        assert int(float(App_Order_Price)) == int(float(hammerPrice)) == sum_price
                        assert float(App_Order_Postage) == float(postage)
                        assert float(App_Order_YJ) == float(buyerCommission) == \
                               float(sum_price * float(lotBuyerCommissionPercent)) / 100
                    App_remindtime = driver.find_elements_by_id('order_item_state_time')[i]
                    remindtime = ''.join(re.findall('\d', App_remindtime.text))
                    assert remindtime != '00'
                    retrun_button = driver.find_elements_by_id(Config(BuyOrderPage).get('retrun_button'))[i]
                    check_logistics = driver.find_elements_by_id(Config(BuyOrderPage).get('check_logistics'))[i]
                    delayd_confirm = driver.find_elements_by_id(Config(BuyOrderPage).get('delayd_confirm'))[i]
                    confirm_button = driver.find_elements_by_id(Config(BuyOrderPage).get('confirm_button'))[i]
                    assert retrun_button.is_displayed() == True
                    assert retrun_button.is_enabled() == True
                    assert check_logistics.is_displayed() == True
                    assert check_logistics.is_enabled() == True
                    assert delayd_confirm.is_enabled() == True
                    assert delayd_confirm.is_displayed() == True
                    assert confirm_button.is_displayed() == True
                    assert confirm_button.is_enabled() == True
            else:
                print(f'当前买家账号{self.username}不存在待收货订单')
        except:
            assert True == False

    # 进入待评价订单列表--验证前三个订单的正确行
    def into_Waitcomment_Order(self, driver):
        PulicClass().Login(driver)
        wait_comment = V5_ORDER().findBuyerWaitCommentPage_500()
        assert wait_comment.status_code == 200
        ele_receiving = Config(MinePage).get('my_order_waitcomment')
        ele_title = Config(BuyOrderPage).get('orderTitle')
        try:
            driver.find_element_by_id(ele_receiving).click()
            time.sleep(1)
            assert driver.current_activity == Config(ActivityPath).get('BuyOrder')
            assert driver.find_element_by_name('待评价').is_displayed() == True
            assert driver.find_element_by_id(ele_title).text == '我的订单'
            SUM = 0
            length = int(wait_comment.json()['total'])
            if length > 0:
                if length >=3:
                    ftemp = 3
                else:
                    ftemp = length
                for i in range(ftemp):
                    Temp = SUM
                    OrderNum = len(wait_comment.json()['rows'][i]['orderItemList'])  # 当前订单商品总数
                    SUM = SUM + OrderNum
                    countDownTime = wait_comment.json()['rows'][i]['countDownTime']  # 订单最迟自动收货时间
                    bidModel = wait_comment.json()['rows'][i]['bidModel']
                    App_shopname = driver.find_elements_by_id('order_item_name')[i]
                    if bidModel == 'PRODUCT_SHOP':
                        for j in range(Temp, SUM):
                            lotname = wait_comment.json()['rows'][i]['orderItemList'][j - Temp]['lotName']  # 商品名称
                            num = wait_comment.json()['rows'][i]['orderItemList'][j - Temp]['quantity']  # 商品购买数量
                            salesprice = wait_comment.json()['rows'][i]['orderItemList'][j - Temp]['salesPrice']
                            App_productName = driver.find_elements_by_id('order_item_good_name')[j]
                            # 商品名字
                            assert str(App_productName.text).replace('   ', '') == lotname + 'x%s' % num
                            App_proudctPrice = driver.find_elements_by_id('order_item_good_price')[j]
                            APP_every_productPrice = int(float(''.join(re.findall('\d', App_proudctPrice.text))))
                            # 成交价
                            assert APP_every_productPrice == int(float(salesprice))
                            # 成交时间
                            sellDate = wait_comment.json()['rows'][i]['orderItemList'][j - Temp]['sellDate']
                            App_sellDate = driver.find_elements_by_id('order_item_good_time')[j]
                            assert App_sellDate.text[5:] == sellDate[0:-3]
                        sellerShopName = wait_comment.json()['rows'][i]['sellerShopName'][0:10]  # 店铺名称
                        assert App_shopname.text == sellerShopName
                        App_Order = driver.find_elements_by_id('order_item_state_money')[i]
                        App_Order_Price = ''.join(re.findall('\d', App_Order.text.split('/')[0]))
                        App_Order_Postage = ''.join(re.findall('\d', App_Order.text.split('/')[1]))
                        hammerPrice = wait_comment.json()['rows'][i]['hammerPrice']
                        postage = wait_comment.json()['rows'][i]['postage']
                        assert int(float(App_Order_Price)) == int(float(hammerPrice))
                        assert float(App_Order_Postage) == float(postage)
                    else:
                        sum_price = 0
                        for j in range(Temp, SUM):
                            lotname = wait_comment.json()['rows'][i]['orderItemList'][j - Temp]['lotName']  # 商品名称
                            App_productName = driver.find_elements_by_id('order_item_good_name')[j]
                            assert str(App_productName.text) == lotname
                            salesprice = wait_comment.json()['rows'][i]['orderItemList'][j - Temp]['hammerPrice']
                            App_proudctPrice = driver.find_elements_by_id('order_item_good_price')[j]
                            App_everorder_price = int(float(''.join(re.findall('\d', App_proudctPrice.text))))
                            assert App_everorder_price == int(float(salesprice))
                            sum_price += App_everorder_price
                            lotBuyerCommissionPercent = wait_comment.json()['rows'][i]['lotBuyerCommissionPercent']
                            App_sellDate = driver.find_elements_by_id('order_item_good_time')[j]
                            sellDate = waitreq.json()['rows'][i]['orderItemList'][j - Temp]['sellDate']
                            assert App_sellDate.text[5:] == sellDate[0:-3]
                        sellerName = wait_comment.json()['rows'][i]['sellerNickname'][0:10]
                        assert App_shopname.text == sellerName
                        App_Order = driver.find_elements_by_id('order_item_state_money')[i]
                        App_Order_Price = ''.join(re.findall('\d', App_Order.text.split('/')[0]))
                        App_Order_Postage = ''.join(re.findall('\d', App_Order.text.split('/')[2]))
                        App_Order_YJ = float(str(App_Order.text.split('/')[1]).split('¥')[1].strip())
                        hammerPrice = wait_comment.json()['rows'][i]['hammerPrice']
                        postage = wait_comment.json()['rows'][i]['postage']
                        buyerCommission = wait_comment.json()['rows'][i]['buyerCommission']
                        assert int(float(App_Order_Price)) == int(float(hammerPrice)) == sum_price
                        assert float(App_Order_Postage) == float(postage)
                        assert float(App_Order_YJ) == float(buyerCommission) == \
                               float(sum_price * float(lotBuyerCommissionPercent)) / 100
                    App_remindtime = driver.find_elements_by_id('order_item_state_time')[i]
                    remindtime = ''.join(re.findall('\d',App_remindtime.text))
                    assert remindtime != '00'
                    rebuy_button = driver.find_element_by_id(Config(BuyOrderPage).get('rebuy_button'))[i]
                    comment_button = driver.find_element_by_id(Config(BuyOrderPage).get('comment_button'))[i]
                    assert rebuy_button.is_displayed() == True
                    assert rebuy_button.is_enabled() == True
                    assert comment_button.is_displayed() == True
                    assert comment_button.is_enabled() == True
            else:
                print(f'当前买家账号{self.username}不存在待评价订单')
        except:
            assert True == False

    # 进入我的收藏查看
    def into_Mycollect(self):
        try:
            PulicClass().Login(driver)
            getFocus = V5_BBS().findMyFavoritePostPage_300()
            assert getFocus.status_code == 200
            getAuction = V5_BBS().findMyFavoriteAuctionPage_500()
            assert getAuction.status_code == 200
            getProduct = v5().findMemberFavoritePage_500()
            assert getProduct.status_code == 200
            driver.find_element_by_id(Config(MinePage).get('my_collect')).click()
            driver.implicitly_wait(3)
            assert driver.current_activity == '.activity.PatCollectListActivity'
            assert driver.find_element_by_id('tv_title').text == '我的收藏'
            TitleList = driver.find_elements_by_xpath('//*[contains(@resource-id, "tv_tab_title")]')
            TitleList[0].click()    # 查看话题
            FocuseTotal = int(getFocus.json()['total'])
            if FocuseTotal == 0:
                assert driver.find_element_by_id('error_title').text == '还没有收藏的话题哟~'
            else:
                if FocuseTotal > 2:
                    FocuseRecl = 2
                else:
                    FocuseRecl = FocuseTotal
                for i in range(FocuseRecl):
                    INFONAME = driver.find_elements_by_xpath('//*[contains(@resource-id, "info_name")]')[i]
                    assert INFONAME.text == getFocus.json()['rows'][i]['memberNickname']
                    INFOLEVL = driver.find_elements_by_id('info_level')[i]
                    assert INFOLEVL.text == 'V'+getFocus.json()['rows'][i]['memberLevel']
                    INFOSUBJECT = driver.find_elements_by_id('com_content')[i]
                    assert getFocus.json()['rows'][i]['subject'] in INFOSUBJECT.text
                    FocueButton = driver.find_element_by_id('info_focus')
                    assert FocueButton.is_enabled() == True
            TitleList[1].click()  # 查看拍场
            AuctionTotal = int(getAuction.json()['total'])
            if AuctionTotal > 0:
                if AuctionTotal >2:
                    AuctionRecl =2
                else:
                    AuctionRecl = AuctionTotal
                for i in range(AuctionRecl):
                    AuctionName = driver.find_elements_by_id('home_delayed_tv_name')[i]
                    assert AuctionName.text == getAuction.json()['rows'][i]['name']
                    AuctionStartTime = driver.find_elements_by_id('home_delayed_tv_time')[i]
                    assert AuctionStartTime.text == (getAuction.json()['rows'][i]['startTime'])[0:-3]
                    AuctionObNum = driver.find_elements_by_id('home_delayed_tv_count')[i]
                    assert ''.join(re.findall('\d', AuctionObNum.text)) == getAuction.json()['rows'][i]['observerCount']
                    LOTNUM = driver.find_elements_by_id('home_delayed_tv_num')[i]
                    assert ''.join(re.findall('\d', LOTNUM.text)) == getAuction.json()['rows'][i]['lotCount']
                    PriceNum = driver.find_elements_by_id('home_delayed_tv_price_num')[i]
                    assert ''.join(re.findall('\d', PriceNum.text)) == getAuction.json()['rows'][i]['biddingPriceCount']
                    AuctionStatus = driver.find_elements_by_id('home_delayed_tv_state')[i]
                    if getAuction.json()['rows'][i]['auctionState'] == 'F':
                        auction_status = '已结束'
                    elif getAuction.json()['rows'][i]['auctionState'] == 'A':
                        auction_status = '直播中'
                    elif getAuction.json()['rows'][i]['auctionState'] == 'N':
                        auction_status = '未开始'
                    elif getAuction.json()['rows'][i]['auctionState'] == 'P':
                        auction_status = '提前入场'
                    else:
                        auction_status = '暂停中'
                    assert AuctionStatus.text == auction_status
                    AuctionName.click()
                    driver.implicitly_wait(2)
                    assert driver.current_activity == '.activity.AuctionGroupDetailNewActivity'
                    assert (driver.find_element_by_id('title_title_text_view').text)[0:-3] in \
                           getAuction.json()['rows'][i]['name']
                    driver.back()
                    if i == (AuctionRecl -1):
                        driver.find_elements_by_id('home_delayed_collection')[i].click()   # 取消收藏最后一个拍场
                        try:
                            DelAuction = WebDriverWait(driver, timeout=5).until\
                                (EC.visibility_of_element_located((By.NAME, AuctionName.text)))
                            print(f'取消收藏UI功能存在问题')
                        except:
                            print(f'取消收藏UI功能正常')
            TitleList[2].click()        # 进入我收藏的商品
            ProductTotal = int(getProduct.json()['total'])
            if ProductTotal > 0:
                if ProductTotal > 4:
                    ProductRecl = 4
                else:
                    ProductRecl = ProductTotal
                for i in range(ProductRecl):
                    PRODUCTNAME = driver.find_elements_by_id('product_good_name')[i]
                    SALESPRICE = driver.find_elements_by_id('product_good_price')[i]
                    assert PRODUCTNAME.text == getProduct.json()['rows'][i]['name']
                    WaitPrice = getProduct.json()['rows'][i]['waitPrice']
                    ReShow = getProduct.json()['rows'][i]['reShow']
                    ONshelf = getProduct.json()['rows'][i]['onShelf']
                    if ReShow:
                        assert SALESPRICE.text == '已被恭请'
                    else:
                        if WaitPrice:
                            assert SALESPRICE.text == '估价待询'
                        else:
                            if 'salesPrice' in list(getProduct.json()['rows'][i].keys()):
                                SALESPRICETEXT = str(SALESPRICE.text).replace('¥', '').replace(',', '').strip()
                                assert float(SALESPRICETEXT) == float(getProduct.json()['rows'][i]['salesPrice'])
                                DELPRICE = driver.find_elements_by_id('product_layout')[i].\
                                    find_element_by_id('product_good_del_price')
                                DELPRICETEXT = str(DELPRICE.text).replace('¥','').replace(',','').strip()
                                assert float(DELPRICETEXT) == float(getProduct.json()['rows'][i]['originalPrice'])
                            else:
                                SALESPRICETEXT = str(SALESPRICE.text).replace('¥','').replace(',','').strip()
                                assert float(SALESPRICETEXT) == float(getProduct.json()['rows'][i]['originalPrice'])
                    PRODUCTNAME.click()
                    driver.implicitly_wait(4)
                    if ONshelf:
                        assert driver.current_activity == '.shop.mall.ShopGoodsDetailActivity'
                        driver.back()
                    else:
                        assert driver.current_activity == '.activity.PatCollectListActivity'
                    print(PRODUCTNAME.text)
                    if i == (ProductRecl - 1):
                        driver.find_elements_by_id('product_state')[i].click()
                        time.sleep(2)
                        driver.refresh()
                        try:
                            WebDriverWait(driver, timeout=5).until\
                                (EC.visibility_of_element_located((By.XPATH, f"//.contains(@text, {PRODUCTNAME.text})")))
                            print(f'商品取消收藏功能存在问题')
                        except:
                            print(f'商品取消收藏功能正常')
            driver.back()
        except:
            assert True == False
            print(f'查看我的收藏UI板块可能存在问题，请手动验证')

    # 进入商家中心查看
    def into_SallerCenter(self, driver):
        try:
            self.Into_MimePage(driver)
            MemberId = v5().getMemberDetailInfo_112().json()['id']
            OrderComment = V5_ORDER().countOrderComment_112(MemberId)
            assert OrderComment.status_code == 200
            OrderCommentTotal = OrderComment.json()['result']
            getSellerTotal = V5_ORDER().getSellerCalcInfo_400(MemberId)
            assert getSellerTotal.status_code == 200
            sellerSoldOutCount = getSellerTotal.json()['sellerSoldOutCount']    # 成交总量笔数
            sellerSoldOutAmount = float(getSellerTotal.json()['sellerSoldOutAmount'])   # 成交总金额
            sellerOdPositiveRate = getSellerTotal.json()['sellerOdPositiveRate']        # 好评率
            sellerOdSuccessRate = getSellerTotal.json()['sellerOdSuccessRate']          # 成交率
            sellerOdReturnRate = getSellerTotal.json()['sellerOdReturnRate']            # 退货率
            # getOther = v5().getMemberDetailInfo_112()
            # assert getOther.status_code == 200
            # HasShop = getOther.json()['hasShop']
            LOC = (By.ID, Config(MinePage).get('my_store'))
            PulicClass().up_swipe_to_display(driver, *LOC)
            ShopCenter = WebDriverWait(driver, 3).until\
                (EC.visibility_of_element_located(LOC))
            ShopCenter.click()
            driver.implicitly_wait(5)
            assert driver.current_activity == '.activity.MyStoreActivity'
            assert driver.find_element_by_id(Config(SellCenter).get('positive_ratio')).text.strip('好评率: ')\
                   == sellerOdPositiveRate
            assert driver.find_element_by_id(Config(SellCenter).get('LBR')).text.strip('成交率: ') \
                   == sellerOdSuccessRate
            assert driver.find_element_by_id(Config(SellCenter).get('return_rate')).text.strip('退货率: ') \
                   == sellerOdReturnRate
            assert float(driver.find_element_by_id(Config(SellCenter).get('sell_money')).text.strip('元')) == \
                   float(sellerSoldOutAmount)
            assert int(driver.find_element_by_id(Config(SellCenter).get('sell_total')).text.strip('笔')) == \
                   int(sellerSoldOutCount)
            # 订单评价总数
            OrderLoc = (By.ID, Config(SellCenter).get('order_comment'))
            PulicClass().up_swipe_to_display(driver, *OrderLoc)
            OrderCount = WebDriverWait(driver, 3).until\
                (EC.visibility_of_element_located(OrderLoc))
            assert ''.join(re.findall('\d', OrderCount.text.replace(',',''))) == OrderCommentTotal
            # if HasShop:
            #     try:
            #         myshop = WebDriverWait(driver,timeout=5).until\
            #             (EC.visibility_of_element_located((By.NAME, '我的店铺 ')))
            #         print(f'有商品权限时，前端正常显示我的商铺')
            #         myshop.click()
            #         driver.implicitly_wait(5)
            #         assert driver.current_activity == '.shop.store.StoreActivity'
            #         driver.back()
            #     except:
            #         print(f'用户有商铺权限时，前端未显示我的店铺按钮')
            # 点击进入商家订单界面
            # MyOrderList = driver.find_element_by_id('tv_my_order') # 订单List
            # MyOrderList.click()
            # driver.implicitly_wait(5)
            # assert driver.current_activity == '.shop.order.ui.OrderActivity'
            # driver.back()
            # driver.find_element_by_id('tv_obligation').click()     # 待买家付款订单
            # assert driver.current_activity == '.shop.order.ui.OrderActivity'
            # driver.back()
            # driver.find_element_by_id('tv_wait_send_out').click()  # 待发货订单
            # assert driver.current_activity == '.shop.order.ui.OrderActivity'
            # driver.back()
            # driver.find_element_by_id('tv_wait_take').click()      # 待确认收货订单
            # assert driver.current_activity == '.shop.order.ui.OrderActivity'
            # driver.back()
            # driver.find_element_by_id('tv_wait_comment').click()   # 待评价的订单
            # assert driver.current_activity == '.shop.order.ui.OrderActivity'
            # driver.back()
            # driver.find_element_by_id('tv_aftermarket').click()    # 售后订单
            # assert driver.current_activity == '.shop.order.ui.ReturnListActivity'
            # driver.back()
            # driver.find_element_by_id('tv_my_pat').click()         # 我的拍场
            # assert driver.current_activity == '.activity.MyPatActivity'
            # driver.back()
            # driver.find_element_by_id('tv_pat_apply').click()      # 申请中的拍场
            # assert driver.current_activity == '.activity.MyPatActivity'
            # driver.back()
            # driver.find_element_by_id('tv_pat_check').click()      # 审核中的拍场
            # assert driver.current_activity == '.activity.MyPatActivity'
            # driver.back()
            # driver.find_element_by_id('tv_pat_now').click()        # 进行中的拍场
            # assert driver.current_activity == '.activity.MyPatActivity'
            # driver.back()
            # driver.find_element_by_id('tv_pat_waiting').click()    # 即将开始的拍场
            # assert driver.current_activity == '.activity.MyPatActivity'
            # driver.back()
            # driver.find_element_by_id('tv_pat_history').click()    # 历史拍场
            # assert driver.current_activity == '.activity.MyPatActivity'
            # driver.back()
            driver.implicitly_wait(2)
            driver.find_element_by_id('rl_my_baby').click()        # 进入我的宝贝页面
            assert driver.current_activity == '.shop.goods.ui.GoodsListActivity'
            driver.implicitly_wait(2)
            MyProduct().check_page_init(driver)
            # MyProduct().check_unshelf_product(driver)
            # MyProduct().check_add_auctionLot(driver)
            MyProduct().check_add_delayacutionLot(driver)
            # MyProduct().check_onself_product(driver)
        except:
            assert True == False


if __name__ == '__main__':
    dr = Driver().get_driver()
    TestMine().into_SallerCenter(dr)

