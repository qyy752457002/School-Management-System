import pprint
import random
import statistics
from heapq import nsmallest

class Student:
    def __init__(self, id: int, name: str, gender: str, score: int, class_id: int):
        self.id = id
        self.name = name
        self.gender = gender
        self.score = score
        self.class_id = class_id

class LotteryClass:
    def __init__(self, id: int, capacity: int):
        # 属性定义放在init里  不是直接写的 是因为要初始化
        self.id = id
        self.avg_score = 0
        self.gender_percent = 0
        self.total_student_num = 0
        self.total_male_num = 0
        self.total_female_num = 0
        self.students = []
        self.class_capacity = capacity
        self.total_score = 0

        self.is_full = False

    def allocate(self, student):
        self.total_student_num = self.students.__len__()

        if self.total_student_num < self.class_capacity:
            self.is_full = False

        if self.is_full:
            return self, False
        student.class_id = self.id
        self.students.append(student)
        self.total_student_num += 1
        self.total_score += student.score
        if self.total_student_num == self.class_capacity:
            self.is_full = True
        self.total_male_num = sum(1 for s in self.students if s.gender == '男')
        self.total_female_num = sum(1 for s in self.students if s.gender == '女')
        self.gender_percent = self.total_male_num / self.total_female_num if self.total_female_num > 0 else self.total_male_num
        self.gender_percent = round( self.gender_percent ,2)
        self.avg_score = round( self.total_score / self.total_student_num,2)
        print('分配suc')
        return self, True

    def __str__(self):
        for s in self.students:
            print(vars(s))
            pass
        return f"Class {self.id}: {self.students}"

def get_min_value(classes, attribute):
    """
    获取具有最小属性值的班级列表，排除满的。

    参数:
    classes: 包含班级对象的字典。
    attribute: 需要比较的属性名。
    """
    # 初始化结果列表和最小值变量
    result = []
    min_value = None

    # 遍历字典中的每个班级对象
    for class_key, class_obj in classes.items():
        if class_obj.is_full:
            continue
        try:
            # 尝试获取指定属性的值
            value = getattr(class_obj, attribute)
        except AttributeError:
            # 如果属性不存在，跳过当前班级
            continue

        # 如果min_value尚未设置，或当前值更小
        if min_value is None or value < min_value:
            # 更新最小值和结果列表
            min_value = value
            result = [class_key]
        # 如果当前值与最小值相等，添加当前班级到结果列表
        elif value == min_value:
            result.append(class_key)

    return result

def generate_students(num_students):
    """生成随机学生数据"""
    # return [Student(i, f"Student{i}", '女' if random.randint(0, 1) == 0 else '男', random.randint(1, 100), 0) for i in range(1, num_students + 1)]
    return [Student(i, f"Student{i}", '女' if i%2 == 0 else '男',  100- (i%13)*2 , 0) for i in range(1, num_students + 1)]

# 读取csv 格式 学生1,M,85
def read_csv(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        students = []
        i=0
        for line in lines:
            if i==0:
                i+=1
                continue
            parts = line.strip().split(',')
            name = parts[1]
            gender = '男' if  parts[2]=='Male' else '女'
            score = int(parts[3])
            students.append(Student(i,name, gender, score,0))
            i+=1

        return students
def exchange(index, jindex,classes):
    for i in classes[index].students:
        if classes[index].gender_percent<1:
            if i.gender == '女':
                # classes[index].students.remove(i)
                # classes[jindex].students.append(i)
                # classes[jindex].allocate(i)
                # return classes
                pass

            else:
                continue

        for j in classes[jindex].students:
            if i.score == j.score and i.gender != j.gender:
                # i ,j  =  j,i
                # classes[index].students[   classes[index].students.index(i)  ] = j
                # classes[jindex].students[   classes[jindex].students.index(j)  ] = i

                classes[index].students.remove( i )
                classes[jindex].students.remove( j )
                r= classes[index].allocate( j )
                r2= classes[jindex].allocate( i )
                # classes[index].students[   classes[index].students.index(i)  ] = i
                # j.class_id = classes[index].id
                # exchange(index,jindex,classes)
                return classes,True
    return classes,False



def main():
    student_total = 300
    num_classes = 10
    classes_capacity = 30
    # students = generate_students(student_total)
    students = read_csv( 'students_data_300.csv')
    pprint.pprint(students)
    # 按照成绩倒序排序
    students = nsmallest(student_total, students, key=lambda s: s.score)
    # pprint.pprint(students)
    for s in students:
        print(vars(s))


    classes = {i: LotteryClass(i, classes_capacity) for i in range(1, num_classes + 1)}

    while students:
        student = students.pop()
        print(f"当前选中的学生是： student {student}",student.score)

        min_total_student_num = get_min_value(classes, 'total_score')
        min_value_gender_percent = get_min_value(classes, 'gender_percent')
        common_classes = set(min_total_student_num) & set(min_value_gender_percent)
        if not min_total_student_num:
            print('没有最小值班级')
            continue
        # target_class_id =  list(common_classes).pop() if common_classes else min_total_student_num[0]
        # target_class_id = random.choice( list(common_classes)) if common_classes else min_total_student_num[0]
        # 如果是多个 招出比例 和当前性别相反的那个 否则0
        if common_classes:
            target_class_id =  list(common_classes).pop()
        else:
            target_class_id =  min_total_student_num[0]
            if len(min_total_student_num)>1:
                tt = dict()
                for i in min_total_student_num:
                    # if i != target_class_id:
                        tt[i]=classes[i].gender_percent
                # sorted(tt)
                sorted_dict_by_value = [k  for k, v in sorted(tt.items(), key=lambda item: item[1], reverse=True)]

                # print(tt)
                if student.gender == '女':
                    target_class_id =  sorted_dict_by_value[0]
                else:
                    target_class_id =  sorted_dict_by_value[len(sorted_dict_by_value)-1]






        class_obj, res = classes[target_class_id].allocate(student)
        if res:
            print(f"学生 {student} 分配到班级 {target_class_id} 成功")
        else:
            print(f"学生 {student} 分配到班级 {target_class_id} 失败")

    # classes = sorted(classes, key=lambda stu_list: stu_list.gender_percent, reverse=True)

    # classes =  dict(classes)

    sorted_dict_by_value = {k: v for k, v in sorted(classes.items(), key=lambda item: item[1].gender_percent, reverse=True)}
    new_dict = {i: sorted_dict_by_value[value] for i, value in enumerate(sorted_dict_by_value)}
    # print(sorted_dict_by_value)  # 输出: {'cherry': 1, 'banana': 3, 'apple': 4}
    classes= new_dict
    res=[]
    res_avg=[]
    res2=[]
    i=0
    ii = 0
    #  尝试匆最高和最低的 取  分数一直 性别相反的交换
    # classes,is_changed=exchange( len(classes)-1,0, classes)
    is_changed=False
    while not is_changed and ii< len(classes)-2 :
        classes,is_changed=exchange( len(classes)-1,ii , classes)
        ii+=1
        print(is_changed)
    # classes=exchange( len(classes)-2,1, classes)
    classes,is_changed=exchange( len(classes)-2,1 , classes)

    for cls, stu_list in classes.items():
        # print(stu_list,1111)

        res.append(stu_list.total_score)
        res_avg.append(stu_list.avg_score)
        res2.append(stu_list.gender_percent)
        if i==0 or i== len(classes)-1:
            # print( (stu_list.students))
            print(stu_list)
            pass
        i+=1
        # print(vars(stu_list))
        # print(stu_list.__str__())
    for cls, stu_list in classes.items():
        if cls<=1 or cls== len(classes):
            # print( (stu_list.students))
            # print(stu_list)
            pass

        delattr(stu_list, 'students')
        print(vars(stu_list),222)
    # 使用statistics模块计算方差
    variance = statistics.variance(res)
    variance_avg = statistics.variance(res_avg)
    variance2 = statistics.variance(res2)
    print(f"分数方差: {variance}")
    print(f"平君分方差: {variance_avg}")
    print(f"性别方差: {variance2}")

if __name__ == '__main__':
    main()
