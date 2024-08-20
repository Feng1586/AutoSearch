# 演示代码示例，继承UserTaskBase，并实现start以及stop
# 导入logger用于日志记录
from app.log import logger
# 导入UserTaskBase作为基类
from app.plugins.customplugin.task import UserTaskBase

import requests
import time

# 定义一个继承自UserTaskBase的类HelloWorld
class HelloWorld(UserTaskBase):
    def __init__(self):
        self.ip_address = "192.168.31.151"
        self.username = "admin"
        self.password = "Aa123456"
        
        # 登录接口
        self.login_url = f"http://{self.ip_address}:3000/api/v1/login/access-token"
        # 获取订阅列表接口
        self.sub_list = f"http://{self.ip_address}:3000/api/v1/subscribe/"
        # 提交搜索接口
        self.search = f"http://{self.ip_address}:3000/api/v1/subscribe/search/"
        
        self.data = {
            "username": self.username,
            "password": self.password
        }
        
        self.flag = 1
        
    def start(self):
        """
        开始任务时调用此方法
        """
        # 记录任务开始的信息
        logger.info("Hello World. Start.")
        # 获取AccessToken数据
        self.get_accessToken()
        if self.flag == 1:
            self.get_sub_list()
            if self.flag == 1:
                self.submit_serch()

    def stop(self):
        """
        停止任务时调用此方法
        """
        # 记录任务停止的信息
        logger.info("Hello World. Stop.")
    
    def get_accessToken(self):
        response = requests.post(url=self.login_url, data=self.data)
        if response.status_code == 200:
            #解析 JSON 相应
            json_data = response.json()
            #获取 access_token
            self.access_token = json_data.get("access_token")
            #log 输出access_token
            logger.info(self.access_token)
            logger.info("成功获取AccessToken")
        else:
            self.flag = 0
            logger.info("获取失败,任务已停止")
    
    def get_sub_list(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
            
        # 发送请求
        response = requests.get(url=self.sub_list, headers=headers)
        
        if response.status_code == 200:
            # 解析数据
            self.sub_list = response.json()
            logger.info("成功获取订阅列表")
        else:
            self.flag = 0
            logger.info("订阅列表获取失败,任务已停止")
    
    def submit_serch(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        for name in self.sub_list:
            search_url = self.search + str(name["id"])
            logger.info(search_url)
            
            response = requests.get(url=search_url, headers=headers)
            if response.status_code == 200:
                message = response.json()
                if message["success"] == True:
                    logger.info(name["name"]+"已提交搜索请求")
            else:
                logger.info("遇到错误,任务已停止")
                break
            
            time.sleep(60)