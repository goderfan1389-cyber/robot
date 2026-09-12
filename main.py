import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
from config import BOT_TOKEN
import db
from handlers import (
    handle_start, handle_callback, handle_earn_coins,
    handle_order_member, handle_back, handle_wallet,
    handle_wallet_balance, handle_wallet_transfer, handle_wallet_buy,
    handle_vip_buy, handle_my_orders,
    handle_channel_id_input,
    handle_transfer_target_input, handle_transfer_amount_input,
    handle_receipt_input,
    handle_svc_purchase_menu, handle_svc_platform_menu, handle_svc_service_start,
    handle_svc_amount_input, handle_svc_link_input, handle_svc_receipt_input,
    handle_mjoin_link_input, handle_mjoin_days_input, handle_mjoin_receipt_input,
    mandatory_join_checker, _required_channels_gate,
    load_users, save_users, _remember_user_profile, handle_pricing,
    check_and_penalty_left_channels,
    order_channel_monitor,
    build_reply_main_menu, bale_api,
    LANGS, _T, _get_user_lang, ADMIN_ID,
    handle_leaderboard_menu,
    handle_best_member, handle_best_referral, handle_best_purchase,
    handle_member_prize_info, handle_referral_prize_info, handle_purchase_prize_info,
    leaderboard_scheduler,
    handle_games_menu, handle_rps_start, handle_penalty_start, handle_guess_start,
    handle_guess_input,
    handle_gift_menu, handle_invite_friends, handle_daily_gift, handle_lucky_wheel,
    handle_gift_code_entry, handle_gift_code_input, handle_signup_gift_menu,
    handle_signup_offer,
    handle_ad_menu, handle_ad_content_input, handle_ad_receipt_input,
    handle_arka_info, handle_change_lang, handle_account,
    handle_support, handle_support_message,
    handle_admin_message,
    handle_rules, handle_mandatory_join_menu,
    handle_spam_warning, handle_phone_contact, check_spam,
    handle_photo_design_start, handle_photo_design_desc_input,
    handle_photo_design_invalid_desc, handle_photo_design_receipt_input,
    handle_photo_design_admin_upload, handle_photo_design_invalid_upload,
    is_bot_enabled, is_maintenance_mode, is_admin_user,
    handle_pre_checkout_query, handle_successful_payment,
    _ADMIN_PANEL_LOADED,
)

# ── import مستقیم از admin_panel ──
_admin_panel_btn_text = {"fa": "⚙️ پنل ادمین", "en": "⚙️ Admin Panel",
                         "fr": "⚙️ Admin Panel", "ar": "⚙️ Admin Panel"}
if _ADMIN_PANEL_LOADED:
    try:
        from admin_panel import (
            handle_admin_panel_button as _do_admin_panel,
            handle_admin_callback,
            build_reply_main_menu_admin,
            ADMIN_TEXTS as _AT_DICT,
        )
        _admin_panel_btn_text = {
            lang: (v.get("btn_admin_panel", "⚙️ پنل ادمین"))
            for lang, v in _AT_DICT.items()
        }
    except Exception as _e:
        print(f"[admin_panel direct import] {_e}")
        _ADMIN_PANEL_LOADED = False
        def _do_admin_panel(*a, **k): pass
        def build_reply_main_menu_admin(lang="fa"): return build_reply_main_menu(lang)
else:
    def _do_admin_panel(*a, **k): pass
    def build_reply_main_menu_admin(lang="fa"): return build_reply_main_menu(lang)


def _is_admin_panel_btn(text, lang):
    return text == _admin_panel_btn_text.get(lang, "⚙️ پنل ادمین")

executor = ThreadPoolExecutor(max_workers=50)
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(
    pool_connections=20, pool_maxsize=50,
    max_retries=requests.adapters.Retry(total=3, backoff_factor=0.1)
)
session.mount("https://", adapter)


def _background_penalty_checker():
    while True:
        try:
            users = load_users()
            for uid_str, udata in users.items():
                if udata.get("joined_channels"):
                    try:
                        check_and_penalty_left_channels(int(uid_str))
                    except Exception as e:
                        print(f"[penalty] {e}")
        except Exception as e:
            print(f"[checker] {e}")
        time.sleep(300)


def _match_lang_btn(msg_text, key):
    """Check if msg_text matches the key in any language."""
    for lang_data in LANGS.values():
        if lang_data.get(key) == msg_text:
            return True
    return False


_MENU_BUTTON_KEYS = [
    "btn_account","btn_ad","btn_arka_info","btn_back","btn_balance",
    "btn_best_member","btn_best_member_prize","btn_best_purchase","btn_best_purchase_prize",
    "btn_best_referral","btn_best_referral_prize","btn_blubank","btn_buy_coins","btn_buy_vip",
    "btn_change_lang","btn_daily_gift","btn_earn_coins","btn_games","btn_gift","btn_gift_code",
    "btn_guess","btn_invite","btn_lb_back","btn_leaderboard","btn_mandatory_join","btn_melligold",
    "btn_milligold","btn_my_orders","btn_order_member","btn_penalty","btn_platform_bale",
    "btn_platform_eitaa","btn_platform_rubika","btn_pricing","btn_rps","btn_rules",
    "btn_signup_gift","btn_support","btn_svc_bale_member","btn_svc_bale_reaction","btn_svc_bale_sin",
    "btn_svc_eitaa_member","btn_svc_eitaa_sin","btn_svc_purchase","btn_svc_rubika_member",
    "btn_svc_rubika_reaction","btn_svc_rubika_sin","btn_transfer","btn_wallet","btn_wheel",
    "btn_svc_edit_coins","btn_svc_edit_uses","btn_photo_design",
]

def _is_menu_button(msg_text):
    """
    چک می‌کند که آیا پیام دقیقاً متن یکی از دکمه‌های اصلی منو (به هر زبانی) است.
    اگر بله، یعنی کاربر واقعاً روی یک دکمه‌ی منو زده، نه اینکه دارد ورودیِ
    مورد انتظار یک state خاص (مثل لینک کانال) را می‌فرستد — پس نباید آن را
    به‌عنوان ورودیِ state پردازش کرد، حتی اگر کاربر وسط یک فرایند چندمرحله‌ای باشد.
    """
    if not msg_text:
        return False
    for key in _MENU_BUTTON_KEYS:
        if _match_lang_btn(msg_text, key):
            return True
    return False


def _is_admin_panel_btn(msg_text, lang):
    """چک می‌کنه آیا متن دکمه پنل ادمین هست."""
    if not _ADMIN_PANEL_LOADED:
        return False
    at = _AT_DICT.get(lang) or _AT_DICT["fa"]
    return msg_text == at.get("btn_admin_panel", "⚙️ پنل ادمین")


def process_update(update):
    try:
        if "message" in update:
            message = update["message"]
            chat_id = message.get("chat", {}).get("id")
            from_obj = message.get("from")
            if not from_obj:
                return
            user_id = from_obj.get("id")
            if not chat_id or not user_id:
                return

            # ── گیت سراسری روشن/خاموش و حالت تعمیرات ربات (ادمین همیشه معاف است) ──
            if not is_admin_user(user_id):
                if not is_bot_enabled():
                    return
                if is_maintenance_mode():
                    _maint_lang = _get_user_lang(user_id)
                    _maint_t = _T(_maint_lang)
                    bale_api.send_message(chat_id, _maint_t("bot_maintenance_msg"))
                    return

            try:
                _profile_users = load_users()
                _remember_user_profile(_profile_users, str(user_id), from_obj)
                save_users(_profile_users)
            except Exception as e:
                print(f"[profile] {e}")

            # ── Contact (phone number for unblock) ──
            if message.get("contact"):
                handle_phone_contact(chat_id, user_id, message["contact"], from_obj=from_obj)
                return

            users_data = load_users()
            user_record = users_data.get(str(user_id), {})

            # ── Permanently blocked ──
            if user_record.get("perm_blocked"):
                return

            # ── Blocked — only allow phone send ──
            if user_record.get("is_blocked"):
                lang = _get_user_lang(user_id)
                t = _T(lang)
                bale_api.send_message(chat_id, t("blocked_msg"))
                return

            msg_text = message.get("text", "")
            lang = _get_user_lang(user_id)
            t = _T(lang)

            # ── پرداخت موفق از طریق کیف پول بله ──
            if message.get("successful_payment"):
                handle_successful_payment(chat_id, user_id, message["successful_payment"])
                return

            # ── Spam check (non-admin) ──
            if not is_admin_user(user_id):
                if check_spam(user_id):
                    handle_spam_warning(chat_id, user_id)
                    return

            # ── ادمین: state machine پنل ادمین + support reply ──
            if is_admin_user(user_id) and not msg_text.startswith("/"):
                if handle_admin_message(chat_id, user_id, message):
                    return

            # ── گیت سراسری عضویت اجباری (کانال‌های ثابت + جوین اجباری خریداری‌شده) ──
            if not msg_text.startswith("/start") and _required_channels_gate(chat_id, user_id):
                return

            if not msg_text:
                state = user_record.get("state", "idle")
                if state == "waiting_for_support_msg":
                    handle_support_message(chat_id, user_id, message, from_obj)
                elif state == "waiting_for_receipt" and message.get("photo"):
                    handle_receipt_input(chat_id, user_id, message, is_vip_receipt=False)
                elif state == "waiting_for_vip_receipt" and message.get("photo"):
                    handle_receipt_input(chat_id, user_id, message, is_vip_receipt=True)
                elif state == "waiting_for_svc_receipt" and message.get("photo"):
                    handle_svc_receipt_input(chat_id, user_id, message)
                elif state == "waiting_for_mjoin_receipt" and message.get("photo"):
                    handle_mjoin_receipt_input(chat_id, user_id, message)
                elif state == "waiting_for_ad_content":
                    handle_ad_content_input(chat_id, user_id, message)
                elif state == "waiting_for_ad_receipt":
                    handle_ad_receipt_input(chat_id, user_id, message)
                elif state == "waiting_for_photo_design_desc":
                    handle_photo_design_invalid_desc(chat_id, user_id)
                elif state == "waiting_for_photo_design_receipt" and message.get("photo"):
                    handle_photo_design_receipt_input(chat_id, user_id, message)
                elif state == "waiting_for_photo_design_upload":
                    handle_photo_design_admin_upload(chat_id, user_id, message)
                return

            state = user_record.get("state", "idle")

            # ── اگر کاربر وسط یک state (مثل پشتیبانی یا ورود لینک کانال) باشد
            #    ولی روی یک دکمه‌ی واقعی منو بزند، آن state باید پاک شود ──
            if state != "idle" and _is_menu_button(msg_text):
                try:
                    users_data[str(user_id)]["state"] = "idle"
                    save_users(users_data)
                except Exception:
                    pass
                state = "idle"

            # ── Support waiting state ──
            if state == "waiting_for_support_msg" and not _match_lang_btn(msg_text, "btn_back"):
                handle_support_message(chat_id, user_id, message, from_obj)
                return

            if msg_text == "/start":
                handle_start(chat_id, user_id, from_obj=from_obj)
            elif msg_text.startswith("/start "):
                handle_start(chat_id, user_id, msg_text.split(" ", 1)[1].strip(), from_obj=from_obj)

            # ── دکمه پنل ادمین (هندلر داخلی خودش مجوز را چک می‌کند تا پیام «دیگر ادمین نیستید» هم نمایش داده شود) ──
            elif _is_admin_panel_btn(msg_text, lang):
                _do_admin_panel(chat_id, user_id)

            # ── Main menu ──
            elif _match_lang_btn(msg_text, "btn_earn_coins"):
                handle_earn_coins(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_gift"):
                handle_gift_menu(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_ad"):
                handle_ad_menu(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_arka_info"):
                handle_arka_info(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_change_lang"):
                handle_change_lang(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_account"):
                handle_account(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_order_member"):
                handle_order_member(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_pricing"):
                handle_pricing(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_back") or _match_lang_btn(msg_text, "btn_lb_back"):
                handle_back(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_wallet"):
                handle_wallet(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_my_orders"):
                handle_my_orders(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_svc_purchase"):
                handle_svc_purchase_menu(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_leaderboard"):
                handle_leaderboard_menu(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_games"):
                handle_games_menu(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_support"):
                handle_support(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_rules"):
                handle_rules(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_mandatory_join"):
                handle_mandatory_join_menu(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_photo_design"):
                handle_photo_design_start(chat_id, user_id)

            # ── Gift sub-menu ──
            elif _match_lang_btn(msg_text, "btn_invite"):
                handle_invite_friends(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_daily_gift"):
                handle_daily_gift(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_wheel"):
                handle_lucky_wheel(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_gift_code"):
                handle_gift_code_entry(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_signup_gift"):
                handle_signup_gift_menu(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_milligold"):
                handle_signup_offer(chat_id, user_id, "milligold")
            elif _match_lang_btn(msg_text, "btn_blubank"):
                handle_signup_offer(chat_id, user_id, "blubank")
            elif _match_lang_btn(msg_text, "btn_melligold"):
                handle_signup_offer(chat_id, user_id, "melligold")

            # ── Wallet sub-menu ──
            elif _match_lang_btn(msg_text, "btn_balance"):
                handle_wallet_balance(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_transfer"):
                handle_wallet_transfer(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_buy_coins"):
                handle_wallet_buy(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_buy_vip"):
                handle_vip_buy(chat_id, user_id)

            # ── 💟 خرید ممبر-لایک-سین sub-menu ──
            elif _match_lang_btn(msg_text, "btn_platform_bale"):
                handle_svc_platform_menu(chat_id, user_id, "bale")
            elif _match_lang_btn(msg_text, "btn_platform_eitaa"):
                handle_svc_platform_menu(chat_id, user_id, "eitaa")
            elif _match_lang_btn(msg_text, "btn_platform_rubika"):
                handle_svc_platform_menu(chat_id, user_id, "rubika")
            elif _match_lang_btn(msg_text, "btn_svc_bale_member"):
                handle_svc_service_start(chat_id, user_id, "bale_member")
            elif _match_lang_btn(msg_text, "btn_svc_bale_reaction"):
                handle_svc_service_start(chat_id, user_id, "bale_reaction")
            elif _match_lang_btn(msg_text, "btn_svc_bale_sin"):
                handle_svc_service_start(chat_id, user_id, "bale_sin")
            elif _match_lang_btn(msg_text, "btn_svc_eitaa_member"):
                handle_svc_service_start(chat_id, user_id, "eitaa_member")
            elif _match_lang_btn(msg_text, "btn_svc_eitaa_sin"):
                handle_svc_service_start(chat_id, user_id, "eitaa_sin")
            elif _match_lang_btn(msg_text, "btn_svc_rubika_member"):
                handle_svc_service_start(chat_id, user_id, "rubika_member")
            elif _match_lang_btn(msg_text, "btn_svc_rubika_reaction"):
                handle_svc_service_start(chat_id, user_id, "rubika_reaction")
            elif _match_lang_btn(msg_text, "btn_svc_rubika_sin"):
                handle_svc_service_start(chat_id, user_id, "rubika_sin")

            # ── Leaderboard sub-menu ──
            elif _match_lang_btn(msg_text, "btn_best_member"):
                handle_best_member(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_best_referral"):
                handle_best_referral(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_best_purchase"):
                handle_best_purchase(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_best_member_prize"):
                handle_member_prize_info(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_best_referral_prize"):
                handle_referral_prize_info(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_best_purchase_prize"):
                handle_purchase_prize_info(chat_id, user_id)

            # ── Games sub-menu ──
            elif _match_lang_btn(msg_text, "btn_rps"):
                handle_rps_start(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_penalty"):
                handle_penalty_start(chat_id, user_id)
            elif _match_lang_btn(msg_text, "btn_guess"):
                handle_guess_start(chat_id, user_id)

            else:
                if state == "waiting_for_channel_id":
                    handle_channel_id_input(chat_id, user_id, msg_text)
                elif state == "waiting_for_transfer_target":
                    handle_transfer_target_input(chat_id, user_id, msg_text)
                elif state == "waiting_for_transfer_amount":
                    handle_transfer_amount_input(chat_id, user_id, msg_text)
                elif state == "waiting_for_receipt":
                    handle_receipt_input(chat_id, user_id, message, is_vip_receipt=False)
                elif state == "waiting_for_vip_receipt":
                    handle_receipt_input(chat_id, user_id, message, is_vip_receipt=True)
                elif state == "waiting_for_svc_amount":
                    handle_svc_amount_input(chat_id, user_id, msg_text)
                elif state == "waiting_for_svc_link":
                    handle_svc_link_input(chat_id, user_id, msg_text)
                elif state == "waiting_for_svc_receipt":
                    handle_svc_receipt_input(chat_id, user_id, message)
                elif state == "waiting_for_mjoin_link":
                    handle_mjoin_link_input(chat_id, user_id, msg_text)
                elif state == "waiting_for_mjoin_days":
                    handle_mjoin_days_input(chat_id, user_id, msg_text)
                elif state == "waiting_for_mjoin_receipt":
                    handle_mjoin_receipt_input(chat_id, user_id, message)
                elif state == "waiting_for_guess":
                    handle_guess_input(chat_id, user_id, msg_text)
                elif state == "waiting_for_gift_code":
                    handle_gift_code_input(chat_id, user_id, msg_text)
                elif state == "waiting_for_ad_content":
                    handle_ad_content_input(chat_id, user_id, message)
                elif state == "waiting_for_ad_receipt":
                    handle_ad_receipt_input(chat_id, user_id, message)
                elif state == "waiting_for_photo_design_desc":
                    handle_photo_design_desc_input(chat_id, user_id, msg_text)
                elif state == "waiting_for_photo_design_receipt":
                    handle_photo_design_receipt_input(chat_id, user_id, message)
                elif state == "waiting_for_photo_design_upload":
                    handle_photo_design_invalid_upload(chat_id)
                else:
                    fallback_kb = build_reply_main_menu_admin(lang) if is_admin_user(user_id) else build_reply_main_menu(lang)
                    bale_api.send_message(chat_id,
                        t("use_buttons"),
                        reply_markup=fallback_kb)

        elif "callback_query" in update:
            handle_callback(update["callback_query"])

        elif "pre_checkout_query" in update:
            handle_pre_checkout_query(update["pre_checkout_query"])

    except Exception as e:
        print(f"[process_update] {e}")


def main():
    offset = 0
    url = f"https://tapi.bale.ai/bot{BOT_TOKEN}/getUpdates"
    print("Connecting to database...")
    db.init_db()
    print("Bot is running...")
    threading.Thread(target=_background_penalty_checker, daemon=True).start()
    threading.Thread(target=leaderboard_scheduler, daemon=True).start()
    threading.Thread(target=mandatory_join_checker, daemon=True).start()
    threading.Thread(target=order_channel_monitor, daemon=True).start()

    while True:
        try:
            response = session.get(url,
                params={"offset": offset, "timeout": 30, "limit": 100}, timeout=40)
            response.raise_for_status()
            updates = response.json()
            if updates.get("ok") and updates.get("result"):
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    executor.submit(process_update, update)
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.RequestException as e:
            print(f"[network] {e}")
            time.sleep(1)
        except Exception as e:
            print(f"[main] {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
