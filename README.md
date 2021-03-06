# IMDB Web Crawler

Web crawlers are computer programs often referred to as spider-bots or crawlers that automatically scans documents on the web to generate structured data from unstructured sources. Web crawlers are most commonly used by search engines for creating indexes on other web pages, mining data for research purposes or by monitoring systems that keep track of trends in product prices or reviews.

PersusBetaSpider is a web-crawler developed using Python's Scrapy framework. The crawler extracts relevant details from the top 250 movies on IMDB and publishes the scraped data to a compacted kafka topic. The kafka topic can in turn be used as a source for dumping the data to other database systems like Postgres or ElasticSearch for querying or visualizing the collected data. 

# Pre-Requsites
- Python
- Scrapy
- Anaconda
- Apache Kafka


![techbox](https://user-images.githubusercontent.com/29629955/115445990-31a79f00-a234-11eb-8955-f5ab766ae910.png)


# Setting up Scrapy using Anaconda

[Anaconda](https://www.anaconda.com/) is a distribution of the Python and R programming languages for scientific computing (data science, machine learning applications, large-scale data processing, predictive analytics, etc.), that aims to simplify package management and deployment. The distribution includes data-science packages suitable for Windows, Linux, and macOS.

Conda is the package manager for Anaconda that is responsible for installing or updating packages and associated dependencies. The big difference between `pip` package manager and Conda is the way in which package dependencies are handled. Unlike pip, Conda is able to analyse the existing environment and works out how gracefully packages can be installed or upgraded without introducing conflicts.

Anaconda also offers Anaconda-navigator, a GUI included in Anaconda distribution that allows users to launch applications and manage conda packages, environments and channels without using command-line commands. Navigator can search for packages on Anaconda Cloud or in a local Anaconda Repository, install them in an environment, run the packages and update them. Anaconda comes bundled with a free integrated development environment, [Spyder IDE](https://www.spyder-ide.org/) or the Scientific Python Development Environment, that includes extensive editing, interactive testing, debugging, and introspection features. 

Using Anaconda-Navigator, we can easily setup a new environment "ScrapyEnvironmemnt" with desired python version and get Scrapy or any other packages that will be required as part of web-crawler development installed on to this environment. It is recommended to create a separate environment as this helps us to easily manage packages and dependencies without resulting in conflicts with system level packages.

Conda's `activate` command can be used to launch the ScrapyEnvironment that we just created for web-crawler development. From this virtual environment we will be able to take full advantage of the various functionalities offered by Scrapy's command-line tool to setup project directory, use interactive shell for testing out Scrapy Selectors for extracting data and finally initiate crawls.

```sh
 conda activate ScrapyEnvironment
```

Scrapy's `startproject` command creates a project directory with the given project name, default settings and implementations for core scrapy components. Any custom spider class that we will be implementing as part of this project needs to be placed under the "spider" directory.

```sh
 scrapy startproject <project-name>
 ```

For more details on Scrapy installation and project setup -> [Scrapy Installation Guide](https://docs.scrapy.org/en/latest/intro/install.html)

# Basic Scrapy Concepts

## Spider
Spiders are classes which define how a certain site will be scraped, including how to perform the crawl, restrictions that need to be followed by the crawler and how structured data needs to be generated from the crawled web pages.

Following are some of the default methods and attributes associated with Scrapy's Spider class :
- `name` : A string that defines the name of the spider. Needs to be unique as it will be used by Scrapy to keep track of all the spiders and instantiate them for crawls.
- ``allowed_domains`` : An optional list of strings containing domains that the Spider is allowed to crawl. Requests for URLs not belonging to the domain names specified in this list or their subdomains won’t be followed. This attribute can be used to restrict the links to be followed and thereby ensuring that our spider does not fall to any traps and crawl data endlessly.
- ``start_urls`` : A list of URLs that Spider will use to initiate the crawl.
- ``parse()`` : Spider's default callback method for handling responses. It takes Response objects obtained from requests to start URLs and either generates an iterable of Item objects containing extracted data or more Response objects with links to follow. Any method that needs to be used as a callback in Scrapy must take a Response object as parameter and generate either Item objects that hold relevant data or more Requests objects with links for further scraping. parse() will be used by Spider as the default callback for handling responses if we have not explicitly provided a custom callback in the corresponding Request objects.
- ``start_request()`` : Returns a list of requests for the spider to initiate the crawl. Scrapy calls it only once, so it is safe to implement start_requests() as a generator.The default implementation generates Request objects for each URL in start_urls list. Hence as a shortcut , its not required to provide an implementation for start_request(), rather assign a list of initial crawl URLs to start_urls attribute and let Spider's own implementation generate Request objects for these URLs with parse() as the callback for handling responses.


## Selectors
[Scrapy Selectors](https://docs.scrapy.org/en/latest/topics/selectors.html) as the name suggests are used to select specific parts of the HTML document specified by either CSS or Xpath expressions. Scrapy selectors are built upon `parsel` library which in turn uses `lxml` library under the hood for parsing XML documents. 

Xpath expressions are very powerful though it is less popular compared to CSS selectors, it can both navigate the structure as well as identify the data. Xpath serves as the foundation for Scrapy Selectors and internally Scrapy converts CSS selectors to Xpath expressions. If we are extracting data by class then it is recommended to use CSS selectors as providing Xpath expressions to select class elements can be rather verbose. CSS and Xpath selectors can also be used in a nested manner since both return the same type of Selector objects.

Scrapy offers an interactive shell to try out various combinations of css or xpath selectors to extract data from web pages. Scrapy shell allows us to easily debug mainly the data extraction part of the code, without having to execute the spider for every change. [Selector Gadget](https://selectorgadget.com/) is a nice tool to quickly find CSS selector for visually selected elements, which works in many browsers.


```sh
 scrapy shell https://www.imdb.com/title/tt0045152/
 In [1]: response.css('.title_wrapper').css('h1::text').get()[:-1]
 Out[1]: "Singin' in the Rain"
```
First Scrapy downloads the contents of the web page and assigns the Response object to a shell variable. Then a CSS selector is used to extract the name of the movie


## Items

The main goal of a scraper is to generate structured data from unstructured sources generally web pages. Spider uses Item objects to return the extracted data as key-value pairs. Item is an extension of standard dict-API with few additional features. 

Item allows us to define field names and declare them using Field objects. Field objects are also used to specify meta data to be associated with each field , for example custom serialization methods that will be internally used by Scrapy while processing the data. Item exporters can export scraped objects even if data is not available for all the fields. 

An object in Scrapy is treated as a valid item that can be passed to item-pipelines or feed-exporters for further processing if it is an instance of either Item class or dict class. It is important to note that the Field objects used to declare the item do not stay assigned as class attributes. Instead, they can be accessed through the Item.fields attribute. This restricts the set of allowed field names and prevents typos, raising KeyError when referring to undefined fields.

In Addition to Item class, Scrapy provides two other item types Dataclass and attr.s that work similar to Item, but also allows us to define type and default values for fields.


## Feed-Exporters
One of the most frequently required features when implementing scrapers is being able to store the scraped data properly and, quite often, that means generating an “export file” with the scraped data commonly called “export feed” to be consumed by other systems.

Scrapy provides this functionality out of the box with the Feed Exports, which allows us to generate feeds with scraped items, using multiple serialization formats and storage backends. Common serialization formats supported by Scrapy include Json, JsonLines, CSV and XML. However these formats can be extended via `FEED_EXPORTERS` setting. Scrapy also supports multiple backend storage systems like Google Cloud Storage or Amazon S3, these are defined using URI schemes under the `FEEDS` setting

## Item-Pipeline
An item once scraped by Spider is passed to an Item-pipeline for further processing. Item-Pipeline is a simple Python class that implements a method which takes an Item as parameter and performs appropriate action on the received item, these include cleansing , duplicate checks, validations or persisting to a database. For activating custom pipelines we must add our item-pipeline class name under the `ITEM_PIPELINE` settings. 

Any item-pipeline in Scrapy is required to provide implementation for `process_item()` that handles items scraped by the Spider. The method must return an Item object, a Deferred or raise a DropItem exception. Dropped items are no longer processed by  further pipeline components.

`open_spider()` is executed during Spider start-up for initializing pipeline components whereas `close_spider()` is executed once the Spider has completed its processing and is generally used to clean up resources.

`from_crawler()` is a class method that takes a Crawler object as parameter and returns a new instance of the pipeline. Through the Crawler object, the pipeline can access all the core Scrapy components like settings and signal, eg: accessing database configuration from settings.py file while initializing DB connections during Spider start up, to be later used by the item-pipeline for dumping scraped items to the database.

# Implementation


- Currently PersusBetaSpider supports crawling details for Top 250 movies in IMDB. The crawl is initiated using `https://www.imdb.com/chart/top` as the start_url, that hosts a table containing the Top 250 movies as rated by IMDB users. We have also restricted the crawler's scope by giving only "imdb.com" as part of the allowed_domains attribute.

- `parse()` on receiving response from Top 250 URL will generate subsequent Request objects for each of the 250 movies and assign parseInDetail() as the callback method.

- `parseInDetail()` is responsible for extracting relevant details associated with a movie like title, release date, popularity, rating and so on. This method also generates the follow up Request object for the movie's credits page with parseCast() as the specified callback. 

- `parseCast()` receives a Response object corresponding to the credits page along with meta data containing all the details extracted in the previous step. This callback method returns the final MovieItem object containing all the fields and their values.


- MovieItem objects are handled by a custom item-pipeline with support for publishing data to a kafka topic. `process_item()` converts the received item to a JSON payload before publishing it to the kafka topic. Here the kafka message's value is the JSON payload generated from the MovieItem object whereas the unique IMDB ID associated with the movies serves as the message's key.


Sample MovieItem kafka message:

```json
{
   "director":[
      "Christopher Nolan"
   ],
   "writer":[
      "Jonathan Nolan",
      "Christopher Nolan",
      "Christopher Nolan",
      "David S. Goyer",
      "Bob Kane"
   ],
   "year":2008,
   "producer":[
      "Kevin de la Noy",
      "Jordan Goldberg",
      "Philip Lee",
      "Benjamin Melniker",
      "Christopher Nolan"
   ],
   "genre":"Action,Crime,Drama",
   "@timestamp":"2021-02-28T15:46:05.589Z",
   "title":"The Dark Knight",
   "posterUrl":"https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@.jpg",
   "popularity":"NA",
   "cast":[
      " Christian Bale",
      " Heath Ledger",
      " Aaron Eckhart",
      " Michael Caine",
      " Maggie Gyllenhaal",
      " Gary Oldman",
      " Morgan Freeman"
   ],
   "rating":9,
   "duration":"2h 32min",
   "key":"tt0468569",
   "releaseDate":"18 July 2008 (USA)",
   "cinematographer":[
      "Wally Pfister"
   ]
}
```
For initiating the crawl use the following command, provided all prerequisites are met the spider will be able to scrape data for top 250 movies in IMDB and publish it to the kafka topic provided in the settings.

```sh
scrapy crawl PerseusBetaSpider
```
Alternatively we can disable the custom kafka item-pipeline and just use the spider to generate a feed-export.

```sh
scrapy crawl PerseusBetaSpider-o movies.jl
```

# Visualization

For querying or visualizing the scraped movies data , we can easily leverage the features offered by ELK stack. Logstash can be used to feed the data from the kafka topic to an ElasticSearch instance. Using Kibana, we can easily set up dashboards or perform text based searching. Attached screenshot is an example where movies are retrieved based on an actor’s name.
![Screenshot from 2021-04-19 13-24-04](https://user-images.githubusercontent.com/29629955/115443833-6403cd00-a231-11eb-8307-78e3ffa6a880.png)

# Further Reading:

- ELK stack documentation : https://www.elastic.co/what-is/elk-stack
- Kafka documentation and installation guide : https://kafka.apache.org/
- Scrapy documentation : https://docs.scrapy.org/en/latest/index.html

 







