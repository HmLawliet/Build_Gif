import imageio
import os 
from PIL import Image


def save_gif(image_list, gif_name, duration):
    '''
    save_gif 保存动图
    :param image_list  图片路径列表
    :param gif_name     生成gif的图片名称
    :param duration   动图的频率
    '''
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    print('生成完毕')



def adjust_image(image_list,path_split,x_s):
    '''
    adjust_image 调整图片的大小
    :param image_list  图片所在路径
    :param path_split  路径分隔符
    :param x_s      调整的像素大小参数
    '''
    adjust_image_list = []
    for image in image_list:
        im = Image.open(image)
        x,y = im.size #read image size
        y_s =int(y * x_s / x)  #calc height based on standard width
        out = im.resize((x_s,y_s),Image.ANTIALIAS) # resize image with high-quality
        *root,file_name = image.strip().split(path_split)
        root = f'{path_split}'.join(root)
        adjust_image_name = f'{root}{path_split}adjust_{file_name}'
        out.save(adjust_image_name)
        adjust_image_list.append(adjust_image_name)
    return adjust_image_list
    
    


def gif(path,gif_name='one.gif',path_split = '/',duration=0.35,x_s=300):
    '''
    gif 多张图生成动图
    :param path  图片所在目录路径 
    :param gif_name  动图的名称
    :param path_split  路径分割符   windows \\  linux /
    :param duration  动图的变换频率
    :param x_s   归一化图片的像素大小
    '''
    if not os.path.isdir(path):
        return 

    image_list = []
    for root,_,files in os.walk(path):
        image_list = [f'{root}{path_split}{item}'.strip() for item in files]

    adjust_image_list = adjust_image(image_list,path_split,x_s)
    if not adjust_image_list:
        return 
    save_gif(adjust_image_list, gif_name, duration)


if __name__ == '__main__':

    root_dir =  os.path.dirname(os.path.abspath(__file__))
    path_split =  '/'
    if os.name == 'nt':
        path_split = '''\\'''
    else:
        path_split = '/'
    
    image_dir = f'{root_dir}{path_split}static'
    gif(image_dir,path_split=path_split)

    # print(os.name)