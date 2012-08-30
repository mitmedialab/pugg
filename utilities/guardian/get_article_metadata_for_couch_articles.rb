require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'
require './utilities/guardian/couch.rb'

error_counter = 0

baseurls = {"telegraph"=>"http://telegraph.co.uk", "dailymail"=>"http://dailymail.co.uk", "guardian"=>""}
url_key = {"telegraph"=>"url", "dailymail"=>"url", "guardian" => "webUrl"}
xml_byline_query_key = {"telegraph"=>"", "dailymail"=>"a.author"}

server = Couch::Server.new("localhost", "5984")

index_data = JSON.parse(server.get("/#{ARGV[0]}/_all_docs").response.body)


def fetch_dailymail_fulltext xml
  x = (xml/'div#content')
  if x.size != 0
   xml = x
  end
  xml.search('div.relatedItemsTopBorder').remove
  xml.search('div.digg-button').remove
  xml.search('div.article-icon-links-container').remove
  author = xml.search('a.author')
  if(author.size>0 and !author[0].parent.nil?)
    author[0].parent.inner_html=""
  end
  xml.search('div.item').remove
  xml.search('div.relatedItems').remove
  xml.search('div.most-read-news-wrapper').remove
  xml.search('div.column-content').remove
  xml.search('div.reader-comments').remove ##we could actually catalogue these
  xml.search('div.rc-title').remove
  xml.search('ul#rc-tabs').remove
  xml.search('view-more-container').remove
  xml.search('div.js-comments').remove
  xml.search('p.comment-body').remove
  xml.search('p.user-info').remove
  xml.search('div.beta').remove
  xml.search('div.and-footer').remove
  xml.search('div.page-footer').remove
  xml.search('div.supplements').remove
  xml.search('li').remove
  xml.search("script").remove
  
  #note div.artSplitter is images

  fulltext =""
  (xml/"p|h2").each do |element|
    line = element.inner_text.strip
    if(line.size > 50 and line.index("The views expressed in the contents above").nil? and
       line.index("no longer accepting comments").nil?)
      fulltext += line + " " 
    end
  end
  fulltext
end


index_data["rows"].each do |row|
  index = row["id"]
  article = JSON.parse(server.get("/#{ARGV[0]}/#{index}").response.body)
  filename = "data/#{ARGV[0]}/articles/#{article["fulltext"]}.html"
  begin
    xml = Hpricot::XML(File.open(filename).read)
  rescue Exception=>e
    puts e
    next
  end

  post = false

  if !article.has_key?("raw_byline") or article["raw_byline"]==""
    byline_tag = (xml/xml_byline_query_key[ARGV[0]])
    if byline_tag and byline_tag.size>0
      byline = byline_tag[0].inner_html.strip
      print "."
    else
      article["raw_byline"] = byline
      post = true
    end
  end

  if !article.has_key?("body_text")
    begin
      article["body_text"] = fetch_dailymail_fulltext(xml) 
      post = true
    rescue Exception=>e
      puts e
    end
    puts "========YEAH YEAH (#{filename}) YEAH YEAH======="
  end

  server.put("/#{ARGV[0]}/#{index}", article.to_json) if post
end
