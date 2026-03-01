from flask import Flask, request, jsonify, render_template
from model import ImageDescriptionGenerator
import os
from hashtags import process_sentence_and_get_hashtags
import base64
import requests

app = Flask(__name__)

# -----------------------------
# Download the model if not present
# -----------------------------
MODEL_URL = "https://huggingface.co/rukesh2507/twitter-caption-model/resolve/main/best_model.h5"
MODEL_PATH = "best_model.h5"
TOKENIZER_PATH = "tokenizer.pkl"

if not os.path.exists(MODEL_PATH):
    print("Downloading model from Hugging Face...")
    r = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(r.content)
    print("Model downloaded successfully.")

# Initialize the custom model
img_desc_gen = ImageDescriptionGenerator(MODEL_PATH, TOKENIZER_PATH)

# -----------------------------
# Flask Routes
# -----------------------------
@app.route('/')
def index():
    posts = [
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk',
            'handle': '@elonmusk',
            'description': 'Hey Hi!.',
            'image': 'https://www.andhrafriends.com/uploads/gallery/category_1/gallery_49204_1_313485.gif',
            'views': '3K',
            'likes': '2.9K',
            'reposts': '8.1K',
            'replies': '2.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk',
            'handle': '@elonmusk',
            'description': 'Time padithe pattindhi ley ra, success ayethe adhe happy.',
            'image': 'https://media.tenor.com/DuTGu5wclWgAAAAd/brahmi-adhurs.gif',
            'views': '25K',
            'likes': '2.4K',
            'reposts': '9.1K',
            'replies': '12.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk',
            'handle': '@elonmusk',
            'description': 'padhandi ra podham.',
            'image': 'https://media.tenor.com/_2K_8ys_VBgAAAAC/adhurs-brahmi.gif',
            'views': '21K',
            'likes': '4.2K',
            'reposts': '6.3K',
            'replies': '21.3K'
        },

        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk',
            'handle': '@elonmusk',
            'description': 'feeling great for SDSU championship #feelingemotional.',
            'image': 'https://media3.giphy.com/media/qiveSXvlFUXf2/giphy.gif?cid=ecf05e47o1vzyo7sb1cp3ji8sk0q10b1ueewr9h0ikdmxngq&ep=v1_gifs_related&rid=giphy.gif&ct=g',
            'views': '25K',
            'likes': '2.4K',
            'reposts': '9.1K',
            'replies': '12.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk',
            'handle': '@elonmusk',
            'description': 'tooo the moon.',
            'image': 'https://media1.giphy.com/media/oNFP9kltPi7fp8TUAV/giphy.gif?cid=ecf05e477urksexznyqvpp9ibiixbxr6rkm3je1yo7wrflau&ep=v1_gifs_search&rid=giphy.gif&ct=g',
            'views': '21K',
            'likes': '4.2K',
            'reposts': '6.3K',
            'replies': '21.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk',
            'handle': '@elonmusk',
            'description': 'Go Bitcoin Go!',
            'image': 'https://media2.giphy.com/media/0XJeBn8nx6HDwdWIDg/giphy.gif?cid=ecf05e474n9inkfvy7mwu4rdtvfxfgn9k72si3l7175tsqvj&ep=v1_gifs_search&rid=giphy.gif&ct=g',
            'views': '3K',
            'likes': '2.9K',
            'reposts': '8.1K',
            'replies': '2.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk',
            'handle': '@elonmusk',
            'description': 'Time padithe pattindhi ley ra, success ayethe adhe happy.',
            'image': 'https://media.tenor.com/DuTGu5wclWgAAAAd/brahmi-adhurs.gif',
            'views': '25K',
            'likes': '2.4K',
            'reposts': '9.1K',
            'replies': '12.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk',
            'handle': '@elonmusk',
            'description': 'padhandi ra podham.',
            'image': 'https://media.tenor.com/_2K_8ys_VBgAAAAC/adhurs-brahmi.gif',
            'views': '21K',
            'likes': '4.2K',
            'reposts': '6.3K',
            'replies': '21.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk',
            'handle': '@elonmusk',
            'description': 'Hey Hi!.',
            'image': 'https://www.andhrafriends.com/uploads/gallery/category_1/gallery_49204_1_313485.gif',
            'views': '3K',
            'likes': '2.9K',
            'reposts': '8.1K',
            'replies': '2.3K'
        },
    ]
    return render_template('upload.html', posts=posts)


@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['image']

        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': 'Invalid file type'})

        # Save the uploaded file temporarily
        filename = os.path.join('./', file.filename)
        file.save(filename)

        # Get the description of the image
        description = img_desc_gen.get_description(filename)
        try:
            os.remove(filename)
        except FileNotFoundError:
            print(f"File not found: {filename}")

        return jsonify({'description': description})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})


@app.route('/hashtags', methods=['POST'])
def hashtags():
    try:
        data = request.get_json()

        if 'hashtags' in data and isinstance(data['hashtags'], list) and len(data['hashtags']) > 0:
            new_hashtags = process_sentence_and_get_hashtags(data['hashtags'], data['description'])
            return jsonify({'hashtags': new_hashtags})
        else:
            return jsonify({'error': 'Hashtags has to be present in the body and should be a non-empty list.'})
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})


@app.route('/clarifai', methods=['POST'])
def clarifai_api():
    try:
        image_file = request.files['image']
        image_bytes = image_file.read()
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        url = 'https://api.clarifai.com/v2/models/general-image-recognition/versions/aa7f35c01e0642fda5cf400f543e7c40/outputs'
        headers = {
            'Authorization': ,  # Replace with your real key
            'Content-Type': 'application/json'
        }

        data = {
            "inputs": [
                {
                    "data": {
                        "image": {
                            "base64": base64_image
                        }
                    }
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        keywords = []
        if 'outputs' in response_data:
            concepts = response_data['outputs'][0]['data'].get('concepts', [])
            keywords = [f"{c['name'].replace(' ', '')}" for c in concepts[:10]]  # top 10
        print(keywords)
        return jsonify({'hashtags': keywords})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
