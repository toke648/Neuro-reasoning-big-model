from language_generate import large_language_model
from tts_speech import speech_edge_tts
from audio_record import record
from audio_player import play_audio, init_audio, cleanup
import speech_recognition as sr
import logging
import asyncio
import time

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

setting = open('ai_setting_VTuber-Neuro sama.txt', 'r', encoding="utf-8").read()
conversation_history = [{'role': 'system', 'content': f'{setting}'}]  # You can use dictionary to show it

record_language = "en-US"
speech_language = 'en-US-AvaNeural'
output_path = "audio/output.mp3"

recognizer = sr.Recognizer() # 初始化识别器
init_audio() # 初始化音频系统

async def main(content, conversation_history, max_retries=3):
    # Add user input to conversation history
    for attempt in range(max_retries):
        try:
            # Get the model's response
            logger.info(f"User: {content}")
            response = large_language_model(content, conversation_history)
            logger.info(f"Agent: {response}")

            # 生成并播放音频响应
            try:
                # 确保在生成新音频前停止当前播放
                cleanup()
                await speech_edge_tts(text=response, path=output_path, speech_language=speech_language)
                play_audio(output_path)
                return True
            except Exception as e:
                logger.error(f'音频生成或播放错误: {e}')
                raise

        except FileNotFoundError as e:
            logger.error(f'音频文件错误 (尝试 {attempt + 1}/{max_retries}): {e}')
        except Exception as e:
            logger.error(f'处理错误 (尝试 {attempt + 1}/{max_retries}): {e}')
        
        if attempt < max_retries - 1:
            time.sleep(2)  # 在重试之前等待
            continue
    
    logger.error(f'在{max_retries}次尝试后仍然失败')
    return False

async def run():
    try:
        while True:
            content = record(recognizer, record_language)
            if not content: # 如果没有检测到音频，则跳过循环
                continue
            else:
                try:
                    if not await main(content, conversation_history):
                        logger.warning("跳过当前对话，等待下一次输入")
                except Exception as e:
                    logger.error(f"主程序执行错误: {e}")
    finally:
        cleanup() # 确保在程序退出时清理音频资源

if __name__ == '__main__':
    asyncio.run(run())


