TumblrScraper
=============

Scrape images on tumblr with tags and notes

INSTALL
=======

    $ make requirements

USE
===

There are several ways to use this software.

To scrape image data from the web:

    $ make scrape

To get reference data:

    $ make reference

To train an SVM on reference data using 
__Histogram of Oriented Gradients__ (HOG) features:

    $ make <kind>-reference-hog-svm

To train an SVM on scraped data using HOG features:

    $ make <kind>-scrape-hog-svm
