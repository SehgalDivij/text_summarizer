import string
import sys
import traceback
import os
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# list of stop words in english.
stopWords = set(stopwords.words("english"))


def clean_lines(lines, to_lower=False):
    """ clean a list of lines"""
    cleaned = list()
    # prepare a translation table to remove punctuation
    table = str.maketrans('', '', string.punctuation)
    for line in lines:
        # tokenize on white space
        line = line.split()
        # convert to lower case
        if to_lower:
            line = [word.lower() for word in line]
        # remove punctuation from each token
        line = [w.translate(table) for w in line]
        # remove tokens with numbers in them
        line = [word for word in line if word.isalpha()]
        # store as string
        cleaned.append(' '.join(line))
    # remove empty strings
    cleaned = [c for c in cleaned if len(c) > 0]
    return cleaned


def make_freq_table(words, to_lower=False):
    freqTable = dict()
    for word in words:
        if to_lower:
            word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    return freqTable


def get_sentence_value(sentences, freq_table):
    sentenceValue = dict()
    index = 0
    for sentence in sentences:
        index += 1
        for wordValue in freq_table:
            if wordValue in sentence.lower():
                try:
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq_table[wordValue]
                    else:
                        sentenceValue[sentence] = freq_table[wordValue]
                except Exception as ex:
                    print(index, sentenceValue, wordValue)
                    print(traceback.print_exc())
                    print(sentence, len(sentence))
                    sys.exit(0)
    return sentenceValue


def get_summary(sentences, sentence_value):
    """
        Calculate average sentence score using sentence_values.
        Get summary for the text.
    """
    sumValues = 0
    for sentence in sentence_value:
        sumValues += sentence_value[sentence]
    # Average value of a sentence from original text
    average = int(sumValues / len(sentence_value))
    summary = ''
    for sentence in sentences:
        if sentence in sentence_value and sentence_value[sentence] > (1.5 * average):
            summary += sentence + ". "
    return summary


def generate_summary(sentences):
    """
        Generate a summary for a list of sentences.
    """
    cleaned = clean_lines(sentences, False)

    # tokenize the sentences in corpus, after cleaning.
    words = word_tokenize(' \n'.join(cleaned))
    freq_table = make_freq_table(words, True)
    cleaned_values = get_sentence_value(cleaned, freq_table)
    summary = get_summary(cleaned, cleaned_values)
    return summary.strip()


# flipkart_article = "Flipkart is rolling out a number of initiatives for its seller partners, including reduced commissions and a soon-to-be launched benefits scheme for merchants exclusive to its platform as the e-commerce giant looks to stay ahead of its rival Amazon. " + "Flipkart Director (Marketplace) Nishant Gupta said the company has taken a number of steps over the last one year to improve customer experience as well as that of sellers on its platform. " + "There were multiple pain points in seller support. And so, over the last one and a half years, we have made significant investments in technology and support to ensure that sellers have a good experience,\" Gupta told. " + "This has resulted in an increase in net promoter score (willingness of customers to recommend a company's products) measured internally to 70. " + "Flipkart has over one lakh sellers on its platform. " + "We are working on something for sellers who are exclusive on our platform. It would chart out the expectations that we would have from the sellers and what would they get from Flipkart in return,\" Gupta said. " + "While he declined to divulge further details, Gupta said the programme could be launched in the next couple of months on a pilot basis. " + \
#     "According to industry watchers, a programme for exclusive sellers could include more perks and lesser commission among other benefits for merchants that choose to sell exclusively through Flipkart. " + "This, they said, would not only increase the selection on Flipkart's platform but also compete more aggressively against rival Amazon. " + "Flipkart has also scaled up its rewards and recognition programme to present cars, mobile phones and holiday trips to best-performing sellers. " + "Talking about recent initiatives, Gupta said earlier this month, the company had reduced commissions by 4-5 per cent in various categories for products priced under Rs 500. " + \
#     "In April too, it had reduced some charges that helped in a reduction of up to Rs 24 per shipment. " + "Economies of scale ensure that bottomlines don't get impacted,\" he said. " + "Gupta said Flipkart has launched a priority seller support service, introduced a 'tier' system for sellers and invested in fulfilment centres. " + \
#     "Besides these, we offer data intelligence to our sellers, which is most important. This provides insights on movement of various items and the sellers can plan better and grow their business,\" he added."

# text = sent_tokenize(flipkart_article)

# # no summaries generated for this.
# # needs more cleaning?
# random_quora_answer = "First and foremost, it is important to understand that word2vec is not a single monolithic algorithm. In fact, word2vec contains two distinct models (CBOW and skip-gram), each with two different training methods (with/without negative sampling) and other variations (e.g. hierarchical softmax), which amount to small \"space\" of algorithms. To top that, it also contains a honed pre-processing pipeline, whose effects on the overall performance have yet to be studied properly. " + "\nAnother thing that's important to understand, is that word2vec is not deep learning; both CBOW and skip-gram are \"shallow\" neural models. Tomas Mikolov even told me that the whole idea behind word2vec was to demonstrate that you can get better word representations if you trade the model's complexity for efficiency, i.e. the ability to learn from much bigger datasets. " + "\nIn his papers, Mikolov recommends using the skip-gram model with negative sampling (SGNS), as it outperformed the other variants on analogy tasks. " + \
#     "\nYoav Goldberg and I wrote an in-depth explanation of how SGNS works: \nword2vec Explained: Deriving Mikolov et al.'s Negative-Sampling Word-Embedding Method" + "\nIt's not a very long read, but still a little too long for me to port it to Quora. " + \
#     "\nWe later found out that SGNS is implicitly factorizing a word-context matrix, whose cells are the pointwise mutual information (PMI) of the respective word and context pairs, shifted by a global constant:\n" + "Neural Word Embeddings as Implicit Matrix Factorization" + \
#     " PMI matrices are commonly used by the traditional approach to represent words (often dubbed \"distributional semantics\"). What's really striking about this discovery, is that word2vec (specifically, SGNS) is doing something very similar to what the NLP community has been doing for about 20 years; it's just doing it really well."

# quora_ans_text = sent_tokenize(random_quora_answer)

print(__name__)
if __name__ == '__main__':
    path = '.'
    files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and \
             'to_summarize' in i]
    for f_name in files:
        print('reading: ' + f_name)
        with open(f_name) as f:
            print(generate_summary(f.readlines()))
