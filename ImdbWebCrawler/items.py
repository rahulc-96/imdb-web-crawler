# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class MovieItem(scrapy.Item):
    key = Field()
    title = Field()
    year = Field()
    duration = Field()
    rating = Field()
    popularity = Field()
    releaseDate = Field()
    genre = Field()
    posterUrl = Field()
    cast = Field()
    director = Field()
    writer = Field()
    producer = Field()
    cinematographer = Field()


   
    
    

    
    
