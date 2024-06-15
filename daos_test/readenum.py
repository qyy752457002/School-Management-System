import os
import pprint

filepath = 'aa.txt'
data= []
try:
    if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
        with open(filepath, 'r',encoding='utf-8') as f:
            bigcode= ''
            bigcate= ''
            secondcode= ''
            secondcate = ''
            thirdcode= ''
            thirdcate= ''
            id= 4435
            with open('../aa.log', 'w', encoding='utf-8') as f2:
                for i,line in enumerate(f.readlines()):
                    line=line.replace('\n', '')
                    # print(type(line))
                    # print(f"{line}", end="")
                    if line.endswith('大类'):
                        bigcode= line[0:2]
                        bigcate= line[2:]
                        print(f"一级 {bigcode} {bigcate}",i)
                        # print("suc")
                    elif line.find('	')>0:
                        res = line.split('	')
                        # secondcode= line[0:4]
                        # secondcate= line[4:]
                        thirdcate= res[2]
                        thirdcode= res[1]
                        print('三级',type(res),res )
                        # print('xx'.format(res ))
                        print(f"{thirdcode} {thirdcate}",i)
                        outstr='EnumValue(  id=%s,enum_name="major_lv3", enum_value="%s", description="%s", sort_number=0,parent_id="%s",is_enabled=True,created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False), '
                        print(outstr%(id,thirdcode,thirdcate,secondcode))
                        f2.write(outstr%(id,thirdcode,thirdcate,secondcode)+'\n')
                        id+=1

                        # print(f"{res} ",i,thirdcode,thirdcate)
                        # exit(0)
                        # pprint.pprint(res)
                        # print("suc")
                    else:
                        secondcode= line[0:4]
                        secondcate= line[4:]
                        print(f"二级  {secondcode} {secondcate}",i)
                        outstr='EnumValue(  id=%s,enum_name="major_lv2", enum_value="%s", description="%s", sort_number=0,parent_id="%s",is_enabled=True,created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False), '
                        # print(outstr%(id,thirdcode,thirdcate,secondcode))
                        f2.write(outstr%(id,secondcode,secondcate,bigcode)+'\n')
                        id+=1

                        # print("suc")

                    if i==30:
                        # exit()
                        pass
                    # if line.isnumeric() or isinstance(line, float):
                    #     data.append(float(line))
                    #     # print(line)
                    # else:
                    #     print("格式异常 本行数据跳过 ")
                    # pass
            # total = sum(data)
            # avg = total/len(data)
            # maxnumber = max(data)
            # minnumber= min(data)
            print("suc",)
        pass
    else:
        print("File does not exist or is not readable")
except Exception as e:
    print(e,'操作异常')

