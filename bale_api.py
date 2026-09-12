import requests
import json
import os


class BaleAPI:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.base_url = f"https://tapi.bale.ai/bot{bot_token}"
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=requests.adapters.Retry(total=3, backoff_factor=0.3)
        )
        self.session.mount("https://", adapter)

    def send_message(self, chat_id, text, reply_markup=None, parse_mode="Markdown"):
        url = f"{self.base_url}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
        if reply_markup is not None:
            payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in send_message: {e}")
            return None

    def edit_message_text(self, chat_id, message_id, text, reply_markup=None, parse_mode="Markdown"):
        url = f"{self.base_url}/editMessageText"
        payload = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": parse_mode}
        if reply_markup is not None:
            payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in edit_message_text: {e}")
            return None

    def edit_message_caption(self, chat_id, message_id, caption, reply_markup=None, parse_mode="Markdown"):
        url = f"{self.base_url}/editMessageCaption"
        payload = {"chat_id": chat_id, "message_id": message_id, "caption": caption, "parse_mode": parse_mode}
        if reply_markup is not None:
            payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in edit_message_caption: {e}")
            return None

    def edit_message_reply_markup(self, chat_id, message_id, reply_markup=None):
        url = f"{self.base_url}/editMessageReplyMarkup"
        payload = {"chat_id": chat_id, "message_id": message_id}
        if reply_markup is not None:
            payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in edit_message_reply_markup: {e}")
            return None

    def send_invoice(self, chat_id, title, description, provider_token, prices,
                      payload=None, photo_url=None, need_name=False, need_phone_number=False,
                      need_email=False, need_shipping_address=False, is_flexible=False):
        url = f"{self.base_url}/sendInvoice"
        data = {
            "chat_id": chat_id,
            "title": title,
            "description": description,
            "provider_token": provider_token,
            "prices": json.dumps(prices, ensure_ascii=False),
            "need_name": need_name,
            "need_phone_number": need_phone_number,
            "need_email": need_email,
            "need_shipping_address": need_shipping_address,
            "is_flexible": is_flexible,
        }
        if payload is not None:
            data["payload"] = payload
        if photo_url is not None:
            data["photo_url"] = photo_url
        try:
            response = self.session.post(url, data=data, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in send_invoice: {e}")
            return None

    def answer_pre_checkout_query(self, pre_checkout_query_id, ok=True, error_message=None):
        url = f"{self.base_url}/answerPreCheckoutQuery"
        data = {"pre_checkout_query_id": pre_checkout_query_id, "ok": ok}
        if error_message is not None:
            data["error_message"] = error_message
        try:
            response = self.session.post(url, data=data, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in answer_pre_checkout_query: {e}")
            return None

    def forward_message(self, chat_id, from_chat_id, message_id):
        """فوروارد پیام از یک کانال به کانال دیگه"""
        url = f"{self.base_url}/forwardMessage"
        payload = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id
        }
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in forward_message: {e}")
            return None

    def send_photo_with_caption(self, chat_id, file_id, caption, reply_markup=None, parse_mode="Markdown"):
        url = f"{self.base_url}/sendPhoto"
        payload = {"chat_id": chat_id, "photo": file_id, "caption": caption, "parse_mode": parse_mode}
        if reply_markup is not None:
            payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in send_photo_with_caption: {e}")
            return None

    def get_chat_member(self, chat_id, user_id):
        url = f"{self.base_url}/getChatMember"
        payload = {"chat_id": chat_id, "user_id": user_id}
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in get_chat_member: {e}")
            return None

    def answer_callback_query(self, callback_query_id, text=None, show_alert=False):
        url = f"{self.base_url}/answerCallbackQuery"
        payload = {"callback_query_id": callback_query_id, "show_alert": show_alert}
        if text is not None:
            payload["text"] = text
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in answer_callback_query: {e}")
            return None

    def delete_message(self, chat_id, message_id):
        url = f"{self.base_url}/deleteMessage"
        payload = {"chat_id": chat_id, "message_id": message_id}
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in delete_message: {e}")
            return None

    def pin_message(self, chat_id, message_id, note=None):
        """Send a plain message as a visual 'pin note' since Bale may not support pinMessage."""
        if note:
            self.send_message(chat_id, f"📌 {note}")

    def send_photo(self, chat_id, file_id, caption="", reply_markup=None, parse_mode="Markdown"):
        return self.send_photo_with_caption(chat_id, file_id, caption, reply_markup, parse_mode)

    def send_video(self, chat_id, file_id, caption="", reply_markup=None, parse_mode="Markdown"):
        url = f"{self.base_url}/sendVideo"
        payload = {"chat_id": chat_id, "video": file_id,
                   "caption": caption, "parse_mode": parse_mode}
        if reply_markup is not None:
            payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in send_video: {e}")
            return None

    def send_voice(self, chat_id, file_id, reply_markup=None):
        url = f"{self.base_url}/sendVoice"
        payload = {"chat_id": chat_id, "voice": file_id}
        if reply_markup is not None:
            payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in send_voice: {e}")
            return None

    def send_audio(self, chat_id, file_id, reply_markup=None):
        url = f"{self.base_url}/sendAudio"
        payload = {"chat_id": chat_id, "audio": file_id}
        if reply_markup is not None:
            payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in send_audio: {e}")
            return None

    def send_document(self, chat_id, file_id, caption="", reply_markup=None, parse_mode="Markdown"):
        url = f"{self.base_url}/sendDocument"
        payload = {"chat_id": chat_id, "document": file_id,
                   "caption": caption, "parse_mode": parse_mode}
        if reply_markup is not None:
            payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in send_document: {e}")
            return None

    def send_document_file(self, chat_id, file_path, caption="", parse_mode="Markdown"):
        """آپلود و ارسال مستقیم یک فایل از روی دیسک (بر خلاف send_document که فقط file_id می‌گیرد)."""
        url = f"{self.base_url}/sendDocument"
        data = {"chat_id": chat_id}
        if caption:
            data["caption"] = caption
            data["parse_mode"] = parse_mode
        try:
            with open(file_path, "rb") as f:
                files = {"document": (os.path.basename(file_path), f, "application/json")}
                response = self.session.post(url, data=data, files=files, timeout=30)
            return response.json()
        except Exception as e:
            print(f"Error in send_document_file: {e}")
            return None

    def get_chat(self, chat_id):
        url = f"{self.base_url}/getChat"
        payload = {"chat_id": chat_id}
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in get_chat: {e}")
            return None

    def get_chat_administrators(self, chat_id):
        url = f"{self.base_url}/getChatAdministrators"
        payload = {"chat_id": chat_id}
        try:
            response = self.session.post(url, data=payload, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in get_chat_administrators: {e}")
            return None

    def get_me(self):
        url = f"{self.base_url}/getMe"
        try:
            response = self.session.post(url, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error in get_me: {e}")
            return None
