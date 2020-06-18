from flask import Flask, render_template, request, redirect
from PIL import Image
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
        im = im.resize((maxWidth, hsize), Image.ANTIALIAS)

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


def generateRectHtml(pixelData):
    # Set starting values
    rects = []
    x = 0
    y = 0

    # Remove width and height passed through from the getPixelData (first pos is width, second is height)
    w = pixelData.pop(0)
    h = pixelData.pop(0)

    # Cycle through our pixel data creating the html rect element with the values
    index = 0
    for val in pixelData:
        hexVal = convertRgbToHex(val[2])
        temp = '<rect id="rect-'+str(index)+'" x="'+str(x)+'" y="'+str(y)+'" width="10" height="10" fill="'+hexVal+'" stroke="#000" onClick="setStatus(this);"></rect>'
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
        if len(request.files) != 0:
            f = request.files['file']
            # Server side file checking (can be faked if the file uploaded has the name to fit these conditions)
            if str(f.filename).endswith(('.png', '.jpeg', '.jpg', '.PNG')):

                # If file is accepted try to get the pixel data, use to generate the rect elements and send to grid page
                pixelData = getPixelData(f)
                w = pixelData[0]*10
                h = pixelData[1]*10
                rects = generateRectHtml(pixelData)
                return render_template('admin.html', gridData=rects, width=w, height=h)

            else:
                return redirect("http://localhost:5000", code=400)

        elif request.form.get("gridButton"):
            print(request.values.get("gridButton"))
            print(request.values.get("startLocInput"))
            print(request.values.get("destinationLocInput"))
            return "<h1>all good</h1>"

        else:
            return "<h1> in the else statment </h1>"


if __name__ == '__main__':
    app.run(debug=True)


