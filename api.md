- # hot-dry api
- 接口地址（GET，POST）
	- `https://hotdryalert.2ndtool.top/getDataPhoto`
- 示例请求json
	- 
	  ```json
	    {
            "type": "ganhan",
            "ageing": "370",
            "causing_factor": "jiduanganhanrishu",
            "weather_mod": "bcc_cma",
            "data_year": "2023"
	    }
	  ```
- 示例响应json
    - 
	- 数据存在
	  ```json
	    {
	        "base64_image": "data:image/jpeg;base64,    iVBORw0KGgoAAAANSUhEUgAAChIAAAYKCAYAAAA4NGMfAAAAAXNSR0IArs4c6QAAIABJREFUeF7..."
	    }
	  ```
    
    - 数据不存在
	  ```json
	    {
            "code": 404,
            "error": "Data not found"
        }
	  ```
        

- ## 参数说明

| 接口参数       | 解释              | 可选值                                                                                                                                                                                                                    |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| type           | 项目类型          | ['hot', 'ganhan']                                                                                                                                                                                                         |
| ageing         | 时效              | ['guance', 'his', '126', '245', '370', '585']                                                                                                                                                                             |
| causing_factor | 致灾因子          | ['jiduanganhanrishu','leijiganhanliang','CDD','CWD','jiduangaowenliang','jiduangaowenrishu','nuanye(TN90P)','nuanzhou(TX90P)','xiaririshu(SU)','reyerishu(TR)','nianzuidazuigaowendu(TXx)','nianzuixiaozuigaowendu(TXn)'] |
| weather_mod    | 气候模式/数据类型 | ['ACCESS-CM2','bcc_cma','CN05.11','cnrm6','HadGEM-GC31-LL','INM-CM5-0','IPSL-CM6A-LR','MRI-ESM2-0']                                                                                                                       |
| data_year      | 数据年份          |                                                                                                                                                                                                                           |

- 返回值
	- 返回一个包含base64编码的图像数据的JSON对象。
- 注
  - 其中某些值之间存在相互限制的关系（如his不能做出预测），如果后端没有相应数据，则返回404错误。
  - 为了方便开发，在执行时也可直接使用URL参数请求