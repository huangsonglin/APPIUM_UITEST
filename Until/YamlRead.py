import os
import yaml
Base_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = Base_path+r'\Config\config.ymal'
App_LoginToken = Base_path+r'\Config\Token.ymal'
APK_PATH = Base_path + r'\Apk\cn.dcpai.auction.apk'
ActivityPath = Base_path + r'\elements\acitivity.ymal'
MinePage = Base_path + r'\elements\mine.ymal'
HomePage = Base_path + r'\elements\home.ymal'
AuctionPage = Base_path + r'\elements\auction.ymal'
ShopPage = Base_path + r'\elements\shop.ymal'
LoginPage = Base_path + r'\elements\login.ymal'
BuyOrderPage = Base_path + r'\elements\BuyerOrder.ymal'
SellCenter = Base_path + r'\elements\sellcenter.ymal'
Logcat = Base_path + r'\adblogcat'
IMG_PATH = Base_path + r'\Img'
Pid_PATH = Base_path + r'\Config\Pid.ymal'

# 读取yaml文件
class yaml_read:
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):
        # 如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))  # load后是个generator，用list组织成列表
        return self._data

# 精确读取配置文件中的某项内容
class Config:
    def __init__(self, config=CONFIG_FILE):
        self.config = yaml_read(config).data

    def get(self, element, index=0):
        """
        yaml是可以通过'---'分节的。用YamlReader读取返回的是一个list，第一项是默认的节，如果有多个节，可以传入index来获取。
        这样我们其实可以把框架相关的配置放在默认节，其他的关于项目的配置放在其他节中。可以在框架中实现多个项目的测试。
        """
        return self.config[index].get(element)


class yaml_write:
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在！')

    def write(self,aproject):
        with open(self.yamlf,'w') as f:
            yaml.dump(aproject,f)
        f.close()


print(Config(HomePage).get("search_button"))