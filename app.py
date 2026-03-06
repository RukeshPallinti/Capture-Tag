from flask import Flask, request, jsonify, render_template
from model import ImageDescriptionGenerator
import os
from hashtags import process_sentence_and_get_hashtags
import requests
from PIL import Image
import io

app = Flask(__name__)

# Initialize the custom model
model_path = "best_model.h5"
tokenizer_path = "tokenizer.pkl"
img_desc_gen = ImageDescriptionGenerator(model_path, tokenizer_path)

@app.route('/')
def index():
    posts = [
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk',
            'handle': '@elonmusk',
            'description': 'Hey Hi!.',
            'image': 'https://www.andhrafriends.com/uploads/gallery/category_1/gallery_49204_1_313485.gif',
            'views': '3K', 'likes': '2.9K', 'reposts': '8.1K', 'replies': '2.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk', 'handle': '@elonmusk',
            'description': 'Time padithe pattindhi ley ra, success ayethe adhe happy.',
            'image': 'https://media.tenor.com/DuTGu5wclWgAAAAd/brahmi-adhurs.gif',
            'views': '25K', 'likes': '2.4K', 'reposts': '9.1K', 'replies': '12.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk', 'handle': '@elonmusk',
            'description': 'padhandi ra podham.',
            'image': 'https://media.tenor.com/_2K_8ys_VBgAAAAC/adhurs-brahmi.gif',
            'views': '21K', 'likes': '4.2K', 'reposts': '6.3K', 'replies': '21.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk', 'handle': '@elonmusk',
            'description': 'feeling great for SDSU championship #feelingemotional.',
            'image': 'https://media3.giphy.com/media/qiveSXvlFUXf2/giphy.gif?cid=ecf05e47o1vzyo7sb1cp3ji8sk0q10b1ueewr9h0ikdmxngq&ep=v1_gifs_related&rid=giphy.gif&ct=g',
            'views': '25K', 'likes': '2.4K', 'reposts': '9.1K', 'replies': '12.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk', 'handle': '@elonmusk',
            'description': 'tooo the moon.',
            'image': 'https://media1.giphy.com/media/oNFP9kltPi7fp8TUAV/giphy.gif?cid=ecf05e477urksexznyqvpp9ibiixbxr6rkm3je1yo7wrflau&ep=v1_gifs_search&rid=giphy.gif&ct=g',
            'views': '21K', 'likes': '4.2K', 'reposts': '6.3K', 'replies': '21.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk', 'handle': '@elonmusk',
            'description': 'Go Bitcoin Go!',
            'image': 'https://media2.giphy.com/media/0XJeBn8nx6HDwdWIDg/giphy.gif?cid=ecf05e474n9inkfvy7mwu4rdtvfxfgn9k72si3l7175tsqvj&ep=v1_gifs_search&rid=giphy.gif&ct=g',
            'views': '3K', 'likes': '2.9K', 'reposts': '8.1K', 'replies': '2.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk', 'handle': '@elonmusk',
            'description': 'Time padithe pattindhi ley ra, success ayethe adhe happy.',
            'image': 'https://media.tenor.com/DuTGu5wclWgAAAAd/brahmi-adhurs.gif',
            'views': '25K', 'likes': '2.4K', 'reposts': '9.1K', 'replies': '12.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk', 'handle': '@elonmusk',
            'description': 'padhandi ra podham.',
            'image': 'https://media.tenor.com/_2K_8ys_VBgAAAAC/adhurs-brahmi.gif',
            'views': '21K', 'likes': '4.2K', 'reposts': '6.3K', 'replies': '21.3K'
        },
        {
            'avatar': 'https://pbs.twimg.com/profile_images/1683325380441128960/yRsRRjGO_400x400.jpg',
            'username': 'Elon Musk', 'handle': '@elonmusk',
            'description': 'Hey Hi!.',
            'image': 'https://www.andhrafriends.com/uploads/gallery/category_1/gallery_49204_1_313485.gif',
            'views': '3K', 'likes': '2.9K', 'reposts': '8.1K', 'replies': '2.3K'
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

        filename = os.path.join('./', file.filename)
        file.save(filename)

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
def apiverve_api():
    import traceback
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file received"}), 400

        image_file = request.files['image']

        # Read all bytes first to avoid stream issues
        image_bytes = image_file.read()
        print(f"Received image bytes: {len(image_bytes)}")

        # Open image from bytes
        img = Image.open(io.BytesIO(image_bytes))

        # Convert to RGB if needed (e.g. PNG with alpha channel)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Compress image to under 400KB
        img_io = io.BytesIO()
        quality = 85
        img.save(img_io, format='JPEG', quality=quality)
        while img_io.tell() > 400 * 1024 and quality > 10:
            img_io = io.BytesIO()
            quality -= 10
            img.save(img_io, format='JPEG', quality=quality)
        img_io.seek(0)
        print(f"Compressed image size: {img_io.getbuffer().nbytes} bytes at quality {quality}")

        url = "https://api.apiverve.com/v1/imagecaption"
        headers = {
            "X-API-Key": "apv_29e18e3e-44aa-4248-bc41-e03fe3d7dee2"
        }
        response = requests.post(url, headers=headers, files={"image": ("image.jpg", img_io, "image/jpeg")})
        print(f"API status: {response.status_code}")
        print(f"API response: {response.text}")

        response_data = response.json()
        keywords = []
        if response_data.get("status") == "ok":
            caption = response_data["data"].get("caption", "")
            print(f"Caption: {caption}")
            stopwords = {"a", "an", "the", "on", "in", "at", "through", "with", "and", "of", "to", "for", "is"}
            words = caption.lower().split()
            keywords = [f"#{word.strip('.,')}" for word in words if word not in stopwords and len(word) > 2]
        keywords = list(dict.fromkeys(keywords))[:10]
        print(f"Keywords: {keywords}")
        return jsonify({"hashtags": keywords})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
