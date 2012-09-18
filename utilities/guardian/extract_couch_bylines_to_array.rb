require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'
require 'tokenizer'
require './utilities/guardian/couch.rb'

error_counter = 0

baseurls = {"telegraph"=>"http://telegraph.co.uk", "dailymail"=>"http://dailymail.co.uk", "guardian"=>""}
url_key = {"telegraph"=>"url", "dailymail"=>"url", "guardian"=> "webUrl"}
xml_query_key = {"telegraph"=>"", "dailymail"=>"a.author"}

server = Couch::Server.new("localhost", "5984")
database = ARGV[0]

index_data = JSON.load(server.get("/#{database}/_all_docs").response.body)

tokenizer = Tokenizer::Tokenizer.new

index_data["rows"].each do |row|
  index = row["id"]
  article_url = "/#{database}/#{index}"
  article = JSON.load(server.get(article_url).response.body)
  bylines = []

  post = false
  if (database == "guardian" and article.has_key? "fields" and article["fields"].has_key? "byline")
    #byline_tokens = tokenizer.tokenize("byline")
    bylines = article["fields"]["byline"].split(/and |,/).collect{|a|a.strip}
    post = true
  elsif (database =="dailymail" and article.has_key? "raw_byline" and !article["raw_byline"].nil?)
    bylines = article["raw_byline"].downcase.split(/and |,/).collect{|a|a.strip}
    post = true
  end

  bylines.collect! do |byline|
    m = byline.match(/(.*?)( in )/)
    if(m.nil?)
      byline
    else
      m[1]
    end
  end
  bylines.reject! do |byline|
    byline.match(/(editor|correspondent)/)
  end
  article["bylines"] = bylines
  server.put("/#{database}/#{index}", article.to_json)
  #puts bylines
  print bylines.size

end
