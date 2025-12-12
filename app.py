from flask import Flask, request, jsonify
from deepface import DeepFace
import os

app = Flask(__name__)

# Create a temporary folder for uploads
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/', methods=['GET'])
def health_check():
    return "AI Server is Running!"

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    try:
        print("--- Receiving Image ---")
        
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
            
        file = request.files['image']
        
        # Save locally so DeepFace can read it
        temp_path = os.path.join('uploads', "temp_scan.jpg")
        file.save(temp_path)
        
        print("--- Analyzing with DeepFace ---")
        
        # Analyze using the default VGG-Face model (very stable)
        # enforce_detection=False prevents crash if it can't find a face
        objs = DeepFace.analyze(img_path=temp_path, actions=['emotion'], enforce_detection=False)
        
        # Get the first face found
        result = objs[0]
        dominant_emotion = result['dominant_emotion']
        
        print(f"--- Result: {dominant_emotion} ---")
        
        return jsonify({
            "label": dominant_emotion,
            "score": result['emotion'][dominant_emotion]
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render assigns a random port, so we must read it from env
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
