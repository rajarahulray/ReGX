import urllib.request
from re import findall

#Read the webpage:
response = urllib.request.urlopen("https://github.com/rajarahulray")
html = response.read()
text = html.decode()

#Use regular expressions to find the data we want, which looks like:
#   "<span>NN&deg;</span>" where the NN is replaced with digits.
# Note that on extremely hot days it could be NNN and on extremely
# cold days it could be just N.

dataCrop = findall("<div>[0-9]+&deg;</div>", text)
print("The data cropped out of the webpage is:", dataCrop)
