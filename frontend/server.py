from flask import Flask, render_template, request, jsonify
import os

from handlers import vector_search, update_tags

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    """Отображение главной страницы приложения"""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """API-эндпоинт для поиска"""
    data = request.get_json()

    if not data or 'query' not in data:
        return jsonify({'error': 'Missing search query'}), 400

    query = data.get('query', '')
    max_results = data.get('max_results', 10)

    try:
        results = vector_search(query, max_results)
        if results is None:
            raise ValueError
        return jsonify(results)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_tags', methods=['POST'])
def update():
    """API-эндпоинт для обновления тегов"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        for item in data:
            if 'path' not in item or 'tags' not in item:
                continue

            path = item['path']
            tags = item['tags']
            print("path", path, tags)
            update_tags(path, tags)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def launch_frontend():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

