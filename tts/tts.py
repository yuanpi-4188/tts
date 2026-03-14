import edge_tts
import asyncio
import sys
import os
from playsound import playsound

VOICE_MAP = {
    "xx": "zh-CN-XiaoxiaoNeural",
    "xy": "zh-CN-XiaoyiNeural",
    "yj": "zh-CN-YunjianNeural",
    "yx": "zh-CN-YunxiNeural",
    "ya": "zh-CN-YunyangNeural",
}

def show_help():
    print("==================================================")
    print("🎙️ TTS 语音工具")
    print("==================================================")
    print("用法：tts [音色] [参数] 文本")
    print()
    print("音色：")
    print("  -xx 晓晓   -xy 晓伊   -yj 云健   -yx 云希   -ya 云扬")
    print()
    print("参数：")
    print("  -r+30    语速+30%")
    print("  -r-20    语速-20%")
    print("  -v+10    音量+10%")
    print("  -v-20    音量-20%")
    print("  -s=1     保存音频1.mp3")
    print()
    print("示例：")
    print("  tts -xx -r+30 你好")
    print("  tts -xy -r-20 -v+10 慢慢说")
    print("  tts -yx -s=out 保存声音")
    print("==================================================")

async def do_tts(text, voice, rate=None, volume=None, save_path=None):
    kwargs = {}
    if rate:
        kwargs["rate"] = rate
    if volume:
        kwargs["volume"] = volume

    tts = edge_tts.Communicate(text, voice, **kwargs)
    tmp = "~tmp.mp3"
    await tts.save(tmp)

    if save_path:
        os.rename(tmp, save_path)
        print(f"✅ 已保存：{save_path}")
        return

    playsound(tmp)
    os.remove(tmp)

def get_text(input_str):
    if os.path.isfile(input_str):
        try:
            with open(input_str, "r", encoding="utf-8") as f:
                return f.read()
        except:
            return "读取文件失败"
    return input_str

def main():
    if len(sys.argv) == 1:
        show_help()
        return

    args = sys.argv[1:]
    voice = VOICE_MAP["yx"]
    rate = None
    volume = None
    save = None
    text_parts = []

    for arg in args:
        # 音色
        if arg == "-xx": voice = VOICE_MAP["xx"]
        elif arg == "-xy": voice = VOICE_MAP["xy"]
        elif arg == "-yj": voice = VOICE_MAP["yj"]
        elif arg == "-yx": voice = VOICE_MAP["yx"]
        elif arg == "-ya": voice = VOICE_MAP["ya"]

        # 语速 -r+ / -r-
        elif arg.startswith("-r+"):
            num = arg[3:]
            rate = f"+{num}%"
        elif arg.startswith("-r-"):
            num = arg[3:]
            rate = f"-{num}%"

        # 音量 -v+ / -v-
        elif arg.startswith("-v+"):
            num = arg[3:]
            volume = f"+{num}%"
        elif arg.startswith("-v-"):
            num = arg[3:]
            volume = f"-{num}%"

        # 保存 -s=
        elif arg.startswith("-s="):
            save_path = arg[3:]  # 先获取原始路径
            # 自动添加.mp3后缀（如果没有的话）
            if not save_path.endswith('.mp3'):
                save_path += '.mp3'
            save = save_path

        else:
            text_parts.append(arg)

    text = get_text(" ".join(text_parts))
    asyncio.run(do_tts(text, voice, rate, volume, save))

if __name__ == "__main__":
    main()
