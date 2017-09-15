# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GomTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    JobTitle = scrapy.Field()
    JobID = scrapy.Field()
    JobDescription = scrapy.Field()
    # JobResponsibilities = scrapy.Field()
    # JobAttributes = scrapy.Field()
    Band = scrapy.Field()
    Country = scrapy.Field()
    State_Provice = scrapy.Field()
    City_Township_Village = scrapy.Field()
    Business_Group = scrapy.Field()
    BusinessUnit = scrapy.Field()
    PrimaryJobCategory = scrapy.Field()
    SecondaryJobCategory = scrapy.Field()
    JobRole = scrapy.Field()
    SkillSet = scrapy.Field()
    EmploymentType = scrapy.Field()
    ContractType = scrapy.Field()
    RequiredExpertise = scrapy.Field()
    PreferredExperience = scrapy.Field()
    EligibilityRequirements = scrapy.Field()
    RequiredEducation = scrapy.Field()
    PreferredEducation = scrapy.Field()
    TravelRequired = scrapy.Field()
    IsIncentivePosition = scrapy.Field()
    Company = scrapy.Field()
    Manager = scrapy.Field()
    EOStatement = scrapy.Field()
