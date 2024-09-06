import os
import time
import schedule
import requests
import logging
from flask import Flask
from flask_restful import Resource, Api
from threading import Thread

# إعداد تسجيل الأخطاء
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

class Greeting(Resource):
    def get(self):
        return "𝗦𝗰𝗼𝗿𝗽𝗶𝗼 𝘄𝗼𝗿𝗸𝘀 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✅"

api.add_resource(Greeting, '/')

def run_python_command():
    try:
        # تنفيذ الأمر python3 -m StringGen
        logger.info("Executing Python command: python3 -m StringGen")
        result = os.system("python3 -m StringGen")
        logger.info(f"Command executed with result: {result}")
    except Exception as e:
        logger.error(f"Failed to execute Python command - Error: {e}")

# جدولة المهمة لتعمل كل 5 ساعات
schedule.every(5).hours.do(run_python_command)

def run_flask_app():
    try:
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), threaded=True)
    except Exception as e:
        logger.error(f"Failed to start Flask server - Error: {e}")

if __name__ == "__main__":
    # تشغيل خادم Flask في خيط منفصل
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()
    logger.info("Flask server started.")
    
    # الانتظار بضع ثواني للتأكد من أن خادم Flask قد بدأ
    time.sleep(5)
    
    # تشغيل المجدول
    while True:
        schedule.run_pending()
        time.sleep(1)
