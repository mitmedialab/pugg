require 'rubygems'
require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'
require 'iconv'

index_data = JSON.load(File.open(ARGV[0]))
error_counter = 0
counter = 25000

ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')


index_data.each do |date, articles|
  articles.each_index do |index|
    counter -=1
    break if counter <=0
    next if articles[index].has_key? "fulltext"
    filename = date + "_" + index.to_s
    if(File.exists? "data/telegraph/articles/#{filename}.html")
      index_data[date][index]["fulltext"] = filename
      error_counter = 0
      print "e"
      next
    end

    
    basepath = ""
    basepath ="http://telegraph.co.uk" if(!articles[index]["url"].match(/http/))
    url = basepath + articles[index]["url"]

    begin
      text = URI.parse(url).read
      text = ic.iconv(text + ' ')[0..-2]

      article = Hpricot::XML(text)
      article_text = (article/'div.twoThirds')[0].inner_html
      article_text = article if article_text.nil?
      #article_text = URI.parse(url).read
    rescue  Exception => e
      sleep(2)
      if e.message=="Timeout::Error"
        print "X"
        error_counter += 1
        redo if error_counter <= 3
      else
        print "x"
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
File.open(ARGV[1], "wb"){|f|
  f.write index_data.to_json
}
