import json
import os


def genarate_image_jsons(mygoddata_path, images_path, images_version):
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    image_dirs = os.listdir(images_path)
    if len(image_dirs) <= 0:
        print("images child count = 0!")
        return
    images_list = []
    for image in image_dirs:
        if image.endswith(".jpg"):
            images_list.append(image.split('.')[0])
    image_dic = {'images': images_list, "imagesVersion": images_version}
    json_str = json.dumps(image_dic)
    json_path = mygoddata_path + "/images.json"
    with open(json_path, 'w') as f:
        f.write(json_str)


def update_images_json_version(json_path):
    with open(json_path, "r") as json_file:
        json_str = json_file.read()
    json_dic = json.loads(json_str)
    json_dic['imagesVersion'] += 1
    print(type(json_dic))
    print(json.dumps(json_dic))
    with open(json_path, "w") as json_file:
        json_file.write(json.dumps(json_dic))
    return json_dic['imagesVersion']


if __name__ == '__main__':
    myGodDataPath = os.path.abspath(os.path.join(os.getcwd(), "../../../MyGodData"))
    mygoddata_images_path = myGodDataPath + "/images"
    images_version = update_images_json_version(myGodDataPath + "/version.json")
    genarate_image_jsons(myGodDataPath, mygoddata_images_path, images_version)
