DESTINATION_PATH=/deploy/scrapy
RSYNC_PARAMS = -avlP --exclude='__pycache__/*' --exclude=.[!.]*

DESTINATION_SERVER = sigma@192.168.1.200

DEPLOY_COMMAND='cd /deploy/plusfun && docker restart plusfun_nginx_1'

upload:
	rsync $(RSYNC_PARAMS) ./ $(DESTINATION_SERVER):$(DESTINATION_PATH)

download:
	rsync $(RSYNC_PARAMS) $(DESTINATION_SERVER):$(DESTINATION_PATH) ./

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