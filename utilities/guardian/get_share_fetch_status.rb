require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'
require './utilities/guardian/couch.rb'

error_counter = 0

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
