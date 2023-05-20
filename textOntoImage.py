# take a jpg and a text file
# it then creates a new jpg with the text written on it in the color of the original image
#16px = 12pt font

def guessBackgroundColorOfImage(imageName):
    from PIL import Image
    with Image.open(imageName).convert('RGB') as im:
        answer = max(im.getcolors(im.size[0]*im.size[1]))
        return answer[1]

# imports needed modules from PIL
# needs image name with extension
# needs desired background color RGB values, can work with any color but works best if is the background of the image
def getLocationOfCharectersThatCanBePlacedOnImage(imageName, backgroundColor):
    from PIL import Image
    # read in image, must be 1080x1080 pixels
    with Image.open(imageName, 'r').convert('RGB') as im:
    
        # get the width and height of the image
        width, height = im.size
        print("width:", width, "  height:", height)
        # get pixels
        pix_val = list(im.getdata()) # a list of tuples of all the rgb values in the image
        pix_val = [pix_val[i * width:(i + 1) * width] for i in range(height)] # a list of lists of tuples the lenght of the height of the image, each index is a row of pixels
        print("number of pixels:", len(pix_val) * len(pix_val[0]))
        # show first 10 pixels
        print("first 10 pixels:", pix_val[0][0:10])
        backgroundLocations = [] # a list of lists of tuples the pixel locations in the image
        
        # determine the number of white background pixels
        for i in range(0, height - 1, 10):
            for j in range(0, width - 1, 8):
                if pix_val[i][j] == backgroundColor:
                    backgroundLocations.append((j, i))
                    
        return backgroundLocations

def writeTextOntoImage(imageName, textFileName, backgroundColor, textColor):
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw
    
    # get locations for text
    backgroundLocations = getLocationOfCharectersThatCanBePlacedOnImage(imageName, backgroundColor)
    
    with Image.open(imageName, 'r').convert('RGB') as im:
        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(im)
        # Custom font style and font size
        myFont = ImageFont.truetype('font.ttf', 12)
        
        # open text file
        with open(textFileName, 'r') as f:
            # Read all lines from the file
            lines = f.readlines()

            # Remove leading and trailing whitespace from each word, and remove blank lines
            cleaned_lines = [line.strip() for line in lines if line.strip()]

            # Concatenate all lines into a single string
            concatenated_string = "".join(cleaned_lines)

            # Store all characters in a list
            characters_list = list(concatenated_string)
  
        # determine a height and width of the image that breaks it into chucks the size of the number of characters in the text file
        # write text onto image I1.text((0, 0), text[0], font=myFont, fill=(0, 0, 0))
        # because 12pt font is 16px, after each line we go down 4px and after each character we go over 4px
        print("number of characters:", len(characters_list))
        print("number of background locations:", len(backgroundLocations))
        if len(characters_list) < len(backgroundLocations):
            print("WARNING! Not enough characters to fill image")
            for i in range(0, len(characters_list)):
                I1.text(backgroundLocations[i], characters_list[i], font=myFont, fill=textColor)
                print("writing character:", characters_list[i], "at location:", backgroundLocations[i])
        elif len(characters_list) > len(backgroundLocations):
            print("WARNING! Too many characters to fill image")
            for i in range(0, len(backgroundLocations)):
                I1.text(backgroundLocations[i], characters_list[i], font=myFont, fill=textColor)
            
        # output the image    
        im.save("out.png")
    
# main
imagename = "mario.jpg"
backgroundColor = guessBackgroundColorOfImage(imagename)
backgroundColor = (255,255,255)
textColor = (0,0,0)
print("background color:", backgroundColor)
textFileName = "generation.txt"

writeTextOntoImage(imagename, textFileName, backgroundColor, textColor)
