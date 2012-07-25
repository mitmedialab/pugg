require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'

index_data = JSON.load(File.open(ARGV[0]).read)
error_counter =0

index_data.each do |key, value|
  next if value.size > 1
  articles = []
  dateformat =  key
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
        articles << {:url=>link[0]['href'], :title=>link.inner_html, :section=>current_section} if(!link.nil? and link.size >0 and link[0]["href"])
      end
      print "."
      $stdout.flush
    end
  rescue Exception => e
    if e.message=="Timeout::Error" and error_counter<=3
      puts "TIMEOUT"
      error_counter +=1
      redo
    else
      articles << ["READ ERROR"]
      puts e.message
      puts e.backtrace
    end
  end
  index_data[dateformat] = articles
  error_counter = 0 
  sleep(2)
end
File.open(ARGV[1], "wb"){|f|
  f.write index_data.to_json
}
