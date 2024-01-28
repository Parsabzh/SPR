import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

class TextSummarizer:
    def __init__(self, scaling_factor=1.2):
        self.scaling_factor = scaling_factor
        self.stopWords = set(stopwords.words("english"))

    def tokenize_text(self, text):
        """Tokenize the text into words and sentences."""
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        return words, sentences

    def create_frequency_table(self, words):
        """Create a frequency table for words in the text."""
        freq_table = {}
        for word in words:
            word = word.lower()
            if word not in self.stopWords:
                freq_table[word] = freq_table.get(word, 0) + 1
        return freq_table

    def score_sentences(self, sentences, freq_table):
        """Score each sentence based on word frequencies."""
        sentence_value = {}
        for sentence in sentences:
            for word, freq in freq_table.items():
                if word in sentence.lower():
                    sentence_value[sentence] = sentence_value.get(sentence, 0) + freq
        return sentence_value

    def calculate_average_score(self, sentence_value):
        """Calculate the average score of sentences."""
        sum_values = sum(sentence_value.values())
        average = int(sum_values / len(sentence_value))
        return average

    def generate_summary(self, text):
        """Generate a summary of the text."""
        words, sentences = self.tokenize_text(text)
        freq_table = self.create_frequency_table(words)
        sentence_value = self.score_sentences(sentences, freq_table)
        average_score = self.calculate_average_score(sentence_value)

        summary = ''
        for sentence in sentences:
            if sentence_value.get(sentence, 0) > (self.scaling_factor * average_score):
                summary += " " + sentence

        return summary.strip()


