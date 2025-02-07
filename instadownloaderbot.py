import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import instaloader

# تنظیمات لاگ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# تابع برای دستور /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('سلام! لینک پست اینستاگرام رو برام بفرست.')

# تابع برای دریافت لینک اینستاگرام
async def handle_instagram_link(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    try:
        # دریافت اطلاعات پست از اینستاگرام
        L = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        
        # دانلود عکس یا ویدیو
        if post.is_video:
            await update.message.reply_video(post.video_url)
        else:
            await update.message.reply_photo(post.url)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text('مشکلی پیش اومده. لطفا دوباره تلاش کن.')

# تابع اصلی
def main() -> None:
    # توکن ربات تلگرام
    token = '7417919991:AAH4C5d-EN1MzlMpIdoSi_2RaHaoB3xaa-E'
    
    # ایجاد Application
    application = Application.builder().token(token).build()

    # ثبت دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()