from flask import Flask, request, jsonify
import redis
import requests

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Translation API (Google Translate or LibreTranslate)
TRANSLATE_API_URL = "https://api.mymemory.translated.net/get"

@app.route('/translate', methods=['GET'])
def translate():
    word = request.args.get('word')
    lang = request.args.get('lang')

    if not word or not lang:
        return jsonify({"error": "Missing word or language"}), 400

    # Check Redis Cache
    cache_key = f"{word}:{lang}"
    cached_translation = r.get(cache_key)

    if cached_translation:
        return jsonify({"word": word, "translation": cached_translation, "source": "cache"})

    # Fetch from Translation API
    params = {"q": word, "langpair": f"en|{lang}"}
    response = requests.get(TRANSLATE_API_URL, params=params)
    data = response.json()
    
    if "responseData" in data:
        translation = data["responseData"]["translatedText"]

        # Store in Redis (cache for 1 hour)
        r.setex(cache_key, 3600, translation)

        return jsonify({"word": word, "translation": translation, "source": "API"})

    return jsonify({"error": "Translation failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)
