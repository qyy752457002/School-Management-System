import json

# 已有的数据


data = """[{"value":"preSchoolEducation","label":"学前教育","children":[{"value":"kindergarten","label":"幼儿园","children":[{"value":"kindergarten","label":"幼儿园"},{"value":"attachedKindergartenClass","label":"附设幼儿班"}]}]},{"value":"primaryEducation","label":"初等教育","children":[{"value":"primarySchool","label":"小学","children":[{"value":"primarySchool","label":"小学"},{"value":"primarySchoolTeachingPoint","label":"小学教学点"},{"value":"attachedPrimarySchoolClass","label":"附设小学班"}]},{"value":"adultPrimarySchool","label":"成人小学","children":[{"value":"staffPrimarySchool","label":"职工小学"},{"value":"migrantWorkerPrimarySchool","label":"农民工小学"},{"value":"primarySchoolClass","label":"小学班"},{"value":"literacyClass","label":"扫盲班"}]}]},{"value":"secondaryEducation","label":"中等教育","children":[{"value":"ordinaryJuniorHigh","label":"普通初中","children":[{"value":"vocationalJuniorHigh","label":"职业初中"},{"value":"attachedVocationalJuniorHighClass","label":"附设职业初中班"},{"value":"adultEmployeeJuniorHigh","label":"成人职工初中"},{"value":"adultFarmerJuniorHigh","label":"成人农民初中"}]},{"value":"vocationalJuniorHigh","label":"职业初中","children":[{"value":"vocationalJuniorHigh","label":"职业初中"},{"value":"attachedVocationalJuniorHighClass","label":"附设职业初中班"}]},{"value":"adultJuniorHigh","label":"成人初中","children":[{"value":"adultEmployeeJuniorHigh","label":"成人职工初中"},{"value":"adultFarmerJuniorHigh","label":"成人农民初中"}]},{"value":"ordinaryHighSchool","label":"普通高中","children":[{"value":"comprehensiveHighSchool","label":"完全中学"},{"value":"seniorHighSchool","label":"高级中学"},{"value":"twelveYearSystemSchool","label":"十二年一贯制学校"},{"value":"attachedOrdinaryHighSchoolClass","label":"附设普通高中班"}]},{"value":"adultHighSchool","label":"成人高中","children":[{"value":"adultEmployeeHighSchool","label":"成人职工高中"},{"value":"adultFarmerHighSchool","label":"成人农民高中"}]},{"value":"secondaryVocationalSchool","label":"中等职业学校","children":[{"value":"adjustedSecondaryVocationalSchool","label":"调整后中等职业学校"},{"value":"secondaryTechnicalSchool","label":"中等技术学校"},{"value":"secondaryNormalSchool","label":"中等师范学校"},{"value":"adultSecondaryProfessionalSchool","label":"成人中等专业学校"},{"value":"vocationalHighSchool","label":"职业高中学校"},{"value":"technicalSchool","label":"技工学校"},{"value":"attachedVocationalClass","label":"附设中职班"},{"value":"otherVocationalInstitutions","label":"其他中职机构"}]},{"value":"workStudySchool","label":"工读学校","children":[{"value":"workStudySchool","label":"工读学校"}]}]},{"value":"specialEducation","label":"特殊教育","children":[{"value":"specialEducationSchool","label":"特殊教育学校","children":[{"value":"schoolForBlind","label":"盲人学校"},{"value":"schoolForDeaf","label":"聋人学校"},{"value":"schoolForIntellectuallyDisabled","label":"培智学校"},{"value":"otherSpecialEducationSchools","label":"其他特教学校"},{"value":"attachedSpecialEducationClasses","label":"附设特教班"}]}]},{"value":"otherEducation","label":"其他教育","children":[{"value":"jinxingInstitution","label":"进修机构","children":[{"value":"jinxingInstitution","label":"进修机构"}]},{"value":"researchInstitution","label":"研究机构","children":[{"value":"educationResearchInstitute","label":"教育研究院"}]},{"value":"practiceInstitution","label":"实践机构","children":[{"value":"practiceBase","label":"实践基地"}]}]},{"value":"trainingInstitution","label":"培训机构"}]"""

datas = [ data,"""[{"value":"PublicOwnership","label":"公办"},{"value":"PrivateOwnership","label":"民办"}]""",

          """{
  "star_level": [
    { "label": "一星", "value": "1" },
    { "label": "二星", "value": "2" },
    { "label": "三星", "value": "3" },
    { "label": "四星", "value": "4" },
    { "label": "五星", "value": "5" }
  ],
  "id_type": [
    { "label": "居民身份证", "value": "resident_id_card" },
    { "label": "军官证", "value": "military_officer_id" },
    { "label": "士兵证", "value": "soldier_id" },
    { "label": "文职干部证", "value": "civilian_officer_id" },
    { "label": "部队离退休证", "value": "military_retiree_id" },
    { "label": "香港特区护照/身份证明", "value": "hong_kong_passport_id" },
    { "label": "澳门特区护照/身份证明", "value": "macau_passport_id" },
    { "label": "台湾居民来往大陆通行证", "value": "taiwan_resident_travel_permit" },
    { "label": "境外永久居住证", "value": "overseas_permanent_residence_permit" },
    { "label": "护照", "value": "passport" },
    { "label": "出生证明", "value": "birth_certificate" },
    { "label": "户口薄", "value": "household_register" },
    { "label": "其他", "value": "other" }
  ],
  "gender": [
    { "label": "男", "value": "male" },
    { "label": "女", "value": "female" }
  ]
} """,

          ]

def extract_labels_values(data):
    labels_values = []

    def recursive_extract(obj):
        if isinstance(obj, dict):
            if 'label' in obj and 'value' in obj:
                labels_values.append({'label': obj['label'], 'value': obj['value']})
            for val in obj.values():
                recursive_extract(val)
        elif isinstance(obj, list):
            for item in obj:
                recursive_extract(item)

    recursive_extract(data)
    return labels_values
res=dict()
for data in datas:

    # 解析字符串
    parsed_data = json.loads(data)

    # 提取label和value
    labels_values = extract_labels_values(parsed_data)
    res.update({i['value']:i['label'] for i in labels_values})
print(res)
# # 打印提取的结果
# for item in labels_values:
#     print(item)


