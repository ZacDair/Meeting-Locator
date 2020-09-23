from flask import Flask, render_template, request, redirect
from PIL import Image
import pymysql
app = Flask(__name__)


# This function takes in a file object (an image) and retrieves each pixel into a pixel data list.
# Pixel Data List item structure: [x coordinate, y coordinate, RBG value]
# The image is processed and if it is bigger than the max width it will be scaled down using antialiasing
def getPixelData(file):
    # Open the file as an image
    im = Image.open(file)

    # Get width and height
    width, height = im.size
    maxWidth = 50

    # Shrink but keep aspect ratio, if the width is bigger than the max width
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


# This function converts the standard RBG value into a hex code
def convertRgbToHex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


# Returns the hex code for white or black based on the tolerance of what is considered black or white
def toleranceTiedProcessing(rgb, tolerance):
    # if less than tolerance -> black, else white
    if int(rgb[0]) <= tolerance or int(rgb[1]) <= tolerance or int(rgb[2]) <= tolerance:
        return "#000000"
    else:
        return "#FFFFFF"


# Loop to remove count from color list, count was an unused bi-product of a previous function
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

    # Group colors if there is two values then the biggest is floor, lowest is walls
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


# Function to create and return the rect element html code for the webpage
# This function takes into account the pixel data found earlier, the processing method,
# and the tolerance value (only used if the tolerance tied processing method is used)
# This function is called after the image has been uploaded and submitted to the backend from the index.html page
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

    # If we are using automatic processing, sort the colors in order to find the floor cells
    if processingMethod == "Auto":
        floors = colorSortAndRefine(colors)

    # Cycle through our pixel data, creating an element for each pixel using the processing method,
    # The processing method defines how the pixel is considered a floor or a wall cell.
    # The distinction between floor and wall cells is that floor cells are white #000000 and walls are black #FFFFFF
    # The rects list stores these values [index, x coord, y coord, hex code] for each cell
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


# Render our index.html page as a default starting page
@app.route('/')
def home():
    return render_template('index.html')


# Render our admin.html page when /uploader is accessed
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    # if we accessed this page through a post request check for a file
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

            # If file is accepted try to get the pixel data, to generate the rect elements values and send to grid page
            pixelData = getPixelData(f)
            w = pixelData[0]*10
            h = pixelData[1]*10
            rects = generateRectHtml(pixelData, processingMethod, tolerance)
            return render_template('admin.html', gridData=rects, width=w, height=h)

        else:
            return redirect("http://localhost:5000", code=400)


# Test route for if /database is accessed, this was an attempt at database integration, more work needed
@app.route('/database')
def database():
    # Attempt to connect to the database - values were removed
    con = pymysql.connect(host='IP', port='PORT', user='USER', password='PASS', database='DATABASE NAME')
    print(con)


if __name__ == '__main__':
    app.run(debug=True)


