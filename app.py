# app.py
from flask import Flask, jsonify
import logging
import os
import json

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
    try:
        # نُرجع تنبؤاً وهمياً
        return jsonify({"predictions": [0, 1, 0, 1]}), 200
    except Exception as e:
        logging.error(f"خطأ في التنبؤ: {str(e)}")
        return jsonify({"error": str(e)}), 500

# --- نقطة النهاية: إعادة التدريب ---
@app.route('/train', methods=['POST'])
def retrain():
    try:
        logging.info("Model retraining triggered")
        return jsonify({"message": "Model retrained successfully"}), 200
    except Exception as e:
        logging.error(f"Error during retraining: {str(e)}")
        return jsonify({"error": str(e)}), 500

# --- نقطة النهاية: التقييم ---
@app.route('/scoring', methods=['GET'])
def scoring():
    try:
        # نُرجع نتيجة F1 وهمية
        return jsonify({"f1_score": "0.87"}), 200
    except Exception as e:
        logging.error(f"خطأ في التقييم: {str(e)}")
        return jsonify({"error": str(e)}), 500

# --- نقطة النهاية: السجلات ---
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        if os.path.exists('logs/api.log'):
            with open('logs/api.log', 'r', encoding='utf-8') as f:
                logs = f.readlines()
            return jsonify({"logs": logs[-10:]}), 200
        else:
            return jsonify({"logs": []}), 200
    except Exception as e:
        logging.error(f"خطأ في قراءة السجلات: {str(e)}")
        return jsonify({"error": str(e)}), 500

# --- تشغيل الخادم ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)