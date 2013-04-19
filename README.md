Twitter--The-spread-of-truth-and-debunking.
===========================================

A python sketch that works with the user to characterise tweets for journalistic integrity, and assess their spread.

!!! This is an experiment for University Homework. Not ready to be used in production. Real conclusions should not be drawn.

I'm pushing it now in the hope of getting feedback on the process, code and ideas.
 Cheers, 
 Fergus Pitt


Question: What happened with various entities' reports of various news stories about the suspects in Boston Bombing?


- What was the difference in attention between assertion and corrections?
- What was the difference in attention between different entities' statements of the same story?

- Measures of attention for tweets: Retweets, Replies, (These can be either in absolute, or relative to the number of followers)
- Measures of attention for URLs (NOT YET IMPLEMENTED): Links from twitter; bit.ly link metrics

Relevant Ontology of a tweet: Time, AccountHolder (CLASSIFICATION By Brand, Reporter, Govt, SubBrand/Program, Unaffiliated Citizen NOT YET IMPLEMENTED), Number of Replies, Number of RTs, Number of Favorites, content, 
Relevant Ontology of a story: News Event, Attribution (Official, Other Media, Own Sources, Statement), Type (Assertion, Clarification, Retraction, Debunking), Accuracy

Notes: The Ontology of the story will be entered manually, because I think it needs human intelligence. The attribution might want more refining: Should there be differentiation between named, unnamed and official sources?
