# JarBeGone - A Text Summarizer For Academic Papers

## Project Description

JarBeGone is a text summarizer that uses Natural Language Processing techniques to make academic papers eacher for students to comprehend. Unlike other summarizers, JarBeGone is designed to handle the complex jargon and formats of academic papers.

The main aspect of JarBeGone is that is uses the TextRank algorithm, outlined in [this paper](https://aclanthology.org/W04-3252/), to generate a summary for the 8 papers included. Each sentence is ranked based on its relevance to the overall ideas of the paper. Then, the top N sentences, where N is determined by the user-selected length, are displayed in order of appearance. This is to preserve the context of the original paper.  

Read more about this project on the University of Washington Bothell Capstone & Symposium website [here](https://uwb-stem.github.io/spring-2022/csse-abstract-page.html?csse-6-100).

## Technologies

JarBeGone was built with:
- Python 3.8
- Flask 2.0.3
- Jinja2 3.0.3
- HTML and CSS
  

## Demonstration

Because JarBeGone is a prototype, installation is not recommended as there are many bugs that may occur. The video below shows a demonstration of the JarBeGone prototype.
Click the image to be redirected to a YouTube video.

[![Image of JarBeGone Home screen](https://i.imgur.com/P4IpDLI.png)](http://www.youtube.com/watch?v=5C65vyYi93Y)



