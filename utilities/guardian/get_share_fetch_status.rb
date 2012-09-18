require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'
require './utilities/guardian/couch.rb'

error_counter = 0

<<<<<<< HEAD
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
=======
databases = ["telegraph", "dailymail", "guardian"]

server = Couch::Server.new("localhost", "5984")

sharedata_count = {"telegraph"=>{"total"=>0, "fetched"=>0}, 
                   "dailymail"=>{"total"=>0, "fetched"=>0}, 
                   "guardian"=>{"total"=>0, "fetched"=>0}}

databases.each do |database|

index_url = "/#{database}/_all_docs"
puts index_url
index_data = JSON.load(server.get(index_url).response.body)
puts database

index_data["rows"].each do |row|
  index = row["id"]
  article_url = "/#{database}/#{index}"
  article = JSON.load(server.get(article_url).response.body)

  if article.has_key? "sharedata" 
    if database=="dailymail" and  article["sharedata"]["total"]!=0
    else
      sharedata_count[database]["fetched"]+=1
    end
  end
  print "."
end
end

puts sharedata_count
>>>>>>> 475d63241309e7a435fbf3ce99b60d76d2aa500a
