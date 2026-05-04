# tf–idf

# tf–idf - Wikipedia

In [information retrieval](https://en.wikipedia.org/wiki/Information_retrieval "Information retrieval"), tf–idf (also TFIDF, TFIDF, TF–IDF, or Tf–idf), short for term frequency–inverse document frequency, is a measure of importance of a word to a [document](https://en.wikipedia.org/wiki/Document "Document") in a collection or [corpus](https://en.wikipedia.org/wiki/Text_corpus "Text corpus"), adjusted for the fact that some words appear more frequently in general.\[^1\] Like the bag-of-words model, it models a document as a [multiset](https://en.wikipedia.org/wiki/Multiset "Multiset") of words, without [word order](https://en.wikipedia.org/wiki/Word_order "Word order"). It is a refinement over the simple [bag-of-words model](https://en.wikipedia.org/wiki/Bag-of-words_model "Bag-of-words model"), by allowing the weight of words to depend on the rest of the corpus.

It was often used as a [weighting factor](https://en.wikipedia.org/wiki/Weighting_factor "Weighting factor") in searches of information retrieval, [text mining](https://en.wikipedia.org/wiki/Text_mining "Text mining"), and [user modeling](https://en.wikipedia.org/wiki/User_modeling "User modeling"). A survey conducted in 2015 showed that 83% of text-based recommender systems in digital libraries used tf–idf.\[^2\] Variations of the tf–idf weighting scheme were often used by [search engines](https://en.wikipedia.org/wiki/Search_engine "Search engine") as a central tool in scoring and ranking a document's [relevance](https://en.wikipedia.org/wiki/Relevance\_\\(information_retrieval\\) "Relevance (information retrieval)") given a user [query](https://en.wikipedia.org/wiki/Information_retrieval "Information retrieval").

One of the simplest [ranking functions](https://en.wikipedia.org/wiki/Ranking_function "Ranking function") is computed by summing the tf–idf for each query term; many more sophisticated ranking functions are variants of this simple model.

[Karen Spärck Jones](https://en.wikipedia.org/wiki/Karen_Sp%C3%A4rck_Jones "Karen Spärck Jones") (1972) conceived a statistical interpretation of term-specificity called Inverse Document Frequency (idf), which became a cornerstone of term weighting:\[^3\]

> The specificity of a term can be quantified as an inverse function of the number of documents in which it occurs.

For example, the df (document frequency) and idf for some words in Shakespeare's 37 plays are as follows:\[^4\]

| Word | df | idf | 
|---|---|---|
| Romeo | 1 | 1\.57 | 
| salad | 2 | 1\.27 | 
| Falstaff | 4 | 0\.967 | 
| forest | 12 | 0\.489 | 
| battle | 21 | 0\.246 | 
| wit | 34 | 0\.037 | 
| fool | 36 | 0\.012 | 
| good | 37 | 0 | 
| sweet | 37 | 0 | 

We see that "[Romeo](https://en.wikipedia.org/wiki/Romeo "Romeo")", "[Falstaff](https://en.wikipedia.org/wiki/John_Falstaff "John Falstaff")", and "salad" appears in very few plays, so seeing these words, one could get a good idea as to which play it might be. In contrast, "good" and "sweet" appears in every play and are completely uninformative as to which play it is.

1. The tf–idf is the product of two statistics, term frequency and inverse document frequency. There are various ways for determining the exact values of both statistics.

2. A formula that aims to define the importance of a keyword or phrase within a document or a web page.

| weighting scheme | tf weight | 
|---|---|
| binary | ${displaystyle {0,1}}$ | 
| raw count | ${displaystyle f_{t,d}}$ | 
| term frequency | ${displaystyle f_{t,d}{Bigg /}{sum _{t'in d}{f_{t',d}}}}$ | 
| log normalization | ${displaystyle log(1+f_{t,d})}$ | 
| double normalization 0.5 | ${displaystyle 0.5+0.5cdot {frac {f_{t,d}}{max _{{t'in d}}{f_{t',d}}}}}$ | 
| double normalization K | ${displaystyle K+(1-K){frac {f_{t,d}}{max _{{t'in d}}{f_{t',d}}}}}$ | 

Term frequency, tf(t,d), is the relative frequency of term t within document d,

${displaystyle mathrm {tf} (t,d)={frac {f_{t,d}}{sum _{t'in d}{f_{t',d}}}}}$ ,

where f<sub><i>t</i>,<i>d</i></sub> is the raw count of a term in a document, i.e., the number of times that term t occurs in document d. Note the denominator is simply the total number of terms in document d (counting each occurrence of the same term separately). There are various other ways to define term frequency:\[^5\]

- the raw count itself: tf(t,d) = f<sub><i>t</i>,<i>d</i></sub>

- [Boolean](https://en.wikipedia.org/wiki/Boolean_data_type "Boolean data type") "frequencies": tf(t,d) = 1 if t occurs in d and 0 otherwise;

- [logarithmically scaled](https://en.wikipedia.org/wiki/Logarithmic_scale "Logarithmic scale") frequency: tf(t,d) = log (1 + f<sub><i>t</i>,<i>d</i></sub>);\[^6\]

- augmented frequency, to prevent a bias towards longer documents, e.g. raw frequency divided by the raw frequency of the most frequently occurring term in the document:

${displaystyle mathrm {tf} (t,d)=0.5+0.5cdot {frac {f_{t,d}}{max{f_{t',d}:t'in d}}}}$

## Inverse Document Frequency

| weighting scheme | idf weight ( ${displaystyle n\_{t}= | {din D:tin d} | }$ ) | 
|---|---|---|---|
| unary | 1 |  |  | 
| inverse document frequency | ${displaystyle log {frac {N}{n_{t}}}=-log {frac {n_{t}}{N}}}$ |  |  | 
| inverse document frequency smooth | ${displaystyle log left({frac {N}{1+n_{t}}}right)+1}$ |  |  | 
| inverse document frequency max | ${displaystyle log left({frac {max _{{t'in d}}n_{t'}}{1+n_{t}}}right)}$ |  |  | 
| [probabilistic](probabilistic) inverse document frequency | ${displaystyle log {frac {N-n_{t}}{n_{t}}}}$ |  |  | 

The inverse document frequency is a measure of how much information the word provides, i.e., how common or rare it is across all documents. It is the [logarithmically scaled](https://en.wikipedia.org/wiki/Logarithmic_scale "Logarithmic scale") inverse fraction of the documents that contain the word (obtained by dividing the total number of documents by the number of documents containing the term, and then taking the logarithm of that quotient):

${displaystyle mathrm {idf} (t,D)=log {frac {N}{|{d:din D{text{ and }}tin d}|}}}$

with

![31508eed6b8224f99b186e5115ddf49b_MD5.png](31508eed6b8224f99b186e5115ddf49b_MD5.png)

Plot of different inverse document frequency functions: standard, smooth, [probabilistic](probabilistic).

## Term frequency–inverse Document Frequency

| weighting scheme | [tf-idf](tf-idf) | 
|---|---|
| count-idf | ${displaystyle f_{t,d}cdot log {frac {N}{n_{t}}}}$ | 
| double normalization-idf | ${displaystyle left(0.5+0.5{frac {f_{t,q}}{max _{t}f_{t,q}}}right)cdot log {frac {N}{n_{t}}}}$ | 
| log normalization-idf | ${displaystyle (1+log f_{t,d})cdot log {frac {N}{n_{t}}}}$ | 

Then tf–idf is calculated as

${displaystyle mathrm {tfidf} (t,d,D)=mathrm {tf} (t,d)cdot mathrm {idf} (t,D)}$

A high weight in tf–idf is reached by a high term [frequency](https://en.wikipedia.org/wiki/Frequency\_\\(statistics\\) "Frequency (statistics)") (in the given document) and a low document frequency of the term in the whole collection of documents; the weights hence tend to filter out common terms. Since the ratio inside the idf's log function is always greater than or equal to 1, the value of idf (and tf–idf) is greater than or equal to 0. As a term appears in more documents, the ratio inside the logarithm approaches 1, bringing the idf and tf–idf closer to 0.

# Justification of Idf

Idf was introduced as "term specificity" by [Karen Spärck Jones](https://en.wikipedia.org/wiki/Karen_Sp%C3%A4rck_Jones "Karen Spärck Jones") in a 1972 paper. Although it has worked well as a [heuristic](https://en.wikipedia.org/wiki/Heuristic "Heuristic"), its theoretical foundations have been troublesome for at least three decades afterward, with many researchers trying to find [information theoretic](https://en.wikipedia.org/wiki/Information_theory "Information theory") justifications for it.\[^understanding-7\]

Spärck Jones's own explanation did not propose much theory, aside from a connection to [Zipf's law](https://en.wikipedia.org/wiki/Zipf%27s_law "Zipf's law").\[^understanding-7\] Attempts have been made to put idf on a \[[probabilistic](probabilistic)\](<https://en.wikipedia.org/wiki/Probability_theory> "Probability theory") footing,\[^8\] by estimating the probability that a given document d contains a term t as the relative document frequency,

${displaystyle P(t|D)={frac {|{din D:tin d}|}{N}},}$

so that we can define idf as

${displaystyle {begin{aligned}mathrm {idf} &=-log P(t|D)&=log {frac {1}{P(t|D)}}&=log {frac {N}{|{din D:tin d}|}}end{aligned}}}$

Namely, the inverse document frequency is the logarithm of "inverse" relative document frequency.

This [probabilistic](probabilistic) interpretation in turn takes the same form as that of [self-information](https://en.wikipedia.org/wiki/Self-information "Self-information"). However, applying such information-theoretic notions to problems in information retrieval leads to problems when trying to define the appropriate [event spaces](https://en.wikipedia.org/wiki/Event_space "Event space") for the required [probability distributions](https://en.wikipedia.org/wiki/Probability_distribution "Probability distribution"): not only documents need to be taken into account, but also queries and terms.\[^understanding-7\]

# Link with Information Theory

Both term frequency and inverse document frequency can be formulated in terms of [information theory](https://en.wikipedia.org/wiki/Information_theory "Information theory"); it helps to understand why their product has a meaning in terms of joint informational content of a document. A characteristic assumption about the distribution ${displaystyle p(d,t)}$ is that:

${displaystyle p(d|t)={frac {1}{|{din D:tin d}|}}}$

This assumption and its implications, according to Aizawa: "represent the heuristic that tf–idf employs."\[^aizawa_2003_45%e2%80%9365-9\]

The [conditional entropy](https://en.wikipedia.org/wiki/Conditional_entropy "Conditional entropy") of a "randomly chosen" document in the corpus ${displaystyle D}$ , conditional to the fact it contains a specific term ${displaystyle t}$ (and assuming that all documents have equal probability to be chosen) is:

${displaystyle H({cal {D}}|{cal {T}}=t)=-sum _{d}p_{d|t}log p_{d|t}=-log {frac {1}{|{din D:tin d}|}}=log {frac {|{din D:tin d}|}{|D|}}+log |D|=-mathrm {idf} (t)+log |D|}$

In terms of notation, ${displaystyle {cal {D}}}$ and ${displaystyle {cal {T}}}$ are "random variables" corresponding to respectively draw a document or a term. The [mutual information](https://en.wikipedia.org/wiki/Mutual_information "Mutual information") can be expressed as

${displaystyle M({cal {T}};{cal {D}})=H({cal {D}})-H({cal {D}}|{cal {T}})=sum _{t}p_{t}cdot (H({cal {D}})-H({cal {D}}|W=t))=sum _{t}p_{t}cdot mathrm {idf} (t)}$

The last step is to expand ${displaystyle p_{t}}$ , the unconditional probability to draw a term, with respect to the (random) choice of a document, to obtain:

${displaystyle M({cal {T}};{cal {D}})=sum _{t,d}p_{t|d}cdot p_{d}cdot mathrm {idf} (t)=sum _{t,d}mathrm {tf} (t,d)cdot {frac {1}{|D|}}cdot mathrm {idf} (t)={frac {1}{|D|}}sum _{t,d}mathrm {tf} (t,d)cdot mathrm {idf} (t).}$

This expression shows that summing the Tf–idf of all possible terms and documents recovers the mutual information between documents and term taking into account all the specificities of their joint distribution.\[^aizawa_2003_45%e2%80%9365-9\] Each Tf–idf hence carries the "bit of information" attached to a term x document pair.

Suppose that we have term count tables of a corpus consisting of only two documents, as listed on the right.

| Term | Term Count | 
|---|---|
| this | 1 | 
| is | 1 | 
| another | 2 | 
| example | 3 | 



| Term | Term Count | 
|---|---|
| this | 1 | 
| is | 1 | 
| a | 2 | 
| sample | 1 | 

The calculation of tf–idf for the term "this" is performed as follows:

In its raw frequency form, tf is just the frequency of the "this" for each document. In each document, the word "this" appears once; but as the document 2 has more words, its relative frequency is smaller.

${displaystyle mathrm {tf} ({mathsf {''this''}},d_{1})={frac {1}{5}}=0.2}$

${displaystyle mathrm {tf} ({mathsf {''this''}},d_{2})={frac {1}{7}}approx 0.14}$

An idf is constant per corpus, and accounts for the ratio of documents that include the word "this". In this case, we have a corpus of two documents and all of them include the word "this".

${displaystyle mathrm {idf} ({mathsf {''this''}},D)=log left({frac {2}{2}}right)=0}$

So tf–idf is zero for the word "this", which implies that the word is not very informative as it appears in all documents.

${displaystyle mathrm {tfidf} ({mathsf {''this''}},d_{1},D)=0.2times 0=0}$

${displaystyle mathrm {tfidf} ({mathsf {''this''}},d_{2},D)=0.14times 0=0}$

The word "example" is more interesting - it occurs three times, but only in the second document:

${displaystyle mathrm {tf} ({mathsf {''example''}},d_{1})={frac {0}{5}}=0}$

${displaystyle mathrm {tf} ({mathsf {''example''}},d_{2})={frac {3}{7}}approx 0.429}$

${displaystyle mathrm {idf} ({mathsf {''example''}},D)=log left({frac {2}{1}}right)=0.301}$

Finally,

${displaystyle mathrm {tfidf} ({mathsf {''example''}},d_{1},D)=mathrm {tf} ({mathsf {''example''}},d_{1})times mathrm {idf} ({mathsf {''example''}},D)=0times 0.301=0}$

${displaystyle mathrm {tfidf} ({mathsf {''example''}},d_{2},D)=mathrm {tf} ({mathsf {''example''}},d_{2})times mathrm {idf} ({mathsf {''example''}},D)=0.429times 0.301approx 0.129}$

(using the [base 10 logarithm](https://en.wikipedia.org/wiki/Base_10_logarithm "Base 10 logarithm")).

The idea behind tf–idf also applies to entities other than terms. In 1998, the concept of idf was applied to citations.\[^10\] The authors argued that "if a very uncommon citation is shared by two documents, this should be weighted more highly than a citation made by a large number of documents". In addition, tf–idf was applied to "visual words" with the purpose of conducting object matching in videos,\[^11\] and entire sentences.\[^12\] However, the concept of tf–idf did not prove to be more effective in all cases than a plain tf scheme (without idf). When tf–idf was applied to citations, researchers could find no improvement over a simple citation-count weight that had no idf component.\[^13\]

A number of term-weighting schemes have derived from tf–idf. One of them is TF–PDF (term frequency proportional document frequency).\[^14\] TF–PDF was introduced in 2001 in the context of identifying emerging topics in the media. The PDF component measures the difference of how often a term occurs in different domains. Another derivate is TF–IDuF. In TF–IDuF,\[^15\] idf is not calculated based on the document corpus that is to be searched or recommended. Instead, idf is calculated on users' personal document collections. The authors report that TF–IDuF was equally effective as tf–idf but could also be applied in situations when, e.g., a user modeling system has no access to a global document corpus.

- [Word embedding](https://en.wikipedia.org/wiki/Word_embedding "Word embedding")

- [Kullback–Leibler divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence "Kullback–Leibler divergence")

- [Latent Dirichlet allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation "Latent Dirichlet allocation")

- [Latent semantic analysis](https://en.wikipedia.org/wiki/Latent_semantic_analysis "Latent semantic analysis")

- [Mutual information](https://en.wikipedia.org/wiki/Mutual_information "Mutual information")

- [Noun phrase](https://en.wikipedia.org/wiki/Noun_phrase "Noun phrase")

- [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25 "Okapi BM25")

- [PageRank](https://en.wikipedia.org/wiki/PageRank "PageRank")

- [Vector space model](https://en.wikipedia.org/wiki/Vector_space_model "Vector space model")

- [Word count](https://en.wikipedia.org/wiki/Word_count "Word count")

- [SMART Information Retrieval System](https://en.wikipedia.org/wiki/SMART_Information_Retrieval_System "SMART Information Retrieval System")

\[^1\]: Rajaraman, A.; Ullman, J.D. (2011). ["Data Mining"](http://i.stanford.edu/\~ullman/mmds/ch1.pdf) (PDF). Mining of Massive Datasets. pp. 1–17. [doi](https://en.wikipedia.org/wiki/Doi\_\\(identifier\\) "Doi (identifier)"):[10\.1017/CBO9781139058452.002](https://doi.org/10.1017%2FCBO9781139058452.002). [ISBN](https://en.wikipedia.org/wiki/ISBN\_\\(identifier\\) "ISBN (identifier)") [978-1-139-05845-2](https://en.wikipedia.org/wiki/Special:BookSources/978-1-139-05845-2 "Special:BookSources/978-1-139-05845-2").

\[^2\]: Breitinger, Corinna; Gipp, Bela; Langer, Stefan (2015-07-26). ["Research-paper recommender systems: a literature survey"](http://nbn-resolving.de/urn:nbn:de:bsz:352-0-311312). International Journal on Digital Libraries. 17 (4): 305–338. [doi](https://en.wikipedia.org/wiki/Doi\_\\(identifier\\) "Doi (identifier)"):[10\.1007/s00799-015-0156-0](https://doi.org/10.1007%2Fs00799-015-0156-0). [ISSN](https://en.wikipedia.org/wiki/ISSN\_\\(identifier\\) "ISSN (identifier)") [1432-5012](https://search.worldcat.org/issn/1432-5012). [S2CID](https://en.wikipedia.org/wiki/S2CID\_\\(identifier\\) "S2CID (identifier)") [207035184](https://api.semanticscholar.org/CorpusID:207035184).

\[^3\]: [Spärck Jones, K.](https://en.wikipedia.org/wiki/Karen_Sp%C3%A4rck_Jones "Karen Spärck Jones") (1972). "A Statistical Interpretation of Term Specificity and Its Application in Retrieval". Journal of Documentation. 28 (1): 11–21. [CiteSeerX](https://en.wikipedia.org/wiki/CiteSeerX\_\\(identifier\\) "CiteSeerX (identifier)") [10\.1.1.115.8343](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.115.8343). [doi](https://en.wikipedia.org/wiki/Doi\_\\(identifier\\) "Doi (identifier)"):[10\.1108/eb026526](https://doi.org/10.1108%2Feb026526). [S2CID](https://en.wikipedia.org/wiki/S2CID\_\\(identifier\\) "S2CID (identifier)") [2996187](https://api.semanticscholar.org/CorpusID:2996187).

\[^4\]: Speech and Language Processing (3rd ed. draft), Dan Jurafsky and James H. Martin, chapter 14.<https://web.stanford.edu/>~~jurafsky/slp3/14.pdf~~

\[^5\]: Manning, C.D.; Raghavan, P.; Schutze, H. (2008). ["Scoring, term weighting, and the vector space model"](http://nlp.stanford.edu/IR-book/pdf/06vect.pdf) (PDF). Introduction to Information Retrieval. p. 100. [doi](https://en.wikipedia.org/wiki/Doi\_\\(identifier\\) "Doi (identifier)"):[10\.1017/CBO9780511809071.007](https://doi.org/10.1017%2FCBO9780511809071.007). [ISBN](https://en.wikipedia.org/wiki/ISBN\_\\(identifier\\) "ISBN (identifier)") [978-0-511-80907-1](https://en.wikipedia.org/wiki/Special:BookSources/978-0-511-80907-1 "Special:BookSources/978-0-511-80907-1").

\[^6\]: ["TFIDF statistics | SAX-VSM"](https://jmotif.github.io/sax-vsm_site/morea/algorithm/TFIDF.html).

\[^understanding-7\]: [Robertson, S.](https://en.wikipedia.org/wiki/Stephen_Robertson\_\\(computer_scientist\\) "Stephen Robertson (computer scientist)") (2004). "Understanding inverse document frequency: On theoretical arguments for IDF". Journal of Documentation. 60 (5): 503–520. [doi](https://en.wikipedia.org/wiki/Doi\_\\(identifier\\) "Doi (identifier)"):[10\.1108/00220410410560582](https://doi.org/10.1108%2F00220410410560582).

\[^8\]: See also [Probability estimates in practice](http://nlp.stanford.edu/IR-book/html/htmledition/probability-estimates-in-practice-1.html#p:justificationofidf) in Introduction to Information Retrieval.

\[^10\]: Bollacker, Kurt D.; Lawrence, Steve; Giles, C. Lee (1998-01-01). "CiteSeer". Proceedings of the second international conference on Autonomous agents - AGENTS '98. pp. 116–123. [doi](https://en.wikipedia.org/wiki/Doi\_\\(identifier\\) "Doi (identifier)"):[10\.1145/280765.280786](https://doi.org/10.1145%2F280765.280786). [ISBN](https://en.wikipedia.org/wiki/ISBN\_\\(identifier\\) "ISBN (identifier)") [978-0-89791-983-8](https://en.wikipedia.org/wiki/Special:BookSources/978-0-89791-983-8 "Special:BookSources/978-0-89791-983-8"). [S2CID](https://en.wikipedia.org/wiki/S2CID\_\\(identifier\\) "S2CID (identifier)") [3526393](https://api.semanticscholar.org/CorpusID:3526393).

\[^11\]: Sivic, Josef; Zisserman, Andrew (2003-01-01). "Video Google: A text retrieval approach to object matching in videos". [Proceedings Ninth IEEE International Conference on Computer Vision](http://dl.acm.org/citation.cfm?id=946247.946751). ICCV '03. pp. 1470–. [doi](https://en.wikipedia.org/wiki/Doi\_\\(identifier\\) "Doi (identifier)"):[10\.1109/ICCV.2003.1238663](https://doi.org/10.1109%2FICCV.2003.1238663). [ISBN](https://en.wikipedia.org/wiki/ISBN\_\\(identifier\\) "ISBN (identifier)") [978-0-7695-1950-0](https://en.wikipedia.org/wiki/Special:BookSources/978-0-7695-1950-0 "Special:BookSources/978-0-7695-1950-0"). [S2CID](https://en.wikipedia.org/wiki/S2CID\_\\(identifier\\) "S2CID (identifier)") [14457153](https://api.semanticscholar.org/CorpusID:14457153).

\[^12\]: Seki, Yohei. ["Sentence Extraction by tf/idf and Position Weighting from Newspaper Articles"](http://research.nii.ac.jp/ntcir/workshop/OnlineProceedings3/NTCIR3-TSC-SekiY.pdf) (PDF). National Institute of Informatics.

\[^13\]: Beel, Joeran; Breitinger, Corinna (2017). ["Evaluating the CC-IDF citation-weighting scheme – How effectively can 'Inverse Document Frequency' (IDF) be applied to references?"](https://web.archive.org/web/20200922150304/http://beel.org/publications/2017%20iConference%20--%20Evaluating%20the%20CC-IDF%20citation-weighting%20scheme%20--%20preprint.pdf) (PDF). Proceedings of the 12th IConference. Archived from [the original](http://beel.org/publications/2017%20iConference%20--%20Evaluating%20the%20CC-IDF%20citation-weighting%20scheme%20--%20preprint.pdf) (PDF) on 2020-09-22. Retrieved 2017-01-29.

\[^14\]: Khoo Khyou Bun; Bun, Khoo Khyou; Ishizuka, M. (2001). "Emerging Topic Tracking System". Proceedings Third International Workshop on Advanced Issues of E-Commerce and Web-Based Information Systems. WECWIS 2001. pp. 2–11. [CiteSeerX](https://en.wikipedia.org/wiki/CiteSeerX\_\\(identifier\\) "CiteSeerX (identifier)") [10\.1.1.16.7986](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.16.7986). [doi](https://en.wikipedia.org/wiki/Doi\_\\(identifier\\) "Doi (identifier)"):[10\.1109/wecwis.2001.933900](https://doi.org/10.1109%2Fwecwis.2001.933900). [ISBN](https://en.wikipedia.org/wiki/ISBN\_\\(identifier\\) "ISBN (identifier)") [978-0-7695-1224-2](https://en.wikipedia.org/wiki/Special:BookSources/978-0-7695-1224-2 "Special:BookSources/978-0-7695-1224-2"). [S2CID](https://en.wikipedia.org/wiki/S2CID\_\\(identifier\\) "S2CID (identifier)") [1049263](https://api.semanticscholar.org/CorpusID:1049263).

\[^15\]: Langer, Stefan; Gipp, Bela (2017). ["TF-IDuF: A Novel Term-Weighting Scheme for User Modeling based on Users' Personal Document Collections"](https://www.gipp.com/wp-content/papercite-data/pdf/beel17.pdf) (PDF). IConference.

- [Salton, G](https://en.wikipedia.org/wiki/Gerard_Salton "Gerard Salton"); McGill, M. J. (1986). [Introduction to modern information retrieval](https://archive.org/details/introductiontomo00salt). [McGraw-Hill](https://en.wikipedia.org/wiki/McGraw-Hill "McGraw-Hill"). [ISBN](https://en.wikipedia.org/wiki/ISBN\_\\(identifier\\) "ISBN (identifier)") [978-0-07-054484-0](https://en.wikipedia.org/wiki/Special:BookSources/978-0-07-054484-0 "Special:BookSources/978-0-07-054484-0").

- [Salton, G.](https://en.wikipedia.org/wiki/Gerard_Salton "Gerard Salton"); Fox, E. A.; Wu, H. (1983). "Extended Boolean information retrieval". Communications of the ACM. 26 (11): 1022–1036. [doi](https://en.wikipedia.org/wiki/Doi\_\\(identifier\\) "Doi (identifier)"):[10\.1145/182.358466](https://doi.org/10.1145%2F182.358466). [hdl](https://en.wikipedia.org/wiki/Hdl\_\\(identifier\\) "Hdl (identifier)"):[1813/6351](https://hdl.handle.net/1813%2F6351). [S2CID](https://en.wikipedia.org/wiki/S2CID\_\\(identifier\\) "S2CID (identifier)") [207180535](https://api.semanticscholar.org/CorpusID:207180535).

- [Salton, G.](https://en.wikipedia.org/wiki/Gerard_Salton "Gerard Salton"); Buckley, C. (1988). ["Term-weighting approaches in automatic text retrieval"](https://ecommons.cornell.edu/bitstream/1813/6721/1/87-881.pdf) (PDF). Information Processing & Management. 24 (5): 513–523. [doi](https://en.wikipedia.org/wiki/Doi\_\\(identifier\\) "Doi (identifier)"):[10\.1016/0306-4573(88)90021-0](https://doi.org/10.1016%2F0306-4573%2888%2990021-0). [hdl](https://en.wikipedia.org/wiki/Hdl\_\\(identifier\\) "Hdl (identifier)"):[1813/6721](https://hdl.handle.net/1813%2F6721). [S2CID](https://en.wikipedia.org/wiki/S2CID\_\\(identifier\\) "S2CID (identifier)") [7725217](https://api.semanticscholar.org/CorpusID:7725217).

- Wu, H. C.; Luk, R.W.P.; Wong, K.F.; Kwok, K.L. (2008). "Interpreting [TF-IDF](TF-IDF) term weights as making relevance decisions". ACM Transactions on Information Systems. 26 (3): 1. [doi](https://en.wikipedia.org/wiki/Doi\_\\(identifier\\) "Doi (identifier)"):[10\.1145/1361684.1361686](https://doi.org/10.1145%2F1361684.1361686). [hdl](https://en.wikipedia.org/wiki/Hdl\_\\(identifier\\) "Hdl (identifier)"):[10397/10130](https://hdl.handle.net/10397%2F10130). [S2CID](https://en.wikipedia.org/wiki/S2CID\_\\(identifier\\) "S2CID (identifier)") [18303048](https://api.semanticscholar.org/CorpusID:18303048).

# External Links and Suggested Reading

- [Gensim](https://en.wikipedia.org/wiki/Gensim "Gensim") is a Python library for vector space modeling and includes tf–idf weighting.

- [Anatomy of a search engine](http://www.codeproject.com/KB/IP/AnatomyOfASearchEngine1.aspx)

- [tf–idf and related definitions](https://lucene.apache.org/core/3_6_1/api/all/org/apache/lucene/search/Similarity.html) as used in [Lucene](https://en.wikipedia.org/wiki/Lucene "Lucene")

- [TfidfTransformer](http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html#sklearn.feature_extraction.text.TfidfTransformer) in [scikit-learn](https://en.wikipedia.org/wiki/Scikit-learn "Scikit-learn")

- [Text to Matrix Generator (TMG)](https://www.hpclab.ceid.upatras.gr/tmg/) MATLAB toolbox that can be used for various tasks in text mining (TM) specifically i) indexing, ii) retrieval, iii) dimensionality reduction, iv) clustering, v) classification. The indexing step offers the user the ability to apply local and global weighting methods, including tf–idf.

- [Term-frequency explained](https://www.opinosis-analytics.com/knowledge-base/term-frequency-explained/) Explanation of term-frequency