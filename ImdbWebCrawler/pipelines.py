# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from confluent_kafka import Producer
import json





class IMDBCrwalerPipeline:
    
    def __init__(self, server, batchSize, retries, topic):
        self.server = server
        self.batchSize = batchSize
        self.retries = retries
        self.topic = topic
 
        
    @classmethod
    def from_crawler(cls, crawler):
        print("Producer Configs:{0}->{1}->{2}->{3}".format(crawler.settings.get('BOOTSTRAP_SERVERS'),crawler.settings.get('BATCH_SIZE'), crawler.settings.get('RETRIES'), crawler.settings.get('TOPIC')))
        return cls(
            server=crawler.settings.get('BOOTSTRAP_SERVERS'),
            batchSize=crawler.settings.get('BATCH_SIZE'),
            retries=crawler.settings.get('RETRIES'),
            topic=crawler.settings.get('TOPIC')
        )
    
    
    def open_spider(self, spider):
               self.producer = Producer({'bootstrap.servers' : self.server,'retries' : self.retries, 'batch.size' : self.batchSize, 'client.id': 'IMDBScrapper'})
    

        
        
    def process_item(self, item, spider):
        
        def acked(err, msg):
            if err is not None:
                print("Failed to deliver message with key %s and value: %s due to error:%s" % (str(msg.key()), str(msg.value()), str(err)))
            else:
                print("Message produced with key: %s and value: %s" % (str(msg.key()),str(msg.value())))
                    
        messageValue = json.dumps(ItemAdapter(item).asdict()).encode('utf-8')
        keyValue= item['key']
        print("Message send: {0} with key:{1}".format(messageValue,keyValue))
        self.producer.produce(topic = self.topic, key=keyValue, value=messageValue, callback=acked)
        self.producer.poll(0.5)
        return item
