from aip import AipOcr

# 定义常量
APP_ID = '9902583'
API_KEY = 'R7h09AYY3dNMQdIdz1zaWiWo'
SECRET_KEY = '3245afb910ba976d21bbaad591803899'

# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 初始化ApiOcr对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 定义参数变量
options = {
  'detect_direction': 'true',
  'language_type': 'CHN_ENG',
}

# 网络图片文字识别接口
result = aipOcr.webImage(get_file_content('125090772.png'), options)
print(result)