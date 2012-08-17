require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'
require './utilities/guardian/couch.rb'

error_counter = 0

baseurls = {"telegraph"=>"http://telegraph.co.uk", "dailymail"=>"http://dailymail.co.uk", "guardian"=>""}
url_key = {"telegraph"=>"url", "dailymail"=>"url", "guardian", "webUrl"}

server = Couch::Server.new("localhost", "5984")

index_data = server.get("#{ARGV[0]}/all_docs")


index_data.each do |index|
  article = server.get("#{ARGV[0]}/#{index}")
  next if article.has_key? "sharedata"
  basepath = ""
  basepath = baseurls[ARGV[1]] if(!article[url_key[ARGV[0]]].match(/http/))
  url = "http://localhost:1337/?q=" + basepath + article[url_key[ARGV[0]]]

  begin
    sharedata = JSON.parse(URI.parse(url).read)
  rescue  Exception => e
    print "x"
    sleep(2)
    if e.message=="Timeout::Error"
      error_counter += 1
      redo if error_counter <= 3
    else
      error_counter = 0
      next
    end
  end
  print "."
  article["sharedata"] = sharedata

  server.put("#{ARGV[0]}/#{index}", article)

  error_counter = 0
  sleep(1.0/8.0)
end
