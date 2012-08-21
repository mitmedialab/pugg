require 'hpricot'

dirname = ARGV[0]

Dir.glob(File.join(dirname, "**", "*.html")).each do |filename|
  xml = Hpricot::XML(File.open(filename).read)
  byline = nil
  byline_tag = (xml/'.bylineBody a')
  if byline_tag and byline_tag.size>0
    byline = byline_tag[0].inner_html.strip
    print "."
  else 
    puts filename
  end
end
