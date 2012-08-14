require './couch.rb'
require 'json'
server = Couch::Server.new("localhost", "5984")
server.put("/tmp/12345", {"cat"=>"hat"}.to_json)
