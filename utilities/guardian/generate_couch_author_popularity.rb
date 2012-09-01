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

index_data = JSON.load(server.get("/#{database}/_all_docs").response.body)

index_data["rows"].each do |row|
  index = row["id"]
  article_url = "/#{database}/#{index}"
  article = JSON.load(server.get(article_url).response.body)
  Author.add_article article
  print "."
end

<<<<<<< HEAD
File.open(ARGV[1], "wb") do |f|
=======
File.open(ARGV[1]) do |f|
>>>>>>> 475d63241309e7a435fbf3ce99b60d76d2aa500a
  Author.get_authors.each do |name, author|
    f.write author.to_csv + "\n"
    puts "o"
  end
end
