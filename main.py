# Начало
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import controller as cont
import logging
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv("TOKEN")

# print(TOKEN)

# есть описание через Ctrl

# инициализируем БД
cont.start_work()

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bot.log')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler('help', cont.help_command))
app.add_handler(CommandHandler('view', cont.view_command))
app.add_handler(CommandHandler('add', cont.add_command))
app.add_handler(CommandHandler('find', cont.find_command))
app.add_handler(CommandHandler('del', cont.del_command))

app.run_polling()

# # первый вариант
# # pip install python-dotenv
# import os
# from dotenv import load_dotenv
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)
# # ==========================================================
#
# # второй вариант
# # settings.py
# # importing the load_dotenv from the python-dotenv module
# from dotenv import load_dotenv
#
# ## using existing module to specify location of the .env file
# from pathlib import Path
# import os
#
# load_dotenv()
# env_path = Path('.')/'.env'
# load_dotenv(dotenv_path=env_path)
#
# # retrieving keys and adding them to the project
# # from the .env file through their key names
# SECRET_KEY = os.getenv("SECRET_KEY")
# DOMAIN = os.getenv("DOMAIN")
# EMAIL = os.getenv("EMAIL")
# # ==========================================================

# попробовать
# pip install python-dotenv
# import os
# from dotenv import load_dotenv
# from pathlib import Path
# load_dotenv()
# env_path = Path('.')/'.env'
# load_dotenv(dotenv_path=env_path)
# TOKEN = os.getenv("TOKEN")
