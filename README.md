# News-Article-Text Summarizer GUI Application using Tkinter
## Overview

This application provides a graphical user interface (GUI) to summarize text from different sources, including URLs and PDF files. It uses the Hugging Face's facebook/bart-large-cnn model to generate text summaries based on the provided input. The application also includes options to fetch text from URLs, load PDF files, and generate summaries through a user-friendly interface.


## Features

* Fetch Text from URL: The user can input a URL, and the application fetches the content of the article for summarization.
* Load PDF: The user can load a PDF file, and the application will extract the text for summarization.
* Summarization: The user can click the "Summarize" button to generate a summary of the provided text.
* Text Display: The application displays both the original text and the generated summary in scrollable text fields.


## Technologies Used

* Tkinter: Python's built-in library for creating desktop applications with GUIs.
* Transformers (Hugging Face): The facebook/bart-large-cnn model is used to generate summaries.
* Newspaper3k: A Python library used to extract articles from URLs.
* PyPDF2: A Python library used to extract text from PDF files.
