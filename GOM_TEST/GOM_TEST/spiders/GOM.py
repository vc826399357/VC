# -*- coding: utf-8 -*-
"""
Scrapy + Selenium 解决登陆问题并爬取所有job信息
@Author: Wei Chao Wang (vicky.wang@cn.ibm.com)
@Date: 2017-08-31
"""

import scrapy
from scrapy.selector import Selector
from GOM_TEST.items import GomTestItem
from selenium import webdriver
import time
from scrapy.http import HtmlResponse, Request, request
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json


class GomSpider(scrapy.Spider):
    name = "GOM"

    # browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    # executable_path="C:\Program Files\Internet Explorer\iexplore.exe")
    # executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    # executable_path="C:/Program Files (x86)/Mozilla Firefox/firefox.exe")
    # start_urls = ['https://w3id.sso.ibm.com/auth/sps/samlidp/saml20/logininitial?RequestBinding=HTTPPost&PartnerId=https://2x-dc2.kenexa.com/sps/InboundSSOFederation/saml20&NameIdFormat=email']

    def __init__(self):
        self.browser = webdriver.Chrome(
            executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
        # executable_path="C:/Program Files (x86)/Mozilla Firefox/firefox.exe")
        super(GomSpider, self).__init__()
        self.start_urls = [
            'https://w3id.sso.ibm.com/auth/sps/samlidp/saml20/logininitial?RequestBinding=HTTPPost&PartnerId=https://2x-dc2.kenexa.com/sps/InboundSSOFederation/saml20&NameIdFormat=email']

    # def tem(self):
    #     time.sleep(5)
    #     jobs = self.browser.find_elements_by_xpath('//li[@class="job baseColorPalette ng-scope"]')
    #     for job in jobs:
    #         item = GomTestItem()
    #         item['jobProperty'] = job.find_elements_by_xpath('//div/div/p[@class="jobProperty position1"]')[0].text
    #         item['JobTitle'] = job.find_elements_by_xpath('//div/div/span/a[@class="jobProperty jobtitle"]')[0].text
    #         item['JobLocation'] = job.find_elements_by_xpath('//div/div/p[@class="jobProperty position3"]')[0].text
    #         item['JobDepartment'] = job.find_elements_by_xpath('//div/div/p[@class="jobProperty position3"]')[0].text
    #         item['JobDescription'] = \
    #         job.find_elements_by_xpath('//div/div/p/table/tbody/tr/td[@class="sanitizedText"]/font')[0].text
    #         return item

    def parse(self, response):
        # browser = webdriver.Firefox(executable_path="C:/Program Files (x86)/Mozilla Firefox/firefox.exe")
        # self.browser.implicitly_wait(5)
        self.browser.get(self.start_urls[0])
        # self.browser.implicitly_wait(10)
        # time.sleep(5)
        print("Visiting the login page......")
        self.browser.find_element_by_xpath('//form/input[@name="username"]').clear()
        self.browser.find_element_by_xpath('//form/input[@name="username"]').send_keys("vicky.wang@cn.ibm.com")
        self.browser.find_element_by_xpath('//form/input[@name="password"]').clear()
        self.browser.find_element_by_xpath('//form/input[@name="password"]').send_keys("yj880924")
        self.browser.find_element_by_xpath('//form/button[@class="btn_signin"]').click()
        time.sleep(60)
        results = self.browser.find_element_by_xpath(
            '//div[@class="searchLCol"]/div/div/div/h1[@class="ng-scope ng-binding"]').text  # .text获取文本内容
        self.browser.find_element_by_xpath('//button[@class="primaryButton ladda-button ng-binding"]').click()
        time.sleep(40)
        # 原本想用如下方法在点击search之后，根据6xxx results来提取job的总数，但发现返回的是Most recent jobs posted，所以改为在点击search之前获取job总数
        # results = self.browser.find_element_by_xpath('//div[@class="workArea clearfix ng-scope"]/div[@id="mainJobListContainer"]/div[@class="lightAccentBkg padTop"]/div/div/h2').text
        # results = str(results)
        print(results)
        total = int(results[17:22])
        if total % 50 == 0:
            page_num = int(total / 50) - 1
        else:
            page_num = int(total / 50)
        print(page_num)

        # for i in range(0, page_num):
        #     self.browser.find_element_by_xpath('//div[@class="showMoreJobsContainer ng-scope"]/a[@id="showMoreJobs"]').click()
        #     time.sleep(2)
        job_link_list = []

        # jobs = Selector(self.browser.page_source).xpath('//li[@class="job baseColorPalette ng-scope"]')
        # jobs = self.browser.find_elements_by_xpath('//li[@class="job baseColorPalette ng-scope"]')  #用复数elements做循环
        # jobs = self.browser.find_elements(By.XPATH, '//li')
        source = BeautifulSoup(self.browser.page_source, "html.parser")
        links = source.find_all('a', class_='jobProperty jobtitle')
        for link in links:
            url = link.get('href')
            job_link_list.append(url)

        for detail_link in job_link_list:
            self.browser.get(detail_link)
            time.sleep(5)
            # js = json.loads(str(self.browser.page_source.encode()))
            # data = json.dumps(js)
            # print(data)
            item = GomTestItem()
            item['JobTitle'] = self.browser.find_element_by_xpath('//div[@class="questionClass"]/div/span/h1').text
            item['JobID'] = self.browser.find_element_by_xpath('//div[@class="questionClass"]/div/p[@class="answer ng-scope position3InJobDetails"]').text
            item['JobDescription'] = self.browser.find_element_by_xpath('//div[@class="questionClass"]/div/p[@class="answer ng-scope jobdescriptionInJobDetails"]').text
            # item['JobDescription'] = self.browser.find_element_by_xpath('//div[@class="questionClass"]/div/p/div/font/font').text
            # JobDetails = BeautifulSoup(self.browser.page_source, "html.parser").select('p[class="answer ng-scope jobdescriptionInJobDetails"]>ul[dir="ltr"]')
            i = 0
            # for JobDetail in JobDetails:
            #     if i == 0:
            #         item['JobResponsibilities'] = JobDetail .get_text("|")
            #     elif i == 1:
            #         item['JobAttributes'] = JobDetail.get_text("|")
            #     i = i + 1

            LeftSideDetails = BeautifulSoup(self.browser.page_source, "html.parser").select('p[class="answer ng-scope section2LeftfieldsInJobDetails"]')
            for LeftSideDetail in LeftSideDetails:
                if i == 0:
                    item['Band'] = LeftSideDetail.text
                elif i == 1:
                    item['State_Provice'] = LeftSideDetail.text
                elif i == 2:
                    item['Business_Group'] = LeftSideDetail.text
                elif i == 3:
                    item['PrimaryJobCategory'] = LeftSideDetail.text
                elif i == 4:
                    item['JobRole'] = LeftSideDetail.text
                elif i == 5:
                    item['EmploymentType'] = LeftSideDetail.text
                elif i == 7:
                    item['RequiredEducation'] = LeftSideDetail.text
                elif i == 8:
                    item['TravelRequired'] = LeftSideDetail.text
                elif i == 9:
                    item['Company'] = LeftSideDetail.text
                i = i + 1

            RightSideDetails = BeautifulSoup(self.browser.page_source, "html.parser").select('p[class="answer ng-scope section2RightfieldsInJobDetails"]')
            for RightSideDetail in RightSideDetails:
                if i == 0:
                    item['Country'] = RightSideDetail.text
                elif i == 1:
                    item['City_Township_Village'] = RightSideDetail.text
                elif i == 2:
                    item['BusinessUnit'] = RightSideDetail.text
                elif i == 3:
                    item['SecondaryJobCategory'] = RightSideDetail.text
                elif i == 4:
                    item['SkillSet'] = RightSideDetail.text
                elif i == 5:
                    item['ContractType'] = RightSideDetail.text
                elif i == 6:
                    item['PreferredEducation'] = RightSideDetail.text
                elif i == 7:
                    item['IsIncentivePosition'] = RightSideDetail.text
                elif i == 8:
                    item['Manager'] = RightSideDetail.text
                i = i + 1

            LeftSideTextAreas = BeautifulSoup(self.browser.page_source, "html.parser").select('p[class="answer ng-scope section2LeftfieldsInJobDetails jobDetailTextArea"]')
            for LeftSideTextArea in LeftSideTextAreas:
                if i == 0:
                    item['RequiredExpertise'] = LeftSideTextArea.get_text("|")
                elif i == 1:
                    item['PreferredExperience'] = LeftSideTextArea.get_text("|")
                elif i == 2:
                    item['EligibilityRequirements'] = LeftSideTextArea.text
                elif i == 3:
                    item['EOStatement'] = LeftSideTextArea.text
                i = i + 1
            yield item

            # for link in jobs:
        #     url = link.find_element_by_xpath('//div/div/span[@class="ng-scope"]/a').get_attribute('href')    #get_attribute获取属性值
        #     job_link_list.append(url)

        ######################################
        # for link in links:
        #     url = link.get('href')
        #     job_link_list.append(url)
        #
        # file = open('job_list.txt', 'wt')
        # for a in job_link_list:
        #     file.write(str(a))
        #     file.write("\n")
        # file.close()
        ######################################

        # time.sleep(10)
        # item = self.tem()
        self.browser.close()
        # yield item
        # return Request(url=self.browser.current_url, body=self.browser.page_source, encoding='utf-8', callback=self.tem)



        # return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding='utf-8')

        # def parse(self, response):
        #     filename = 'final.html'
        #     open(filename, 'wb').write(response.body)
