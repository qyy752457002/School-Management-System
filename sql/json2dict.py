import json

# 已有的数据


data = """{
    "ENROLLMENT_METHOD": [
        {
            "label": "寄宿",
            "value": "boarding"
        },
        {
            "label": "走读",
            "value": "day_student"
        }
    ],
    "RELATION": [
        {
            "label": "父亲",
            "value": "father"
        },
        {
            "label": "母亲",
            "value": "mother"
        },
        {
            "label": "爷爷",
            "value": "grandfather"
        },
        {
            "label": "奶奶",
            "value": "grandmother"
        },
        {
            "label": "外公",
            "value": "paternal_grandfather"
        },
        {
            "label": "外婆",
            "value": "paternal_grandmother"
        }
    ],
    "GRADUATION_STATUS": [
        {
            "value": "graduation",
            "label": "毕业"
        },
        {
            "value": "completion",
            "label": "结业"
        },
        {
            "value": "withdrawal",
            "label": "肄业"
        }
    ],
    "FAMILY_MEMBER_OCCUPATION": [
        {
            "label": "国家机关、党群组织、企业、事业单位负责人",
            "value": "government_agency_party_group_leaders",
            "children": [
                {
                    "label": "中国共产党中央委员会和地方各级组织负责人",
                    "value": "ccp_leaders_at_central_and_local_levels"
                },
                {
                    "label": "民主党派和社会团体及其工作机构负责人",
                    "value": "non_ccp_political_parties_social_groups_leaders"
                },
                {
                    "label": "事业单位负责人",
                    "value": "public_institution_leaders"
                },
                {
                    "label": "企业负责人",
                    "value": "enterprise_leaders"
                }
            ]
        },
        {
            "label": "专业技术人员",
            "value": "technical_professionals",
            "children": [
                {
                    "label": "工程技术人员",
                    "value": "engineering_technicians"
                },
                {
                    "label": "农业技术人员",
                    "value": "agricultural_technicians"
                },
                {
                    "label": "飞机和船舶技术人员",
                    "value": "aircraft_and_ship_technicians"
                },
                {
                    "label": "卫生专业技术人员",
                    "value": "healthcare_technical_professionals"
                },
                {
                    "label": "经济业务人员",
                    "value": "economic_business_personnel"
                },
                {
                    "label": "金融业务人员",
                    "value": "financial_business_personnel"
                },
                {
                    "label": "法律专业人员",
                    "value": "legal_professionals"
                },
                {
                    "label": "教学人员",
                    "value": "teaching_personnel"
                },
                {
                    "label": "文学艺术工作人员",
                    "value": "literary_art_workers"
                },
                {
                    "label": "体育工作人员",
                    "value": "sports_workers"
                },
                {
                    "label": "新闻出版、文化工作人员",
                    "value": "news_publication_culture_workers"
                },
                {
                    "label": "宗教职业者",
                    "value": "religious_professionals"
                },
                {
                    "label": "其他专业技术人员",
                    "value": "other_technical_professionals"
                }
            ]
        },
        {
            "label": "办事人员和有关人员",
            "value": "administrative_staff_related_personnel",
            "children": [
                {
                    "label": "行政办公人员",
                    "value": "administrative_office_personnel"
                },
                {
                    "label": "安全保卫和消防人员",
                    "value": "security_fire_protection_personnel"
                },
                {
                    "label": "邮政和电信业务人员",
                    "value": "postal_telecommunications_business_personnel"
                },
                {
                    "label": "其他办事人员和有关人员",
                    "value": "other_administrative_staff_related_personnel"
                }
            ]
        },
        {
            "label": "商业、服务业人员",
            "value": "commerce_service_personnel",
            "children": [
                {
                    "label": "购销人员",
                    "value": "purchasing_sales_personnel"
                },
                {
                    "label": "仓储人员",
                    "value": "warehousing_personnel"
                },
                {
                    "label": "餐馆服务人员",
                    "value": "restaurant_service_personnel"
                },
                {
                    "label": "饭店、旅游及健身娱乐场所服务人员",
                    "value": "hotel_travel_fitness_recreation_facility_staff"
                },
                {
                    "label": "运输服务人员",
                    "value": "transportation_service_personnel"
                },
                {
                    "label": "医疗卫生辅助服务人员",
                    "value": "medical_health_assistance_service_personnel"
                },
                {
                    "label": "社会服务和居民生活服务人员",
                    "value": "social_residential_life_service_personnel"
                },
                {
                    "label": "其他商业、服务业人员",
                    "value": "other_commerce_service_personnel"
                }
            ]
        },
        {
            "label": "农、林、牧、渔、水利业生产人员",
            "value": "agriculture_forestry_animal_husbandry_fishery_water_conservation_workers",
            "children": [
                {
                    "label": "种植业生产人员",
                    "value": "crop_production_workers"
                },
                {
                    "label": "林业生产及野生动物保护人员",
                    "value": "forestry_production_wildlife_conservation_workers"
                },
                {
                    "label": "畜牧业生产人员",
                    "value": "animal_husbandry_production_workers"
                },
                {
                    "label": "渔业生产人员",
                    "value": "fishery_production_workers"
                },
                {
                    "label": "水利设备管理养护人员",
                    "value": "water_management_maintenance_workers"
                },
                {
                    "label": "其他农、林、牧、鱼、水利业生产人员",
                    "value": "other_agriculture_forestry_animal_husbandry_fishery_water_workers"
                }
            ]
        },
        {
            "label": "生产、运输设备操作人员及有关人员",
            "value": "production_transport_equipment_operators_related_personnel",
            "children": [
                {
                    "label": "勘测及矿物开采人员",
                    "value": "surveying_mineral_extraction_workers"
                },
                {
                    "label": "金属冶炼、轧制人员",
                    "value": "metal_smelting_rolling_workers"
                },
                {
                    "label": "化工产品生产人员",
                    "value": "chemical_product_production_workers"
                },
                {
                    "label": "机械制造加工人员",
                    "value": "machinery_manufacturing_processing_workers"
                },
                {
                    "label": "机电产品装配人员",
                    "value": "electromechanical_product_assemblers"
                },
                {
                    "label": "机械设备修理人员",
                    "value": "mechanical_equipment_repair_workers"
                },
                {
                    "label": "电力设备安装、运行、检修及供电人员",
                    "value": "power_equipment_installation_operation_maintenance_supply_workers"
                },
                {
                    "label": "电子元器件与设备制造、装配、调试及维修人员",
                    "value": "electronics_components_device_manufacturing_assembly_debugging_repair_workers"
                },
                {
                    "label": "橡胶和塑料制品生产人员",
                    "value": "rubber_plastic_products_production_workers"
                },
                {
                    "label": "纺织、针织、印染人员",
                    "value": "textile_knitting_dyeing_workers"
                },
                {
                    "label": "裁剪、缝纫和皮革、毛皮制品加工制作人员",
                    "value": "cutting_sewing_leather_fur_products_manufacturing_workers"
                },
                {
                    "label": "粮油、食品、饮料生产加工及饲料生产加工人员",
                    "value": "grain_oil_food_beverage_feed_production_processing_workers"
                },
                {
                    "label": "烟草及其制品加工人员",
                    "value": "tobacco_and_its_products_processing_workers"
                },
                {
                    "label": "药品生产人员",
                    "value": "pharmaceutical_production_workers"
                },
                {
                    "label": "木材加工、人造板生产、木制品制作及制浆、造纸和纸制品生产加工人员",
                    "value": "wood_processing_artificial_board_production_wood_products_making_pulp_paper_paper_products_processing_workers"
                },
                {
                    "label": "建筑材料生产加工人员",
                    "value": "building_materials_production_processing_workers"
                },
                {
                    "label": "玻璃、陶瓷、搪瓷及其制品生产加工人员",
                    "value": "glass_ceramics_enamel_and_their_products_production_processing_workers"
                },
                {
                    "label": "广播影视制品制作、播放及文物保护作业人员",
                    "value": "broadcasting_films_television_programs_production_broadcasting_cultural_relics_protection_workers"
                },
                {
                    "label": "印刷人员",
                    "value": "printing_workers"
                },
                {
                    "label": "工艺、美术品制作人员",
                    "value": "arts_crafts_manufacturing_workers"
                },
                {
                    "label": "文化教育、体育用品制作人员",
                    "value": "cultural_education_sports_goods_manufacturing_workers"
                },
                {
                    "label": "工程施工人员",
                    "value": "construction_engineering_workers"
                },
                {
                    "label": "运输设备操作人员及有关人员",
                    "value": "transport_equipment_operators_related_personnel"
                },
                {
                    "label": "环境监测及废物处理人员",
                    "value": "environmental_monitoring_waste_treatment_workers"
                },
                {
                    "label": "检验、计量人员",
                    "value": "inspection_measurement_workers"
                },
                {
                    "label": "其他生产、运输设备操作人员及有关人员",
                    "value": "other_production_transport_equipment_operators_related_personnel"
                }
            ]
        },
        {
            "label": "军人",
            "value": "military_personnel"
        },
        {
            "label": "不便分类的其他从业人员",
            "value": "other"
        }
    ]
}"""

datas = [ data,

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
id= 6295

with open('../aa.log', 'w', encoding='utf-8') as f2:

    for data in datas:

        # 解析字符串
        parsed_data = json.loads(data)

        # 提取label和value
        labels_values = extract_labels_values(parsed_data)
        res.update({i['value']:i['label'] for i in labels_values})

    for i,value in res.items():
        # EnumValue(id=6294,enum_name="blood_type",description="其他血型",enum_value="other_blood_type",parent_id="",sort_number=0,is_enabled=True,created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False),
        outstr='EnumValue(id=%s,enum_name="major",enum_value="%s",description="%s",parent_id="",sort_number=0,is_enabled=True,created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False), '
        f2.write(outstr%(id,i,value)+'\n')
        id+=1



print(res)
# # 打印提取的结果
# for item in labels_values:
#     print(item)


