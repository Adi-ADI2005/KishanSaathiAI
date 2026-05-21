import os
from sarvamai import SarvamAI
from config import SARVAM_API_KEY

client = SarvamAI(api_subscription_key=SARVAM_API_KEY)


def speech_to_text(file_path):
    """
    Convert speech audio file → text
    Supports multiple languages (auto-detect)
    """

    try:
        # Create job
        job = client.speech_to_text_job.create_job(
            model="saaras:v3",
            mode="transcribe",
            language_code="unknown",   # Auto detect language
            with_diarization=False
        )

        # Upload file
        job.upload_files(file_paths=[file_path])

        # Start processing
        job.start()

        # Wait until done
        job.wait_until_complete()

        # Get result
        results = job.get_file_results()

        if results["successful"]:
            output = results["successful"][0]["transcript"]
            return output

        return "Error: No transcription found"

    except Exception as e:
        print("STT Error:", e)
        return "Error in speech recognition"