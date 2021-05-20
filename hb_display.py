from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time
import os

class display(object):
    """ hueBerry Display API """
    # This class will create a display object and allow
    # hueBerry style text menus to be drawn on an i2c or spi SSD1306 display
    # as well as a few more text drawing functions

    def __init__(self, console=0, mirror = 0, rotation = 0, spi_display = 0):
        self.console = console
        self.mirror = mirror
        self.rotate_angle = rotation
        if (self.console == 0 or self.mirror == 1):
            import Adafruit_SSD1306
            if spi_display == 0:
                self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)
            elif spi_display == 1:
                import Adafruit_GPIO.SPI as SPI
                RST = 24
                DC = 23
                SPI_PORT = 0
                SPI_DEVICE = 0
                self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
            try:
                self.disp.begin()
            except:
                print("Something went wrong... Will try to load SSD1306 as SPI")
                import Adafruit_GPIO.SPI as SPI
                RST = 24
                DC = 23
                SPI_PORT = 0
                SPI_DEVICE = 0
                try:
                    self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
                    self.disp.begin()
                except:
                    print("No display connected? \nOutputting IP address as morse code LOL")
                    import hb_morse
                    hb_morse.ip2morse(mirror = 1)
            self.width = self.disp.width
            self.height = self.disp.height
        else:
            #console specific initiation goes here
            #Adafruit OLED library standard width for string calculation
            self.width = 128
            self.height = 64
        self.image = Image.new('1', (self.width, self.height))
        self.font = ImageFont.load_default()
        self.draw = ImageDraw.Draw(self.image)
        self.time_format = True

    def display_time(self,time_format):
        # Collect current time and date
        self.time_format = time_format
        if(self.time_format):
            current_time = time.strftime("%-I:%M")
        else:
            current_time = time.strftime("%-H:%M")
        current_date = time.strftime("%m / %d / %Y")
        #Get 24 hour time variable
        H = int(time.strftime("%H"))
        if (self.console == 1):
            os.system('clear')
            print(" Currently on Time screen")
            print("----------------------------")
            print("")
            print("")
            print("          "+str(current_time))
            print("")
            print("       "+str(current_date))
            print("----------------------------")
            if (self.mirror == 0):
                return
        # Set font type and size
        if H >= 21 or H < 6:
            font = ImageFont.truetype('BMW_outline.otf', 40)
            #print("outline")
        else:
            font = ImageFont.truetype('BMW_naa.ttf', 45)
            #font = ImageFont.truetype('BMW_outline.otf', 40)
            #print("regular")
        #print H
        #time.sleep(100)
        # Position time
        x_pos = (self.width/2)-(self.string_width(font,current_time)/2)
        y_pos = 2 + (self.disp.height-4-8)/2 - (35/2)
        # Clear image buffer by drawing a black filled box
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        # Draw time
        self.draw.text((x_pos, y_pos), current_time, font=font, fill=255)
        # Set font type and size
        font = ImageFont.truetype('BMW_naa.ttf', 13)
        #font = ImageFont.load_default()
        # Position date
        x_pos = (self.width/2)-(self.string_width(font,current_date)/2)
        y_pos = self.disp.height-10
        # Draw date during daytime hours
        if H < 21 and H > 6:
            self.draw.text((x_pos, y_pos), current_date, font=font, fill=255)
        # Draw the image buffer
        self.send_to_screen()

    def display_2lines(self,line1,line2,size):
        if(self.time_format):
            current_time = time.strftime("%-I:%M")
        else:
            current_time = time.strftime("%-H:%M")
        current_date = time.strftime("%m / %d / %Y")
        if (self.console == 0 or self.mirror == 1):
            font = ImageFont.truetype('BMW_naa.ttf', 11)
            #font = ImageFont.load_default()
            #draw a clock
            # Position time
            x_pos = (self.width/2)-(self.string_width(font,current_time)/2)
            y_pos = 0
            # Clear image buffer by drawing a black filled box
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
            # Draw time
            self.draw.text((x_pos, y_pos), current_time, font=font, fill=255)
            #draw a menu line
            timeheight = 10
            self.draw.line((0, timeheight, self.width, timeheight), fill=255)
            # Set font type and size
            fit_size = self.resize_string(current_size = size, string = line1)
            fit_size = self.resize_string(current_size = fit_size, string = line2)
            font = ImageFont.truetype('BMW_naa.ttf', fit_size, encoding = "unic")
            x_pos = (self.width/2)-(self.string_width(font,line1)/2)
            y_pos = 8 + (self.disp.height-4-8)/2 - (35/2)
            self.draw.text((x_pos, y_pos), line1, font=font, fill=255)
            x_pos = (self.width/2)-(self.string_width(font,line2)/2)
            y_pos = self.disp.height-26
            self.draw.text((x_pos, y_pos), line2, font=font, fill=255)
            self.send_to_screen()
        if (self.console == 1):
            os.system('clear')
            print("Currently Displaying 2 lines")
            print("----------------------------")
            print("         "+str(current_time))
            print("----------------------------")
            print("        "+str(line1))
            print("        "+str(line2))
            print("")
            print("----------------------------")
            return

    def display_3lines(self,line1,line2,line3,size,offset):
        if(self.time_format):
            current_time = time.strftime("%-I:%M")
        else:
            current_time = time.strftime("%-H:%M")
        current_date = time.strftime("%m / %d / %Y")
        if (self.console == 0 or self.mirror == 1):
            # Clear image buffer by drawing a black filled box
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
            font = ImageFont.truetype('BMW_naa.ttf', 11)
            #font = ImageFont.load_default()
            #draw a clock
            # Position time
            x_pos = (self.width/2)-(self.string_width(font,current_time)/2)
            y_pos = 0
            # Draw time
            self.draw.text((x_pos, y_pos), current_time, font=font, fill=255)
            #draw a menu line
            timeheight = 10
            self.draw.line((0, timeheight, self.width, timeheight), fill=255)
            # Set font type and size
            #font = ImageFont.truetype('BMW_naa.ttf', size)
            font = ImageFont.truetype('BMW_naa.ttf', size, encoding = "unic")
            x_pos = (self.width/2)-(self.string_width(font,line1)/2)
            y_pos = 8 + (self.disp.height-4-8)/2 - (35/2)
            self.draw.text((x_pos, y_pos), line1, font=font, fill=255)
            x_pos = (self.width/2)-(self.string_width(font,line2)/2)
            y_pos += offset
            self.draw.text((x_pos, y_pos), line2, font=font, fill=255)
            x_pos = (self.width/2)-(self.string_width(font,line3)/2)
            y_pos += offset
            self.draw.text((x_pos, y_pos), line3, font=font, fill=255)
            self.send_to_screen()
        if (self.console == 1):
            os.system('clear')
            print("Currently Displaying 3 lines")
            print("----------------------------")
            print("         "+str(current_time))
            print("----------------------------")
            print("        "+str(line1))
            print("        "+str(line2))
            print("        "+str(line3))
            print("----------------------------")
            return

    def display_custom(self,text):
        if (self.console == 0 or self.mirror == 1):
            # Clear image buffer by drawing a black filled box
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
            # Set font type and size
            #font = ImageFont.truetype('FreeMono.ttf', 8)
            font = ImageFont.load_default()
            # Position SSID
            x_pos = (self.width/2) - (self.string_width(font,text)/2)
            y_pos = (self.height/2) - (8/2)
            # Draw SSID
            self.draw.text((x_pos, y_pos), text, font=font, fill=255)
            # Draw the image buffer
            self.send_to_screen()
        if (self.console == 1):
            os.system('clear')
            print("       display_custom")
            print("----------------------------")
            print("")
            print("")
            print("        "+str(text))
            print("")
            print("")
            print("----------------------------")
            return

    def draw_flashlight(self):
        if (self.console == 0 or self.mirror == 1):
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=1)
            self.send_to_screen()
        if (self.console == 1):
            os.system('clear')
            print("         Flashlight")
            print("----------------------------")
            print("############################")
            print("############################")
            print("############################")
            print("############################")
            print("############################")
            print("----------------------------")
            return

    def send_to_screen(self):
        if self.rotate_angle > 0 :
            self.disp.image(self.image.rotate(self.rotate_angle))
        else:
            self.disp.image(self.image)
        self.disp.display()

    def resize_string(self, current_size, string):
        font = ImageFont.truetype('BMW_naa.ttf', current_size, encoding = "unic")
        current_width = self.string_width(font,string)
        if current_width > self.width:
            #resize the faka
            while current_width > self.width:
                current_size = current_size - 1
                font = ImageFont.truetype('BMW_naa.ttf', current_size, encoding = "unic")
                current_width = self.string_width(font,string)
        max_size = current_size
        return max_size

    def string_width(self,fontType,string):
        string_width = 0
        for i, c in enumerate(string):
            char_width, char_height = self.draw.textsize(c, font=fontType)
            string_width += char_width
        return string_width

    def IntelliDraw(self,drawer,text,font,containerWidth):
        # Modified and stolen from https://mail.python.org/pipermail/image-sig/2004-December/003064.html
        # I'm not using it yet but this is some good inspiration
        words = text.split()
        lines = [] # prepare a return argument
        lines.append(words)
        finished = False
        line = 0
        while not finished:
            thistext = lines[line]
            newline = []
            innerFinished = False
            while not innerFinished:
                #print 'thistext: '+str(thistext)
                #print newline
                if drawer.textsize(' '.join(thistext),font)[0] > containerWidth:
                    # this is the heart of the algorithm: we pop words off the current
                    # sentence until the width is ok, then in the next outer loop
                    # we move on to the next sentence.
                    newline.insert(0,thistext.pop(-1))
                else:
                    innerFinished = True
                if "\n" in newline:
                    innerFinished = True
                    #This if doesn't work but I want it to work... :'(
            if len(newline) > 0:
                lines.append(newline)
                line = line + 1
            else:
                finished = True
        tmp = []
        for i in lines:
            tmp.append( ' '.join(i) )
        lines = tmp
        (width,height) = drawer.textsize(lines[0],font)
        total_height = len(lines)*(height+1)
        return (lines,width,height,total_height)

    def display_textbrowser(self,text,centered=0):
        try:
            hb_encoder.__name__
        except:
            try:
                import hb_encoder
            except ImportError:
                print("This function requires the hb_encoder module")
        encoder = hb_encoder.RotaryClass()
        encoder.pos = 0
        pos,pushed = encoder.get_state()
        #text = 'One very extremely long string that cannot possibly fit \
        #into a small number of pixels of horizontal width, and the idea \
        #is to break this text up into multiple lines that can be placed like \
        #a paragraph into our image'
        lines,tmp,h,total_h = self.IntelliDraw(self.draw,text,self.font,self.width)
        j = 0
        encoder.wait_for_button_release()
        while True:
            self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
            offset = ((h/2)*-1)*pos
            j = 0
            for i in lines:
                if(centered == 1):
                    x_pos = (self.width/2) - (self.string_width(self.font,i)/2)
                else:
                    x_pos = 0
                self.draw.text( (x_pos,offset+(j*h)), i , font=self.font, fill=255)
                j = j + 1
            self.disp.image(self.image)
            self.disp.display()
            pos,pushed = encoder.get_state()
            if pushed == 1:
                break
            time.sleep(0.01)
        encoder.wait_for_button_release()
        return

    def display_max_text(self,text,centered=0,offset = 0):
        lines,tmp,h,total_h = self.IntelliDraw(self.draw,text,self.font,self.width)
        j = offset
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        offset = 0
        for i in lines:
            #Line Centering code
            if(centered == 1):
                x_pos = (self.width/2) - (self.string_width(self.font,i)/2)
            else:
                x_pos = 0
            self.draw.text( (x_pos,offset+(j*h)), i , font=self.font, fill=255)
            j = j + 1
        if (self.console == 1):
            os.system('clear')
            line_count = 0
            print("      Display Max Text")
            print("----------------------------")
            for i in lines:
                if line_count > 5:
                    break
                print(i)
                line_count += 1
            print("----------------------------")
        if (self.console == 0 or self.mirror == 1):
            self.disp.image(self.image)
            self.disp.display()




if __name__ == "__main__":
    import time
    import hb_display
    test = hb_display.display(console = 1, mirror = 1)
    test.display_time()
    time.sleep(1)
    test.display_custom("holy shit")
    time.sleep(1)
    test.display_2lines("omg","it's working",17)
    time.sleep(1)
    test.display_3lines("for real","it's working","praise cheese",13,15)
    time.sleep(1)
    text = 'One very extremely long string that cannot possibly fit \
    into a small number of pixels of horizontal width, and the idea \
    is to break this text up into multiple lines that can be placed like \
    a paragraph into our image'
    test.display_max_text(text)
    time.sleep(1)
