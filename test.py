import librosa

import numpy as np

def calculate_fluency_score(total_words, non_silent_duration, total_duration):
    """
    Calculate a fluency score based on speech rate and the ratio of speaking duration to total duration,
    scaled between 10% and 100%, with considerations for rushed speech.

    :param total_words: The total number of words spoken.
    :param non_silent_duration: The total duration of non-silent intervals.
    :param total_duration: The total duration of the audio.
    :return: The fluency score as part of the CSS, scaled between 10% and 100%.
    """
    # Ideal speech rate (words per minute) and convert to words per second
    ideal_min_rate, ideal_max_rate = 100 / 60, 160 / 60
    
    # Calculate the actual speech rate (words per second)
    actual_speech_rate = total_words / non_silent_duration
    
    # Calculate the ratio of non-silent duration to total duration
    speaking_ratio = non_silent_duration / total_duration

    # Determine if speech rate is within the ideal range
    if ideal_min_rate <= actual_speech_rate <= ideal_max_rate:
        # Within the ideal range
        speech_rate_score = 1
    else:
        # Outside the ideal range, score is proportional to how close it is to the range
        if actual_speech_rate < ideal_min_rate:
            # Too slow
            speech_rate_score = actual_speech_rate / ideal_min_rate
        else:
            # Too fast
            speech_rate_score = 2 - (actual_speech_rate / ideal_max_rate)
        # Clamp the score between 0 and 1
        speech_rate_score = max(0, min(speech_rate_score, 1))

    # Combine the speech rate score and speaking ratio
    # If speaking ratio is significantly less than the gold standard, reduce the fluency score
    gold_standard_ratio = 0.9  # Assuming 90% speaking time is gold standard for natural speech
    speaking_ratio_score = min(speaking_ratio / gold_standard_ratio, 1)
    
    fluency_score = (speech_rate_score + speaking_ratio_score) / 2

    # Scale the fluency score to be between 10% and 100%
    scaled_fluency_score = 10 + fluency_score * 90  # Scales the score from 10% to 100%

    return scaled_fluency_score


def estimate_continuous_speech_score(audio_path, transcription, word_pronunciation_scores):
    """
    Estimate the Continuous Speech Score based on the transcription and word pronunciation scores.
    
    :param audio_path: Path to the audio file.
    :param transcription: The transcribed text of the speech.
    :param word_pronunciation_scores: List of scores for each transcribed word (1, 2, or 3).
    :return: The estimated Continuous Speech Score.
    """
    
    # Load the audio file
    audio, sr = librosa.load(audio_path)

    # Detect pauses (intervals with low energy)
    non_silent_intervals = librosa.effects.split(audio, top_db=20)  # top_db is a threshold for silence detection
    # Calculate total duration of non-silent intervals
    non_silent_duration = sum([intv[1] - intv[0] for intv in non_silent_intervals]) / sr
    print('Total duration:', len(audio) / sr)
    print('non_silent_duration:', non_silent_duration)
    
    # Define common English filler words
    filler_words = {'um', 'uh', 'like', 'you know'}
    
    # Split the transcription into words and count the filler words
    words = transcription.split()
    filler_word_count = sum(word in filler_words for word in words)
    
    # Estimate the impact of filler words on fluency
    filler_impact = filler_word_count / len(words)
    
    # Calculate the variance in pronunciation scores
    score_variance = np.var(word_pronunciation_scores)
    
    # Combine the filler impact and score variance to estimate the CSS (this is an arbitrary formula and can be adjusted)
    css = max(1, 3 - filler_impact - score_variance)

    return css

# Example usage
# transcription_example = "Well um you know the thing is like uh we need to uh work on this project"
# word_pronunciation_scores_example = [3, 2, 1, 3, 2, 1, 2, 3, 2]
# path = r"C:\Users\20101\Downloads\OSR_us_000_0011_8k.wav"
# css = estimate_continuous_speech_score(path, transcription_example, word_pronunciation_scores_example)
# print(css)

# Example usage
total_words_example = 100 # Replace with the actual word count
non_silent_duration_example = 35  # Replace with the calculated non-silent duration
total_duration_example = 40  # Replace with the total audio duration

fluency_score = calculate_fluency_score(
    total_words_example,
    non_silent_duration_example,
    total_duration_example
)
print(fluency_score)

