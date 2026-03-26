import re, csv

def mask_value(value, sens_type):
    """
    对敏感值进行脱敏
    sens_type: '身份证' 或 '手机号'
    """
    if sens_type == '身份证' and len(value) == 18:
        # 保留前4位和后4位，中间用8个*代替
        return value[:4] + '********' + value[-4:]
    elif sens_type == '手机号' and len(value) == 11:
        # 保留前3位和后4位，中间用4个*代替
        return value[:3] + '****' + value[-4:]
    return value  



def scan_csv(file_path):
    info_list = []

    with open(file_path, 'r', encoding='utf-8') as file:
        readers = csv.reader(file)
        headers = next(readers)

        for row_num, row in enumerate(readers, start=2):
            for col_idx, cell in enumerate(row):
                if re.search( r'\d{17}[\dXx]',cell):
                    info_list.append({
                        '行号': row_num,
                        '列名': headers[col_idx],
                        '类型': "身份证",
                        '原始值': cell,
                        '脱敏值': mask_value(cell, '身份证')
                    })
                elif re.search(r'1[3-9]\d{9}', cell):
                    info_list.append({
                        '行号': row_num,
                        '列名': headers[col_idx],
                        '类型': "手机号",
                        '原始值': cell,
                        '脱敏值': mask_value(cell, '手机号')
                    })
    return info_list

def generate_html_report(results, output_file='report.html'):
    """
    生成HTML格式的扫描报告
    """
    # 统计各类敏感数据的数量
    type_count = {}
    for r in results:
        t = r['类型']
        type_count[t] = type_count.get(t, 0) + 1

    # 开始构建HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>敏感信息扫描报告</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .summary {{
            background-color: #e8f5e9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .footer {{
            margin-top: 20px;
            font-size: 12px;
            color: #777;
            text-align: center;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1>敏感信息扫描报告</h1>

    <div class="summary">
        <h3>扫描统计</h3>
        <ul>
    """

    for t, c in type_count.items():
        html += f"<li>{t}: {c} 条</li>\n"

    html += f"""
        </ul>
        <p><strong>总计:</strong> {len(results)} 条敏感数据</p>
        <p><strong>生成时间:</strong> {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <h3>详细结果</h3>
    <table>
        <tr>
            <th>行号</th>
            <th>列名</th>
            <th>类型</th>
            <th>原始值</th>
            <th>脱敏值</th>
        </tr>
    """

    # 添加表格内容
    for r in results:
        html += f"""
        <tr>
            <td>{r['行号']}</td>
            <td>{r['列名']}</td>
            <td>{r['类型']}</td>
            <td>{r['原始值']}</td>
            <td>{r['脱敏值']}</td>
        </tr>
        """

    html += """
    </table>
    <div class="footer">
        <p>扫描工具 v1.0 | 数据安全报告</p>
    </div>
</div>
</body>
</html>
    """

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML报告已生成: {output_file}")


if __name__ == '__main__':
    # 创建测试数据
    with open('test3.csv', 'w', encoding='utf-8') as f:
        f.write("姓名,身份证号,手机号\n")
        f.write("张三,11010119900307663X,13812345678\n")
        f.write("李四,440301199105124567,13987654321\n")

    # 扫描
    results = scan_csv('test3.csv')

    # 打印控制台结果
    for r in results:
        print(f"第{r['行号']}行 {r['列名']} 发现{r['类型']}: {r['原始值']} -> 脱敏后: {r['脱敏值']}")

    # 生成HTML报告
    generate_html_report(results, '敏感信息报告.html')

    print("\n完成！用浏览器打开 '敏感信息报告.html' 查看报告")


