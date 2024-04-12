import base64
import json
import os
from flask import Flask, request, jsonify, render_template
import logging
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/getSSPDataInfo', methods=['POST', 'GET'])
def getSSPDataInfo():
    # 从 URL 参数中获取参数
    type = request.args.get('type')
    time = request.args.get('time')
    year = request.args.get('year')

    if year is None:
        return jsonify({'error': 'Missing required parameter: year'}), 400

    filename = f"data/getSSPDataInfo-{type}-{time}.json"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 根据年份获取所有省份对应的数据
            year_data = {}
            for province_data in data:
                if year in province_data:
                    province_name = province_data['province']
                    province_name = complete_province_name(province_name)  # 调用补全省份名字的函数
                    year_data[province_name] = province_data[year]
            return jsonify(year_data)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def complete_province_name(name):
    # 按照提供的省份名称列表补全省份名字
    province_names = {
        "河南": "河南省",
        "广东": "广东省",
        "内蒙古": "内蒙古自治区",
        "黑龙江": "黑龙江省",
        "新疆": "新疆维吾尔自治区",
        "湖北": "湖北省",
        "辽宁": "辽宁省",
        "山东": "山东省",
        "陕西": "陕西省",
        "上海": "上海市",
        "贵州": "贵州省",
        "重庆": "重庆市",
        "安徽": "安徽省",
        "福建": "福建省",
        "湖南": "湖南省",
        "海南": "海南省",
        "江苏": "江苏省",
        "青海": "青海省",
        "广西": "广西壮族自治区",
        "宁夏": "宁夏回族自治区",
        "浙江": "浙江省",
        "河北": "河北省",
        "香港特别行政": "香港特别行政区",
        "台湾": "台湾省",
        "澳门特别行政": "澳门特别行政区",
        "甘肃": "甘肃省",
        "四川": "四川省",
        "天津": "天津市",
        "山西": "山西省",
        "西藏": "西藏自治区",
        "吉林": "吉林省",
        "江西": "江西省",
        "北京": "北京市",
        "云南": "云南省"
    }
    return province_names.get(name, name)  # 如果在列表中找到则返回对应的省份名字，否则原样返回

@app.route('/getDataPhoto', methods=['GET','POST'])
def getDataPhoto():
    sel_project_type = ['hot', 'ganhan']
    sel_ageing = ['guance', 'his', '126', '245', '370', '585']
    sel_causing_factor = ['jiduanganhanrishu','leijiganhanliang','CDD','CWD',\
                        'jiduangaowenliang','jiduangaowenrishu','nuanye(TN90P)','nuanzhou(TX90P)',\
                        'xiaririshu(SU)','reyerishu(TR)','nianzuidazuigaowendu(TXx)','nianzuixiaozuigaowendu(TXn)']
    sel_weather_mod = ['ACCESS-CM2','bcc_cma','CN05.11','cnrm6','HadGEM-GC31-LL','INM-CM5-0','IPSL-CM6A-LR','MRI-ESM2-0']
    
    if request.method == 'GET':
        project_type = request.args.get('type')
        ageing = request.args.get('ageing')
        causing_factor = request.args.get('causing_factor')
        weather_mod = request.args.get('weather_mod')
        data_year = request.args.get('data_year')
    else:
        js_data = request.get_json()
        project_type = js_data.get('type')
        ageing = js_data.get('ageing')
        causing_factor = js_data.get('causing_factor')
        weather_mod = js_data.get('weather_mod')
        data_year = js_data.get('data_year')
        
    if project_type == 'hot':
        dir_path = 'img/hot-img/'
    else:
        dir_path = 'img/dry-img/'

    # 创建一个空数组以存储文件名
    file_names = []

    # 遍历目录并将符合筛选条件的文件名追加到数组中
    for file_name in os.listdir(dir_path):
        # 检查文件名是否符合筛选条件
        if (project_type in file_name) and (ageing in file_name) and (causing_factor in file_name) and (weather_mod in file_name) and (data_year in file_name):
            file_names.append(file_name)
        
    # 检查数组是否为空
    if not file_names:
        # 如果数组为空，则返回错误信息
        return jsonify({
            'code': 404,
            'error': 'Data not found'
        })

    file_name = dir_path + file_names[0]
    
    # 读取文件内容并将其编码为base64
    with open(file_name, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # 添加base64编码的图像数据前缀
    base64_image = "data:image/jpeg;base64," + encoded_string

    # 返回带有前缀的base64编码的图像数据
    return jsonify({
        'base64_image': base64_image
    })


if __name__ == '__main__':
    app.run(debug=True, port=6698)