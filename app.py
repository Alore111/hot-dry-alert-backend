import json
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




if __name__ == '__main__':
    app.run(debug=True, port=6698)