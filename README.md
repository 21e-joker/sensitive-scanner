# 敏感信息扫描器
一个轻量级的基于python的敏感信息扫描器。
## 功能
-自动识别csv中的身份证号和手机号
-对身份证号和手机号脱敏（身份证：1101********663X，手机号：138****5678）
-输出结构化报告（HTML)

##快速开始
```bash
# 1. 克隆项目
git clone https://github.com/你的用户名/sensitive-data-scanner.git

# 2. 进入目录
cd sensitive-data-scanner

# 3. 准备测试数据（或使用自己的CSV文件）
echo "姓名,身份证号,手机号" > test.csv
echo "张三,11010119900307663X,13812345678" >> test.csv

# 4. 运行扫描
python sensitive_scanner.py test.csv
