require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'

date_articles = {}

current_date = Date.parse("1 June 2011")
while(current_date <= Date.parse("23 July 2012"))
#while(current_date <= Date.parse("1 June 2011"))
  articles = []
  dateformat =  current_date.strftime("%Y-%-m-%d")
  url = "http://www.telegraph.co.uk/archive/#{dateformat}.html"
  puts "\n" + url
  begin
    daily_index_page = URI.parse(url).read
    xml = Hpricot::XML(daily_index_page)
    current_section = "NONE"
    (xml/'div').each do |div|
      if(div.classes.index "archiveHeader")
        current_section = (div/'h2').inner_html
      elsif(div.classes.index "summary")
        link = (div/'a')
        articles << {:url=>link[0]['href'], :title=>link.inner_html, :section=>current_section}
      end
      print "."
      $stdout.flush
    end
  rescue 
    articles << ["READ ERROR"]
  end
  date_articles[dateformat] = articles
  current_date +=1
  sleep(2)
end
File.open(ARGV[0], "wb"){|f|
  f.write date_articles.to_json
}
