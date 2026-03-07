from typing import Union
from pyrogram.types import Message, Audio, Voice

def get_url(message_1: Message) -> Union[str, None]:
    messages = [message_1]

    if message_1.reply_to_message:
        messages.append(message_1.reply_to_message)

    text = ""
    offset = None
    length = None

    for message in messages:
        if offset:
            break

        if message.entities:
            for entity in message.entities:
                if entity.type == "url":
                    text = message.text or message.caption
                    offset, length = entity.offset, entity.length
                    break

    if offset is None:
        return None

    return text[offset:offset + length]

# Replace your old get_file_name with this one:
def get_file_name(audio: Union[Audio, Voice]):
    if isinstance(audio, Voice):
        return f'{audio.file_unique_id}.ogg'
    
    # Safer extraction: defaults to mp3 if file_name is missing/broken
    ext = "mp3" 
    if audio.file_name and "." in audio.file_name:
        ext = audio.file_name.split(".")[-1]
        
    return f'{audio.file_unique_id}.{ext}'
