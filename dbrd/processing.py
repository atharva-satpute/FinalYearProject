# General Libraries
import re
import warnings

# NLP
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import wordpunct_tokenize
# Pymongo
from pymongo.errors import DuplicateKeyError

warnings.filterwarnings('ignore')


# Check if corpus of stopwords and wordnet exists
try:
    nltk.data.find('./corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('./corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


def cleaning(document):
    try:
        # To remove timestamp and date
        document = re.sub(r"(([A-Z]{2,}\s)*(\([0-9\/]+(\s)*[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2} (AM|PM)*)\))", '', document)

        # To remove XML code
        document = re.sub(r"(\<\?xml[a-zA-Z0-9\.\s\=\?\"\-\>\\n\<\:\/\_]*(\<\/)[a-zA-Z0-9\:\_]*\>)", '', document)

        # To remove any hyperlinks
        document = re.sub(r"(http|https):(\/{2})(www\.)([a-zA-z0-9]*\.([a-z]*)(\.)*)", '', document)
        document = re.sub(r"(http|https):(\/{2}[a-zA-Z0-9\.\-\/\:\?\=]*)", '', document)

        # To remove error string like in bug_id:99873
        # (e.g-line: 62\n\tServerTypeDefinitionUtil.getServerClassPathEntry)
        document = re.sub(
            r"(line\:\s[0-9]*([\\n\\t])*([a-zA-Z0-9\(\)\$\[\]\\n\\t\s]*\.[a-zA-Z0-9\(\)\,\\n\[\]\s\$\_]*\))*)",
            '', document)

        # To remove the org. from error eg(org.eclipse.ui.internal.Workbench.createAndRunWorkbench(Workbench.java:366))
        document = re.sub(r"((\()*(org|sun|java|junit|e.g)\.[a-zA-Z0-9\.\$\(\:\s\-\,\_\\\<\>]*(\)+|))", '', document)

        # To remove string like 'Log: Wed Jun 06 12:51:50 EDT 2001'
        document = re.sub(r"(Log\:[a-zA-Z0-9\s\:]+([0-9]{4}))", '', document)

        # To remove strings like /usr/lib/libthread.so.1  (bug_id:33431)
        document = re.sub(r"((\/opt|\/usr)\/[a-zA-Z0-9\/\.\_\,\-]*)", '', document)

        # To remove hexadecimal numbers (bug_id:33431)
        document = re.sub(r"(0[xX][a-fA-F0-9]+)", '', document)

        # To remove cpp,c,java code
        document = re.sub(r"((\()*[a-zA-Z]+\.(cpp|java)[a-zA-Z0-9\:\\n\#\s\<\>\;\(\,\*\)\{\"\/\+\.\-\_\\n\=]*(\})*)",
                          '', document)

        # To remove text between {}
        document = re.sub(r"(\{[a-zA-Z0-9\s\(\)\\n\\t\{\:\<\-\>\=\'\[\]\"\|\*\.\;\,\?]+\})", '', document)

        # To remove testcase(check bug report no:99844)
        document = re.sub(r"(Testcase\:.*\})", '', document)

        # To remove all text within () or [] or <>
        document = re.sub(
            r"(\([a-zA-Z0-9\s\+\*\.\,\<\-\>\?\\n\-\'\_\/\$\[\]\(\"\:\#\;\%\!]*\)+|(\[[a-zA-Z0-9\s\:]*\])|(\<[a-zA-Z0-9\_\.\s\:\<\,]*\>+))",
            '', document)

        # To remove alphanumeric string like 1GE8YMJ:
        document = re.sub(r"([0-9][a-zA-Z0-9]{6}(\:)*)", '', document)

        # To remove string starting with CVS/
        document = re.sub(r"(CVS(\/)*([a-zA-Z]{1,15}\.[a-zA-Z]*)*)", '', document)

        # To remove file name 'org.eclipse.gmt.am3.usecase.osgipluginmanagement.zip'
        document = re.sub(r"(org\.[a-zA-Z0-9\.\$\=\_\(\:\s]*(zip|gz|tar))", '', document)

        # To remove strings like 'Authors: Mathieu Vénisse & Guillaume Doux'
        document = re.sub(r"(Authors\:[\sA-Za-z\u00C0-\u00ff\&]+)", '', document)

        # To remove string 'Best regards' and NOTES:
        document = re.sub(r"((Best regards\,.+\.)|(NOTES\:))", '', document)

        # To remove strings like OS=linux, ARCH=x86
        document = re.sub(r"([A-Z\.]*(\=)+[a-zA-Z0-9\s\.\_]*)", '', document)

        # To remove strings like (- v, - y)
        document = re.sub(r"((\-)+(\s)*[a-zA-Z]\W)", ' ', document)

        # To remove string like ITPVCM:WINNT
        document = re.sub(r"([a-zA-Z]+:[a-zA-Z]+)", '', document)

        # To change words like Don't to Dont
        document = re.sub(r"(\')", '', document)

        # To remove email
        document = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", '', document)

        # To remove windows path
        document = re.sub(r"([a-zA-Z]:[\\]{2}(?:[a-zA-Z0-9\.]+[\\\/]{1,2})*)", '', document)

        # To remove other special chacters
        #         document = re.sub(r"[\-\'\:\?\/\[\]\"\$\>\<\,\!\+\#\*\_\|\;\}\{\(\)]",' ',document) -> replaced with a short regex
        document = re.sub(r"[^a-zA-Z\s]", ' ', document)

        # To remove string like (STACK 0) (bug_id: 88623)
        document = re.sub(r"([A-Z]+\s[0-9]+)", '', document)

        # To remove \\
        document = re.sub(r"(\\){2}", '', document)

        # To remove repetitive characters (bug_id: 170,146)
        document = re.sub(r"\b[\\](\w+)(?:\w+\1\b)+", '', document)

        # To remove all spaces greater than 2
        document = re.sub(r"((\s){2,})", ' ', document)


    except TypeError:
        print('TypeError for bug id: ', document['bug_id'])
    except DuplicateKeyError:
        print('DuplicateKeyError for bug id: ', document['bug_id'])

    return document


def tokenize(document):
    tokens = wordpunct_tokenize(document)

    return tokens


def removeStopwords(tokens):
    tokens_without_sw = [word.lower() for word in tokens if not word in stopwords.words()]

    return tokens_without_sw


def wordStemming(tokens):
    snow_stemmer = SnowballStemmer(language='english')
    stem_words = [snow_stemmer.stem(word) for word in tokens]

    return stem_words


def processDocument(document, use_word_stemming=2):
    content_of_interest = document['description'] + document['short_desc']  # COI

    cleanedCOI = cleaning(content_of_interest)
    tokenized_COI = tokenize(cleanedCOI)
    COI_without_sw = removeStopwords(tokenized_COI)
    if use_word_stemming == 1:
        return wordStemming(COI_without_sw)
    return COI_without_sw
