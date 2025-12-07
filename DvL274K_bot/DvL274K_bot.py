import logging
import asyncio
import telethon
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes,CallbackQueryHandler,MessageHandler,filters


class DvL274KBot:
    def __init__(self,TOKEN):
        self.token = TOKEN
        self.ID = 
        self.subscribers_id = []
        with open('subscribers_id.txt','r') as ids:
             for id in ids.readlines():
                 self.subscribers_id.append(int(id.strip()))

        self.back_button = InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="bot_back")], ])
        self.text ="""
<b> Protocol: These Are The Command My Master Given Me</b>
 <b>▬▬ι═════════════════ﺤ</b>
<b>Start AD</b> — Deploy automated advertisement routines at fixed intervals.
<b>Add AD</b> — Upload or define your broadcast payload (text or poster). 
<b>My Master</b> — You Can Share Your Query With My Master.  
<b>Add Group</b> — Authorize a group node for broadcast (bot must be present).
<b>Help</b> — More Information Added By My Master.  
<b>Exit</b> — What You Think It Does?.
 <b>▬▬ι═════════════════ﺤ</b>
"""
        self.help_text ="""
▬▬ι══════════════ﺤ

<b>⟢ SYSTEM MANUAL ⟣</b>

• <b>Start AD</b> — Deploy automated ad routines at fixed intervals.
• <b>Add AD</b> — Upload your broadcast content (text or poster).
• <b>Add Group</b> — Authorize a group node for posting (bot must be a member).
• <b>My Master</b> — Contact my creator directly for queries or access.
• <b>Help</b> — Displays this command reference.
• <b>Exit</b> — Terminates the current session.

<b>Note:</b> Certain functions are restricted to authorized users only.

▬▬ι══════════════ﺤ
"""
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)
        logging.info('bot initialized successfully')
        self.app = Application.builder().token(self.token).build()
        job_queue = self.app.job_queue
        self.queue = job_queue
        self.app.add_handler(CommandHandler('start', self.bot_start))
        self.app.add_handler(CallbackQueryHandler(self.bot_Callback_Handler))
        self.app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, self.bot_message_handler))


    async def bot_message_handler(self, update, context):
          if update.effective_user.id in self.subscribers_id:

            if context.user_data.get("confirming_user"):

                chat_id = context.user_data.get("bot_chat_id")
                message_id = context.user_data.get("bot_message_id")
                if chat_id and message_id:
                      await context.bot.delete_message(chat_id = chat_id, message_id = message_id)
                context.user_data["confirming_user"] = False
                del context.user_data["bot_chat_id"]
                del context.user_data["bot_message_id"]
                context.user_data["user_id"] = update.effective_user.id
                if update.effective_message.text:
                    context.user_data["user_text"] = update.effective_message.text
                    context.user_data["user_caption"] = update.effective_message.caption or "no caption"
                    await update.message.reply_text("<b>Sucessfully Added ✅</b>", reply_markup=self.back_button,
                                                    parse_mode="HTML")
                elif update.effective_message.photo:
                    context.user_data["user_img"] = update.effective_message.photo[-1].file_id
                    context.user_data["user_caption"] = update.effective_message.caption or "no caption"
                    await update.message.reply_text("<b>Sucessfully Added ✅</b>", reply_markup=self.back_button,
                                                    parse_mode="HTML")
                elif update.effective_message.video:
                    context.user_data["user_vid"] = update.effective_message.video.file_id
                    context.user_data["user_caption"] = update.effective_message.caption or "no caption"
                    await update.message.reply_text("<b>Sucessfully Added ✅</b>", reply_markup=self.back_button,
                                                    parse_mode="HTML")
                else:
                   msg = await update.message.reply_text("<b>❌ Not Supported File type</b>", parse_mode="HTML")
                   await asyncio.sleep(1)
                   await context.bot.delete_message(chat_id = msg.chat.id, message_id = msg.message_id)
                return
            else:
              msg = await update.message.reply_text(f"""You haven’t added an ad yet using <b>Add AD</b>
Please complete that step first before continuing <b>({update.effective_user.first_name})</b>""", parse_mode="HTML")
              await asyncio.sleep(2)
              await context.bot.delete_message(chat_id=update.effective_chat.id,
                                               message_id=update.effective_message.message_id)
              await context.bot.delete_message(chat_id =msg.chat.id, message_id = msg.message_id)
          else:
              msg = await update.message.reply_text(f"""<b>{update.effective_user.first_name}</b>
Please Use The Commands My Master Applied For Me""", parse_mode="HTML")
              await asyncio.sleep(2)
              await context.bot.delete_message(chat_id = msg.chat.id, message_id = msg.message_id)
    async def bot_Callback_Handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        #adding bot callback query
         bot_callback_query = update.callback_query
         await bot_callback_query.answer()

        #checking chat types
         chat_type = update.effective_chat.type

        #made a back Keyword
         keyword = self.back_button
        #if elif else logic
        #checking if the bot in group or not
         if chat_type in ['group', 'supergroup']:

             if bot_callback_query.data == "group_add":
                  await self.group_add(update,context,bot_callback_query)
             elif bot_callback_query.data == "greet_me":
                  await self.greet_me(update, context,bot_callback_query)

             elif bot_callback_query.data == "my_master_id":
                 await self.my_master_id(update, context,bot_callback_query)

             elif bot_callback_query.data == "help":
                 await bot_callback_query.message.edit_text(self.help_text, parse_mode="HTML", reply_markup=keyword)

             elif bot_callback_query.data == "exit":
                  await self.bot_exit(update, context,bot_callback_query)

             elif bot_callback_query.data in ["add_ad","start_ad"]:
                 await bot_callback_query.message.edit_text(
                     "⚙️ <b>Command restriction:</b>\n"
                     "This command is reserved for <b>private sessions</b> only.\n"
                     "Group execution blocked 🚫.",
                     parse_mode="HTML",
                     reply_markup=self.back_button)

             elif bot_callback_query.data == "bot_back":
              #building back logic
              await bot_callback_query.message.edit_text(self.text, reply_markup=self.bot_get_main_menu(),parse_mode="HTML")
             return
         #checking if the bot in private chat
         elif chat_type == 'private':

            if bot_callback_query.data == "greet_me":
                 await self.greet_me(update, context,bot_callback_query)

            elif bot_callback_query.data == "my_master_id":
               await self.my_master_id(update, context,bot_callback_query)

            elif bot_callback_query.data == "group_add":
                await bot_callback_query.message.edit_text(
                    "⚙️ <b>Command restriction:</b>\n"
                    "This command is designed for <b>group environments</b> only.\n"
                    "Direct acess is denied ❌.",
                    parse_mode="HTML",
                    reply_markup=self.back_button)


            elif bot_callback_query.data == "add_ad":
                       await bot_callback_query.message.edit_text(".𖥔 Add your AD below ˚₊⊹I Am awaiting your input…")
                       context.user_data["confirming_user"] = True
                       context.user_data["bot_chat_id"] = bot_callback_query.message.chat.id
                       context.user_data["bot_message_id"]= bot_callback_query.message.message_id

            elif bot_callback_query.data == "start_ad":
                 loading_stage = ["Starting System",
                                  "⋆｡ﾟ",
                                  "⋆｡ﾟ☁︎",
                                  "⋆｡ﾟ☁ ︎｡⋆ ｡ ﾟ",
                                  "⋆｡ﾟ☁ ︎｡⋆ ｡ ﾟ☾ ﾟ",
                                  "⋆｡ﾟ☁ ︎｡⋆ ｡ﾟ☾ ﾟ｡⋆"]
                 for stage in loading_stage:
                     await bot_callback_query.message.edit_text(stage)
                     await asyncio.sleep(0.1)
                 await self.bot_start_ad(update,context,bot_callback_query)


            elif bot_callback_query.data == "stop_ad":
                await self.bot_stop_ad(update, context, bot_callback_query)
                button = InlineKeyboardButton("Start", callback_data="bot_back")
                start_button = InlineKeyboardMarkup([[button]])
                await bot_callback_query.message.reply_text("Start Again?!",reply_markup=start_button)

            elif bot_callback_query.data == "help":
                 await bot_callback_query.message.edit_text(self.help_text, parse_mode="HTML",reply_markup=keyword)

            elif bot_callback_query.data == "exit":
                await self.bot_exit(update,context,bot_callback_query)

            elif bot_callback_query.data == "bot_back":
                # building back logic
                await bot_callback_query.message.edit_text(self.text, reply_markup=self.bot_get_main_menu(),parse_mode="HTML")

         return
         # start commands


    async def bot_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        #building back logic
        await update.message.reply_text(self.text, reply_markup=self.bot_get_main_menu(), parse_mode="HTML")

    async def my_master_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE,bot_callback_query: CallbackQuery):

        await bot_callback_query.message.edit_text(
            "👑 My Master is the one and only: @DvLKing20\n"
            "🌸 If you need help or want to share feedback, message him directly.",
            reply_markup=self.back_button)

    async def bot_start_ad(self, update: Update, context: ContextTypes.DEFAULT_TYPE,bot_callback_query: CallbackQuery):
        bot_button = InlineKeyboardButton("Stop AD", callback_data="stop_ad")
        stop_ad = InlineKeyboardMarkup([[bot_button]])

        if  update.effective_user.id == context.user_data.get("user_id"):
            await bot_callback_query.message.edit_text("Access granted! ✅.")
            self.queue.run_repeating(lambda ctx:self.bot_auto_post(context), interval=86400, first=0, name=str(update.effective_user.id))
            await bot_callback_query.message.edit_text("Started Auto Posting! ✅",reply_markup=stop_ad)
            return
        else:
            await bot_callback_query.message.edit_text("You didnt added a ad first add a ad with: <b>Add AD</b>❌",reply_markup=self.back_button,parse_mode="HTML")
            return

    async def bot_auto_post(self,context: ContextTypes.DEFAULT_TYPE):
         file_path = f"{context.user_data.get('user_id')}.txt"
         ad_caption = context.user_data.get("user_caption")
         if os.path.exists(file_path):
            with open(file_path) as f:
                 try:
                   for group_id in f.readlines():
                     groud_id = group_id.strip()
                     if context.user_data.get("user_text"): # telegram file_ids start with "Ag"
                        ad_caption = context.user_data.get("user_caption")
                        ad = context.user_data.get("user_text")
                        await context.bot.send_message(chat_id=int(group_id),text=ad)

                     elif context.user_data.get("user_img"):
                         ad = context.user_data.get("user_img")
                         await context.bot.send_photo(chat_id=int(group_id), photo=ad, caption=ad_caption)

                     elif context.user_data.get("user_vid"):
                         ad = context.user_data.get("user_vid")
                         await context.bot.send_video(chat_id=int(group_id), video=ad, caption=ad_caption)
                 except Exception as e:
                     logging.info("Exception occured: ",e)
                     return
         else:
            logging.info(f"File not found: {file_path}")

    async def bot_stop_ad(self, update: Update, context: ContextTypes.DEFAULT_TYPE,bot_callback_query):
        if context.user_data.get("user_id") == update.effective_user.id:
            jobs = self.queue.get_jobs_by_name(str(update.effective_user.id))
            if not jobs:
                await bot_callback_query.message.edit_text("No active job to Stop! ❌",reply_markup=self.back_button)
            else:
                await bot_callback_query.message.edit_text("Stopped :)! ✅")
                await context.bot.delete_message(chat_id=bot_callback_query.message.chat.id, message_id=bot_callback_query.message.message_id)
                for job in jobs:
                    job.schedule_removal()
                context.user_data.clear()
        else:
            msg = await bot_callback_query.message.edit_text("You Didnt Added a AD Yet! ❌")
            await asyncio.sleep(1)
            await context.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)



    async def group_add(self,update,context,bot_callback_query):
        group_id = update.effective_chat.id
        group_name = update.effective_chat.title
        if not os.path.exists(f"{update.effective_user.id}.txt"):
           with open(f"{update.effective_user.id}.txt","w") as f:
                  pass
        with open(f'{update.effective_user.id}.txt', 'r') as f:
            data = f.read().splitlines()
            if str(group_id) not in data:
                def append_group():
                      with open(f'{update.effective_user.id}.txt', 'a') as f:
                         f.write(f"{group_id}\n")
                await asyncio.to_thread(append_group)
                await bot_callback_query.message.edit_text(f"✅ Successfully added group!\n\n"
                f"📛 Group Name: {group_name}\n"
                f"🆔 Group ID: {group_id}\n\n"
                f"I'll now include this group for future updates!",
                                                           reply_markup=self.back_button)
            else:
                await bot_callback_query.message.edit_text(f"⚠️ This group is already registered!\n\n"
                f"📛 Group Name: {group_name}\n"
                f"🆔 Group ID: {group_id}\n\n"
                f"No need to add it again — I’ve already got it saved!",
                 reply_markup=self.back_button)
        return

    async def greet_me(self, update, context, bot_callback_query):
        user_id = update.effective_user.id

        # Initial greeting
        await bot_callback_query.message.edit_text(
            f" ﾟ☾ ﾟ｡⋆ Hey there, {update.effective_user.first_name}!\n\n"
            f"I hope you're having a great day 🌟\n"
            f"Processing..."
        )
        #checking if file exists or not
        if not os.path.exists("PrivateUser_id.txt"):
            with open("PrivateUser_id.txt", "w") as f:
                pass
        # Check if user ID already exists
        with open("PrivateUser_id.txt", "r") as f:
            data = f.read().splitlines()

        if str(user_id) not in data:
            def append_user():
               with open("PrivateUser_id.txt", "a") as f:
                  f.write("\n"+f"{user_id}")

            await asyncio.to_thread(append_user)
            await bot_callback_query.message.edit_text(
                f" ﾟ☾ ﾟ｡⋆ Hey there, {update.effective_user.first_name}!\n\n"
                f"I hope you're having a great day 🌟\n"
                f"Your ID has been saved for future updates — stay tuned ✅!",
                reply_markup=self.back_button
            )
        else:
            await bot_callback_query.message.edit_text(f" ﾟ☾ ﾟ｡⋆ Hey there, {update.effective_user.first_name}!\n\n"
            f"I hope you're having a great day 🌟\n"
            f"Your ID has already been saved for future updates ❌!",
            reply_markup = self.back_button)

    async def bot_exit(self, update: Update, context: ContextTypes.DEFAULT_TYPE, bot_callback_query):
        exit_text = """
        ▬▬ι══════════════ﺤ
        <b>⟢ SESSION TERMINATED ⟣</b>

        All active links have been severed.
        You can reinitialize the system anytime using <b>/start</b>.

        .𖥔 ݁ ˖. ݁₊ ⊹ Connection Closed ˚₊⊹
        ▬▬ι══════════════ﺤ
        """
        button = InlineKeyboardButton("Start",callback_data="bot_back")
        start_button = InlineKeyboardMarkup([[button]])
        await bot_callback_query.message.edit_text(exit_text, parse_mode="HTML",reply_markup=start_button)
        return

    def bot_get_main_menu(self):
        bot_button1 = InlineKeyboardButton("Greet Me", callback_data="greet_me")
        bot_button2 = InlineKeyboardButton("My Master", callback_data="my_master_id")
        bot_button3 = InlineKeyboardButton("Start AD", callback_data="start_ad")
        bot_button4 = InlineKeyboardButton("Add Group", callback_data="group_add")
        bot_button5 = InlineKeyboardButton("Help", callback_data="help")
        bot_button6 = InlineKeyboardButton("Exit", callback_data="exit")
        bot_button7 = InlineKeyboardButton("Add AD", callback_data="add_ad")
        # Packing it into a Markup
        reply_markup = InlineKeyboardMarkup(   [[bot_button3, bot_button7],
                                               [bot_button1, bot_button2],
                                               [bot_button4, bot_button5],
                                                    [bot_button6],])
        return reply_markup

    def run(self):
        print("bot started")
        self.app.run_polling()


if __name__ == '__main__':
    TOKEN = ""
    bot_object = DvL274KBot(TOKEN)
    bot_object.run()
