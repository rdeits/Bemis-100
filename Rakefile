PATTERNS = FileList['static/patterns/**/*.*']
MIX_FOLDERS = FileList['static/patterns/**/']
PREVIEWS = []

PATTERNS.each do |pat|
	preview = pat.sub(/^static\/patterns/, 'static/build/previews').sub(/\.[^.]*$/, '.gif')
	file preview do
		outFolder = preview.sub(/\/[^\/]*$/,'')
		mkdir_p outFolder
		sh "python3 Utilities/GIF_preview.py #{pat} #{preview}"
	end
	PREVIEWS.push(preview)
	thumb = pat.sub(/^static\/patterns/, 'static/build/thumbs')
	outFolder = thumb.sub(/\/[^\/]*$/,'')
	file thumb do
		mkdir_p outFolder
		sh "python3 Utilities/pattern_thumb.py #{pat} #{thumb}"
	end
	PREVIEWS.push(thumb)
end

MIX_FOLDERS.each do |folder|
	outFile = folder.sub(/^static\/patterns/, 'static/build/thumbs') + '/_mix.png'
	inFile = FileList[folder+'/*.*',folder+'/**/*.*']
	file outFile do
		sh "python3 Utilities/shuffle_thumb.py #{outFile} #{inFile}"
	end
	PREVIEWS.push(outFile)
end

file "Web/default_devices.py" do
	cp "Web/default_devices.example.py","Web/default_devices.py"
end

task :default => PREVIEWS

task :serve, [:port] => PREVIEWS + ["Web/default_devices.py"] do |task, args|
	args.with_defaults(:port => '5000')
	sh "python3 -m Web.ledweb #{args[:port]}"
end
