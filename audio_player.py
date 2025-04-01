import pygame
import os

def init_audio():
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)  # 优化音频初始化参数

def play_audio(file_path, retries=3):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"音频文件不存在: {file_path}")
    
    for attempt in range(retries):
        try:
            # 确保pygame mixer已初始化
            if not pygame.mixer.get_init():
                init_audio()
            
            # 停止之前的音频播放
            pygame.mixer.music.stop()
            
            # 加载并播放新的音频文件
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            # 优化等待逻辑，使用更高效的帧率
            clock = pygame.time.Clock()
            while pygame.mixer.music.get_busy():
                clock.tick(30)  # 提高帧率以减少延迟
            
            return True
        
        except Exception as e:
            print(f"音频播放尝试 {attempt + 1} 失败: {e}")
            if attempt < retries - 1:
                pygame.mixer.quit()
                init_audio()
            else:
                raise

def cleanup():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except:
        pass