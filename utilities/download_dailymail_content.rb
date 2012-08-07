require 'rubygems'
require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'
require 'iconv'

index_data = JSON.load(File.open(ARGV[0]))
error_counter = 0
counter = 300000

ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')


index_data.each do |date, articles|
  articles.each_index do |index|
    counter -=1
    break if counter <=0
    next if articles[index].has_key? "fulltext"

    filename = date + "_" + index.to_s
    if(File.exists? "data/dailynail/articles/#{filename}.html")
      index_data[date][index]["fulltext"] = filename
      error_counter = 0
      print "e"
      next
    end

    basepath = ""
    basepath ="http://dailymail.co.uk" if(!articles[index]["url"].match(/http/))
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
    rescue  Exception => e
      print "x"
      sleep(2)
      if e.message=="Timeout::Error"
        error_counter += 1
        redo if error_counter <= 3
      elsif e.message=="404 Not Found"
        index_data[date][index]["fulltext"]="404"
        error_counter = 0
        print "4"
        next
      else
        print "X"
        puts e
        error_counter = 0
        next
      end
    end
    print "."
    File.open("data/dailymail/articles/#{filename}.html", "wb"){|f|
      f.write article_text
    }
    index_data[date][index]["fulltext"] = filename
    error_counter = 0
    sleep(1.0/8.0)
  end
end
File.open(ARGV[1], "wb"){|f|
  f.write index_data.to_json
}
