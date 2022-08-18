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
     - there is no automatic procedure for applying this difference metric​

However, there are several issues and areas of neglect that may arise from this type of methodology:
  * Loanwords and cognates account for many similarities, which may complicate the overall similarity
  * The frequency of words is often not factored into these comparisons
  * Only smaller samples are examined
  * Linguistic domain (the subject of the samples) is not taken into account

Additionally, the methodology of some measures is hidden or unknown. One example is Ethnologue, a pay-walled linguistic reference. 

# Our Proposition and Current Progress
In response to current methods of lexical similarity, we proposed a method that added two details to already established practices
  * When comparing lists of words, we chose to utilize the Levenshtein Distance on pairs of words, but only after the removal of vowels
      - This is due to the observation that consonants are less likely to change between languages
      - e.g. _padre (Spanish)_, _father (English)_, _Vater (German)_ all share similar consonant sounds in p/f/v, d/th/t, and r
  * When collecting samples, we would take linguistic domain into account
      - Linguistic domain can affect how easy it is for a speaker of one language to understand another. An example is that it may be easier for a French speaker to read an English textbook, while they have more difficulty with conversation in a social setting. On the other hand, a German speaker may find reading the textbook more difficult but conversing with others in an everyday context easier. 
      - Between English and French, a good amount of their shared vocabulary is a result of centuries of French influence on English-medium literature and education. Between English and German, the shared vocabulary arises from basic vocabulary, such as words for food or familial relations. 
    



# Links
* Language Conflict Project - https://www.languageconflict.org/
* [Lexical Similarity Presentation (Fall 2021)](https://emailsc-my.sharepoint.com/:p:/g/personal/vdsouza_email_sc_edu/EYujzyTQIQBKsF0oWP0IFGIB5KR9s9LcDZeqY21EFYGxnw?e=yo74IK "Lexical Similarity Presentation (Fall 2021)") 
