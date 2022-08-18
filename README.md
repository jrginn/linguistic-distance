# linguistic-distance
Repo of data tools for the Lexical Distance Project

# About
The Lexical Distance Project (LDP) is a part of the Language Conflict Project at the University of South Carolina. The Language Conflict Project aims to understand, investigate, and document various language conflicts around the world. The Lexical Distance Project helps support this goal through development of a lexical similarity methodology. 

# Methodology
Lexical distance is one way to measure similarity between two languages. In simple terms, it is the amount of shared words between languages.

Currently, popular measures of lexical distance involve comparing lists of words between languages. Some processes used to achieve this include:
  * **Binary Classification** - words are either the same or not
     - e.g. _casa (Italian)_ to _casa (Spanish)_ = 1; _house (English)_ to _casa (Spanish)_ = 0
  * **Levenshtein Distance** - number of edits needed to transform word A to word B
     - e.g. _attack (English)_ to _attaque (French)_ = LD of 3
  * **Herrgen-Schmidt Dialecticality Measures** - considers changes in features between phonemes of the same word
     - there is no automatic procedure for applying this difference metric

However, there are several issues and areas of neglect that may arise from this type of methodology:
  * Loanwords and cognates account for many similarities, which may complicate the overall similarity
  * The frequency of words is often not factored into these comparisons
  * Only smaller samples are examined
  * Linguistic domain (the subject of the samples) is not taken into account
  
  Additionally, the methodology of some measures is hidden or unknown. One example is Ethnologue, a pay-walled linguistic reference. 

 ## Examples
 According to Ethnologue, English and German are 60% similar and English and French are 27% similar. Below are two articles, one in German from _Der Spiegel_ and the other in French from _Le Monde_. The French clipping contains more cognates.
 

# Our Proposition 
In response to current methods of lexical similarity, we proposed a method that added several details to already established practices:
  * When comparing lists of words, we chose to utilize the Levenshtein Distance on pairs of words, but only after the removal of vowels
      - This is due to the observation that consonants are less likely to change between languages
      - e.g. _padre (Spanish)_, _father (English)_, _Vater (German)_ all share similar consonant sounds in p/f/v, d/th/t, and r
  * When collecting samples, we would take linguistic domain into account
      - Linguistic domain can affect how easy it is for a speaker of one language to understand another. An example is that it may be easier for a French speaker to read an English textbook, while they have more difficulty with conversation in a social setting. On the other hand, a German speaker may find reading the textbook more difficult but conversing with others in an everyday context easier. 
      - Between English and French, a good amount of their shared vocabulary is a result of centuries of French influence on English-medium literature and education. Between English and German, the shared vocabulary arises from basic vocabulary, such as words for food or familial relations. 
 * Accounting for word frequency
      - If a shared vocabulary between two langauges includes highly-used words, it is more likely that speakers of those languages could better understand each other
 * Accounting for directionality
     - Within a language pair, it may be easier for speakers of language A to understand language B rather than vice versa
     - A language conflict may be worsened by a lopsided ease-of-understanding. If speakers of a disadvantaged language have more difficulty in learning the advantaged language, it will be harder for them to gain the institutional/societal benefits of speaking the advantaged language 
     - For these reasons, our comparisons will be bi-directional (ex: French-German and German-French).
     
# Current Progress
     Our initial analysis involved several documents representative of two genres: (i) legal texts and (ii) scientific texts. All documents were taken from the United Nations Parallel Corpus. An English version of each source document was used to generate child documents in French, German, Russian, and Spanish using Google Translate, which was used in order to obtain the most literal translation of each word into the target language (as human translators often accommodate the nuances of the language they are translating into, leading to translations that obscure words used in the source text). 
     Further into the project, we extended our analytical method to provide a baseline of lexical similarity. Instead of comparing language pairs using sampled text, we performed a context-free comparison, using the 1000 most frequent words in each language to be compared. The languages used in this method were English, French, and Spanish.

##Examples

# Links
* [Language Conflict Project](https://www.languageconflict.org/, "Language Conflict Project")
* [Lexical Similarity Presentation (Fall 2021)](https://emailsc-my.sharepoint.com/:p:/g/personal/vdsouza_email_sc_edu/EYujzyTQIQBKsF0oWP0IFGIB5KR9s9LcDZeqY21EFYGxnw?e=yo74IK "Lexical Similarity Presentation (Fall 2021)") 
* [United Nations Parallel Corpus](https://opus.nlpl.eu/UNPC.php, "United Nations Parallel Corpus")
