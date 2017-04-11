# A chart by Python
### 使用场景
工作中常常需要通过分析日志，生成图表，直观的应一个系统或应用的状态。Python 处理日志非常方便快捷

## 工具
Python、MySQL、日志文件、hightcharts

# 处理流程

### 分析日志
Python分析日志文件,日志可以是apache、nginx的访问日志，也可以是自定义生成的日志

### 统计数据入库
将Python分析日志得到的统计数据放到MySQL库中

### 利用Flask渲染页面
利用Flask框架，生成路由和渲染图表页面

### 连接MySQL读取数据
图表数据从MySQL库中读取,返回JSON对象，5分钟一条记录

### highcharts
利用highcharts生成实时监控数据图表

# 界面预览

1） 欢迎页

![](doc/wel.png?raw=true)

2） 监控页

![](doc/charts.png?raw=true)

3）监控页2
![](doc/node_pic.png?raw=true)

