from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# 数据库初始化
def init_db():
    conn = sqlite3.connect('carpool.db')
    cursor = conn.cursor()
    
    # 创建表（如果不存在）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carpool_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departure TEXT NOT NULL,
            destination TEXT NOT NULL,
            travel_date TEXT NOT NULL,
            travel_time TEXT NOT NULL,
            details TEXT,
            contact_type TEXT,
            contact_info TEXT,
            nickname TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 检查user_id列是否存在，如果不存在则添加
    cursor.execute("PRAGMA table_info(carpool_requests)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'user_id' not in columns:
        cursor.execute('ALTER TABLE carpool_requests ADD COLUMN user_id TEXT')
        # 为现有数据设置默认user_id
        cursor.execute('UPDATE carpool_requests SET user_id = "default_user" WHERE user_id IS NULL')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    departure = data.get('departure')
    destination = data.get('destination')
    travel_date = data.get('travel_date')
    travel_time = data.get('travel_time')
    
    conn = sqlite3.connect('carpool.db')
    cursor = conn.cursor()
    
    # 查询逻辑：目的地必须相同，日期必须相同，按时间最近+出发地是否一致排序
    cursor.execute('''
        SELECT id, departure, destination, travel_date, travel_time, details,
               contact_type, contact_info, nickname, created_at
        FROM carpool_requests
        WHERE destination = ? AND travel_date = ?
        ORDER BY
            CASE WHEN departure = ? THEN 0 ELSE 1 END,
            ABS(strftime('%s', travel_time) - strftime('%s', ?))
    ''', (destination, travel_date, departure, travel_time))
    
    results = cursor.fetchall()
    conn.close()
    
    # 转换结果为字典格式
    requests = []
    for row in results:
        requests.append({
            'id': row[0],
            'departure': row[1],
            'destination': row[2],
            'travel_date': row[3],
            'travel_time': row[4],
            'details': row[5],
            'contact_type': row[6],
            'contact_info': row[7],
            'nickname': row[8],
            'created_at': row[9]
        })
    
    return jsonify({'requests': requests})

@app.route('/publish')
def publish():
    # 获取查询参数用于自动填充
    departure = request.args.get('departure', '')
    destination = request.args.get('destination', '')
    travel_date = request.args.get('travel_date', '')
    travel_time = request.args.get('travel_time', '')
    
    return render_template('publish.html', 
                         departure=departure, 
                         destination=destination,
                         travel_date=travel_date,
                         travel_time=travel_time)

@app.route('/submit_request', methods=['POST'])
def submit_request():
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'error': '用户ID不能为空'})
    
    conn = sqlite3.connect('carpool.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO carpool_requests
        (user_id, departure, destination, travel_date, travel_time, details, contact_type, contact_info, nickname)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        data['departure'],
        data['destination'],
        data['travel_date'],
        data['travel_time'],
        data['details'],
        data['contact_type'],
        data['contact_info'],
        data['nickname']
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/my_requests')
def my_requests():
    return render_template('my_requests.html')

@app.route('/get_my_requests', methods=['POST'])
def get_my_requests():
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'success': False, 'error': '用户ID不能为空'})
    
    conn = sqlite3.connect('carpool.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, departure, destination, travel_date, travel_time, details,
               contact_type, contact_info, nickname, created_at
        FROM carpool_requests
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', (user_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    requests = []
    for row in results:
        requests.append({
            'id': row[0],
            'departure': row[1],
            'destination': row[2],
            'travel_date': row[3],
            'travel_time': row[4],
            'details': row[5],
            'contact_type': row[6],
            'contact_info': row[7],
            'nickname': row[8],
            'created_at': row[9]
        })
    
    return jsonify({'success': True, 'requests': requests})

@app.route('/delete_request', methods=['POST'])
def delete_request():
    data = request.get_json()
    request_id = data.get('request_id')
    user_id = data.get('user_id')
    
    if not request_id or not user_id:
        return jsonify({'success': False, 'error': '请求ID和用户ID不能为空'})
    
    conn = sqlite3.connect('carpool.db')
    cursor = conn.cursor()
    
    # 验证用户是否有权限删除此请求
    cursor.execute('SELECT user_id FROM carpool_requests WHERE id = ?', (request_id,))
    result = cursor.fetchone()
    
    if not result or result[0] != user_id:
        conn.close()
        return jsonify({'success': False, 'error': '无权删除此请求'})
    
    cursor.execute('DELETE FROM carpool_requests WHERE id = ?', (request_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/update_request', methods=['POST'])
def update_request():
    data = request.get_json()
    request_id = data.get('request_id')
    user_id = data.get('user_id')
    
    if not request_id or not user_id:
        return jsonify({'success': False, 'error': '请求ID和用户ID不能为空'})
    
    conn = sqlite3.connect('carpool.db')
    cursor = conn.cursor()
    
    # 验证用户是否有权限更新此请求
    cursor.execute('SELECT user_id FROM carpool_requests WHERE id = ?', (request_id,))
    result = cursor.fetchone()
    
    if not result or result[0] != user_id:
        conn.close()
        return jsonify({'success': False, 'error': '无权更新此请求'})
    
    cursor.execute('''
        UPDATE carpool_requests
        SET departure = ?, destination = ?, travel_date = ?, travel_time = ?,
            details = ?, contact_type = ?, contact_info = ?, nickname = ?
        WHERE id = ?
    ''', (
        data['departure'],
        data['destination'],
        data['travel_date'],
        data['travel_time'],
        data['details'],
        data['contact_type'],
        data['contact_info'],
        data['nickname'],
        request_id
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)