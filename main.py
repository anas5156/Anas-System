import os, asyncio, random, sys, logging
from pathlib import Path
from telethon import TelegramClient, events, functions, types

# تحسين السرعة لبيئة iSH
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError: pass

API_ID = int(os.getenv("API_ID") or input("🟢 API_ID: ").strip())
API_HASH = os.getenv("API_HASH") or input("🟢 API_HASH: ").strip()

session_file = str(Path.home() / ".nasir_sessions" / "nasir_session")
Path(session_file).parent.mkdir(parents=True, exist_ok=True)
client = TelegramClient(session_file, API_ID, API_HASH)

# مخازن البيانات والسطور (100 سطر من اللي طلبتهم بالحرف)
DATA = {
    "بلش_سطور": [
        "ي ابن القحبة", "ي ابن الشرموطة", "ي ابن الاهبل", "ي ابن الكلب", "ي ابن المسكينة",
        "ي اخو الشرموطة", "ي ابن الورع", "كس امك", "كس ام خالتك", "ي ابن الخنزير",
        "ي ابن المنيوكة", "ي ابن الوصخة", "ي ابن الزنوة", "ي ابن القواد", "ي ابن الصندل",
        "ي ابن الخرا", "ي ابن المفسية", "ي ابن العاهرة", "ي ابن الساقطة", "ي ابن الحرام",
        "ي ابن المومس", "ي ابن الغسيل", "ي ابن النعال", "ي ابن البول", "ي ابن الوسخة",
        "ي ابن الكريهة", "ي ابن الغدر", "ي ابن السلوقية", "ي نغل", "ي ابن الجزمة",
        "ي ابن القحبة", "ي ابن الشرموطة", "ي ابن الاهبل", "ي ابن الكلب", "ي ابن المسكينة",
        "ي اخو الشرموطة", "ي ابن الورع", "كس امك", "كس ام خالتك", "ي ابن الخنزير",
        "ي ابن المنيوكة", "ي ابن الوصخة", "ي ابن الزنوة", "ي ابن القواد", "ي ابن الصندل",
        "ي ابن الخرا", "ي ابن المفسية", "ي ابن العاهرة", "ي ابن الساقطة", "ي ابن الحرام",
        "ي ابن المومس", "ي ابن الغسيل", "ي ابن النعال", "ي ابن البول", "ي ابن الوسخة",
        "ي ابن الكريهة", "ي ابن الغدر", "ي ابن السلوقية", "ي نغل", "ي ابن الجزمة",
        "ي ابن القحبة", "ي ابن الشرموطة", "ي ابن الاهبل", "ي ابن الكلب", "ي ابن المسكينة",
        "ي اخو الشرموطة", "ي ابن الورع", "كس امك", "كس ام خالتك", "ي ابن الخنزير",
        "ي ابن المنيوكة", "ي ابن الوصخة", "ي ابن الزنوة", "ي ابن القواد", "ي ابن الصندل",
        "ي ابن الخرا", "ي ابن المفسية", "ي ابن العاهرة", "ي ابن الساقطة", "ي ابن الحرام",
        "ي ابن المومس", "ي ابن الغسيل", "ي ابن النعال", "ي ابن البول", "ي ابن الوسخة",
        "ي ابن الكريهة", "ي ابن الغدر", "ي ابن السلوقية", "ي نغل", "ي ابن الجزمة",
        "ي ابن القحبة", "ي ابن الشرموطة", "ي ابن الاهبل", "ي ابن الكلب", "ي ابن المسكينة",
        "ي اخو الشرموطة", "ي ابن الورع", "كس امك", "كس ام خالتك", "ي ابن القواد"
    ],
    "بلش_شغال": set(), "بلش_index": {}, "ضرب_tasks": {}, "كتم": set()
}

async def temp_confirm(cid, txt, delay=1.5):
    try:
        m = await client.send_message(cid, txt)
        await asyncio.sleep(delay); await m.delete()
    except: pass

@client.on(events.NewMessage(incoming=True))
async def auto_handler(ev):
    sid, cid = ev.sender_id, ev.chat_id
    if not sid: return
    
    # كتم (حذف رسائل المكتوم)
    if sid in DATA["كتم"]:
        try: await ev.delete()
        except: pass
        return

    # بلش (رد تلقائي بالسطور)
    if sid in DATA["بلش_شغال"]:
        idx = DATA["بلش_index"].get(sid, 0)
        line = DATA["بلش_سطور"][idx % len(DATA["بلش_سطور"])]
        DATA["بلش_index"][sid] = idx + 1
        await ev.reply(line)

@client.on(events.NewMessage(outgoing=True))
async def nasir_engine(ev):
    t = ev.raw_text.strip()
    cid = ev.chat_id
    rep = await ev.get_reply_message()

    # ضرب (ضرب السرعة العدد النص) بالرد
    if t.startswith("ضرب") and rep:
        await ev.delete()
        p = t.split(maxsplit=3)
        try:
            speed, count, msg = float(p[1]), int(p[2]), p[3]
            async def d_task():
                for _ in range(count):
                    if cid not in DATA["ضرب_tasks"]: break
                    await client.send_message(cid, msg, reply_to=rep.id)
                    await asyncio.sleep(speed)
                DATA["ضرب_tasks"].pop(cid, None)
            DATA["ضرب_tasks"][cid] = asyncio.create_task(d_task())
        except: pass

    # مم (مم العدد النص) بالرد
    elif t.startswith("مم") and rep:
        await ev.delete()
        p = t.split(maxsplit=2)
        try:
            count, msg = int(p[1]), p[2]
            for _ in range(count):
                await client.send_message(cid, msg, reply_to=rep.id)
                await asyncio.sleep(0.3)
        except: pass

    # كتم بالرد
    elif t == "كتم" and rep:
        await ev.delete()
        DATA["كتم"].add(rep.sender_id)
        await temp_confirm(cid, "🔇 تم كتمه")

    # الغاء كتم بالرد
    elif t == "الغاء كتم" and rep:
        await ev.delete()
        DATA["كتم"].discard(rep.sender_id)
        await temp_confirm(cid, "🔊 تم فك الكتم")

    # بلش بالرد
    elif t.startswith("بلش") and rep:
        await ev.delete()
        DATA["بلش_شغال"].add(rep.sender_id)
        DATA["بلش_index"][rep.sender_id] = 0
        await temp_confirm(cid, "🔥 بدأ الدعس")

    # ايقاف الكل (يوقف البلش والكتم والضرب)
    elif t == "ايقاف الكل":
        await ev.delete()
        DATA["بلش_شغال"].clear()
        DATA["كتم"].clear()
        for task in DATA["ضرب_tasks"].values(): task.cancel()
        DATA["ضرب_tasks"].clear()
        await temp_confirm(cid, "🛑 توقف كل شيء")

client.start()
print("✅ كل شيء جاهز.. اخلص")

client.run_until_disconnected()
