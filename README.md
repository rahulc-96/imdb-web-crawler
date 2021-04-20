# IMDB Web Crawler

Web crawlers are computer programs often referred to as spider-bots or crawlers that automatically scans documents on the web to generate structured data from unstructured sources. Web crawlers are most commonly used by search engines for creating indexes on other web pages, mining data for research purposes or monitoring sytems that keeps track of trends in product prices or reviews.

IMDB-WEB-CRALWER named as PersusBetaSpider is developed using Python's Scrapy framework. The crawler scraps relevant details corresponding to the top 250 movies on IMDB, generates a JSON payload with scraped data for each movie and publishes the data to a compacted kafka topic. The kafka topic can in turn be used as a source for dumping the data to other database systems like Postgres or ElasticSearch for querying or visualizing the collected data. 

# Pre-Requsites
- Python
- Scrapy
- Anaconda
- Apache Kafka

# Setting up Scrapy using Anaconda

[Anaconda](https://www.anaconda.com/) is a distribution of the Python and R programming languages for scientific computing (data science, machine learning applications, large-scale data processing, predictive analytics, etc.), that aims to simplify package management and deployment. The distribution includes data-science packages suitable for Windows, Linux, and macOS.

Conda is the package manager for Anaconda that is reponsible for installing or updating packages and associated dependencies. The big difference between `pip` package manager and Conda is the way in which package dependencies are handled. Unlike pip, Conda is able to analyse the existing environment and works out how gracefully packages can be installed or upgraded without introducing conflicts.

Anaconda also offers Anaconda-navigator, a GUI included in Anaconda distribution that allows users to launch applications and manage conda packages, environments and channels without using command-line commands. Navigator can search for packages on Anaconda Cloud or in a local Anaconda Repository, install them in an environment, run the packages and update them. Anaconda comes bundled with a free intergrated development environment, [Spyder IDE](https://www.spyder-ide.org/) or the Scientific Python Development Environment. It includes extensive editing, interactive testing, debugging, and introspection features. 

Using Anaconda-Navigator, we can easily setup a new environment say "ScrapyEnvironmemnt" with desired python version and get Scrapy or any other packages that will be required as part of web-crawler development installed on to this environment. It is recommended to create a separate environment as this helps us to easily manage packages and dependencies without resulting in conflicts with system level packages.

Conda's `activate` command can be used to launch the ScrapyEnvironment that we just created for web-crawler development. From this virtual environment we will be able to take full advantage of the various functionalies offered by Scrapy's command-line tool to setup project directory, use interactive shell for testing out Scrapy Selectors for extracting data from web pages and finally initiate crawls.

```sh
 conda activate ScrapyEnvironment
```

 Scrapy's `startproject` command creates a project directory with the given project name, default settings and implementations for core scrapy components. Any custom spider class that we will be implementing as part of this project needs to be placed under the "spider" directory.

```sh
 scrapy startproject <project-name>
 ```

More details on installation steps for Scrapy can be found here: [Scrapy Installation Guide](https://docs.scrapy.org/en/latest/intro/install.html) 

# Basic Scrapy Concepts

## Spider
Spiders are classes which define how a certain site will be scraped, including how to perform the crawl, restrictions that needs to followed by the crawler and how structured data needs to generated from the crawled web pages.

Following are some of the deafult methods and attributes associated with Scrapy's Spider class :
- **name** : A string that defines the name of the spider. The name attribute needs to be unique and will be used by Scrapy to keep track of all the spiders and instantiate them for crawls.
- **allowed_domains** : An optional list of strings containing domains that this spider is allowed to crawl. Requests for URLs not belonging to the domain names specified in this list or their subdomains won’t be followed. This attribute can be used to restrict the links to be followed and thereby ensuring that our spider does not fall to any traps and crawl data endlessly.
- **start_urls** : A list of URLs that Spider will use to intiate the crawl.
- **parse()** : Spider's default callback method for handling responses. It takes Response object obtained from requests to start URLs and either generates an iterable of item objects containing extracted data or more Response objects with links to follow. Any method that needs to be used as a callback must take a Response object as parameter and generate either items which hold relevant data or more Requests objects with links for further scraping. parse() method will be used by Spider as default callback method for handling responses from requests if we have not explicitly provided custom callback method in the corresponding Request objects.
- **start_request()** : Returns a list of requests for the spider to initate the crawl. Scrapy calls it only once, so it is safe to implement start_requests() as a generator.The default implementation generates Request objects for each URL in start_urls list. Hence as a shortcut , its not required to provide an implementation for start_request(), rather assign a list of initial crawl URLs to start_urls attribute and let Spider's own implementation generate Request objects for these URLs with parse() method as the callback method for handling responses.

## Selectors
[Scrapy Selectors](https://docs.scrapy.org/en/latest/topics/selectors.html) as the name suggests are used to select specific part of the HTML document specified by either CSS or Xpath expressions. Scrapy selectors are built upon `parsel` library which in turn uses `lxml` library under the hood for parsing XML documents. 

Xpath expressions are very powerful though its less popular compared to CSS selectors, it can both navigate the structure as well as identify the data. Xpath serves as the foundation of Scrapy Selectors and internally Scrapy converts CSS selectors to Xpath expressions. If we are exracting data by class then its recommended to use CSS selectors as providing Xpath expression to select class elements can be rather verbose. CSS and Xpath selectors can also used in a nested manner since both return same type of Selector objects.

Scrapy offers an interactive shell to try out various combinations of css or xpath selectors to extract data from web pages that about to be scraped. Scrapy shell allows us to easily debug mainly the data extraction part of the code, without having to execute the spider for every change. [Selector Gadget](https://selectorgadget.com/) is a nice tool to quickly find CSS selector for visually selected elements, which works in many browsers.
```sh
 scrapy shell https://www.imdb.com/title/tt0045152/
 In [1]: response.css('.title_wrapper').css('h1::text').get()[:-1]
 Out[1]: "Singin' in the Rain"
```
First Scrapy downloaded the contents of the web page from the given URL and assigned the Response object to a shell variable. Then a CSS selector was used to extract the title of the movie from the response.



