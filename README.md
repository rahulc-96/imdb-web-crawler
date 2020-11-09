# imdb-web-crawler

A Pyhon Spyder developed using Scrapy Framework that can be used to crawl the top 250 movies from IMDB website, generates JSON payload with all the relevant details for each movie and pushes it to compacted kafka topic. Logstash is configured to consume data from the compacted kafka topic and stream the data to a elastic search instance. Kibana has been used to query and set up custom dashboards for visualizing the movie data scraped by the crawler.
