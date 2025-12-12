from flask import Flask, request, jsonify
from deepface import DeepFace
import os

app = Flask(__name__)

# Create upload folder
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/', methods=['GET'])
def health_check():
    return "AI Server is Running!"

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image part"}), 400
            
        file = request.files['image']
        temp_path = os.path.join('uploads', "temp.jpg")
        file.save(temp_path)
        
        # Analyze
        # enforce_detection=False prevents crash if face isn't clear
        objs = DeepFace.analyze(img_path=temp_path, actions=['emotion'], enforce_detection=False)
        
        result = objs[0]
        dominant_emotion = result['dominant_emotion']
        
        # --- THE FIX IS HERE ---
        # Convert numpy.float32 to standard python float
        raw_score = result['emotion'][dominant_emotion]
        score = float(raw_score) 
        
        return jsonify({
            "label": dominant_emotion,
            "score": score
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
