import edge_tts
import os
import asyncio
from filelock import FileLock

async def speech_edge_tts(text: str, path: str, speech_language: str, retries=3) -> None:
    rate = '-5%'
    volume = '+50%'
    lock = FileLock(f"{path}.lock", timeout=1)  # 添加超时设置

    for attempt in range(retries):
        try:
            async with asyncio.timeout(10):  # 添加总体超时控制
                with lock:
                    if os.path.exists(path):
                        try:
                            os.remove(path)
                        except Exception as e:
                            print(f'Failed to remove existing file: {e}')
                            continue

                    communicate = edge_tts.Communicate(text=text,
                                               voice=speech_language,
                                               rate=rate,
                                               volume=volume)
                    await communicate.save(path)
                
                    if os.path.exists(path) and os.path.getsize(path) > 0:
                        return
                    else:
                        raise Exception("Generated audio file is invalid or empty")
                
        except Exception as e:
            print(f'Speech generation attempt {attempt + 1} failed: {e}')
            with lock:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception as cleanup_error:
                        print(f'Failed to cleanup corrupted audio file: {cleanup_error}')
            
            if attempt < retries - 1:
                await asyncio.sleep(1)  # 减少重试等待时间
                continue
            else:
                raise Exception(f'Speech generation failed after {retries} attempts: {e}')






