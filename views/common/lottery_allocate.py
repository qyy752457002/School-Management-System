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
            return self,False
        self.students.append(student)
        self.total_student_num = len(self.students)
        self.total_score+=student.score
        if self.total_student_num == self.class_capacity:
            self.is_full = True
        self.total_male_num=0
        self.total_female_num=0
        for i,v in enumerate(self.students):

            if v.gender == '男':
                self.total_male_num+=1
            else:
                self.total_female_num+=1
        self.gender_percent=self.total_male_num/self.total_female_num if self.total_female_num>0 else self.total_male_num
        return self,True

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
    min_total_student_num=min(stu_numbers)
    res=[]

    for i,v in classes.items():
        if v.gender_percent == min_total_student_num:
            res.append(i)

    return res



def main():

    #  打乱顺序   性别均衡  成绩均衡  年龄 生日  小学  初中要素包含 来源学校小学/ 乡镇
    # 假设我们有一个学生列表，每个学生有一个唯一的ID
    student_total = 30   #总学生数
    # 班级数量
    num_classes = 3
    classes_capacity = 10  #班级人数上限
    students = list(range(1, student_total+1))  # 假设有个学生
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

    # 首先将学生列表按分数排序
    # studic.sort(key=lambda x: x['score'], reverse=False)

    # 初始化班级字典
    classes = {i: LotteryAllocateTempClass(i,classes_capacity) for i in range(1, num_classes + 1)}
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
            id = min_value_total.pop()

        else:
            id = com.pop()

        # 获取字典中的最小值对应的键
        classes[id],res=classes[id].allocate(student)
        if res:
            print(f"学生 {student} 分配到班级 {id} 成功")
        else:
            print(f"学生 {student} 分配到班级 {id} 失败")
            # studic.append(student)

    # 打印最终的班级分配结果
    for cls, stu_list in classes.items():
        print(f"Class {cls}: {stu_list}")
        print(stu_list.students.__str__())
        print(vars(stu_list))


if __name__ == '__main__':
    main()