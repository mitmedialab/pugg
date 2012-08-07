require 'date'
require 'hpricot'
require 'open-uri'
require 'pp'
require 'json'

index_data = JSON.load(File.open(ARGV[0]))
error_counter = 0
counter = 500

baseurls = {"telegraph"=>"http://telegraph.co.uk", "dailymail"=>"http://dailymail.co.uk"}

index_data.each do |date, articles|
  articles.each_index do |index|
    counter -=1
    if counter <=0
      File.open(ARGV[2], "wb"){|f|
        f.write index_data.to_json
      }
      counter = 500
    end
    next if articles[index].has_key? "sharedata"
    basepath = ""
    basepath = baseurls[ARGV[1]] if(!articles[index]["url"].match(/http/))
    url = "http://localhost:1337/?q=" + basepath + articles[index]["url"]
    #puts url

    begin
      sharedata = JSON.parse(URI.parse(url).read)
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
    index_data[date][index]["sharedata"] = sharedata
    error_counter = 0
    sleep(1.0/8.0)
  end
end
