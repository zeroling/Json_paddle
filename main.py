import os
import json


def get_parent_directory(file_path):
    # 获取文件所在目录
    directory = os.path.dirname(file_path)
    filename = os.path.basename(directory)
    # 获取文件所在目录的上一级目录
    parent_directory = os.path.dirname(directory)
    # 返回上一级目录的名称
    return str(os.path.basename(parent_directory)+filename)


def extract_text_coordinates_from_images(image_folder, json_subfolder):
    # 获取图片文件夹中所有图片文件的路径
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    # 打开文件，设置为追加模式
    with open(image_folder+'\\'+'Label.txt', 'a', encoding='utf-8') as output_file:
        for image_file in image_files:
            print(image_file)
            # 获取文件名前缀
            base_name = os.path.splitext(image_file)[0]
            # 构造匹配的 .json 文件名
            json_file = base_name + '.json'
            json_path = os.path.join(image_folder, json_subfolder, json_file)
            # 检查 .json 文件是否存在
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                # 提取坐标和文本
                result = []
                for item in data['text_block']:
                    coordinates = item["coordinate"]
                    texts = item["texts"]

                    # 遍历每个坐标和对应的文本
                    for coord, text in zip(coordinates, texts):
                        upper_left = coord["upper_left"]
                        lower_right = coord["lower_right"]
                        points = [
                            upper_left,
                            [lower_right[0], upper_left[1]],
                            lower_right,
                            [upper_left[0], lower_right[1]]
                        ]
                        result.append({
                            "transcription": text,
                            "points": points,
                            "difficult": "false"
                        })
                        # 将单个结果转换为字符串，并写入文件
                output_file.write("DangT/"+str(image_file)+"\t"+str(result).replace("'", '"').replace("False", "false") + '\n')
                # 这行不需要,因为用pplabel检查时依然会报为保存提醒,直接检查顺带修正一下吧,如果你不用pplabel检查,直接划分数据集可以加上这行
                # with open('fileState.txt', 'a', encoding='utf-8') as output_file2:
                #     output_file2.write(image_folder+"\\"+str(image_file) + "\t" + "1" + '\n')
            else:
                print(f"没有找到匹配的 .json 文件: {json_path}")



if __name__ == '__main__':
    # 待转换图片文件夹
    image_folder = r"C:\Users\16406\Desktop\DangT"
    # json放在image_folder+tmp下
    json_subfolder = 'tmp'
    extract_text_coordinates_from_images(image_folder, json_subfolder)

