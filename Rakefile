PATTERNS = FileList['Web/static/patterns/**/*.*']
MIX_FOLDERS = FileList['Web/static/patterns/**/'][1..-1]
PREVIEWS = []

PATTERNS.each do |pat|
	preview = pat.sub(/^Web\/static\/patterns/, 'Web/static/build/previews').sub(/\.[^.]*$/, '.gif')
	file preview do
		outFolder = preview.sub(/\/[^\/]*$/,'')
		mkdir_p outFolder
		sh "python Utilities/GIF_preview.py #{pat} #{preview}"
	end
	PREVIEWS.push(preview)
	thumb = pat.sub(/^Web\/static\/patterns/, 'Web/static/build/thumbs')
	outFolder = thumb.sub(/\/[^\/]*$/,'')
	file thumb do
		mkdir_p outFolder
		sh "python Utilities/pattern_thumb.py #{pat} #{thumb}"
	end
	PREVIEWS.push(thumb)
end

MIX_FOLDERS.each do |folder|
	outFile = folder.sub(/^Web\/static\/patterns/, 'Web/static/build/thumbs') + '/_mix.png'
	inFile = FileList[folder+'/*.*']
	file outFile do
		sh "python Utilities/shuffle_thumb.py #{outFile} #{inFile}"
	end
	PREVIEWS.push(outFile)
end

task :default => PREVIEWS

task :serve => PREVIEWS do
	Dir.chdir "Web"
	sh "python ledweb.py"
end