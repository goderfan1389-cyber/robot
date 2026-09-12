import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# برای چک عضویت و لینک کانال
CHANNEL_USERNAME = "@Arka_Member"  # نام کاربری کانال (با @)
CHANNEL_URL = "https://ble.ir/Arka_Member"  # لینک کانال در بله

# آیدی ادمین
# ادمین اصلی: 1050936429 | ادمین دوم: 94018510
ADMIN_ID = int(os.environ.get("ADMIN_ID", "1050936429"))
OWNER_IDS = [int(x.strip()) for x in os.environ.get("OWNER_IDS", "1050936429,94018510").split(",") if x.strip()]
WALLET_PROVIDER_TOKEN = os.environ.get("WALLET_PROVIDER_TOKEN")

# متن قوانین (۴ زبان)
RULES_MESSAGES = {
"fa": """*«ربات ممبرگیر آرکا | 𝙰𝚛𝚔𝚊 𝙼𝚎𝚖𝚋𝚎𝚛 𝙱𝚘t»*

لطفاً پیش از هرگونه ثبت درخواست یا پرداخت، موارد زیر را با دقت مطالعه فرمایید. ثبت درخواست به منزله پذیرش کامل این قوانین است.

*۱. رعایت ادب و احترام*
رعایت شئونات اخلاقی و احترام در تمامی پیام‌ها الزامی است. در صورت مشاهده هرگونه بی‌احترامی، همکاری فوراً متوقف خواهد شد.

*۲. مسئولیت محتوای ارسالی*
مسئولیت کامل محتوای ارسالی (متن، تصویر، لینک، بنر و …) بر عهده ارسال‌کننده است. در صورت وجود هرگونه تخلف قانونی یا محتوای نامناسب، مسئولیت حقوقی آن متوجه کاربر خواهد بود.

*۳. عدم استرداد وجه*
وجوه پرداخت‌شده تحت هیچ شرایطی قابل عودت نمی‌باشد.

*۴. پرداخت ناقص*
در صورت واریز مبلغ کمتر از تعرفه تعیین‌شده — حتی به میزان ۱ ریال — وجه پرداختی بازگردانده نخواهد شد و کاربر موظف است مابه‌التفاوت را به طور کامل پرداخت نماید.

*۵. ثبت نهایی پس از پرداخت کامل*
ارائه خدمات صرفاً پس از تأیید پرداخت کامل و نهایی انجام خواهد شد.

*۶. حق بررسی و رد درخواست*
مدیریت «ربات ممبرگیر آرکا | 𝙰𝚛𝚔𝚊 𝙼𝚎𝚖𝚋𝚎𝚛 𝙱𝚘t» حق بررسی، تأیید یا رد هرگونه درخواست را بدون الزام به ارائه توضیح محفوظ می‌دارد.

*۷. تغییر قوانین*
در صورت لزوم، قوانین و شرایط ممکن است به‌روزرسانی شوند و نسخه جدید از زمان انتشار لازم‌الاجرا خواهد بود.

*۸. فیش جعلی*
در صورت ارسال هرگونه فیش جعلی، پشتیبانان قادر به انجام اقدام قضایی خواهند بود. شما با پذیرفتن این قوانین این قانون مهم را می‌پذیرید.

*با ثبت درخواست و استفاده از خدمات، شما تأیید می‌کنید که تمامی موارد فوق را مطالعه کرده و می‌پذیرید.*

*با احترام مدیریت ربات پیشرفته《آرکا》*""",

"en": """*«Arka Member Bot | 𝙰𝚛𝚔𝚊 𝙼𝚎𝚖𝚋𝚎𝚛 𝙱𝚘t»*

Please read the following carefully before submitting any request or payment. Submitting a request means you fully accept these rules.

*1. Respect & Courtesy*
Respect and proper conduct are required in all messages. If any disrespect is observed, cooperation will be stopped immediately.

*2. Responsibility for Submitted Content*
Full responsibility for submitted content (text, image, link, banner, etc.) lies with the sender. Any legal violation or inappropriate content is the user's legal responsibility.

*3. No Refunds*
Payments made are non-refundable under any circumstances.

*4. Incomplete Payment*
If the amount paid is less than the set price — even by 1 Rial — the payment will not be refunded, and the user must pay the remaining difference in full.

*5. Final Registration After Full Payment*
Services will only be provided after full and final payment confirmation.

*6. Right to Review and Reject Requests*
The management of «Arka Member Bot | 𝙰𝚛𝚔𝚊 𝙼𝚎𝚖𝚋𝚎𝚛 𝙱𝚘t» reserves the right to review, approve, or reject any request without obligation to provide an explanation.

*7. Changes to Rules*
These rules and terms may be updated when necessary, and the new version will take effect from the time of publication.

*8. Fake Receipts*
If any fake receipt is sent, support staff may take legal action. By accepting these rules, you accept this important condition.

*By submitting a request and using the services, you confirm that you have read and accept all of the above.*

*Sincerely, the management of the advanced《Arka》bot*""",

"fr": """*«Bot Membre Arka | 𝙰𝚛𝚔𝚊 𝙼𝚎𝚖𝚋𝚎𝚛 𝙱𝚘t»*

Veuillez lire attentivement ce qui suit avant de soumettre une demande ou un paiement. Soumettre une demande signifie que vous acceptez pleinement ces règles.

*1. Respect et courtoisie*
Le respect et une bonne conduite sont requis dans tous les messages. En cas d'irrespect constaté, la coopération sera immédiatement interrompue.

*2. Responsabilité du contenu envoyé*
La responsabilité totale du contenu envoyé (texte, image, lien, bannière, etc.) incombe à l'expéditeur. Toute violation légale ou contenu inapproprié engage la responsabilité juridique de l'utilisateur.

*3. Aucun remboursement*
Les paiements effectués ne sont remboursables en aucune circonstance.

*4. Paiement incomplet*
Si le montant payé est inférieur au tarif fixé — même d'1 Rial — le paiement ne sera pas remboursé, et l'utilisateur doit payer intégralement la différence restante.

*5. Enregistrement final après paiement complet*
Les services ne seront fournis qu'après confirmation du paiement complet et final.

*6. Droit d'examen et de rejet des demandes*
La direction du «Bot Membre Arka | 𝙰𝚛𝚔𝚊 𝙼𝚎𝚖𝚋𝚎𝚛 𝙱𝚘t» se réserve le droit d'examiner, d'approuver ou de rejeter toute demande sans obligation de justification.

*7. Modification des règles*
Ces règles et conditions peuvent être mises à jour si nécessaire, et la nouvelle version entrera en vigueur dès sa publication.

*8. Faux reçus*
En cas d'envoi d'un faux reçu, le support pourra engager des poursuites judiciaires. En acceptant ces règles, vous acceptez cette condition importante.

*En soumettant une demande et en utilisant les services, vous confirmez avoir lu et accepté tout ce qui précède.*

*Cordialement, la direction du bot avancé《Arka》*""",

"ar": """*«بوت أركا للأعضاء | 𝙰𝚛𝚔𝚊 𝙼𝚎𝚖𝚋𝚎𝚛 𝙱𝚘t»*

يرجى قراءة ما يلي بعناية قبل تقديم أي طلب أو دفعة. تقديم الطلب يعني قبولك الكامل لهذه القواعد.

*1. الاحترام واللباقة*
الاحترام وحسن السلوك مطلوبان في جميع الرسائل. في حال ملاحظة أي إساءة، سيتم إيقاف التعاون فورًا.

*2. مسؤولية المحتوى المُرسل*
تقع المسؤولية الكاملة عن المحتوى المُرسل (نص، صورة، رابط، بانر، إلخ) على المُرسل. أي مخالفة قانونية أو محتوى غير لائق تقع مسؤوليته القانونية على المستخدم.

*3. عدم استرداد الأموال*
المبالغ المدفوعة غير قابلة للاسترداد تحت أي ظرف.

*4. الدفع الناقص*
إذا كان المبلغ المدفوع أقل من السعر المحدد — حتى ولو بمقدار 1 ريال — فلن يتم استرداد المبلغ المدفوع، ويجب على المستخدم دفع الفرق المتبقي بالكامل.

*5. التسجيل النهائي بعد الدفع الكامل*
لن يتم تقديم الخدمات إلا بعد تأكيد الدفع الكامل والنهائي.

*6. حق المراجعة ورفض الطلبات*
تحتفظ إدارة «بوت أركا للأعضاء | 𝙰𝚛𝚔𝚊 𝙼𝚎𝚖𝚋𝚎𝚛 𝙱𝚘t» بحق مراجعة أو قبول أو رفض أي طلب دون التزام بتقديم تفسير.

*7. تغيير القواعد*
قد يتم تحديث هذه القواعد والشروط عند الحاجة، وستكون النسخة الجديدة سارية المفعول من وقت نشرها.

*8. الإيصالات المزورة*
في حال إرسال أي إيصال مزور، يحق لفريق الدعم اتخاذ إجراء قانوني. بقبولك لهذه القواعد، فإنك تقبل هذا الشرط المهم.

*بتقديم الطلب واستخدام الخدمات، فإنك تؤكد أنك قرأت ووافقت على جميع ما سبق.*

*مع الاحترام، إدارة بوت《آركا》المتطور*""",
}

RULES_MESSAGE = RULES_MESSAGES["fa"]

# پیام وقتی کاربر هنوز عضو کانال نشده
JOIN_CHANNEL_PROMPT_MESSAGE = """*کاربر گرامی⚠️*

عضو خانواده آرکا شو!✔️

بعدش رو *عضو شدم✔️* بزن!🖐"""

# پیام وقتی عضویت تایید نشد
NOT_IN_CHANNEL_ALERT_MESSAGE = """*کاربر گرامی⚠️*

عضویت شما تأیید نشد!✖️

لطفا ابتدا عضویت خود را بررسی نمایید و سپس بر روی دکمه *عضو شدم✔️* کلیک نمایید!

@Arka_Member"""

# پیام وقتی عضویت تایید شد
SUCCESSFUL_VERIFICATION_MESSAGE = """*کاربر گرامی⚠️*

به خانواده آرکا خوش آمدید!✔️

از منوی زیر استفاده کنید!🖐"""

# متن دکمه‌ها
RULES_ACCEPT_BUTTON_TEXT = "قوانین را تأیید می‌کنم!✔️"
JOIN_CHANNEL_BUTTON_TEXT = "عضو آرکا شو!⚠️"
MEMBERSHIP_CHECK_BUTTON_TEXT = "عضو شدم✔️"

# متن‌های جدید برای قابلیت دریافت سکه
EARN_COINS_MESSAGE = """*کاربر گرامی⚠️*

جهت عضویت و کسب سکه وارد کانال 《ممبرگیر آرکا | 𝙰𝚛𝚔𝚊 𝙼𝚎𝚖𝚋𝚎𝚛 》شوید و در کانال های ثبت شده عضو شوید!✔️

از طریق لینک زیر اقدام نمایید!🖐

@Arka_Member"""

EARN_COINS_BUTTON_TEXT = "به《ممبرگیر آرکا | 𝙰𝚛𝚔𝚊 𝙼𝚎𝚖𝚋𝚎𝚁 》برو✔️"

# ================== NEW FEATURES ==================

# دکمه‌های منوی اصلی
MAIN_BUTTON_TEXT = "📢 عضویت و دریافت سکه"
ORDER_MEMBER_BUTTON_TEXT = "➕ ثبت سفارش ممبر"
PRICING_BUTTON_TEXT = "⚠️ تعرفه سفارش"
BACK_BUTTON_TEXT = "🔙 بازگشت"

# پیام ثبت سفارش ممبر
ORDER_MEMBER_MESSAGE = """*کاربر گرامی⚠️*

جهت ثبت سفارش آیدی کانال خود را ارسال نمایید!✔️

مثال : @Arka_Member

📌کانال شما باید عمومی باشد و ربات نیز در آن ادمین باشد!"""

# پیام تعرفه سفارش
PRICING_MESSAGE = """*کاربر گرامی⚠️*

تعرفه سفارش به شرح زیر است!✔️

📌10 سکه : 5 عضو

📌20 سکه : 10 عضو

📌30 سکه : 15 عضو

📌40 سکه : 20 عضو

📌50 سکه : 25 عضو

📌60 سکه : 30 عضو

📌هر 1 عضو = 2 سکه

@Arka_Member"""

# پیام ادمین نبودن ربات
NOT_ADMIN_MESSAGE = """*⚠️کاربر گرامی⚠️*

ابتدا ربات را در کانال مورد نظر ادمین کنید!✔️

سپس دوباره امتحان کنید!🖐"""

# پیام درخواست تعداد ممبر
REQUEST_MEMBER_COUNT_MESSAGE = """*کاربر گرامی⚠️*

تعداد ممبر مورد نیاز خود را ثبت نمایید!✔️

با توجه به سکه های خود سفارش دهید!🖐"""

# پیام کمبود سکه
INSUFFICIENT_COINS_MESSAGE_TEMPLATE = """*کاربر گرامی⚠️*

جهت ثبت این سفارش شما نیاز به {needed} سکه دارید!✔️

دارایی شما {balance} سکه است!🖐"""

INSUFFICIENT_COINS_TRANSFER_MESSAGE_TEMPLATE = """*کاربر گرامی⚠️*

جهت انتقال این مبلغ شما نیاز به {needed} سکه دارید!✔️

دارایی شما {balance} سکه است!🖐"""



# پیام سفارش در کانال
ORDER_CHANNEL_MESSAGE_TEMPLATE = """*⚠️سفارش شماره #{order_id}*

*📌لینک کانال کاربر :*

*{channel_link}*"""

# متن دکمه‌های پیام سفارش در کانال
JOIN_CHANNEL_ORDER_BUTTON_TEXT = "⚠️عضو کانال شو"
JOINED_CHANNEL_ORDER_BUTTON_TEXT = "عضو کانال شدم✔️"
ENTER_BOT_BUTTON_TEXT = "📌ورود به ربات"
REPORT_CHANNEL_BUTTON_TEXT = "🚫گزارش کانال"

# پیام ثبت گزارش
REPORT_REGISTERED_MESSAGE = "گزارش شما ثبت گردید✔️"

# پیام گزارش برای ادمین
ADMIN_REPORT_MESSAGE_TEMPLATE = """*ادمین گرامی⚠️*

یک کاربر این کانال را گزارش کرده است!📌

{channel_id}"""

# متن دکمه‌های ادمین
CONFIRM_REPORT_BUTTON_TEXT = "تأیید گزارش✔️"
REJECT_REPORT_BUTTON_TEXT = "رد گزارش✖️"

# پیام تأیید گزارش برای ادمین
ADMIN_CONFIRM_REPORT_MESSAGE = "شما گزارش را تأیید کردید!✔️"

# پیام رد گزارش برای ادمین
ADMIN_REJECT_REPORT_MESSAGE = "شما گزارش را رد کردید!✔️"

# پیام لغو سفارش برای کاربر
ORDER_CANCELLED_MESSAGE = """*کاربر گرامی⚠️*

سفارش شما به دلیل گزارش کاربران لغو شد و سکه باقی مانده سفارش شما به حسابتان بازگشت!📌

جهت اعتراض به این گزارش به پشتیبانی مراجعه نمایید!🖐"""

# آیدی ربات
BOT_USERNAME = "@Arka_Member_Bot"
BOT_URL = "https://ble.ir/Arka_Member_Bot"

# ================== GIFT FEATURE ==================
GIFT_BUTTON_TEXT = "🎁 دریافت هدیه"
INVITE_FRIENDS_BUTTON_TEXT = "🎖دعوت دوستان"
DAILY_GIFT_BUTTON_TEXT = "🎁 هدیه روزانه"
LUCKY_WHEEL_BUTTON_TEXT = "🎡 گردونه شانس"
GIFT_CODE_BUTTON_TEXT = "📨 ثبت کد هدیه"
SIGNUP_GIFT_BUTTON_TEXT = "🎄ثبت نام و کسب هدیه"

MILLIGOLD_SIGNUP_BUTTON_TEXT = "🎖50 سکه رایگان با ثبت نام در میلی‌گلد"
BLUBANK_SIGNUP_BUTTON_TEXT = "🎖30 سکه رایگان با ثبت نام در بلو بانک"
MELLIGOLD_SIGNUP_BUTTON_TEXT = "🎖20 سکه رایگان با ثبت نام در ملی‌گلد"

MILLIGOLD_SIGNUP_URL = "https://milli.gold/?utm_source=milliapp&utm_medium=refferal#benefits-list"
BLUBANK_SIGNUP_URL = "https://blubank.sb24.ir/download"
MELLIGOLD_SIGNUP_URL = "https://melligold.com/application"

# ================== NEW MESSAGES ==================
COIN_ADDED_MESSAGE = "1 سکه به اکانت شما اضافه شد!✔️"
ALREADY_JOINED_MESSAGE = "شما قبلا عضو این کانال شده اید!✖️"
LEFT_EARLY_PENALTY_MESSAGE = """*کاربر گرامی⚠️*

شما از کانالی که برای عضویت در آن سکه دریافت کرده‌اید خارج شده‌اید!📌

به دلیل خروج ۲ سکه از حساب شما کسر شد!✖️

لطفاً به قوانین ربات احترام بگذارید.🖐"""

# ================== MAGAZINE FEATURE ==================

MAGAZINE_BUTTON_TEXT = "💟 مجله-لایک-سین"
MAGAZINE_PRICING_BUTTON_TEXT = "⚠️تعرفه ثبت مجله"
ORDER_MAGAZINE_BUTTON_TEXT = "📚 سفارش مجله"

REACTION_BUTTON_TEXT = "❤ سفارش ری اکشن"
REACTION_PRICING_BUTTON_TEXT = "⚠️تعرفه ثبت ری اکشن"
ORDER_REACTION_BUTTON_TEXT = "❤ سفارش ری اکشن"

# بسته‌های ری اکشن: (تعداد، سکه)
REACTION_OPTIONS = [
    (25,  35.0),
    (50,  70.0),
    (75,  105.0),
    (100, 140.0),
]

REACTION_PRICING_MESSAGE = """*کاربر گرامی⚠️*

❤️ ثبت 25 ری اکشن =🎖35 سکه

❤️ ثبت 50 ری اکشن = 🎖 70 سکه

❤️ ثبت 75 ری اکشن = 🎖 105 سکه

❤️ ثبت 100 ری اکشن = 🎖 140 سکه

@Arka_Member"""

REACTION_CANCEL_MESSAGE = """*کاربر گرامی⚠️*

به منوی اصلی بازگشتید!✔️

از منوی زیر استفاده نمایید!📌"""

REACTION_CHANNEL_MESSAGE_TEMPLATE = """❤ سفارش ری اکشن

لینک پیام جهت ثبت ری اکشن در پایین قرار داده شده است✔️

{post_link}"""

REACTION_COIN_ADDED_MESSAGE = "0.5 سکه به اکانت شما اضافه شد!✔️"
REACTION_VIP_COIN_ADDED_MESSAGE = "🎖کاربر《VIP》1.5 سکه به حساب شما اضافه شد!"

MAGAZINE_MENU_MESSAGE = """*کاربر گرامی⚠️*

گزینه مورد نظر خود را انتخاب نمایید!✔️

از منوی زیر استفاده کنید!📌"""

MAGAZINE_ORDER_PROMPT_MESSAGE = """*کاربر گرامی⚠️*

لینک پیام خود را جهت سفارش مجله ارسال نمایید!✔️

لینک پیام باید متعلق به کانال باشد!📌"""

MAGAZINE_INVALID_LINK_MESSAGE = """*کاربر گرامی⚠️*

لینک پیام شما نامعتبر است!✖️

لطفا لینک معتبر ارسال نمایید!📌"""

MAGAZINE_CONFIRM_MESSAGE = """*کاربر گرامی⚠️*

در صورت تایید سفارش مجله بر روی دکمه تایید✔️ کلیک نمایید و در غیر این صورت، بر روی دکمه لغو✖️ کلیک نمایید!

جهت آگاهی از تعرفه ثبت مجله بر روی دکمه ⚠️تعرفه ثبت مجله کلیک نمایید!📌"""

MAGAZINE_CANCEL_MESSAGE = """*کاربر گرامی⚠️*

به منوی اصلی بازگشتید!✔️

از منوی زیر استفاده نمایید!📌"""

MAGAZINE_PRICING_MESSAGE = """*کاربر گرامی⚠️*

📚 ثبت 5 مجله =🎖25 سکه

@Arka_Member"""

MAGAZINE_CHANNEL_MESSAGE_TEMPLATE = """📚 سفارش مجله

لینک پیام جهت ثبت پیام به عنوان مجله در پایین قرار داده شده است✔️

{post_link}"""

MAGAZINE_NOT_REGISTERED_MESSAGE = "ابتدا پیام را به عنوان مجله ثبت نمایید!✖️"

MAGAZINE_COIN_ADDED_MESSAGE = "2 سکه به اکانت شما اضافه شد!✔️"
MAGAZINE_VIP_COIN_ADDED_MESSAGE = "🎖کاربر《VIP》3 سکه به حساب شما اضافه شد!"

MAGAZINE_LEFT_EARLY_PENALTY_MESSAGE = """*کاربر گرامی⚠️*

شما پیامی که برای مجله ثبت کرده بودید را حذف یا تغییر داده‌اید!📌

به دلیل این اقدام ۲ سکه از حساب شما کسر شد!✖️

لطفاً به قوانین ربات احترام بگذارید.🖐"""

MAGAZINE_ADMIN_REPORT_TEMPLATE = """*ادمین گرامی⚠️*

یک کاربر این مجله را گزارش کرده است!📌

لینک مجله: {post_link}"""
# ═══════════ SIN (سین) ═══════════
ORDER_SIN_BUTTON_TEXT = "👁‍🗨 سفارش سین"
SIN_PRICING_BUTTON_TEXT = "⚠️تعرفه ثبت سین"

SIN_OPTIONS = [
    (50,  25.0),
    (100, 50.0),
    (150, 75.0),
    (200, 100.0),
]

SIN_PRICING_MESSAGE = """*کاربر گرامی⚠️*

تعرفه ثبت سفارش سین به شرح زیر است!✔️

👁‍🗨 50 سین = 🎖25 سکه

👁‍🗨 100 سین = 🎖 50 سکه

👁‍🗨 150 سین = 🎖 75 سکه

👁‍🗨 200 سین = 🎖 100 سکه

@Arka_Member"""

SIN_COIN_ADDED_MESSAGE = "0.5 سکه به اکانت شما اضافه شد!✔️"
SIN_VIP_COIN_ADDED_MESSAGE = "🎖کاربر《VIP》1 سکه به حساب شما اضافه شد!"
SIN_NOT_VIEWED_MESSAGE = "*کاربر گرامی⚠️*\n\nشما هنوز پیام را سین نزده‌اید!✖️\n\nابتدا روی دکمه ⚠️سین بزن کلیک کنید!"
# ═══════════════════════════════════════════════════════
# این بخش رو به انتهای config.py اضافه کن
# ═══════════════════════════════════════════════════════

# ================== LEADERBOARD FEATURE ==================

LEADERBOARD_BUTTON_TEXT = "🏆 برترین کاربران"

# دکمه‌های داخلی لیدربورد
BEST_MEMBER_BUTTON_TEXT     = "🎁 برترین عضویت 🎁"
BEST_MEMBER_PRIZE_BTN       = "⚠️ هدیه عضویت ⚠️"
BEST_REFERRAL_BUTTON_TEXT   = "🎁 برترین زیرمجموعه 🎁"
BEST_REFERRAL_PRIZE_BTN     = "⚠️ هدیه زیرمجموعه ⚠️"
BEST_PURCHASE_BUTTON_TEXT   = "🎁 برترین خرید 🎁"
BEST_PURCHASE_PRIZE_BTN     = "⚠️ هدیه خرید ⚠️"
LEADERBOARD_BACK_BTN        = "🔙 بازگشت به منو"

# جوایز (سکه)
LEADERBOARD_PRIZE_1ST = 100
LEADERBOARD_PRIZE_2ND = 50
LEADERBOARD_PRIZE_3RD = 25

# پیام‌های میزان هدیه
MEMBER_PRIZE_MESSAGE = """🏆 *میزان هدیه | برترین عضویت*

🥇 نفر اول  ←  100 سکه

🥈 نفر دوم  ←   50 سکه

🥉 نفر سوم  ←   25 سکه

📌 *شرط دریافت جایزه:*

کاربرانی که عضو کانالی نشده باشند، جایزه‌ای دریافت نخواهند کرد.

⏰ جوایز هر *جمعه ساعت 12 شب* واریز می‌شوند.

🎖پس از واریز، آمار هفتگی ریست و دور جدید آغاز می‌شود.

@Arka_Member"""

REFERRAL_PRIZE_MESSAGE = """🏆 *میزان هدیه | برترین زیرمجموعه‌گیری*

🥇 نفر اول  ←  100 سکه

🥈 نفر دوم  ←   50 سکه

🥉 نفر سوم  ←   25 سکه

📌 *شرط دریافت جایزه:*

کاربرانی که هیچ زیرمجموعه‌ای معرفی نکرده باشند، جایزه‌ای دریافت نمی‌کنند.

⏰ جوایز هر *جمعه ساعت 12 شب* واریز می‌شوند.

🎖پس از واریز، آمار هفتگی ریست و دور جدید آغاز می‌شود.

@Arka_Member"""

PURCHASE_PRIZE_MESSAGE = """🏆 *میزان هدیه | برترین خرید*

🥇 نفر اول  ←  100 سکه

🥈 نفر دوم  ←   50 سکه

🥉 نفر سوم  ←   25 سکه

📌 *شرط دریافت جایزه:*

کاربرانی که هیچ خریدی در هفته جاری نداشته باشند، جایزه‌ای دریافت نمی‌کنند.
خرید شامل: اشتراک VIP و خرید سکه می‌شود.

⏰ جوایز هر *جمعه ساعت 12 شب* واریز می‌شوند.

پس از واریز، آمار هفتگی ریست و دور جدید آغاز می‌شود.

@Arka_Member"""

# پیام اعلان جایزه به برندگان
PRIZE_WIN_MESSAGE_TEMPLATE = """🎉 *تبریک! شما برنده شدید!*

╔══════════════════════╗
║  🏆 {category}  ║
╚══════════════════════╝

🥇 رتبه شما: *{rank}*
🎁 جایزه دریافتی: *{prize} سکه*
📊 امتیاز شما: *{score}*

سکه‌های جایزه به حساب شما واریز شد! ✔️

آمار هفته جدید از همین لحظه آغاز شده است. 🚀
موفق باشید! 💪

@Arka_Member"""

LEADERBOARD_MENU_MESSAGE = """📌 *برترین کاربران هفتگی*

🎖جوایز هر جمعه ساعت 12 شب

🎁گزینه مورد نظر خود را انتخاب کنید!"""

# ================== GAMES FEATURE ==================
GAMES_BUTTON_TEXT         = "🧩 سرگرمی‌ها"
RPS_BUTTON_TEXT           = "سنگ کاغذ قیچی ✂️"
PENALTY_BUTTON_TEXT       = "پنالتی بزن ⚽️"
GUESS_BUTTON_TEXT         = "حدس عدد 🎮"

# ================== AD POSTING FEATURE ==================
AD_BUTTON_TEXT = "📢 ثبت آگهی"

# کانال هدف برای انتشار آگهی‌ها
AD_CHANNEL_USERNAME = CHANNEL_USERNAME  # کانال اصلی آرکا (نه کانال اطلاع‌رسانی)

# کانال‌های اجباری
REQUIRED_CHANNELS = [
    {"username": "@Arka_Member",     "chat_id": 5551572936,  "url": "https://ble.ir/Arka_Member",     "label": "ممبرگیر آرکا | 𝙰𝚛𝚔𝚊 𝙼𝚎𝚖𝚋𝚎𝚛"},
    {"username": "@Arka_Updates",    "chat_id": None,        "url": "https://ble.ir/Arka_Updates",    "label": "اطلاع‌رسانی آرکا | 𝙰𝚛𝚔𝚊 𝚄𝚙𝚍𝚊𝚝𝚎𝚜"},
    {"username": "@Computer_Program","chat_id": None,        "url": "https://ble.ir/Computer_Program","label": "کدنویسی آرکا | 𝙰𝚛𝚔𝚊 𝙲𝚘𝚍𝚒𝚗𝚐"},
]

AD_PRICING_MESSAGE = """*کاربر گرامی⚠️*

📌تعرفه ثبت آگهی به شرح زیر است!

🎖1 روز 🟰 50,000 تومان

🎖7 روز 🟰 350,000 تومان

🎖31 روز 🟰 1,550,000 تومان

📚 آگهی شما پس از پایان مهلت از کانال حذف خواهد شد!

⏳️تنها برای یک بار آگهی شما در کانال ارسال می شود! منظور از تعداد روز، میزان باقی ماندن آگهی شما در کانال است!

@Arka_Member"""

AD_PACKAGES = [
    {"days": 1,  "price_str": "50,000",    "label": "🎖1 روز"},
    {"days": 7,  "price_str": "350,000",   "label": "🎖7 روز"},
    {"days": 31, "price_str": "1,550,000", "label": "🎖31 روز"},
]

AD_DISCLAIMER_TEXT = "*این پیام تبلیغات است⚠️*"
