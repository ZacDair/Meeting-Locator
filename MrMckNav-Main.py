from flask import Flask, render_template, request, redirect
from PIL import Image
import pymysql
app = Flask(__name__)


def getPixelData(file):
    # Open the file as an image
    im = Image.open(file)

    # Get width and height
    width, height = im.size
    maxWidth = 100

    # Shrink but keep aspect ratio, if the width is bigger than 100
    if width > maxWidth:
        wpercent = (maxWidth / float(im.size[0]))
        hsize = int((float(im.size[1]) * float(wpercent)))
        im = im.resize((maxWidth, hsize), Image.BICUBIC)

    # Re define width and height as they will have changed
    width, height = im.size

    # Get the pixel rbg values
    pixelValues = list(im.getdata())

    # Append x and y coords and pixel rbg values
    pixelData = []
    x = 0
    y = 0
    pixelData.append(width)
    pixelData.append(height)
    pixelData.append(im.getcolors(512))
    for val in pixelValues:
        temp = [x, y, val]
        pixelData.append(temp)
        x = x + 1
        if x == width:
            x = 0
            y = y + 1
    return pixelData


def convertRgbToHex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


# Returns the hex code for white or black based on the tolerance of what is considered black or white
def toleranceTiedProcessing(rgb, tolerance):
    # if less than tolerance -> black, else white
    if int(rgb[0]) <= tolerance or int(rgb[1]) <= tolerance or int(rgb[2]) <= tolerance:
        return "#000000"
    else:
        return "#FFFFFF"


# Loop to remove count from color list
def colorsRefine(colors):
    i = 0
    while i < len(colors):
        colors[i] = colors[i][1]
        i = i + 1
    return colors


# Sort and refine colors and return the floor list
def colorSortAndRefine(colors):
    # Sort by first rgb value
    colors.sort(key=takeCount)

    # Remove count from colors
    colors = colorsRefine(colors)

    # Group colors if there is two biggest is floor, lowest is walls
    # else use 50/50 split
    if len(colors) == 2:
        floors = colors[0]
    else:
        colorCount = len(colors)
        halfCount = int(round(colorCount / 2))
        floors = colors[0:halfCount]
    return floors


# check if the color is in floors list
def colorInFloors(rgb, floors):
    if rgb in floors:
        return "#000000"
    else:
        return "#FFFFFF"


# Function used to get the first element to use as a key in sorting the colors (first element is the color count)
def takeCount(listItem):
    return listItem[1][0]


def generateRectHtml(pixelData, processingMethod, tolerance):
    # Set starting values
    rects = []
    x = 0
    y = 0

    # Remove width and height passed through from the getPixelData (first pos is width, second is height)
    w = pixelData.pop(0)
    h = pixelData.pop(0)

    # Get colors out of the pixelData list
    colors = pixelData.pop(0)
    floors = []
    if processingMethod == "Auto":
        floors = colorSortAndRefine(colors)

    # Cycle through our pixel data creating the html rect element with the values
    index = 0
    for val in pixelData:
        if processingMethod == "Auto":
            hexVal = colorInFloors(val[2], floors)
        elif processingMethod == "TTied":
            hexVal = toleranceTiedProcessing(val[2], tolerance)
        else:
            hexVal = convertRgbToHex(val[2])
        temp = [str(index), x, y, hexVal]
        rects.append(temp)
        index = index + 1
        x = x + 10

        # if the x value of an element of pixel data is equal to the width-1, start a new line of pixels
        if val[0] == w-1:
            y = y + 10
            x = 0
    return rects


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']

        # Convert post request data to a dict
        postResults = request.values.to_dict()

        # Get actual values from our post request form that's now a dict
        # TO DO: Needs error checking in case the required values aren't in the dict
        tolerance = int(postResults["tolerance"])
        processingMethod = postResults["processingOption"]

        # Set the processing method to none if something else was sent and print an error
        if processingMethod != "Auto" and processingMethod != "TTied" and processingMethod != "None":
            processingMethod = "Auto"
            print("Error - the processing method was a different value than expected")

        # Server side file checking (can be faked if the file uploaded has the name to fit these conditions)
        # TO DO: Test if it can actually be faked
        if str(f.filename).endswith(('.png', '.jpeg', '.jpg', '.PNG')):

            # If file is accepted try to get the pixel data, use to generate the rect elements and send to grid page
            pixelData = getPixelData(f)
            w = pixelData[0]*10
            h = pixelData[1]*10
            rects = generateRectHtml(pixelData, processingMethod, tolerance)
            return render_template('admin.html', gridData=rects, width=w, height=h)

        else:
            return redirect("http://localhost:5000", code=400)


@app.route('/database')
def database():
    # Attempt to connect to the database - if it works return true else false
    con = pymysql.connect(host='176.34.142.64', port='53', user='ubuntu', password='root', database='mediScreenDatabase')
    print(con)


if __name__ == '__main__':
    app.run(debug=True)


