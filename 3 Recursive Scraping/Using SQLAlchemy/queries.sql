SELECT * FROM scraped_urls_logs JOIN urls_t ON scraped_urls_logs.url_id = urls_t.id ;

SELECT * FROM url_contents_t;

SELECT * FROM scraped_urls_logs JOIN url_contents_t ON scraped_urls_logs.url_contents_id = url_contents_t.content_id ;

SELECT * FROM scraped_urls_logs 
	JOIN url_contents_t ON scraped_urls_logs.url_contents_id = url_contents_t.content_id
	JOIN urls_t ON scraped_urls_logs.url_id = urls_t.id ;
