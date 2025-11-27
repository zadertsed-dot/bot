import discord
import os


# Конфигурация
YOUR_USER_ID = 675065037030817792  # Ваш Discord ID
TARGET_CHANNEL_ID = 1421130256202338486  # ID канала для отслеживания

# Настройка интентов
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Бот запущен! Вошел как {client.user}')

@client.event
async def on_message(message):
    # Игнорируем сообщения не из целевого канала
    if message.channel.id != TARGET_CHANNEL_ID:
        return

    # Игнорируем сообщения от самого бота
    if message.author == client.user:
        return

    # Логируем для диагностики
    print(f'Обработка сообщения от {message.author} (тип: {message.type}, '
          f'embeds: {len(message.embeds)}, attachments: {len(message.attachments)}): '
          f'{message.content[:100] if message.content else "[без текста]"}')

    try:
        # Получаем пользователя для ЛС
        user = await client.fetch_user(YOUR_USER_ID)
        
        # Формируем контент для пересылки
        files = []
        for attachment in message.attachments:
            # Скачиваем каждое вложение
            file = await attachment.to_file()
            files.append(file)

        # Отправляем пересланное сообщение в ЛС
        await user.send(
            content=message.content,
            embeds=message.embeds,
            files=files
        )

        # Удаляем оригинальное сообщение
        await message.delete()

        print(f'Сообщение от {message.author} успешно переслано в ЛС и удалено.')

    except Exception as error:
        print(f"Ошибка при пересылке или удалении: {error}")
        # Если ошибка, не удаляем сообщение, чтобы не потерять его

# Запуск бота
client.run(os.getenv('TOKEN'))
