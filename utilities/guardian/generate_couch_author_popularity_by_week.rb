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
database = ARGV[0]

class Author
  attr_accessor :name, :googleplus, :twitter, :facebook, :articles
  @@authors = {}

  def initialize name, article
    @articles = 1
    @name = name
    @googleplus = 0
    @twitter = 0
    @facebook = 0 
    if(article.has_key? "sharedata")
      if(!article["sharedata"].nil? and article["sharedata"].has_key? "googlePlus")
        @googleplus = article["sharedata"]["googlePlus"]["count"]
      end
      if(!article["sharedata"].nil? and article["sharedata"].has_key? "twitter")
        @twitter = article["sharedata"]["twitter"]["count"]
      end
      if(!article["sharedata"].nil? and article["sharedata"].has_key? "facebook")
        @facebook = article["sharedata"]["facebook"]["shares"]
        @facebook += article["sharedata"]["facebook"]["likes"]
      end
    end
  end

  def add_article article
    @articles += 1
    if(article.has_key? "sharedata")
      if(!article["sharedata"].nil? and article["sharedata"].has_key? "googlePlus")
        count = article["sharedata"]["googlePlus"]["count"]
        @googleplus += count if !count.nil?
      end
      if(!article["sharedata"].nil? and article["sharedata"].has_key? "twitter")
        count = article["sharedata"]["twitter"]["count"]
        @twitter += count if !count.nil?
      end
      if(!article["sharedata"].nil? and article["sharedata"].has_key? "facebook")
        count = article["sharedata"]["facebook"]["shares"]
        @facebook += count if !count.nil?
        count = article["sharedata"]["facebook"]["likes"]
        @facebook += count if !count.nil?
      end
    end
  end

  def Author.add_article article
    return if !article.has_key? "bylines"
    article["bylines"].each do |byline|
      author = Author.get_author(byline)
      if(author)
        author.add_article article
      else
        @@authors[byline] =  Author.new byline, article
      end
    end
  end

  def Author.get_authors
    @@authors
  end

  def Author.get_author name
    @@authors[name]
  end

  def Author.delete_all!
    @@authors = {}
  end

  def to_csv
    "#{@name},#{@articles},#{@facebook},#{@googleplus},#{@twitter}"
  end

  def to_hash
    {:name=>@name,
     :articles=>@articles,
     :facebook=>@facebook,
     :googleplus=>@googleplus,
     :twitter=>@twitter}
  end
end

def Author.write_authors yearweek
  File.open(ARGV[1] + "_#{yearweek}.csv", "wb") do |f|
    Author.get_authors.each do |name, author|
      f.write author.to_csv + "\n"
    end
    puts "==o=="
  end
end

index_data = JSON.load(server.get("/#{database}/_design/dates/_view/dates?limit=1").response.body)
prevdate = Date.parse(index_data["rows"][0]["value"]["webPublicationDate"])
prevdate_week = prevdate.year.to_s + prevdate.cweek.to_s

startkey = index_data["rows"][0]["key"]

more_articles = true
rows_per_page = 200

#this while loop processes every article, in a paged manner
while more_articles
  row_id = 0 
  index_data = JSON.load(server.get("/#{database}/_design/dates/_view/dates?startkey=#{startkey}&limit=#{rows_per_page + 1}").response.body)
  print "|"
  index_data["rows"].each do |row|
    row_id += 1

    #for pagination: if it's the last row, use that as
    # the startkey for the next page, and continue without processing
    #TODO: Fix something in this bit of code
    if index_data["rows"].size == 1
      Author.write_authors prevdate_week
      puts "END OF SCRIPT"
      more_articles = false 
      break
      #end state: this is the final item in the entire dataset,
      #so save it and conclude
    elsif row_id >= index_data["rows"].size() -1
      puts "END OF INDEX"
      startkey = row["key"]
      break
    end
    article = row["value"]

    curdate = Date.parse(article["webPublicationDate"])
    curdate_week = curdate.year.to_s + curdate.cweek.to_s
    if(curdate_week!=prevdate_week)
      puts prevdate_week
      Author.write_authors prevdate_week
      Author.delete_all!
    end
    #TODO: Calculate the current week, compare to prev week
    #      decide if you need to write the month
    #      and add the article appropriately
    Author.add_article article
    #print "."
    prevdate = curdate
    prevdate_week = curdate_week
  end

end
