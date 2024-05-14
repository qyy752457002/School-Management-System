import pprint
import random

class Student:
    def __init__(self,id:int,name:str,gender:str,score:int,class_id:int):
        self.id = id
        self.name = name
        self.gender = gender
        self.score = score
        self.class_id = class_id

class LotteryAllocateTempClass:
    students = []
    id= 0
    total_score = 0
    gender_percent = 0
    total_student_num=0
    total_male_num=0
    total_female_num=0
    is_full = False

    def __init__(self,id:int ,capacity:int ):
        self.id = id
        self.class_capacity = capacity
        pass
    def allocate(self,student):
        if self.is_full:
            return False
        self.students.append(student)
        self.total_student_num = len(self.students)
        self.total_score+=student.score
        # self.gender_percent+=student.gender_percent
        if self.total_student_num == self.class_capacity:
            self.is_full = True
        self.total_male_num=0
        self.total_female_num=0
        for i,v in enumerate(self.students):

            if v.gender == '男':
                self.total_male_num+=1
            else:
                self.total_female_num+=1
                # v.class_id = self.id
        self.gender_percent=self.total_male_num/self.total_female_num if self.total_female_num>0 else self.total_male_num
        return True

        pass



def get_min_total_student_num( classes):
    stu_numbers=[]
    for i,v in classes.items():
        stu_numbers.append(v.total_student_num)
    print(stu_numbers)
    min_total_student_num=min(stu_numbers)
    res=[]
    for i,v in classes.items():
        if v.total_student_num == min_total_student_num:
            res.append(i)
    return res

def get_min_gender_percent( classes):
    stu_numbers=[]
    for i,v in classes.items():
        stu_numbers.append(v.gender_percent)
    # stu_numbers = map(lambda x: x.gender_percent, classes)
    min_total_student_num=min(stu_numbers)
    res=[]

    for i,v in classes.items():
        if v.gender_percent == min_total_student_num:
            res.append(i)

    return res



def main():

    #  打乱顺序   性别均衡  成绩均衡  年龄 生日  小学  初中要素包含 来源学校小学/ 乡镇
    # 假设我们有一个学生列表，每个学生有一个唯一的ID
    student_total = 15   #总学生数
    # 班级数量
    num_classes = 3
    classes_capacity = 10  #班级人数上限
    students = list(range(1, student_total+1))  # 假设有个学生
    # studic = dict(
    studic=[]
    # 随机 学生信息
    for i in students:
        tt = random.randint(0, 1)
        score = random.randint(1, 100)
        stutt={"id":i ,"gender":'女' if tt==0 else '男' ,"score":score
        }
        stu= Student(i,'',stutt['gender'],stutt['score'],0)
        studic.append(stu)

    pprint.pprint(studic)

    # random.shuffle(studic)
    # print(students)

    # print('打乱顺序',studic)

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
    classes = {i: LotteryAllocateTempClass(i,classes_capacity) for i in range(1, num_classes + 1)}
    # classes_total = {i: 0 for i in range(1, num_classes + 1)}
    # classes_male = {i: 0 for i in range(1, num_classes + 1)}
    # classes_female = {i: 0 for i in range(1, num_classes + 1)}
    print(classes)

    # 公平拉票过程
    while studic:
        # 随机选择一个学生
        student = studic.pop()
        print(f"当前选中的学生是： student {student}")


        min_value_total = get_min_total_student_num(classes)
        min_value_gender_percent = get_min_total_student_num(classes)
        s1= set(min_value_total)
        s2= set(min_value_gender_percent)
        com = s2 & s1
        if len(min_value_total)==0:
            print('没有最小值')
            exit(2)
        if len(com)==0:
            # min_key_total = min(classes, key=classes.get)
            id = min_value_total.pop()

        else:
            # min_key_total = random.choice(com)
            id = com.pop()

        # 获取字典中的最小值对应的键
        # min_key_total = min(classes_total, key=classes_total.get)
        # print(f"最小值对应的键是： {min_key_total}", min_value_total,'最小值')
        res=classes[id].allocate(student)
        if res:
            print(f"学生 {student} 分配到班级 {id} 成功")
        else:
            print(f"学生 {student} 分配到班级 {id} 失败")
            # studic.append(student)





        # 如果当前学生的性别为男
        # if student['gender'] == '男':
            # 如果A班的男生数量少于B班，或者A班的男生数量等于B班但A班的总分低于B班  获取 男生数量最少得班级
            # min(classes_male)
            # 获取字典中的最小值
            # min_value = min(classes_male.values())

            # 获取字典中的最小值对应的键
            # min_key = min(classes_male, key=classes_male.get)
            # print(f"最小值对应的键是： {min_key}", min_value,'最小值male')



            # if min_key==min_key_total:
            #     # classes[min_key].append(student)
            #     # classes_total[min_key]+=1
            #     # classes_male[min_key]+=1
            #     # total_score_a += student['score']
            #     # male_count_a += 1
            # else:
            #     # class_b.append(student)
            #     # total_score_b += student['score']
            #     # male_count_b += 1
            #     print(classes)
                # pass
        # 如果当前学生的性别为女
        # if student['gender'] == '女':
        #     min_value = min(classes_female.values())
        #
        #     # 获取字典中的最小值对应的键
        #     min_key = min(classes_female, key=classes_female.get)
        #     print(f"最小值对应的键是： {min_key}", min_value,'最小值female')
        #
        #     # 如果A班的女生数量少于B班，或者A班的女生数量等于B班但A班的总分低于B班
        #     if min_key==min_key_total:
        #         classes[min_key].append(student)
        #         classes_total[min_key]+=1
        #         classes_female[min_key]+=1
        #     else:
        #         print(classes)





        # 随机选择一个班级
        # chosen_class = random.randint(1, num_classes)
        # print(f"Chosen class {chosen_class}")

        # 如果该班级还没有满员，将学生分配到该班级
        # if len(classes[min_key]) < classes_capacity:  # 假设每个班级最多10人
            # classes[chosen_class].append(student)
            # students.remove(student)  # 从待分配学生列表中移除
        #     print('池子剩余学生数量',len(studic))
        # else:
        #     print(f"需要移除刚才那个分配 Class {min_key} is full, skipping student {student}")

    # 打印两个班级的学生列表
    # print("班级A的学生:")
    # pprint.pprint(class_a)
    # print("班级B的学生:")
    # pprint.pprint(class_b)

    # 打印两个班级的分数总和
    # print("班级A的总分:", student_total)
    # # print("班级B的总分:", total_score_b)
    #
    # # 打印两个班级的性别数量
    # print("班级的男生数量:", classes_male)
    # print("班级的女生数量:", classes_female)
    # print("班级B的男生数量:", male_count_b)
    # print("班级B的女生数量:", female_count_b)

    # 打印最终的班级分配结果
    for cls, stu_list in classes.items():
        print(f"Class {cls}: {stu_list}")
        print(stu_list.students.__str__())
        print(vars(stu_list))


if __name__ == '__main__':
    main()