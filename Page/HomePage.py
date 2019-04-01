#!user/bin/python
#-*- coding: utf-8 -*-
__author__: 'huangsonglin@dcpai.cn'
__Time__: '2019/2/21 15:50'

import os,sys
import time
import re, string
from Until.YamlRead import *
from Driver.Driver import *
from Command.command import command as cmd
from appium.webdriver.common import mobileby
from selenium.webdriver.common.by import By
from API.new_500 import *
from API.Order500 import *
from API.BBS500 import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from Until.YamlRead import *
from Page.PulicClass import *
from Until.DB import *
from Page.Auction_LotPage import *
from Page.Auction_Page import *
from Page.Delay_Auction import *

class HomeCase:

    username = Config(CONFIG_FILE).get('username')
    password = Config(CONFIG_FILE).get('password')
    Day = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def Into_HomePage(self, driver):
        homePage = Config(HomePage).get('home_RadioButton')
        HomePageButton = driver.find_element_by_id(homePage)
        HomePageButton.click()
        time.sleep(1)

    # banner信息查看
    def Banner(self, driver):
        AdvList = v5().findAdvertiseContent_260('P4')
        AdvNum = len(AdvList.json()['appAdvertiseDtoList'])
        homePage = Config(HomePage).get('home_RadioButton')
        HomePageButton = driver.find_element_by_id(homePage)
        HomePageButton.click()
        BannerTitle = []
        for titles in AdvList.json()['appAdvertiseDtoList']:
            BannerTitle.append(titles['title'])
        try:
            BannerHome = WebDriverWait(driver, timeout=3).until\
                (EC.visibility_of_element_located((By.ID, Config(HomePage).get('banner_home'))))
            BannerRels = driver.find_elements_by_xpath\
                ('//*[contains(@resource-id, "circleIndicator")]/android.widget.ImageView')
            BannerImge = driver.find_element_by_xpath\
                ('//*[@resource-id="cn.dcpai.auction:id/bannerViewPager"]/android.widget.ImageView')
            assert len(BannerRels) == AdvNum
            Y = BannerRels[0].location['y']
            X = BannerRels[0].location['x']
            for BannerRel in BannerRels:
                BannerImge.click()
                try:
                    driver.implicitly_wait(2)
                    # 导航界面的title
                    pageTitle = WebDriverWait(driver, 3, 0.5).until\
                        (EC.visibility_of_element_located((By.ID, "tv_title")))
                    assert pageTitle.text in BannerTitle
                    BannerTitle = BannerTitle.remove(pageTitle.text)
                    print(f'当前banner跳转功能正常')
                except:
                    WebDriverWait(driver, timeout=3).until \
                        (EC.visibility_of_element_located((By.XPATH, '//*[contains(@text, "轰啪拍场")]')))
                    print(f'当前banner跳转存在问题，请手动验证')
                    driver.save_screenshot(IMG_PATH + f'\HomeBanner_%d%s.png' %(BannerRels.index(BannerRel), self.Day))
                    pass
                driver.back()
                driver.swipe(X-20, Y, 20, Y, duration=1000)
        except:
            assert True == False

    # 四点讲堂
    def FourTeacher(self, driver):
        try:
            RQ = v5().findForumGuide()
            assert RQ.status_code == 200
            if len(RQ.text) == 0:
                print(f'当前界面未配置四点讲堂，跳过该用例~~~')
            else:
                try:
                    LIVEID = RQ.json()['id']
                    RQName = RQ.json()['name']
                    RQStartTime = RQ.json()['startTime']
                    if str(datetime.datetime.now().date()) in RQStartTime:
                        RQStartTime = '今天' + RQStartTime.split(str(datetime.datetime.now().date()))[1]
                    RQTeacher = RQ.json()['speakerName']
                    ELE = WebDriverWait(driver, timeout=10).until \
                        (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'foruguide_background')]")))
                    # 四点讲堂名字
                    Name = WebDriverWait(driver, timeout=10).until \
                        (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'foruguide_name')]")))
                    # 主讲人及时间
                    Detail = WebDriverWait(driver, timeout=10).until \
                        (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'foruguide_spack_name')]")))
                    StartTime = re.findall('时间:(.*?)主讲人', Detail.text)[0].strip()       # 开始时间
                    Teacher = re.findall('主讲人:(.*)', Detail.text)[0].strip()             # 讲师
                    ELE.click()
                    driver.implicitly_wait(10)
                    assert driver.current_activity == '.forum.view.VideoClassDetailActivity'  # 四点讲堂界面的acitivity
                    # 页面title
                    PageTitle = WebDriverWait(driver, timeout=10).until \
                        (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'tv_title')]")))
                    assert PageTitle.text == Name.text == RQName, u'详情页和首页推广名字保存一致'
                    # 进入直播按钮
                    LIVEBUTTON = WebDriverWait(driver, timeout=10).until \
                        (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'tv_live')]")))
                    assert LIVEBUTTON.text == '进入直播'
                    PageTeacher = WebDriverWait(driver, timeout=10).until \
                        (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'tv_teacher')]")))
                    assert str(PageTeacher.text).split(':')[1] == Teacher == RQTeacher
                    PageStartTime = WebDriverWait(driver, timeout=10).until \
                        (EC.visibility_of_element_located((By.XPATH, "//*[contains(@resource-id, 'tv_start_time')]")))
                    assert RQStartTime[0:-3] == StartTime
                    [cmd(driver).up_swipe() for i in range(3)]
                    OtherNames = driver.find_elements_by_xpath('//*[contains(@resource-id, "tv_name")]')
                    DRQ = v5().findLiveDetail_450(LIVEID)
                    for Other in OtherNames:
                        Name = DRQ.json()['otherLive'][OtherNames.index(Other)]['name']
                        assert Other.text == Name
                    driver.back()
                except:
                    assert True == False
        except:
            print(f'四点讲堂UI界面存在问题，请测试人员及时排查问题')
            assert True == False

    # 首页下滑操作
    def DownAfter_CSS(self, driver):
        try:
            homePage = Config(HomePage).get('home_RadioButton')
            HomePageButton = driver.find_element_by_id(homePage)
            HomePageButton.click()
            AuctionReq = v5().findExquisiteAuctionList_260()
            assert AuctionReq.status_code == 200
            DelayAuctionReq = v5().findExquisiteDelayAucAuctionList_430()
            assert DelayAuctionReq.status_code == 200
            AuctionNum = len(AuctionReq.json())
            DelayAuctionNum = len(DelayAuctionReq.json())
            # 如果秒啪和轰啪都不未空时，上滑操作验证
            if AuctionNum > 0 and DelayAuctionNum > 0:
                cmd(dr).up_swipe()
                time.sleep(1)
                try:
                    Auction = driver.find_element_by_id('home_lot_txt')             # u'轰啪拍场按钮'
                    DelayAuction = driver.find_element_by_id('home_delayed_txt')    # u'秒啪拍场按钮'
                    YouLike = driver.find_element_by_id('home_like_txt')            # u'猜你喜欢按钮'
                    assert Auction.is_displayed() == True
                    assert DelayAuction.is_displayed() == True
                    assert YouLike.is_displayed() == True
                except:
                    driver.save_screenshot(IMG_PATH+ r'\HomeCss_%s.png' % {self.Day})
                    print(f'首页下滑后样式存在问题，请及时查看')
                cmd(driver).down_swipe()
                dr.implicitly_wait(2)
                try:
                    WebDriverWait(driver, timeout=5).until\
                        (EC.visibility_of_element_located((By.ID, "home_lot_txt")))
                    WebDriverWait(driver, timeout=5).until \
                        (EC.visibility_of_element_located((By.ID, "home_delayed_txt")))
                    assert True == False
                except:
                    assert True == True
            else:
                try:
                    Auction = dr.find_element_by_id('home_lot_txt'), u'轰啪拍场按钮'
                    driver.save_screenshot(IMG_PATH + r'\HomeCss_%s.png' % self.Day)
                    print(f'轰啪或者秒啪不同时存在时，却存在轰啪按钮，样式不正确请及时查看')
                    assert True == False
                except:
                    assert True == True
        except:
            print(f'首页下滑后界面样式存在问题，请测试人员及时排查问题')
            assert True == False

    # 查看首页的轰啪拍场
    def Check_HomePage_Auction(self, dr):
        self.Into_HomePage(dr)
        try:
            SearchButton = WebDriverWait(dr, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/home_img_search_btn")))
            M = PulicClass().get_box(dr, SearchButton)[3] - PulicClass().get_box(dr, SearchButton)[1]
            AuctionReq = v5().findExquisiteAuctionList_260()
            assert AuctionReq.status_code == 200
            NUM = len(AuctionReq.json())
            if NUM == 0:
                print(f'首页当前无轰啪拍场，跳过用例')
            else:
                # 元素-轰啪拍场文字
                AuctionText = dr.find_element_by_android_uiautomator('new UiSelector().text("轰啪拍场")')
                # banner是否存在
                BannerLoc = (By.ID, 'cn.dcpai.auction:id/bannerContainer')
                if cmd(dr).is_elementExits(*BannerLoc):
                    dr.drag_and_drop(AuctionText, SearchButton)
                    PulicClass().randow_hight_swipe(dr, int(M/2))
                    time.sleep(1)
                else:
                    pass
                for i in range(NUM):
                    print(i)
                    status = AuctionReq.json()[i]['auctionState']
                    startTime = AuctionReq.json()[i]['startTime']
                    LotIdList = []
                    for LotId in AuctionReq.json()[i]['lotList']:
                        LotIdList.append(LotId['id'])
                    if str(datetime.datetime.now().date()) in startTime:
                        startTime = '今天' + startTime.split(str(datetime.datetime.now().date()))[1][0:-3]
                    else:
                        startTime = startTime[5:-3]
                        startTime = startTime.replace('-', '月').split(' ')
                        startTime = startTime[0]+'日 '+ startTime[1]
                    if i < NUM-1:
                        AuctionRoot = dr.find_elements_by_id('home_exquisite_root')
                        MUNBER = len(AuctionRoot)
                        time.sleep(0.5)
                        # 拍场名字
                        AuctioName = AuctionRoot[0].find_element_by_id("home_exquisite_tv_name")
                        assert AuctioName.text == AuctionReq.json()[i]['name']
                        # 拍场状态
                        AuctionStatus = AuctionRoot[0].find_element_by_id("home_exquisite_tv_state")
                        # 拍场开始时间|距结束时间
                        AuctionTime = AuctionRoot[0].find_element_by_id("home_exquisite_tv_time")
                        if status == 'F':
                            auction_status = '已结束'
                            # 总出价次数
                            BidPriceTotal = AuctionRoot[0].find_element_by_id('home_exquisite_tv_num')
                            # 总成交价
                            PriceTotal = AuctionRoot[0].find_element_by_id('home_exquisite_tv_price')
                            assert ''.join(re.findall('\d', BidPriceTotal.text)) == \
                                   AuctionReq.json()[i]['biddingPriceCount']
                            assert float(''.join(re.findall('\d', str(PriceTotal.text).replace(',', '')))) \
                                   == float(AuctionReq.json()[i]['hammerPriceTotal'])
                            assert AuctionTime.text == startTime
                        elif status == 'A':
                            auction_status = '竞拍中'
                            assert '距结束' in AuctionTime.text
                        elif status == 'N':
                            auction_status = '未开始'
                            assert AuctionTime.text == startTime
                        elif status == 'P':
                            auction_status = '提前入场'
                            assert AuctionTime.text == startTime
                        else:
                            auction_status = '暂停中'
                            assert AuctionTime.text == startTime
                        assert auction_status == AuctionStatus.text
                        # 拍场围观次数
                        AuctionOBNum = AuctionRoot[0].find_element_by_id('home_exquisite_tv_count')
                        assert ''.join(re.findall('\d', AuctionOBNum.text.replace(',', ''))) == \
                               AuctionReq.json()[i]['observerCount']
                        Y = PulicClass().get_box(dr, AuctionStatus)[3] - PulicClass().get_box(dr, AuctioName)[1]
                        print(AuctioName.text, AuctionReq.json()[i]['name'])
                        PulicClass().randow_hight_swipe(dr, int(Y/3))
                        time.sleep(1)
                        # 拍场拍品图片
                        AuctionLot = AuctionRoot[0].find_element_by_xpath \
                            ("//*[contains(@resource-id, 'home_exquisite_recycler')]")
                        # 图片列表
                        LotImgList = AuctionLot.find_elements_by_id('cn.dcpai.auction:id/lot_imageView')
                        for k in range(math.ceil(len(LotIdList)/len(LotImgList))):
                            for m in range(k, len(LotImgList)):
                                LotImgList[m].click()
                                dr.implicitly_wait(10)
                                AuctionLotPage().Assert_Activity(dr)
                                if k == 0:
                                    AuctionLotPage().Lot_Information(dr, LotIdList[m])
                                dr.back()
                            dr.drag_and_drop(LotImgList[-1], LotImgList[0])
                            time.sleep(1)
                        dr.drag_and_drop(AuctionLot, SearchButton)
                        time.sleep(0.5)
                        PulicClass().randow_hight_swipe(dr, M + 20)
                        time.sleep(0.5)
                    else:
                        AuctionRoot = dr.find_elements_by_id('home_exquisite_root')
                        # 拍场名字
                        AuctioName = AuctionRoot[-1].find_element_by_xpath \
                            ("//*[contains(@resource-id, 'home_exquisite_tv_name')]")
                        # 拍场状态
                        AuctionStatus = AuctionRoot[-1].find_element_by_xpath \
                            ("//*[contains(@resource-id, 'home_exquisite_tv_state')]")
                        # 拍场围观次数
                        AuctionOBNum = AuctionRoot[-1].find_element_by_xpath \
                            ("//*[contains(@resource-id, 'home_exquisite_tv_count')]")
                        # 拍场开始时间|距结束时间
                        AuctionTime = AuctionRoot[-1].find_element_by_xpath \
                            ("//*[contains(@resource-id, 'home_exquisite_tv_time')]")
                        assert AuctioName.text == AuctionReq.json()[i]['name']
                        assert ''.join(re.findall('\d', AuctionOBNum.text.replace(',', ''))) == \
                               AuctionReq.json()[i]['observerCount']
        except:
            assert True == False

    # 查看首页的秒啪拍场
    def Chekc_Hompage_DelayAuction(self, dr):
        self.Into_HomePage(dr)
        try:
            SearchButton = WebDriverWait(dr, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/home_img_search_btn")))
            M = PulicClass().get_box(dr, SearchButton)[3] - PulicClass().get_box(dr, SearchButton)[1]
            AuctionReq = v5().findExquisiteDelayAucAuctionList_430()
            assert AuctionReq.status_code == 200
            NUM = len(AuctionReq.json())
            if NUM == 0:
                print(f'首页当前无秒啪拍场，跳过用例')
            else:
                AuctionTextLoc = (By.XPATH, '//*[@resource-id="cn.dcpai.auction:id/home_delayed_layout"]/'
                                            'android.widget.TextView')
                # PulicClass().up_swipe_to_display(dr, *AuctionTextLoc)
                cmd(dr).up_swipe()
                time.sleep(1)
                DelayAuction = dr.find_element_by_id('home_delayed_txt')            #  u'秒啪拍场按钮'
                DelayAuction.click()
                AuctionText = WebDriverWait(dr, 3).until(EC.visibility_of_element_located(AuctionTextLoc))
                dr.drag_and_drop(AuctionText, SearchButton)
                PulicClass().randow_hight_swipe(dr, int(M / 2))
                for i in range(NUM):
                    if i < NUM-1:
                        DelayAuctionRoot = dr.find_elements_by_id('cn.dcpai.auction:id/home_delayed_root')
                        time.sleep(0.5)
                        # 秒啪名字
                        DelayAuctionName = DelayAuctionRoot[0].find_element_by_id('home_delayed_tv_name')
                        assert  DelayAuctionName.text == AuctionReq.json()[i]['name']
                        DelayAuctionObNum = DelayAuctionRoot[0].find_element_by_id('home_delayed_tv_count')
                        assert ''.join(re.findall('\d', DelayAuctionObNum.text.replace(',',''))) == \
                               AuctionReq.json()[i]['observerCount']
                        # 拍品件数
                        DelayLotNum = DelayAuctionRoot[0].find_element_by_id('home_delayed_tv_num')
                        assert ''.join(re.findall('\d', DelayLotNum.text)) == AuctionReq.json()[i]['lotCount']
                        # 出价次数
                        DelayAuctionPrice = DelayAuctionRoot[0].find_element_by_id('home_delayed_tv_price_num')
                        assert ''.join(re.findall('\d', DelayAuctionPrice.text.replace(',', ''))) == \
                               AuctionReq.json()[i]['biddingPriceCount']
                        dr.drag_and_drop(DelayLotNum, SearchButton)
                        PulicClass().randow_hight_swipe(dr, M)
                    else:
                        DelayAuctionRoot = dr.find_elements_by_id('cn.dcpai.auction:id/home_delayed_root')
                        # 秒啪名字
                        DelayAuctionName = DelayAuctionRoot[-1].find_element_by_id('home_delayed_tv_name')
                        assert DelayAuctionName.text == AuctionReq.json()[i]['name']
                        # 围观次数
                        DelayAuctionObNum = DelayAuctionRoot[-1].find_element_by_id('home_delayed_tv_count')
                        assert ''.join(re.findall('\d', DelayAuctionObNum.text.replace(',', ''))) == \
                               AuctionReq.json()[i]['observerCount']
        except:
            assert True == False

    # 猜你喜欢
    def Chekc_Hompage_YouLike(self, driver):
        self.Into_HomePage(driver)
        try:
            SearchButton = WebDriverWait(dr, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/home_img_search_btn")))
            M = PulicClass().get_box(dr, SearchButton)[3] - PulicClass().get_box(dr, SearchButton)[1]
            LikeRq = v5().recommendLotList_420()
            assert LikeRq.status_code == 200
            NUM = len(LikeRq.json())
            if NUM == 0:
                print(f'首页当前无猜你喜欢拍品，直接跳过用例')
            else:
                LikeTextLoc = (By.XPATH, '//*[@resource-id="cn.dcpai.auction:id/home_rec_layout"]'
                                         '/android.widget.TextView')
                # PulicClass().up_swipe_to_display(dr, *LikeTextLoc)
                cmd(driver).up_swipe()
                time.sleep(1)
                DelayAuction = dr.find_element_by_id('home_like_txt')            #  u'秒啪拍场按钮'
                DelayAuction.click()
                LikeText = WebDriverWait(dr, 3).until(EC.visibility_of_element_located(LikeTextLoc))
                driver.drag_and_drop(LikeText, SearchButton)
                PulicClass().randow_hight_swipe(dr, int(M / 2))
                LotNameList = driver.find_elements_by_xpath('//*[contains(@resource-id, "home_rec_txt_name")]')
                time.sleep(0.5)
                LotPrice = driver.find_elements_by_xpath('//*[contains(@resource-id, "home_rec_txt_price")]')
                time.sleep(0.5)
                LotTotalPrice = driver.find_elements_by_xpath(
                    '//*[contains(@resource-id, "home_rec_txt_price_num")]')
                time.sleep(0.5)
                for i in range(len(LotNameList)):
                    assert LotNameList[i].text in LikeRq.json()[i]['name']
                    assert float(''.join(re.findall('\d', LotPrice[2*i].text.replace(',', ''))))\
                           == float(LikeRq.json()[i]['currentPrice'])
                    assert float(''.join(re.findall('\d', LotTotalPrice[i].text.replace(',', '')))) \
                           == float(LikeRq.json()[i]['biddingPriceCount'])
        except:
            assert True == False

    # 返回顶部按钮
    def Check_Homepage_Top(self, driver):
        self.Into_HomePage(driver)
        try:
            loc = (By.ID, "cn.dcpai.auction:id/home_rlayout_top")
            PulicClass().up_swipe_to_display(driver, *loc)
            TopButton  = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(loc))
            TopButton.click()
            time.sleep(1)
            # Banner图
            BannerHome = WebDriverWait(driver, timeout=3).until \
                (EC.visibility_of_element_located((By.ID, Config(HomePage).get('banner_home'))))
            BannerRels = driver.find_elements_by_xpath \
                ('//*[contains(@resource-id, "circleIndicator")]/android.widget.ImageView')
            print(f'返回顶部功能正常')
        except:
            assert True == False

    # 测试秒啪界面相关内容
    def test_delay(self, dr):
        SearchButton = WebDriverWait(dr, timeout=3).until \
            (EC.visibility_of_element_located((By.ID, "cn.dcpai.auction:id/home_img_search_btn")))
        M = PulicClass().get_box(dr, SearchButton)[3] - PulicClass().get_box(dr, SearchButton)[1]
        AuctionReq = v5().findExquisiteDelayAucAuctionList_430()
        assert AuctionReq.status_code == 200
        NUM = len(AuctionReq.json())
        if NUM == 0:
            print(f'首页当前无秒啪拍场，跳过用例')
        else:
            # cmd(dr).up_swipe()
            time.sleep(1)
            LikeTextLoc = (By.XPATH, '//*[@text="秒啪拍场"]')
            PulicClass().up_swipe_to_display(dr, *LikeTextLoc)
            # DelayAuction = dr.find_element_by_id('home_delayed_txt')  # u'秒啪拍场按钮'
            # DelayAuction.click()
            dr.find_elements_by_id('home_delayed_tv_name')[0].click()
            time.sleep(1)
            Delay_Auction_Page().Check_Page_InitSatus(dr)
            Delay_Auction_Page().Check_DelayLot_BiddPrice(dr, AuctionReq.json()[0]['id'])




if __name__ == '__main__':
    dr = Driver().get_driver()
    HomeCase().test_delay(dr)
    dr.quit()


