import pprint
import random


def main():

    # todo 打乱顺序   性别均衡  成绩均衡  年龄 生日  小学  初中要素包含 来源学校小学/ 乡镇
    # 假设我们有一个学生列表，每个学生有一个唯一的ID
    student_total = 20   #总学生数
    # 班级数量
    num_classes = 2
    classes_capacity = 10  #班级人数上限
    students = list(range(1, student_total+1))  # 假设有个学生
    # studic = dict(
    studic=[]
    for i in students:
        tt = random.randint(0, 1)
        score = random.randint(1, 100)
        stu={"id":i ,"gender":'女' if tt==0 else '男' ,"score":score
        }
        studic.append(stu)




    pprint.pprint(studic)

    # random.shuffle(studic)
    # print(students)

    print('打乱顺序',studic)

    # 首先将学生列表按分数排序
    # studic.sort(key=lambda x: x['score'], reverse=False)

    # 初始化两个班级
    class_a = []
    class_b = []

    # 记录两个班级的分数总和 4个维度
    total_score_a = 0
    total_score_b = 0

    # 记录两个班级的性别数量
    male_count_a = 0
    female_count_a = 0
    male_count_b = 0
    female_count_b = 0



    # 初始化班级字典
    classes = {i: [] for i in range(1, num_classes + 1)}
    classes_total = {i: 0 for i in range(1, num_classes + 1)}
    classes_male = {i: 0 for i in range(1, num_classes + 1)}
    classes_female = {i: 0 for i in range(1, num_classes + 1)}
    print(classes)

    # 公平拉票过程
    while studic:
        # 随机选择一个学生
        student = studic.pop()
        print(f"当前选中的学生是： student {student}")


        min_value_total = min(classes_total.values())

        # 获取字典中的最小值对应的键
        min_key_total = min(classes_total, key=classes_total.get)
        print(f"最小值对应的键是： {min_key_total}", min_value_total,'最小值')



        # 如果当前学生的性别为男
        if student['gender'] == '男':
            # 如果A班的男生数量少于B班，或者A班的男生数量等于B班但A班的总分低于B班  获取 男生数量最少得班级
            # min(classes_male)
            # 获取字典中的最小值
            min_value = min(classes_male.values())

            # 获取字典中的最小值对应的键
            min_key = min(classes_male, key=classes_male.get)
            print(f"最小值对应的键是： {min_key}", min_value,'最小值male')



            if min_key==min_key_total:
                classes[min_key].append(student)
                classes_total[min_key]+=1
                classes_male[min_key]+=1
                # total_score_a += student['score']
                # male_count_a += 1
            else:
                # class_b.append(student)
                # total_score_b += student['score']
                # male_count_b += 1
                print(classes)
                # pass
        # 如果当前学生的性别为女
        if student['gender'] == '女':
            min_value = min(classes_female.values())

            # 获取字典中的最小值对应的键
            min_key = min(classes_female, key=classes_female.get)
            print(f"最小值对应的键是： {min_key}", min_value,'最小值female')

            # 如果A班的女生数量少于B班，或者A班的女生数量等于B班但A班的总分低于B班
            if min_key==min_key_total:
                classes[min_key].append(student)
                classes_total[min_key]+=1
                classes_female[min_key]+=1
            else:
                print(classes)





        # 随机选择一个班级
        # chosen_class = random.randint(1, num_classes)
        # print(f"Chosen class {chosen_class}")

        # 如果该班级还没有满员，将学生分配到该班级
        if len(classes[min_key]) < classes_capacity:  # 假设每个班级最多10人
            # classes[chosen_class].append(student)
            # students.remove(student)  # 从待分配学生列表中移除
            print('池子剩余学生数量',len(studic))
        else:
            print(f"需要移除刚才那个分配 Class {min_key} is full, skipping student {student}")

    # 打印两个班级的学生列表
    # print("班级A的学生:")
    # pprint.pprint(class_a)
    # print("班级B的学生:")
    # pprint.pprint(class_b)

    # 打印两个班级的分数总和
    print("班级A的总分:", student_total)
    # print("班级B的总分:", total_score_b)

    # 打印两个班级的性别数量
    print("班级的男生数量:", classes_male)
    print("班级的女生数量:", classes_female)
    # print("班级B的男生数量:", male_count_b)
    # print("班级B的女生数量:", female_count_b)

    # 打印最终的班级分配结果
    for cls, stu_list in classes.items():
        print(f"Class {cls}: {stu_list}")


if __name__ == '__main__':
    main()