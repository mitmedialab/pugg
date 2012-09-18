require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'
require './utilities/guardian/couch.rb'

error_counter = 0

baseurls = {"telegraph"=>"http://telegraph.co.uk", "dailymail"=>"http://dailymail.co.uk", "guardian"=>""}
url_key = {"telegraph"=>"url", "dailymail"=>"url", "guardian"=> "webUrl"}
section_key = {"guardian"=>"sectionId","dailymail"=>""}
xml_query_key = {"telegraph"=>"", "dailymail"=>"a.author"}
server = Couch::Server.new("localhost", "5984")
database = ARGV[0]

index_data = JSON.load(server.get("/#{database}/_all_docs").response.body)

index_data["rows"].each do |row|
  index = row["id"]
  article_url = "/#{database}/#{index}"
  article = JSON.load(server.get(article_url).response.body)
  Author.add_article article
  print "."
end

File.open(ARGV[1], "wb") do |f|
  Author.get_authors.each do |name, author|
    f.write author.to_csv + "\n"
    puts "o"
  end
end
