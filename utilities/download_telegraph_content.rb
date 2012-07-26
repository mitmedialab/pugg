require 'rubygems'
require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'

index_data = JSON.load(File.open(ARGV[0]))
error_counter = 0
counter = 5000

index_data.each do |date, articles|
  articles.each_index do |index|
    counter -=1
    break if counter <=0
    next if articles[index].has_key? "sharedata"
    basepath = ""
    basepath ="http://telegraph.co.uk" if(!articles[index]["url"].match(/http/))
    url = basepath + articles[index]["url"]

    begin
      article_text = URI.parse(url).read
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
    filename = date + index.to_s
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
