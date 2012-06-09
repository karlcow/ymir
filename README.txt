Ymir
====

Ymir is a script used for managing the publication of La Grange
blog at http://www.la-grange.net/ It has been used on the site 
since January 1st, 2012. It is not very useful for the rest of 
you, but feel free to improve it or steal it. 


    ymir /path/to/the/article.html

It will update the Atom feed, create and update indexes. This 
script is not managing any kind of Web applications. All the 
files which have been created, modified, etc. need to be 
synchronized across the network. You might use a shell script 
for doing so. Something such as:


	echo "Synchronization: Start"
	# List of Exclude
	cat << "EOF" > /tmp/rsync.exclude
	.DS_Store
	EOF

	rsync --rsh=ssh \
	        -rpgtaz --stats --delete \
	        --exclude-from=/tmp/rsync.exclude \
	        -v /home/user/blah/foo/ \
	        user@example.org:/somewhere/blah/foo/

	if [ $? = 0 ]; 
	        then 
	                echo "Synchro: Done!"
	        else 
	                echo "Synchro: Problem - Check error messages"
	                exit 1
	fi



See LICENSE.txt

Author
======

* `Karl Dubost <http://www.la-grange.net/karl/>`


Contributors
============

* `David Larlet <https://larlet.fr/david/>`
