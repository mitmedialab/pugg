require 'rubygems'
require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'
require 'iconv'
require './utilities/guardian/couch.rb'

puts ARGV[0]
index_data = JSON.load(File.open(ARGV[0]).read)
error_counter = 0
counter = 300000
database = "telegraph"
url_key = "url"

ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')

server = Couch::Server.new("localhost", "5984")

index_data.each do |date, articles|
  articles.each_index do |index|
    counter -=1
    break if counter <=0
    next if articles[index].has_key? "fulltext"
    filename = date + "_" + index.to_s
    if(File.exists? "data/telegraph/articles/#{filename}.html")
      index_data[date][index]["fulltext"] = filename
      error_counter = 0
    else
      print "x"
      next
    end
    
    begin
      result = JSON.load(server.get("/#{database}/_design/query/_view/url?key=\"#{URI::encode(index_data[date][index]["url"])}\"").response.body)
    rescue Exception => e
      puts e
      next
    end
    if(result["rows"].size == 0)
      print "X"
      next
    end

    article = result["rows"][0]["value"]
    next if article.has_key? "fulltext"

    article["fulltext"] = filename
    server.put("/#{database}/#{article["_id"]}", article.to_json)
    print "."

    ## COMPLETE SHORT-CIRCUIT THE FETCHING FOR NOW
    next 
    ## RE-ENABLE IF NEEDED LATER
   
    basepath = ""
    basepath ="http://telegraph.co.uk" if(!articles[index]["url"].match(/http/))
    url = basepath + articles[index]["url"]

    begin
      text = URI.parse(url).read
      text = ic.iconv(text + ' ')[0..-2]

      article = Hpricot::XML(text)
      at = (article/'div.twoThirds')
      if(at and at.size>0)
        article_text = at[0].inner_html
      else
        article_text = article
      end
      article_text = text if article_text.nil?
      #article_text = URI.parse(url).read
    rescue  Exception => e
      sleep(2)
      if e.message=="Timeout::Error"
        print "X"
        error_counter += 1
        redo if error_counter <= 3
      elsif e.message=="404 Not Found"
        print "4"
        index_data[date][index]["fulltext"]="404"
        error_counter = 0
        next
      else
        print "X"
        puts e
        error_counter = 0
        next
      end
    end
    print "."
    File.open("data/telegraph/articles/#{filename}.html", "wb"){|f|
      f.write article_text
    }
    index_data[date][index]["fulltext"] = filename
    error_counter = 0
    sleep(1.0/8.0)
  end
end
#File.open(ARGV[1], "wb"){|f|
#  f.write index_data.to_json
#}
