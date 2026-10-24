import os
import re
import io
import aiohttp
import discord
import threading
from dotenv import load_dotenv
from http.server import BaseHTTPRequestHandler, HTTPServer

load_dotenv()

TOKEN1 = os.getenv("DISCORD_TOKEN")
TOKEN2 = os.getenv("DISCORD_TOKEN2")

intents1 = discord.Intents.default()
intents1.message_content = True
client1 = discord.Client(intents=intents1)

intents2 = discord.Intents.default()
client2 = discord.Client(intents=intents2)

# سيرفر وهمي عشان Render ما يقفل البوت
class WebServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), WebServer)
    server.serve_forever()

# محرك الفك
def deobfuscate_engine(text):
    if "ALPHA85" in text and "d85" in text:
        try:
            m_u = re.search(r"local U=\{([\s\S]*?)\}\s*local segs=", text)
            m_segs = re.search(r"local segs=\{([\s\S]*?)\}\s*for _,s in ipairs\(segs\)", text)
            if m_u and m_segs:
                u_str = "{" + m_u.group(1) + "}"
                segs_str = "{" + m_segs.group(1) + "}"
                U = eval(u_str.replace("nil", "None"))
                segs = eval(segs_str)
                
                alpha85 = "".join(chr(c) for c in range(35, 127) if c not in (34, 92))[:85]
                b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
                O = {char: i for i, char in enumerate(alpha85)}
                W = {char: i for i, char in enumerate(b64)}
                
                def d85(s):
                    if not s.startswith("?"): return s
                    out = bytearray()
                    for i in range(1, len(s), 5):
                        chunk = s[i:i+5]
                        if len(chunk) < 5: break
                        v = 0
                        for j in range(5): v = v * 85 + O.get(chunk[j], 0)
                        out.extend([(v >> 24) & 0xFF, (v >> 16) & 0xFF, (v >> 8) & 0xFF, v & 0xFF])
                    return out.rstrip(b'\0').decode('latin-1', errors='replace')
                    
                def d64(s):
                    if not s.startswith("\163"): return s
                    out = bytearray()
                    for i in range(1, len(s), 4):
                        chunk = s[i:i+4]
                        if len(chunk) < 2: break
                        v1 = W.get(chunk[0], 0); v2 = W.get(chunk[1], 0)
                        v3 = W.get(chunk[2], 0) if len(chunk) > 2 and chunk[2] != '=' else 0
                        v4 = W.get(chunk[3], 0) if len(chunk) > 3 and chunk[3] != '=' else 0
                        n = v1 * 262144 + v2 * 4096 + v3 * 64 + v4
                        out.append((n >> 16) & 0xFF)
                        if len(chunk) > 2 and chunk[2] != '=': out.append((n >> 8) & 0xFF)
                        if len(chunk) > 3 and chunk[3] != '=': out.append(n & 0xFF)
                    return out.decode('latin-1', errors='replace')

                for seg in segs:
                    a, b = seg[0] - 1, seg[1] - 1
                    while a < b:
                        U[a], U[b] = U[b], U[a]
                        a += 1; b -= 1

                Z = []
                for item in U:
                    if not isinstance(item, str): continue
                    if item.startswith("?"): Z.append(d85(item))
                    elif item.startswith("\163"): Z.append(d64(item))
                    else: Z.append(item)
                
                source = "-- [ تم فك تشفير WRD بالكامل ] --\n\n" + "\n".join([f"-- {z}" for z in Z if isinstance(z, str) and len(z) > 3])
                return source, "تم فك WRD بنجاح"
        except Exception: pass

    if "string.char" in text:
        def decode_char(m):
            nums = [int(x) for x in m.group(1).split(",") if x.strip().isdigit()]
            if nums:
                try: return '"' + "".join(chr(n) for n in nums if 0 <= n <= 255).replace('"', '\\"') + '"'
                except: return m.group(0)
            return m.group(0)
        new_text = re.sub(r"string\.char\(([0-9,\s]+)\)", decode_char, text)
        if new_text != text: return new_text, "تم فك تشفير النصوص بنجاح"

    if "Luraph" in text or "luraph_runtime1" in text or "MoonSec" in text:
        keys = re.findall(r'script_key\s*=\s*"([0-9a-f]{32})"', text)
        msg = "تم اكتشاف Luraph/Moonsec. السورس مرفق."
        if keys: msg += f"\nالمفتاح المستخرج: {keys[0]}"
        return text, msg

    return text, "السكربت نظيف أو غير معروف."

async def fetch_url(url):
    headers = {"User-Agent": "Roblox/WinInetRobloxApp/0.673.0.6730711"}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=30) as r:
                return await r.text() if r.status == 200 else None
    except: return None

@client2.event
async def on_ready():
    print(f"[بوت الخاص] شغال: {client2.user}")

@client1.event
async def on_ready():
    print(f"[بوت الفك] شغال: {client1.user}")

@client1.event
async def on_message(message):
    if message.author == client1.user: return

    if message.content.startswith(".l"):
        # 1. نحذف رسالة المستخدم على طول عشان محد يشوفها
        try:
            await message.delete()
        except:
            pass

        text = None
        src_name = "script.lua"
        
        if message.attachments:
            attachment = message.attachments[0]
            text = (await attachment.read()).decode("utf-8", errors="replace")
            src_name = attachment.filename
        elif len(message.content.split()) > 1:
            url = message.content.split()[1]
            match = re.search(r'(https?://[^\s"\']+)', url)
            if match: url = match.group(1)
            text = await fetch_url(url)
            src_name = "url_script.lua"

        # 2. نرسل له بالخاص إننا بدينا
        try:
            await message.author.send("جاري الفك... انتظر شوي.")
        except:
            return # إذا خاصه مسكر، نوقف

        if not text:
            await message.author.send("ما قدرت أقرأ الملف أو الرابط. جرب ترفعه مرة ثانية.")
            return

        # 3. نفك السكربت
        source_code, status = deobfuscate_engine(text)
        
        # 4. نرسل السكربت المفكوك للخاص
        try:
            file_data = discord.File(fp=io.BytesIO(source_code.encode('utf-8')), filename=f"deobf_{src_name}")
            await message.author.send(content=f"تم الفك ({status}).\nتفضل السورس:", file=file_data)
        except Exception as e:
            await message.author.send(f"صار خطأ وأنا أرسل الملف: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    
    t1 = threading.Thread(target=client1.run, args=(TOKEN1,))
    t2 = threading.Thread(target=client2.run, args=(TOKEN2,))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
