require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'
require './utilities/guardian/couch.rb'

error_counter = 0

baseurls = {"telegraph"=>"http://telegraph.co.uk", "dailymail"=>"http://dailymail.co.uk", "guardian"=>""}
url_key = {"telegraph"=>"url", "dailymail"=>"url", "guardian", "webUrl"}
xml_query_key = {"telegraph"=>"", "dailymail"=>"a.author"}

server = Couch::Server.new("localhost", "5984")

index_data = server.get("#{ARGV[0]}/all_docs")


index_data.each do |index|
  article = server.get("#{ARGV[0]}/#{index}")
  next if article["raw_byline"]
  filename = "data/#{ARGV[0]}/articles/#{article["fulltext"]}"
  xml = Hpricot::XML(File.open(filename).read)
  byline_tag = (xml/xml_query_key[ARGV[0]])
  if byline_tag and byline_tag.size>0
    byline = byline_tag[0].inner_html.strip
    print "."
  else

  article["raw_byline"] = byline

  server.put("#{ARGV[0]}/#{index}", article)
end
