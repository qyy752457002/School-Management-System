import os


def rename_files(folder_path):
    # 获取文件夹中的所有文件名
    file_list = os.listdir(folder_path)

    for filename in file_list:
        # 检查是否为文件
        if os.path.isfile(os.path.join(folder_path, filename)):
            # 分割文件名，添加下划线并将大写字母改为小写
            new_filename = ''.join(
                ['_' + c.lower() if c.isupper() and idx > 0 else c.lower() for idx, c in enumerate(filename)])

            # 重命名文件
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))


# 指定当前文件夹路径
folder_path = '.'

# 调用函数进行重命名操作
rename_files(folder_path)

