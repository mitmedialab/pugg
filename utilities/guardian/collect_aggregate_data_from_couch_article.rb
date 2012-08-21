require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'
require './utilities/guardian/couch.rb'

error_counter = 0

baseurls = {"telegraph"=>"http://telegraph.co.uk", "dailymail"=>"http://dailymail.co.uk", "guardian"=>""}
url_key = {"telegraph"=>"url", "dailymail"=>"url", "guardian"=> "webUrl"}
xml_query_key = {"telegraph"=>"", "dailymail"=>"a.author"}

server = Couch::Server.new("localhost", "5984")

index_data = JSON.load(server.get("/#{ARGV[0]}/_all_docs?limit=10").response.body)

index_data["rows"].each do |index|
  article_url = "/#{database}/#{index}"
  article = JSON.load(server.get(article_url).response.body)
  server.put("/#{ARGV[1]}/#{index}", article.to_json)
  print "."
end
