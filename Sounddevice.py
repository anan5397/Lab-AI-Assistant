import time


audio_buffer = []
def test(indata):
    audio = indata.flatten()
    while True:
        time.sleep(0.1)  # Sleep for a short duration to reduce CPU usage
        print("Ask your question...")
        audio_buffer.extend(audio)
        if len(audio_buffer) >= 5 * 16000: #Checking when the question is done. 
                break
    
    print("SPEAKING DONE",audio_buffer)

