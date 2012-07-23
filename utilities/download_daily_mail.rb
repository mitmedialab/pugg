require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'

date_articles = {}

current_date = Date.parse("1 June 2011")
while(current_date <= Date.parse("23 July 2012"))
#while(current_date <= Date.parse("3 June 2011"))
  articles = []
  dateformat =  current_date.strftime("%Y%m%d")
  puts "\nhttp://www.dailymail.co.uk/home/sitemaparchive/day_#{dateformat}.html"
  daily_index_page = URI.parse("http://www.dailymail.co.uk/home/sitemaparchive/day_#{dateformat}.html").read
  xml = Hpricot::XML(daily_index_page)
  (xml/'.wogr2 a').each do |article|
    articles << {:url=>article['href'], :title=>article.inner_html}
    print "."
    $stdout.flush
  end
  date_articles[dateformat] = articles
  current_date +=1
  sleep(4)
end
File.open(ARGV[0], "wb"){|f|
  f.write date_articles.to_json
}
