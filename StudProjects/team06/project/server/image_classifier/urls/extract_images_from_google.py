# Get links from google images
# https://github.com/toffebjorkskog/ml-tools/blob/master/gi2ds.md
# (function(e, s) {
#     e.src = s;
#     e.onload = function() {
#         jQuery.noConflict();
#         jQuery('<style type="text/css"> .remove { opacity:0.3;}\n .urlmodal {padding: 10px; background-color: #eee; position: fixed; bottom: 0; right: 0; height: 100px; width: 300px; z-index: 1000;} .urlmodal textarea {width: 100%; height: 250px;}</style>').appendTo('head');
#         jQuery('<div class="urlmodal"><h3>Let\'s create a dataset</h3><textarea>Scoll all the way down\nClick "Show more images"\nScroll more\nClick on the images you want to remove from the dataset\nThe urls will appear in this box for you to copy.</textarea></div>').appendTo('body');

#         jQuery('#rg').on('click', '.rg_di', function() {
#             jQuery(this).toggleClass('remove');
#             updateUrls();
#             return false;
#         });
#         jQuery(window).scroll(updateUrls);
#         jQuery('.urlmodal textarea').focus(function() {updateUrls(); setTimeout(selectText, 100)}).mouseup(function() {return false;});

#         function updateUrls() {
#             var urls = Array.from(document.querySelectorAll('.rg_di:not(.remove) .rg_meta')).map(el=>JSON.parse(el.textContent).ou);
#             var search_term = jQuery('.gsfi').val();
#             jQuery('.urlmodal textarea').val(urls.join("\n"));
#             jQuery('.urlmodal h3').html(search_term + ": " + urls.length);
#         }

#         function selectText() {
#             jQuery('.urlmodal textarea').select();
#         }
#     };
#     document.head.appendChild(e);
# })(document.createElement('script'), '//code.jquery.com/jquery-latest.min.js');

from imutils import paths
import argparse
import requests
import cv2
import os


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", required=True,
	help="path to file containing image URLs")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())
 
# grab the list of URLs from the input file, then initialize the
# total number of images downloaded thus far
rows = open(args["urls"]).read().strip().split("\n")
total = 0

# loop the URLs
for url in rows:
	try:
		# try to download the image
		r = requests.get(url, timeout=60)
 
		# save the image to disk
		p = os.path.sep.join([args["output"], "{}.jpg".format(
			str(total).zfill(8))])
		f = open(p, "wb")
		f.write(r.content)
		f.close()
 
		# update the counter
		print("[INFO] downloaded: {}".format(p))
		total += 1
 
	# handle if any exceptions are thrown during the download process
	except Exception as e:
		print(e)
		print("[INFO] error downloading {}...skipping".format(p))



# loop over the image paths we just downloaded
for imagePath in paths.list_images(args["output"]):
	# initialize if the image should be deleted or not
	delete = False
 
	# try to load the image
	try:
		image = cv2.imread(imagePath)
 
		# if the image is `None` then we could not properly load it
		# from disk, so delete it
		if image is None:
			delete = True
 
	# if OpenCV cannot load the image then the image is likely
	# corrupt so we should delete it
	except:
		print("Except")
		delete = True
 
	# check to see if the image should be deleted
	if delete:
		print("[INFO] deleting {}".format(imagePath))
		os.remove(imagePath)