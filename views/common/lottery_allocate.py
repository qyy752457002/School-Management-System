import random


def main():

    # todo 打乱顺序   性别均衡  成绩均衡
    # 假设我们有一个学生列表，每个学生有一个唯一的ID
    students = list(range(1, 101))  # 假设有100个学生
    # studic = dict(
    studic=[]
    for i in students:
        tt = random.randint(0, 1)
        score = random.randint(1, 100)
        stu={"stu_id":i ,"gender":tt ,"score":score
        }
        studic.append(stu)




    print(studic)

    random.shuffle(students)
    print(students)

    # 班级数量
    num_classes = 10

    # 初始化班级字典
    classes = {i: [] for i in range(1, num_classes + 1)}

    # 公平拉票过程
    while students:
        # 随机选择一个学生
        student = random.choice(students)
        print(f"Selected student {student}")

        # 随机选择一个班级
        chosen_class = random.randint(1, num_classes)
        print(f"Chosen class {chosen_class}")

        # 如果该班级还没有满员，将学生分配到该班级
        if len(classes[chosen_class]) < 10:  # 假设每个班级最多10人
            classes[chosen_class].append(student)
            students.remove(student)  # 从待分配学生列表中移除
        else:
            print(f"Class {chosen_class} is full, skipping student {student}")

    # 打印最终的班级分配结果
    for cls, stu_list in classes.items():
        print(f"Class {cls}: {stu_list}")


if __name__ == '__main__':
    main()