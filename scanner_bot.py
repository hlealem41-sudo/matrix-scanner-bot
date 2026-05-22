import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiTelegramException
import socket
import requests
import time
import re
import os
from threading import Thread
from http.server import SimpleHTTPRequestHandler, HTTPServer

# --- 🛰️ CHOREO SERVICE PASSTHROUGH passive SCANNING MAINBOARD v16.0 ---
BOT_TOKEN = "8356994434:AAHsz9bKclh5GbSDZFdzOzdMgrBB3eCGJQ0"
CHANNEL_USERNAME = "@SIGNAL_HUNTER_X"
DEVELOPER_NAME = "Ｍʀ 𓆩✘𓆪 ♱"
DEVELOPER_USERNAME = "@MrX_OfficiaI"

bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}
user_payload_methods = {}

# --- 🌐 CHOREO HEALTH CHECK FAKE SERVER ENGINE ---
def run_choreo_fake_server():
    # Choreo የሚሰጠውን ፖርት ያነባል፣ ከሌለ በነባሪ 8080 ይጠቀማል
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    print(f"📡 [CHOREO SYSTEM] Fake Health Server live on port {port}")
    server.serve_forever()

def sanitize_and_fix_domain(domain_text):
    clean_domain = domain_text.lower().strip()
    clean_domain = re.sub(r'^(https?://)?(www\.)?', '', clean_domain)
    
    if 'ethiotelecoem' in clean_domain or 'ethiotelecom' in clean_domain or 'ethio-telecom' in clean_domain:
        return "ethiotelecom.et"
    if 'telecom.et' in clean_domain and not clean_domain.startswith('ethio'):
        return "ethiotelecom.et"
        
    parts = clean_domain.split('.')
    if len(parts) > 2:
        if parts[-1] == 'et' and parts[-2] in ['com', 'gov', 'edu', 'org', 'net']:
            return ".".join(parts[-3:])
        return ".".join(parts[-2:])
        
    return clean_domain

def is_cloudflare(ip_addr):
    cf_prefixes = (
        "103.21.244.", "103.22.200.", "103.31.4.", "104.16.", "104.17.", "104.18.", 
        "104.19.", "104.20.", "104.21.", "104.22.", "104.23.", "104.24.", "104.25.", 
        "104.26.", "104.27.", "108.162.192.", "131.0.72.", "141.101.64.", "162.158.", 
        "172.64.", "172.65.", "172.66.", "172.67.", "172.68.", "172.69.", "172.70.", 
        "172.71.", "173.245.48.", "188.114.96.", "190.93.240.", "197.234.240.", "198.41.128."
    )
    return any(ip_addr.startswith(prefix) for prefix in cf_prefixes)

def is_user_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'administrator', 'creator']
    except ApiTelegramException: return False
    except Exception: return False

def send_force_join_msg(chat_id):
    markup = InlineKeyboardMarkup()
    btn_join = InlineKeyboardButton(text="📢 ⛓️ JOIN PRIVATE NETWORK ⛓️ 📢", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")
    btn_verified = InlineKeyboardButton(text="🔄 🔐 VERIFY SYSTEM ACCESS 🔐 🔄", callback_data="check_sub")
    markup.add(btn_join)
    markup.add(btn_verified)
    
    msg_text = (
        "⚡ <b>[ ACCESS DENIED ]</b> ⚡\n\n"
        "<code>🎚️ Secure handshake required. You must be an active member of our core network to unlock this terminal.</code>\n\n"
        f"🛰️ <b>Terminal Link:</b> {CHANNEL_USERNAME}\n"
        "📡 <i>Join and trigger the network bypass verification below.</i>"
    )
    bot.send_message(chat_id, msg_text, reply_markup=markup, parse_mode="HTML")

def get_main_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton("🌐 HOST TO IP")
    btn2 = KeyboardButton("🌀 PAYLOAD GENERATOR")
    btn3 = KeyboardButton("🔌 PORT SCANNER")
    btn4 = KeyboardButton("🛡️ PAYLOAD HEADERS")
    btn5 = KeyboardButton("🔍 SUBDOMAIN CHECK")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup

def get_payload_methods_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton("📐 CONNECT Method")
    btn2 = KeyboardButton("📐 GET Method")
    btn3 = KeyboardButton("📐 HEAD Method")
    btn4 = KeyboardButton("📐 POST Method")
    btn5 = KeyboardButton("📐 ALL Methods")
    btn6 = KeyboardButton("🔙 BACK TO MAIN MENU")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

def trigger_progress_bar(chat_id, message_id, target, mode_name):
    progress_stages = [
        ("📡 [🌍 25%] Injecting protocol layers...", "█░░░░░░░░░"),
        (f"🛰️ [📡 65%] Formatting HTTP {mode_name} payload...", "██████░░░░"),
        ("⚡ [⚙️ 100%] Compiling custom matrix configuration!", "██████████")
    ]
    for status_text, bar in progress_stages:
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"⏳ <b>BUILDING FOR:</b> <code>{target}</code>\n\n<code>{bar}</code>\n{status_text}",
                parse_mode="HTML"
            )
            time.sleep(0.4)
        except Exception: pass

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if not is_user_subscribed(message.from_user.id):
        send_force_join_msg(message.chat.id)
        return
    welcome_text = (
        "🌪️ <b>CORE INFRASTRUCTURE MATRIX SCANNER v16.0</b> 🌪️\n\n"
        "🛸 <i>The advanced Choreo-optimized passive terminal is active. Select an option from the menu.</i>\n\n"
        f"🛡️ <b>Main Architect:</b> <code>{DEVELOPER_NAME}</code>\n"
        f"🌌 <b>Network Operations:</b> {DEVELOPER_USERNAME}"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_verify_subscription(call):
    if is_user_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Access Granted! Terminal unlocked.", show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        welcome_text = (
            "🌪️ <b>ACCESS UNLOCKED</b> 🌪️\n\n"
            "🛸 <i>Handshake verified successfully. Welcome back to the core mainframe.</i>"
        )
        bot.send_message(call.message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode="HTML")
    else:
        bot.answer_callback_query(call.id, "❌ Verification Failed! You haven't joined the channel yet.", show_alert=True)

@bot.message_handler(func=lambda message: True)
def handle_text_inputs(message):
    if not is_user_subscribed(message.from_user.id):
        send_force_join_msg(message.chat.id)
        return

    chat_id = message.chat.id
    raw_text = message.text.strip()

    if raw_text == "🌐 HOST TO IP":
        user_states[chat_id] = "host2ip"
        bot.send_message(chat_id, "🎯 <b>[ MODE: HOST TO IP ]</b>\n\nSend the target domain name to resolve its IP address:", parse_mode="HTML")
        return
    elif raw_text == "🌀 PAYLOAD GENERATOR":
        bot.send_message(chat_id, "⚙️ <b>[ PAYLOAD CONFIGURATION LAYER ]</b>\n\nSelect your desired HTTP Method or choose ALL from the sub-menu below:", reply_markup=get_payload_methods_menu(), parse_mode="HTML")
        return
    elif raw_text == "🔌 PORT SCANNER":
        user_states[chat_id] = "port"
        bot.send_message(chat_id, "🎯 <b>[ MODE: PORT SCANNER ]</b>\n\nSend host name to map active web ports and banners:", parse_mode="HTML")
        return
    elif raw_text == "🛡️ PAYLOAD HEADERS":
        user_states[chat_id] = "payload"
        bot.send_message(chat_id, "🎯 <b>[ MODE: SECURITY PAYLOAD HEADERS ]</b>\n\nSend target domain to audit defense configs:", parse_mode="HTML")
        return
    elif raw_text == "🔍 SUBDOMAIN CHECK":
        user_states[chat_id] = "subdomain"
        bot.send_message(chat_id, "🎯 <b>[ MODE: PASSIVE INTELLIGENCE GATHERING ]</b>\n\nSend any root domain (e.g., <code>example.com</code>) to scan:", parse_mode="HTML")
        return
    elif raw_text == "🔙 BACK TO MAIN MENU":
        bot.send_message(chat_id, "🔙 Returning to main control panel.", reply_markup=get_main_menu(), parse_mode="HTML")
        return

    if raw_text in ["📐 CONNECT Method", "📐 GET Method", "📐 HEAD Method", "📐 POST Method", "📐 ALL Methods"]:
        method_type = raw_text.split(" ")[1]
        user_states[chat_id] = "generate_payload_final"
        user_payload_methods[chat_id] = method_type
        bot.send_message(chat_id, f"✅ <b>Method locked:</b> <code>{method_type}</code>\n\nNow, send your SNI/Host name to execute generation:", parse_mode="HTML")
        return

    current_state = user_states.get(chat_id, "host2ip")
    target_domain = sanitize_and_fix_domain(raw_text)

    status_msg = bot.reply_to(message, f"📡 <b>Target Cleansed:</b> <code>{target_domain}</code>\n<i>Initializing matrix handshake...</i>", parse_mode="HTML")

    if current_state == "host2ip":
        try:
            resolved_ip = socket.gethostbyname(target_domain)
            cf_status = " ☁️ [CLOUDFLARE]" if is_cloudflare(resolved_ip) else ""
            result = f"🌐 <b>[ HOST TO IP RESOLUTION ]</b>\n\n🔹 Target Host: <code>{target_domain}</code>\n🔹 Resolved IP Address:\n<pre>{resolved_ip}</pre><b>{cf_status}</b>"
        except Exception:
            result = f"🌐 <b>[ HOST TO IP RESOLUTION ]</b>\n\n❌ Failed to resolve host context."
        bot.delete_message(chat_id, status_msg.message_id)
        bot.send_message(chat_id, result, reply_markup=get_main_menu(), parse_mode="HTML")
        return

    elif current_state == "generate_payload_final":
        selected_method = user_payload_methods.get(chat_id, "CONNECT")
        trigger_progress_bar(chat_id, status_msg.message_id, target_domain, selected_method)
        
        try:
            resolved_ip = socket.gethostbyname(target_domain)
            cf_status = " ☁️ (Cloudflare Protected)" if is_cloudflare(resolved_ip) else ""
            ip_line = f"📍 Resolved Host IP: <code>{resolved_ip}</code>{cf_status}\n"
        except Exception: ip_line = ""

        p_connect = f"CONNECT [host_port] [protocol][crlf]Host: {target_domain}[crlf]X-Online-Host: {target_domain}[crlf][crlf]"
        p_get = f"GET http://{target_domain}/ HTTP/1.1[crlf]Host: {target_domain}[crlf]X-Online-Host: {target_domain}[crlf]Connection: Keep-Alive[crlf][crlf]"
        p_head = f"HEAD http://{target_domain}/ HTTP/1.1[crlf]Host: {target_domain}[crlf]X-Online-Host: {target_domain}[crlf][crlf]"
        p_post = f"POST http://{target_domain}/ HTTP/1.1[crlf]Host: {target_domain}[crlf]X-Online-Host: {target_domain}[crlf]Content-Length: 9999[crlf][crlf]"

        output = f"🌀 <b>[ INJECTION ENGINE MATRIX ]</b>\n\n"
        output += f"🎯 Target: <code>{target_domain}</code>\n{ip_line}"
        output += f"📐 Selected Mode: <code>{selected_method}</code>\n\n"

        if selected_method == "ALL":
            output += "📦 <b>ALL GENERATED PAYLOAD STRINGS:</b>\n"
            output += f"🔹 <i>CONNECT:</i>\n<pre>{p_connect}</pre>\n"
            output += f"🔹 <i>GET:</i>\n<pre>{p_get}</pre>\n"
            output += f"🔹 <i>HEAD:</i>\n<pre>{p_head}</pre>\n"
            output += f"🔹 <i>POST:</i>\n<pre>{p_post}</pre>\n"
        else:
            output += "📦 <b>GENERATED PAYLOAD STRINGS:</b>\n"
            if selected_method == "CONNECT": output += f"<pre>{p_connect}</pre>"
            elif selected_method == "GET": output += f"<pre>{p_get}</pre>"
            elif selected_method == "HEAD": output += f"<pre>{p_head}</pre>"
            elif selected_method == "POST": output += f"<pre>{p_post}</pre>"

        output += "\n====================================\n"
        output += f"📡 Operator: <code>{DEVELOPER_NAME}</code>"

        bot.delete_message(chat_id, status_msg.message_id)
        bot.send_message(chat_id, output, reply_markup=get_main_menu(), parse_mode="HTML")
        user_states[chat_id] = "host2ip"
        return

    elif current_state == "port":
        try:
            resolved_ip = socket.gethostbyname(target_domain)
            ports_config = {22: ("SSH", "TCP"), 80: ("HTTP", "TCP"), 443: ("HTTPS", "TLS/SSL"), 8080: ("PROXY", "TCP")}
            
            port_box = ""
            for port, info in ports_config.items():
                svc_name, method_type = info
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.2)
                
                if sock.connect_ex((resolved_ip, port)) == 0:
                    port_box += f" ├─ 🟢 Port {port} [{svc_name} ({method_type})]: OPEN\n"
                    if port in [80, 443, 8080]:
                        try:
                            protocol = "https" if port == 443 else "http"
                            res = requests.get(f"{protocol}://{target_domain}:{port}", timeout=2.5, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=False)
                            server_banner = res.headers.get('Server', 'Unknown Engine')
                            port_box += f" │   └── 📝 Response: {res.status_code} ({server_banner})\n"
                        except requests.exceptions.Timeout:
                            port_box += f" │   └── 📝 Response: Timeout\n"
                        except Exception:
                            port_box += f" │   └── 📝 Response: Handshake Failed\n"
                else:
                    port_box += f" ├─ 🔴 Port {port} [{svc_name} ({method_type})]: CLOSED\n"
                sock.close()
                
            output = f"🔌 <b>[ PORT CHECKER REPORT ]</b>\n\n🎯 Target: <code>{target_domain}</code>\n📍 IP: <code>{resolved_ip}</code>\n\n<pre>{port_box}</pre>"
        except Exception:
            output = "<pre>❌ Port scanning failed. Target host unreachable.</pre>"
            
        bot.delete_message(chat_id, status_msg.message_id)
        bot.send_message(chat_id, output, reply_markup=get_main_menu(), parse_mode="HTML")
        return

    elif current_state == "payload":
        try:
            res = requests.get(f"http://{target_domain}", timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            xss = res.headers.get('X-XSS-Protection', 'MISSING')
            frame = res.headers.get('X-Frame-Options', 'MISSING')
            output = f"🛡️ <b>[ SECURITY HEADERS AUDIT ]</b>\n\n🔹 XSS Protection:\n<pre>{xss}</pre>\n🔹 Frame Options:\n<pre>{frame}</pre>"
        except Exception: output = "<pre>❌ Failed to grab headers.</pre>"
        bot.delete_message(chat_id, status_msg.message_id)
        bot.send_message(chat_id, output, reply_markup=get_main_menu(), parse_mode="HTML")
        return

    elif current_state == "subdomain":
        subdomains = set()
        try:
            crt_url = f"https://crt.sh/?q=%.{target_domain}&output=json"
            response = requests.get(crt_url, timeout=15)
            if response.status_code == 200:
                json_data = response.json()
                for item in json_data:
                    name_value = item['name_value']
                    for sub in name_value.split('\n'):
                        sub = sub.strip().lower()
                        if sub and not sub.startswith('*.'): subdomains.add(sub)
        except Exception: pass

        try:
            ht_url = f"https://api.hackertarget.com/hostsearch/?q={target_domain}"
            response = requests.get(ht_url, timeout=10)
            if response.status_code == 200 and "error" not in response.text:
                for line in response.text.split('\n'):
                    if ',' in line:
                        sub = line.split(',')[0].strip().lower()
                        if sub: subdomains.add(sub)
        except Exception: pass

        active_block = ""
        inactive_block = ""
        online_count = 0
        offline_count = 0
        
        if len(subdomains) > 0:
            bot.edit_message_text(chat_id=chat_id, message_id=status_msg.message_id, text=f"⏳ <b>LOGS FOUND: {len(subdomains)} hosts mapped!</b>\n\n<code>██████████</code>\n📡 Processing clean copyable structure...", parse_mode="HTML")

        for sub in sorted(subdomains):
            try:
                sub_ip = socket.gethostbyname(sub)
                if is_cloudflare(sub_ip): active_block += f"☁️ {sub} -> {sub_ip} [CF]\n"
                else: active_block += f"🟢 {sub} -> {sub_ip}\n"
                online_count += 1
            except Exception:
                inactive_block += f"{sub}\n"
                offline_count += 1

        output = f"🔍 <b>[ PASSIVE MATRIX INTERFACE ]</b>\n🎯 Resolved Root: <code>{target_domain}</code>\n📊 Metrics: <b>{len(subdomains)} Checked</b>\n━━━━━━━━━━━━━━━━━━━━\n\n🟢 <b>ACTIVE NODES ({online_count}):</b>\n"
        if active_block: output += f"<pre>{active_block}</pre>"
        else: output += "<code>None detected.</code>\n"
        output += f"\n🔴 <b>INACTIVE NODES ({offline_count}):</b>\n"
        if inactive_block: output += f"<pre>{inactive_block}</pre>"
        else: output += "<code>None detected.</code>\n"
            
        bot.delete_message(chat_id, status_msg.message_id)
        if len(output) > 4096:
            for x in range(0, len(output), 4000): bot.send_message(chat_id, output[x:x+4000], reply_markup=get_main_menu(), parse_mode="HTML")
        else: bot.send_message(chat_id, output, reply_markup=get_main_menu(), parse_mode="HTML")
        return

# --- 🚀 START FAKE SERVER FOR CHOREO HEALTH CHECK BEFORE BOT POLLING ---
Thread(target=run_choreo_fake_server, daemon=True).start()

print("====================================")
print("📌 MATRIX MAINBOARD v16.0: LIVE!")
print("☁️ Choreo Service Fake Port Server Active!")
print("====================================")

bot.remove_webhook()
bot.infinity_polling()
