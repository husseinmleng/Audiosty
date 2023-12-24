import numpy as np
import librosa

def calculate_expected_value(scores):

    # First calculate the probability of each unique score
    unique_scores, counts = np.unique(scores, return_counts=True)
    probabilities = counts / len(scores)
    
    # Then calculate the expected value as the sum of scores times their probabilities   
    expected_value = np.dot(unique_scores, probabilities)
    return expected_value


def calculate_fluency_score(audio_path, total_words, word_pronunciation_scores, base_script_len): 
    
    avg_pronunciation_score = calculate_expected_value(word_pronunciation_scores)
    if (total_words / base_script_len) < 0.15 or avg_pronunciation_score < 1.5:
        return 10
    audio, sr = librosa.load(audio_path)
    non_silent_intervals = librosa.effects.split(audio, top_db=22)
    non_silent_duration = sum([intv[1] - intv[0] for intv in non_silent_intervals]) / sr
    
    total_duration = len(audio) / sr
    
    
    non_silent_duration = non_silent_duration if total_words > 4 else 0
    ideal_min_rate, ideal_max_rate = 120 / 60, 140 / 60
    actual_speech_rate = (total_words / (non_silent_duration + 1e-7)) * (total_words / base_script_len)
    speaking_ratio = non_silent_duration / total_duration
    # Existing speech rate score calculation
 
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

    # If speaking ratio is significantly less than the gold standard, reduce the fluency score
    gold_standard_ratio = 0.9  # Assuming 90% speaking time is gold standard for natural speech
    speaking_ratio_score = min(speaking_ratio / gold_standard_ratio, 1)
    

    # Pronunciation score calculation
    avg_pronunciation_score = (avg_pronunciation_score - 1) / 2
    pronunciation_variance = np.var(word_pronunciation_scores, ddof=1,)

    # Weighted combination of scores
    # Adjust weights as needed
    weight_speech_rate = 0.20
    weight_speaking_ratio = 0.20
    weight_pronunciation = 0.50
    weight_pronunciation_variance = 0.10

    combined_score = (speech_rate_score * weight_speech_rate + 
                      speaking_ratio_score * weight_speaking_ratio + 
                      avg_pronunciation_score * weight_pronunciation + 
                      (1 / (1 + pronunciation_variance)) * weight_pronunciation_variance)
    
    # Scale the combined score to be between 10% and 100%
    scaled_fluency_score = 10 + combined_score * 80

    return scaled_fluency_score

def calculate_pronunciation_accuracy(word_pronunciation_scores, fluency_score, base_script_len):
    if len(word_pronunciation_scores) / base_script_len < 0.25:
        return 10
    # Calculate average word pronunciation score
    avg_pronunciation_score = calculate_expected_value(word_pronunciation_scores)
    print(avg_pronunciation_score)
    # Adjust pronunciation score based on fluency
    # fluency_score = fluency_score / 100
    # This is a simplistic adjustment. It can be refined based on more detailed analysis
    fluency_adjustment = fluency_score / 100
    print(fluency_adjustment)
    adjusted_pronunciation_score = avg_pronunciation_score * fluency_adjustment
    print(adjusted_pronunciation_score)
    # Map to 0-5 scale based on score guide
    # These thresholds can be adjusted based on empirical data or further analysis
    if adjusted_pronunciation_score >= 2.4:
        score_guide_level = 5
    elif adjusted_pronunciation_score >= 1.7:
        score_guide_level = 4
    elif adjusted_pronunciation_score >= 1.0:
        score_guide_level = 3
    elif adjusted_pronunciation_score >= 0.5:
        score_guide_level = 2
    else:
        score_guide_level = 1

    # Scale to 10% - 90%
    final_score = 10 + (score_guide_level - 1) * 20  # Scale each level to a range of 20%

    return final_score

def calculate_fluency_and_pronunciation(audio_path, transcription, word_pronunciation_scores, base_script_len):
    
    fluency_score = calculate_fluency_score(audio_path, transcription, word_pronunciation_scores, base_script_len)
    
    pronunciation_accuracy = calculate_pronunciation_accuracy(word_pronunciation_scores, fluency_score, base_script_len)
    
    return {'fluency_score': fluency_score, 'pronunciation_accuracy': pronunciation_accuracy}
    

if __name__ == '__main__':
    pass