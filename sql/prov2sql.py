import json

with open('province.json', 'r', encoding='utf-8') as f:
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



    # cursor.execute(insert_template, values)

# connection.commit()
# cursor.close()
# connection.close()