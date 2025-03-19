            balance_line = extract_balance_line(msg)
            if currency == '$' and balance >= 10:
                if user_id not in verified_ids:
                    expire = datetime.utcnow() + timedelta(hours=24)
                    invite_link: ChatInviteLink = await context.bot.create_chat_invite_link(
                        chat_id=private_group_id,
                        member_limit=1,
                        expire_date=expire
                    )
                    await update.message.reply_text(
                        f"تم التحقق بنجاح ✅\nرابط الدخول للقروب الخاص (صالح لمدة 24 ساعة):\n{invite_link.invite_link}"
                    )
                    if balance > 700:
                        group15_invite_link: ChatInviteLink = await context.bot.create_chat_invite_link(
                            chat_id=group_15_deals_id,
                            member_limit=1,
                            expire_date=expire
                        )
                        await update.message.reply_text(
                            f"تم تأهيلك لجروب 15 صفقة ربح مباشر ✅ (صالح لمدة 24 ساعة):\n{group15_invite_link.invite_link}"
                        )

                    username = update.message.from_user.username or "بدون معرف"
                    await context.bot.send_message(
                        chat_id=admin_user_id,
                        text=f"✅ تم إرسال الرابط إلى المعرف:\nID: {user_id}\n{balance_line}\nUsername: @{username}"
                    )

                    verified_ids.add(user_id)
                    save_ids(verified_file, verified_ids)
            else:
                await update.message.reply_text("تم التحقق بنجاح ✅ اكمل الخطوة القادمة بعمل ايداع واعد الارسال.")

            # إزالة من قائمة المعالجة
            pending_ids.discard(user_id)
            save_ids(pending_file, pending_ids)

        client.remove_event_handler(response_handler)

async def handle_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(auto_reply)

# تشغيل البوت
print("جاري تسجيل الدخول على حساب تليجرام...")
client = TelegramClient(session_name, api_id, api_hash)
client.start()

print("جاري تشغيل بوت تلجرام...")
app = Application.builder().token(bot_token).build()
app.add_handler(CommandHandler("start", start_command))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
app.add_handler(MessageHandler(~filters.TEXT, handle_non_text))
app.run_polling()
