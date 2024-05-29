class Student:
    def __init__(self, name, score, gender):
        self.name = name
        self.score = score
        self.gender = gender

def balance_classes(students, num_classes):
    # 将学生按分数从高到低排序
    sorted_students = sorted(students, key=lambda student: student.score, reverse=True)

    # 初始化班级列表
    classes = {f'班级{i+1}': {'male': [], 'female': []} for i in range(num_classes)}

    # 记录每个班级的男女学生数量
    class_counts = {'male': [0] * num_classes, 'female': [0] * num_classes}

    # 分配学生到班级
    for student in sorted_students:
        # 找到当前人数最少的班级
        # 寻找最小类别索引
        # 根据学生的性别和各个类别的计数，找出类别计数中最小的类别索引。
        # 这个表达式首先生成一个数字范围(0到num_classes-1)，然后使用lambda函数作为key参数，
        # 该函数根据学生的性别和类别的计数来计算每个范围内的索引对应的计数值。
        # 最后，返回计数值最小的类别索引。
        min_class_index = min(range(num_classes), key=lambda i: class_counts[student.gender][i])
        # 将学生添加到该班级
        classes[f'班级{min_class_index+1}'][student.gender].append(student)
        # 更新班级人数计数
        class_counts[student.gender][min_class_index] += 1

    # 返回班级列表
    return classes





# 创建学生列表
students = [
    Student("学生A", 90, 'male'), Student("学生B", 85, 'female'), Student("学生C", 70, 'male'),
    Student("学生D", 60, 'female'), Student("学生E", 50, 'male'), Student("学生F", 95, 'female')
]

# 调用函数进行分班
num_classes = 3
class_distribution = balance_classes(students, num_classes)

# 打印分班结果
for class_name, class_students in class_distribution.items():
    print(f"{class_name}:")
    print("男生:")
    for student in class_students['male']:
        print(student.name, student.score)
    print("女生:")
    for student in class_students['female']:
        print(student.name, student.score)
    print("------")
