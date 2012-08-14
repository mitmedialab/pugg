require './utilities/guardian/couch.rb'
require 'json'
require 'digest/sha1'
require 'iconv'


ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')

#args: ruby import_json_to_couch database jsonfile

server = Couch::Server.new("localhost", "5984")

Dir.glob(File.join(ARGV[1], "**", "*.json")).each do |filename|
index_data = JSON.load(File.open(ARGV[1]))

index_data["response"]["results"].each do |date, articles|
  articles.each_index do |index|
    begin
      uuid = Digest::SHA1.hexdigest(articles[index]["id"])
      #articles[index]["title"] =ic.iconv(articles[index]["title"] + ' ')[0..-2]
      server.put("/#{ARGV[0]}/#{uuid}", articles[index].to_json)
      print "."
    rescue Exception=>e
      uuid = Digest::SHA1.hexdigest("#{Time.now.to_f}")
      server.put("/#{ARGV[0]}/#{uuid}", articles[index].merge({"timebased_id"=>true}).to_json)
      print "x"
      File.open("data/couch_import_#{ARGV[0]}.log", "a"){|f|
        f.write articles[index].merge({"uuid"=>uuid}).to_json + "\n"
      }
    end
  end
    print "\n" + date +": "
end
end
