#!/bin/bash

echo "<html><body style='font-size:8px'><center><h1>Click image to remove from list at bottom</h1><div style='float: left'>" > ./antigay-report.html

if [[ "$1" == "" ]]; then echo "USAGE: dir [-nojailbait] [-nogay] [-nokids]"; exit -1; fi
if [[ "$2" == "" ]]; then OPTS="-nogay -nokids"; else OPTS=""; fi

DIRR="$1"
shift

echo "Scanning directory ..."

find "$DIRR" -type f \( -iname \*.jpg -o -iname \*.png -o -iname \*.gif -o -iname \*.jpeg \) -exec ./script.py $OPTS $* '{}' \; 2>/dev/null | while read line; do
	echo "<div style='display: inline-block'><img src='file://$line' onclick='this.parentNode.parentNode.removeChild(this.parentNode);' style='max-width: 200px'><br><center>$line</center></div>" >> ./antigay-report.html
	echo "Found $line"
done 

cat >> ./antigay-report.html << EOL 
</div><p><br><p>
<textarea id='removeme' style='width: 100%; height: 600px'></textarea>
<script>

window.setTimeout(listimgs, 100);

function listimgs() 
{
	document.getElementById("removeme").value = "";
	var images = document.getElementsByTagName('img'); 
	for(var i = 0; i < images.length; i++) {
	    document.getElementById("removeme").value += "rm '"+images[i].src.slice(7)+"'\n";
	}
	window.setTimeout(listimgs, 100);
}	
</script>
</center></body></html>
EOL

if firefox ./antigay-report.html; then echo ''; else chromium ./antigay-report.html; fi
