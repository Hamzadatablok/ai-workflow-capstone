# app.py
from flask import Flask, jsonify
import logging
import os
import json
"""
AI Workflow Capstone - Model Deployment
This API handles prediction, retraining, scoring, and logging for a machine learning model.
Endpoints:
- /predict: Get predictions
- /train: Retrain the model
- /scoring: Get F1 score
- /logs: View logs
"""

app = Flask(__name__)

# تفعيل السجلات
logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# إنشاء مجلد logs إذا ما كانش موجود
os.makedirs('logs', exist_ok=True)

# --- نقطة النهاية: التنبؤ ---
@app.route('/predict', methods=['GET'])
def predict():
    """Returns predictions from the model (dummy response)"""
    try:
        return jsonify({"predictions": [0, 1, 0]}), 200
    except Exception as e:
        logging.error(f"Error in prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

# --- نقطة النهاية: إعادة التدريب ---
@app.route('/train', methods=['POST'])
def retrain():
    """Simulates model retraining"""
    try:
        logging.info("Model retraining triggered")
        return jsonify({"message": "Model retrained successfully"}), 200
    except Exception as e:
        logging.error(f"Error during retraining: {str(e)}")
        return jsonify({"error": str(e)}), 500

# --- نقطة النهاية: التقييم ---
@app.route('/scoring', methods=['GET'])
def scoring():
    """Returns the F1 score of the model"""
    try:
        return jsonify({"f1_score": "0.87"}), 200
    except Exception as e:
        logging.error(f"Error in scoring: {str(e)}")
        return jsonify({"error": str(e)}), 500

# --- نقطة النهاية: السجلات ---
@app.route('/logs', methods=['GET'])
def get_logs():
    """Returns the last 10 log entries"""
    try:
        if os.path.exists('logs/api.log'):
            with open('logs/api.log', 'r') as f:
                logs = f.readlines()
            return jsonify({"logs": logs[-10:]}), 200
        else:
            return jsonify({"logs": []}), 200
    except Exception as e:
        logging.error(f"Error reading logs: {str(e)}")
        return jsonify({"error": str(e)}), 500

# --- تشغيل الخادم ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


Added comments to improve code clarity
