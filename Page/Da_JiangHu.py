#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/3/25 14:05'

import os,sys
import time
import re, string
from Until.YamlRead import *
from Driver.Driver import *
from Command.command import command as cmd
from selenium.webdriver.common.by import By
from API.new_500 import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Page.PulicClass import *
from Until.DB import *
from Page.Pay_Margin import *
from API.V5down import *
from API.BBS500 import *
from API.new_500 import *
from Page.BBS_Infromation_Page import *
from Page.School_Page import *

class Da_JiangHU:



    # 进入龖江湖首页
    def into_page(self, dr):
        try:
            JiangHu = WebDriverWait(dr, 1).until\
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/jianghu")))
            JiangHu.click()
            # try:
            #     # 首次进入提示信息--加入门派按钮
            #     JoinButton = WebDriverWait(dr, 1).until\
            #         (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/join_forum_button")))
            #     # 首次进入提示信息--加入门派按钮
            #     CreteButton = WebDriverWait(dr, 1).until \
            #         (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/create_forum_button")))
            #     CloseButton  = WebDriverWait(dr, 1).until \
            #         (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/jorum_close_im")))
            #     CloseButton.click()
            # except:
            #     pass
        except:
            print(f'进入龖江湖首页失败')
            pass

    # 初始信息验证
    def check_init_status(self, dr):
        self.into_page(dr)
        try:
            # 精选
            choiceness = WebDriverWait(dr, 2).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/select_tv")))
            # 发布按钮
            send_button = WebDriverWait(dr, 2).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/send_topic_imageview")))
            # 门派
            school = WebDriverWait(dr, 2).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/jiang_shool_tv")))
            school.click()
            try:
                MySchool = WebDriverWait(dr, 2).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[@text='我的门派']")))
                HotSchool = WebDriverWait(dr, 2).until \
                (EC.visibility_of_element_located((By.XPATH, "//*[@text='热门门派']")))
            except:
                print(f'切换到门派页面时，初始信息可能存在问题。请及时查看~~~')
                PulicClass().save_img(dr, "DaJH_School_InitPage")
            # 交流
            exchange = WebDriverWait(dr, 2).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/communication_tv")))
            exchange.click()
            try:
                # 查看帖子分类列表
                TypeList = dr.find_elements_by_id('title')
                ListReq = Down_V5Api().findAllPostType_320()
                for i in range(len(TypeList)):
                    if i == 0:
                        assert TypeList[i].text == '全部'
                    else:
                        assert TypeList[i].text == ListReq.json()[i-1]['name']
                display_view = WebDriverWait(dr, 2).until \
                    (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/com_change_view_img")))
                send = WebDriverWait(dr, 2).until \
                    (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/com_send_img")))
            except:
                print(f'切换到交流页面时，初始信息可能存在问题。请及时查看~~~')
                PulicClass().save_img(dr, "DaJH_Exchange_InitPage")
            # 视频
            video = WebDriverWait(dr, 2).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/select_tv_video")))
            video.click()
            try:
                VideoList = ['全部', '16点讲堂', "拍卖巡展", "拍场回放", "其他"]
                TypeList = dr.find_elements_by_id('title')
                for i in range(len(TypeList)):
                    assert TypeList[i].text == VideoList[i]
            except:
                print(f'切换到视频页面时，初始信息可能存在问题。请及时查看~~~')
                PulicClass().save_img(dr, "DaJH_Video_InitPage")
        except:
            print(f'进入龖江湖界面初始化信息状态存在问题,请手动查看~~~')
            PulicClass().save_img(dr, 'DajiangHu_HomePage')
            pass

    # 点击查看公告信息
    def check_notice_information(self, driver):
        self.into_page(driver)
        req = Down_V5Api().findOfficialBulletin_300()
        Num = len(req.json())
        choiceness = WebDriverWait(dr, 2).until \
            (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/select_tv")))
        choiceness.click()
        if Num == 0:
            print(f'当前未发布任何公告,跳过该条测试用例')
            try:
                WebDriverWait(driver, 2).until\
                    (EC.visibility_of_element_located((By.ID, "exquit_announcement_linearLayout")))
                print('Error! 未发布公告时，存在公告属性字段信息')
            except:
                pass
        else:
            try:
                NoticeLiner = WebDriverWait(driver, 2).until \
                    (EC.visibility_of_element_located((By.ID, "exquit_announcement_linearLayout")))
                Notice_Title = NoticeLiner.find_element_by_id('cn.dcpai.auction:id/exquit_topic_announcement_content_tv')
                assert Notice_Title.text == req.json()[0]['subject']
                Notice_Title.click()
                driver.implicitly_wait(5)
                Text = driver.find_element_by_android_uiautomator\
                    ('new UiSelector().resourceId("cn.dcpai.auction:id/exquisite_announcement_content_tv")')
                assert (Text.text[0:-3].strip() in req.json()[0]['content'].strip()) == True
                CloseButton = driver.find_element_by_android_uiautomator\
                    ('new UiSelector().resourceId("cn.dcpai.auction:id/close_img")')
                CloseButton.click()
            except:
                assert True == False
                print(f'查看公告信息存在问题，请及时手动验证')

    # 查看置顶消息
    def check_topImformation(self, driver):
        Notice = Down_V5Api().findOfficialBulletin_300()    # 查看公告信息
        Top = Down_V5Api().findOfficialTopPost_300()
        self.into_page(driver)
        choiceness = WebDriverWait(dr, 2).until \
            (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/select_tv")))
        choiceness.click()
        NNum = len(Notice.json())
        TNum = len(Top.json())
        if TNum == 0:
            print(f'当前未配置置顶消息')
            try:
                WebDriverWait(driver, 2).until\
                    (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/stick_top_linearLayout")))
                print(f'未配置置顶消息时，显示了置顶相关信息内容')
            except:
                pass
        else:
            Titles = driver.find_elements_by_android_uiautomator \
                ('new UiSelector().resourceId("cn.dcpai.auction:id/exquit_topic_stick_top_content_tv")')
            for i in range(len(Titles)):
                assert (Top.json()[i]['subject']).startswith( Titles[i].text[0:-3]) == True
                PostId = Top.json()[i]['id']
                Titles[i].click()
                BBS_Imfromation().check_init_status(driver, PostId)
                BBS_Imfromation().check_detail_information(driver, PostId)
                BBS_Imfromation().check_comment_bbs(driver, PostId)
                driver.back()

    # 依次查看帖子
    def check_BBS_Detail(self, driver):
        self.into_page(driver)
        choiceness = WebDriverWait(dr, 2).until \
            (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/select_tv")))
        BOX = PulicClass().get_box(driver, choiceness)
        choiceness.click()
        req = Down_V5Api().findHotPostPage_300()
        assert req.status_code == 200
        FocusList = []
        FocusReq = Down_V5Api().findFocusByFasId_204()
        for result in FocusReq.json()['rows']:
            FocusList.append(result['id'])
        try:
            BBS_Root = driver.find_elements_by_id("cn.dcpai.auction:id/exquitste_topic_item_linearlayout")
            for i in range(8):
                postId = req.json()['rows'][i]['id']
                memberId = req.json()['rows'][i]['memberId']
                # 发帖人
                Poster = BBS_Root[0].find_element_by_id('exquitste_topic_nickname_tv').text
                assert Poster == req.json()['rows'][i]['memberNickname']
                # 发帖人等级
                PosterLevel = BBS_Root[0].find_element_by_id('exquitste_topic_iv_level')
                assert PosterLevel.text == 'V%s' % (req.json()['rows'][i]['memberLevel'])
                # 关注/已关注按钮
                LikeButton = BBS_Root[0].find_element_by_id('cn.dcpai.auction:id/exquitste_topic_focus')
                if memberId in FocusList:
                    assert LikeButton.text == '已关注'
                    LikeButton.click()
                    ToastText = driver.find_element_by_android_uiautomator\
                        ('new UiSelector().resourceId("cn.dcpai.auction:id/dlg_content")').text
                    assert Poster in ToastText
                    SureEsc = driver.find_element_by_android_uiautomator\
                        ('new UiSelector().resourceId("cn.dcpai.auction:id/dlg_sure_tv")')
                    SureEsc.click()
                    assert LikeButton.text == '关注'
                else:
                    assert LikeButton.text == '关注'
                    LikeButton.click()
                    assert LikeButton.text == '已关注'
                if 'subject' in list(req.json()['rows'][i].keys()):
                    # BBS帖子
                    BBSTitle = BBS_Root[0].find_element_by_id('cn.dcpai.auction:id/exquitste_topic_content_tv')
                    if BBSTitle.text.startswith('img '):
                        assert BBSTitle.text[4:-1] in req.json()['rows'][i]['subject']
                    else:
                        assert BBSTitle.text in req.json()['rows'][i]['subject']
                # 围观次数/查看次数
                ObsverCount = BBS_Root[0].find_element_by_id('cn.dcpai.auction:id/exquitste_topic_observercount_tv')
                if len(req.json()['rows'][i]['observerCount']) >= 5:
                    pass
                else:
                    assert ''.join(re.findall('\d', ObsverCount.text.replace(',', ''))) == \
                           req.json()['rows'][i]['observerCount']
                # 评论数量
                CommentCount = BBS_Root[0].find_element_by_id('cn.dcpai.auction:id/exquitste_topic_comment_count_tv')
                if len(req.json()['rows'][i]['commentCount']) >= 5:
                    pass
                else:
                    assert ''.join(re.findall('\d', CommentCount.text.replace(',', ''))) == \
                           req.json()['rows'][i]['commentCount']
                PulicClass().touch_tap(driver, BBS_Root[0])
                BBS_Imfromation().check_init_status(driver, postId)
                BBS_Imfromation().check_detail_information(driver, postId)
                BBS_Imfromation().check_comment_bbs(driver, postId)
                driver.back()
                PushTime = BBS_Root[0].find_element_by_id('cn.dcpai.auction:id/exquitste_topic_time_tv')
                driver.drag_and_drop(PushTime, choiceness)
                PulicClass().randow_hight_swipe(driver, (BOX[3] - BOX[1]) *2)
            TopButton = driver.find_element_by_id('cn.dcpai.auction:id/top_view_img')
            TopButton.click()
        except:
            assert True == False
            print(f'查看当个详情帖子时存在一定的问题，请测试人员及时手动查看~~~')
            PulicClass().save_img(driver, 'BBS_Detail_Page')

    # 发布话题
    def check_postBBS(self, driver):
        self.into_page(driver)
        choiceness = WebDriverWait(driver, 2).until \
            (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/select_tv")))
        choiceness.click()
        try:
            # 发布按钮
            send_button = WebDriverWait(driver, 2).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/send_topic_imageview")))
            send_button.click()
            ChoosePhoto = driver.find_element_by_id('cn.dcpai.auction:id/photo_img')
            ChoostVideo = driver.find_element_by_id('cn.dcpai.auction:id/video_img')
            ChooseClose = driver.find_element_by_id('cn.dcpai.auction:id/publish_close')
            ChoosePhoto.click()
            time.sleep(1)
            assert driver.current_activity == 'com.lzy.imagepicker.ui.ImageGridActivity', u'选择照片界面activity正常'
            CheckBoxList = driver.find_elements_by_id('cn.dcpai.auction:id/cb_check')
            for i in range(int(len(CheckBoxList)/2)):
                CheckBoxList[i].click()
            driver.find_element_by_id('cn.dcpai.auction:id/btn_ok').click()
            time.sleep(1)
            assert driver.current_activity == '.activity.AddTopicNewActivity'
            pagetitle = driver.find_element_by_id('cn.dcpai.auction:id/tv_title')
            assert pagetitle.text == '发布话题'
            # 添加评论
            add_content = driver.find_element_by_id('cn.dcpai.auction:id/add_content')
            add_content.clear()
            add_content.send_keys(PulicClass().Chinese(5))
            Req = Down_V5Api().findAllPostType_320()
            # 选择分类
            ChooseClassFy = driver.find_element_by_xpath('//*[@text="选择分类"]')
            driver.drag_and_drop(ChooseClassFy, pagetitle)
            ClassFyNameList = driver.find_elements_by_id('cn.dcpai.auction:id/item_name_tv')
            for i in range(len(ClassFyNameList)):
                assert ClassFyNameList[i].text == Req.json()[i]['name']
            ClassFyNameList[random.randint(0, len(ClassFyNameList)-1)].click()
            # 分享至微信
            loc = (By.ID, 'cn.dcpai.auction:id/share_switch')
            PulicClass().up_swipe_to_display(driver, *loc)
            share_weixin = WebDriverWait(driver, 2).until(EC.visibility_of_element_located(loc))
            if share_weixin.get_attribute('checked') == 'true':
                share_weixin.click()
            send_new_bbs = driver.find_element_by_id('cn.dcpai.auction:id/add_release_tv')
            send_new_bbs.click()
            try:
                assert PulicClass().new_toast(driver, '发布成功') == True
            except:
                pass
        except:
            PulicClass().save_img(driver, "PostBBS")
            print(f'发布话题功能可能存在问题，请及时查看相关功能~~~')

    # 我的门派
    def check_my_school(self, driver):
        self.into_page(driver)
        req = V5_BBS().findMyForumPage_300()
        NUM = int(req.json()['total'])
        HotForum = []
        for result in V5_BBS().findHotForum_300().json():
            HotForum.append(result['name'])
        try:
            # 门派
            school = WebDriverWait(dr, 2).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/jiang_shool_tv")))
            school.click()
            if NUM == 0:
                try:
                    NoSchool = PulicClass().new_toast(driver, '你还没有加入任何门派')
                    Searchschool = PulicClass().new_toast(driver, "搜索门派")
                    assert NoSchool == Searchschool == True
                    print(f'当前用户未参加|未创建门派时，界面显示正常')
                    SearchschoolButton = driver.find_element_by_id('cn.dcpai.auction:id/school_layout_not')
                    PulicClass().touch_tap(driver, SearchschoolButton)
                    assert driver.current_activity == '.activity.JianghuSearchWebViewActivity'
                    SearchText = driver.find_element_by_id('cn.dcpai.auction:id/search_src_text')
                    assert SearchText.text == '搜索门派'
                    SearchText.clear()
                    Text = random.choice(HotForum)
                    SearchText.send_keys(Text)
                    driver.press_keycode(66)    # 按搜索键，详情件Androidbutton.txt
                    time.sleep(2)
                    try:
                        searchresults = driver.find_elements_by_id('cn.dcpai.auction:id/guild_item')
                        searchreq = V5_BBS().searchForumPage_300(Text)
                        for searchresult in searchresults:
                            index = searchresults.index(searchresult)
                            name = searchresult.find_element_by_id('cn.dcpai.auction:id/search_guild_name')
                            assert name.text in Text
                            data = searchresult.find_element_by_id('cn.dcpai.auction:id/search_guild_scale')
                            assert ''.join(re.findall('\d', data.text.split('·')[0].replace(',', ''))) == \
                                   searchreq.json()['rows'][index]['reputation']
                            assert ''.join(re.findall('\d', data.text.split('·')[1].replace(',', ''))) == \
                                   searchreq.json()['rows'][index]['postCount']
                            assert ''.join(re.findall('\d', data.text.split('·')[2].replace(',', ''))) == \
                                   searchreq.json()['rows'][index]['memberCount']
                    except:
                        print(f'搜索功能存在问题。请测试人员及时查看~~~')
                    driver.back()
                except:
                    PulicClass().save_img(driver, 'No_School')
                    print(f'当前无任何门派时，显示或者搜索功能存在问题')
            else:
                schoollist = driver.find_element_by_id('cn.dcpai.auction:id/school_layout')
                name = schoollist.find_elements_by_class_name('android.widget.TextView')
                for i in range(len(name)):
                    assert name[i].text == req.json()['rows'][i]['name']
                    name[i].click()
                    SchoolPage().check_init_page(driver, req.json()['rows'][i]['id'])
                    driver.back()
        except:
            PulicClass().save_img(driver, 'Myschool')
            print(f'查看我的门派功能存在问题')

    # 创建门派
    def check_create_school(self, driver):
        self.into_page(driver)
        req = V5_BBS().findMyForumPage_300()
        memberList = []
        for result in req.json()['rows']:
            memberList.append(result['memberId'])
        Mymember = v5().getMemberDetailInfo_112().json()['id']
        # 门派
        school = WebDriverWait(dr, 2).until \
            (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/jiang_shool_tv")))
        school.click()
        # 当前用户还未曾创建门派
        if Mymember not in memberList:
            try:
                name = PulicClass().Chinese(3)
                desc = PulicClass().Chinese(30)
                create_button = driver.find_element_by_id('cn.dcpai.auction:id/school_create')
                create_button.click()
                assert driver.current_activity == '.activity.CreateForumNameFirstActivity'
                input_name = driver.find_element_by_id('cn.dcpai.auction:id/create_forum_name_edit')
                input_name.clear()
                input_name.send_keys(name)
                driver.find_element_by_id('cn.dcpai.auction:id/create_forum_name_edit').click() # 输入名字后点击下一步
                assert driver.current_activity == '.activity.CreateForumSecondActivity'
                driver.find_element_by_id('cn.dcpai.auction:id/create_forum_flag_im').click()   # 点击添加门派图片按钮
                assert driver.current_activity == 'com.lzy.imagepicker.ui.ImageGridActivity', u'选择照片界面activity正常'
                CheckBoxList = driver.find_elements_by_id('cn.dcpai.auction:id/iv_thumb')
                CheckBoxList[random(0, len(CheckBoxList)-2)].click()
                driver.find_element_by_id('cn.dcpai.auction:id/btn_ok').click()                 # 点击图片裁剪完成
                driver.find_element_by_id('cn.dcpai.auction:id/create_forum_name_edit').click()  # 点击下一步
                assert driver.current_activity == '.activity.CreateForumThirdActivity'
                input_desc = driver.find_element_by_id('cn.dcpai.auction:id/create_forum_declaration_EditText')
                input_desc.clear()
                input_desc.send_keys(desc)
                driver.find_element_by_id('cn.dcpai.auction:id/create_forum_name_edit').click()  # 点击下一步
                assert driver.current_activity == '.activity.CreateForumFourthActivity'
                page_title = driver.find_element_by_id('cn.dcpai.auction:id/tv_title')
                assert page_title.text == '创建成功'
                # 管理门派
                manage_button = driver.find_element_by_id('cn.dcpai.auction:id/create_forum__manager_btn')
                # 招贤纳士
                select_member_button = driver.find_element_by_id('cn.dcpai.auction:id/create_forum_share_btn')
                driver.back()
                schoollist = driver.find_element_by_id('cn.dcpai.auction:id/school_layout')
                assert schoollist.find_elements_by_class_name('android.widget.TextView')[-1].text == name
            except:
                print(f'创建们拍功能存在问题，请测试人员及时查看~~~')
                PulicClass().save_img(driver, 'create_school')
        else:
            print(f'当前用户已创建门派，无法再次创建门派信息')



if __name__ == '__main__':
    dr = Driver().get_driver()
    Da_JiangHU().check_my_school(dr)