import speech_recognition as sr

def record(recognizer, language='en-US'):
    with sr.Microphone() as source:
        # 调整麦克风参数以减少环境噪音
        recognizer.dynamic_energy_threshold = False
        recognizer.energy_threshold = 300
        recognizer.pause_threshold = 0.5

        try:
            # 减少超时时间，提高响应速度
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
            text = recognizer.recognize_google(audio, language=language)

            print(f"You told: {text}")
            return text
        except sr.UnknownValueError:
            print('Can not understand audio')
            return
        except sr.WaitTimeoutError:
            print('No Sound detected')
            return
        except sr.RequestError as e:
            print(f"Identification service error: {e}")
            return
