require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'

index_data = JSON.load(File.open("data/dailymail/index/dailymail_full_20110601_20120723.json").read)
error_counter = 0

index_data.each do |key, value|
  next if value.size > 1
  articles = []
  dateformat = key
  puts "\nhttp://www.dailymail.co.uk/home/sitemaparchive/day_#{dateformat}.html"
  begin
    daily_index_page = URI.parse("http://www.dailymail.co.uk/home/sitemaparchive/day_#{dateformat}.html").read
    xml = Hpricot::XML(daily_index_page)
    (xml/'.wogr2 a').each do |article|
      articles << {:url=>article['href'], :title=>article.inner_html}
      print "."
      $stdout.flush
    end
  rescue  Exception => e
    if e.message=="Timeout::Error"
      error_counter += 1
      redo if error_counter <= 3
    else
      articles << ["READ ERROR"]
    end
  end
  index_data[dateformat] = articles
  error_counter = 0
  sleep(2)
end
File.open(ARGV[0], "wb"){|f|
  f.write index_data.to_json
}
