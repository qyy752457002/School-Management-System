import json

import os

directory_to_traverse = "./country"

for root, dirs, files in os.walk(directory_to_traverse):
    for file in files:
        file_path = os.path.join(root, file)  # 构造文件的完整路径
        print(file_path)  # 打印文件的完整路径
        if file.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(data)
                insert_template = """
    INSERT INTO lfun_enum_value (   enum_name   , enum_value, description ,is_enabled , created_at,updated_at , is_deleted 
    ) VALUES (  'province',  '%s', '%s', True ,'2020-10-01 00:00:00','2020-10-01 00:00:00', False  );
    """


                con = [ ]
                for item in data:
                    values = (item['value'], item['label'] )  # 从JSON对象中提取值
                    # print(values)


                    tt =formatted_string = insert_template % (item['value'], item['label'])
                    print(tt)
                    con.append(tt)


                    # break
                with open("output.txt", "w", encoding="utf-8") as file:
                    for line in con:
                        file.write(line)
                        file.write("\n")  # 添加换行符


# with open('province.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#     print(data)
#
#
#     insert_template = """
#     INSERT INTO lfun_enum_value (   enum_name   , enum_value, description ,is_enabled , created_at,updated_at , is_deleted
#     ) VALUES (  'province',  '%s', '%s', True ,'2020-10-01 00:00:00','2020-10-01 00:00:00', False  );
#     """
#
#
#     con = [ ]
#     for item in data:
#         values = (item['value'], item['label'] )  # 从JSON对象中提取值
#         # print(values)
#
#
#         tt =formatted_string = insert_template % (item['value'], item['label'])
#         print(tt)
#         con.append(tt)
#
#
#         # break
#     with open("output.txt", "w", encoding="utf-8") as file:
#         for line in con:
#             file.write(line)
#             file.write("\n")  # 添加换行符



    # cursor.execute(insert_template, values)

# connection.commit()
# cursor.close()
# connection.close()