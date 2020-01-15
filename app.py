from flask import Flask, render_template, url_for
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
from data import messages
import os
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def weish_img_mk(messa, who):

    target = os.path.join(APP_ROOT, 'static/')
    if not os.path.isdir(target):
        print(target)
        os.mkdir(target)
    else:
        print(f'path is created {target}')
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    # variables for image size
    x1 = 612
    y1 = 612
    # my quote
    sentence = messa + '\n' + str(who)
    # choose a font
    fnt = ImageFont.truetype('static/Cinzel-Regular.ttf', 30)
    img = Image.new('RGB', (x1, y1), color=(b, g, r))
    d = ImageDraw.Draw(img)
    # find the average size of the letter
    sum = 0
    for letter in sentence:
        sum += d.textsize(letter, font=fnt)[0]
    average_length_of_letter = sum/len(sentence)
    # find the number of letters to be put on each line
    number_of_letters_for_each_line = (x1/1.618)/average_length_of_letter
    incrementer = 0
    fresh_sentence = ''
    # add some line breaks
    for letter in sentence:
        if(letter == '-'):
            fresh_sentence += '\n\n' + letter
        elif(incrementer < number_of_letters_for_each_line):
            fresh_sentence += letter
        else:
            if(letter == ' '):
                fresh_sentence += '\n'
                incrementer = 0
            else:
                fresh_sentence += letter
        incrementer += 1
    print(fresh_sentence)
    # render the text in the center of the box
    dim = d.textsize(fresh_sentence, font=fnt)
    x2 = dim[0]
    y2 = dim[1]
    qx = (x1/2 - x2/2)
    qy = (y1/2-y2/2)
    d.text((qx, qy), fresh_sentence, align="center",
           font=fnt, fill=(0, 0, 0))
    destination = '/'.join([target, 'quote.png'])
    img.save(destination)


@app.route('/')
@app.route('/info/<string:num>', methods=["GET", 'POST'])
def home(name=None, num='-Muhammad KAMAL'):
    weish_img_mk(random.choice(messages), num)
    return render_template('card.html', name=name, time=datetime.now())


if __name__ == '__main__':
    # weish_img_mk(random.choice(messages), random.randint(0, 255),
    #              random.randint(0, 255), random.randint(0, 255))
    app.run(debug=True)
