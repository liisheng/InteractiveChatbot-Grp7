from flask import Flask, request, jsonify
import requests #pip install Flask requests/ #pip install requests/ 

app = Flask(__name__)

API_KEY = '4b7013ee7a874d41a19510f4fab17afb'  # Replace with your actual News API key

def fetch_news(query, page_size=5):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'pageSize': page_size,
        'apiKey': API_KEY,
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()['articles']
    else:
        print(f"Error: {response.status_code}")
        return []

@app.route('/get_news', methods=['POST'])
def get_news():
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    articles = fetch_news(query)
    
    if articles:
        response = [{'title': article['title'], 'source': article['source']['name'], 'url': article['url']} for article in articles]
        return jsonify(response)
    else:
        return jsonify({'message': 'No articles found'}), 404

@app.route('/')
def home():
    return app.send_static_file('news.html')



if __name__ == '__main__':
    app.run(debug=True)
