# elastic  

用于下载或同步elasticsearch数据库  

使用方法:
elastic/spider/search.py中填写es服务的ip和要下载的index,   
也可根据单条数据的大小选择合适的返回结果的数量修改size参数  

项目采用的是下载到redis, 可根据需要开发pipeline

