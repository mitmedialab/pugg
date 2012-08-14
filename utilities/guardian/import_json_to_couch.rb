require './utilities/guardian/couch.rb'
require 'json'
require 'digest/sha1'
require 'iconv'


ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')

#args: ruby import_json_to_couch database jsonfile

server = Couch::Server.new("localhost", "5984")

Dir.glob(File.join(ARGV[1], "**", "*.json")).each do |filename|
  index_data = JSON.load(File.open(filename))
  puts "#{filename}:"
  puts index_data["response"]["results"].size
  index_data["response"]["results"].each do |article|
      begin
        uuid = Digest::SHA1.hexdigest(article["id"])
        #articles[index]["title"] =ic.iconv(articles[index]["title"] + ' ')[0..-2]
        server.put("/#{ARGV[0]}/#{uuid}", article.to_json)
        print "."
      rescue Exception=>e
        uuid = Digest::SHA1.hexdigest("#{Time.now.to_f}")
        server.put("/#{ARGV[0]}/#{uuid}", article.merge({"timebased_id"=>true}).to_json)
        print "x"
        File.open("data/couch_import_#{ARGV[0]}.log", "a"){|f|
          f.write article.merge({"uuid"=>uuid}).to_json + "\n"
        }
      end
  end
end
