import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp
import os

# إعدادات التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة التعامل مع الأمر /start
async def start(update: Update, context):
    await update.message.reply_text(
        "مرحباً! استخدم /start أو /download لتحميل الفيديوهات."
    )

# دالة لتحميل الفيديو من الرابط
async def download_video(update: Update, context):
    message = update.message.text
    if message.startswith("http"):
        await update.message.reply_text(f"جارٍ تحميل الفيديو من الرابط: {message}")
        
        # تحميل الفيديو باستخدام yt-dlp
        try:
            # إعداد خيارات yt-dlp لتحميل الفيديو
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',  # تحميل أفضل جودة للفيديو والصوت
                'outtmpl': 'video.%(ext)s',  # حفظ الفيديو بصيغة مناسبة
                'noplaylist': True,  # تجاهل قوائم التشغيل
            }

            # تحميل الفيديو باستخدام yt-dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(message, download=True)  # تنزيل الفيديو من الرابط

            # تحديد اسم الملف الذي تم تنزيله
            video_file = f"video.{result['ext']}"

            # إرسال الفيديو بعد تحميله
            with open(video_file, 'rb') as file:
                await update.message.reply_video(file)

            # حذف الفيديو بعد إرساله
            os.remove(video_file)

        except Exception as e:
            await update.message.reply_text(f"حدث خطأ أثناء تحميل الفيديو: {e}")
    else:
        await update.message.reply_text("يرجى إرسال رابط صالح للفيديو.")

# الدالة الرئيسية لإعداد البوت
def main():
    # تم إضافة رمز API الخاص بك
    application = Application.builder().token("7239744250:AAHeCRJ-XYy7uxbjQ1sk10eYvltLdVt782Y").build()

    # معالج الأوامر
    application.add_handler(CommandHandler("start", start))

    # معالج الرسائل العامة (لتعامل مع الرسائل التي تحتوي على رابط)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    application.run_polling()

if __name__ == '__main__':
    main()