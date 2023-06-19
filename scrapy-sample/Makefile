0_scrapy_at_a_glance_quotes_to_scrape_call_directly:
	scrapy runspider my_project/spiders/0_scrapy_at_a_glance_quotes_to_scrape.py \
		-o results/0_scrapy_at_a_glance_quotes_to_scrape.jsonl

0_scrapy_at_a_glance_quotes_to_scrape_call_by_spider_name:
	scrapy crawl 0.scrapy_at_a_glance \
		-o results/0_scrapy_at_a_glance_quotes_to_scrape.jsonl

start_splash:
	docker run -p 8050:8050 scrapinghub/splash

stackoverflow:
	scrapy crawl stack -o stackoverflow.json -t json

facebook-selenium:
	scrapy crawl facebook-selenium-spider -o facebook-selenium.json -t json

loza:
	scrapy crawl loza -o loza.json -t json

test:
	scrapy crawl test

mongodb-start:
	docker run -d --name test_crawl_data_mongodb \
				-p 27017:27017 \
				-e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
				-e MONGO_INITDB_ROOT_PASSWORD=secret \
				-e MONGO_INITDB_DATABASE=my_database \
				mongo
				# -v /tmp/test-mongodb-data:/data/db \

mongodb-shell:
	docker exec -it test_crawl_data_mongodb mongosh -u "mongoadmin" -p "secret"
	# then create normal user for access my_database
	# use my_database
	db.createUser({user: "xuananh", pwd: "123", roles : [{role: "readWrite", db: "my_database"}]});
	# reference: https://stackoverflow.com/a/57752119/7639845
