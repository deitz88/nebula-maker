  
import cairo, sys, argparse, copy, math, random

def make_nebula():

    float_gen = lambda a, b: random.uniform(a, b)

    colors = []
    # for x in range(10):
    #     colors.append((0,0,0))
    for i in range(15):
        colors.append((float_gen(.1, 1.3), float_gen(.1, .5), float_gen(.1, 1.3)))
        colors.append((0, 0, 0))

    def octagon(x_orig, y_orig, side):
        side = side * random.randint(1, 3)
        x = x_orig
        y = y_orig
        d = side / math.sqrt(2)

        oct = []

        oct.append((x, y))

        x += side
        oct.append((x, y))

        x += d
        y += d
        oct.append((x, y))

        y += side
        oct.append((x, y))

        x -= d
        y += d
        oct.append((x, y))

        x -= side
        oct.append((x, y))

        x -= d
        y -= d
        oct.append((x, y))

        y -= side
        oct.append((x, y))

        x += d
        y -= d
        oct.append((x, y))

        return oct

    def deform(shape, iterations, variance):
        for i in range(iterations):
            for j in range(len(shape)-1, 0, -1):
                midpoint = ((shape[j-1][0] + shape[j][0])/2 + float_gen(-variance, variance), (shape[j-1][1] + shape[j][1])/2 + float_gen(-variance, variance))
                shape.insert(j, midpoint)
        return shape


    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("--width", default=3000, type=int)
        parser.add_argument("--height", default=2000, type=int)
        parser.add_argument("-i", "--initial", default=1, type=int)
        parser.add_argument("-d", "--deviation", default=500, type=int)
        parser.add_argument("-bd", "--basedeforms", default=1, type=int)
        parser.add_argument("-fd", "--finaldeforms", default=3, type=int)
        parser.add_argument("-mins", "--minshapes", default=1, type=int)
        parser.add_argument("-maxs", "--maxshapes", default=200, type=int)
        parser.add_argument("-sa", "--shapealpha", default=.0045, type=float)
        # parser.add_argument("--mult", default=random.randint(1, 5), type=range)
        args = parser.parse_args()

        width, height = args.width, args.height
        initial = args.initial
        deviation = args.deviation

        basedeforms = args.basedeforms
        finaldeforms = args.finaldeforms

        minshapes = args.minshapes
        maxshapes = args.maxshapes
        # mult = args.mult
        
        # if mult == 1:
        #     multi = (random.randint(width, width+500), 1.9)
        # elif mult == 2:
        #     multi = (1.5, 9)
        # elif mult == 3:
        #     multi = (.9, 1.2)
        # elif mult == 4:
        #     multi = (.4, .8)
            
        shapealpha = args.shapealpha

        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(ims)

        # background black
        cr.set_source_rgb(0, 0, 0)
        # cr.rectangle(0, 0, width*3, height*3)
        cr.rectangle(0, 0, width, height)
        
        cr.fill()
        

        cr.set_line_width(1)

        for p in range(-int((height*.2)/3), int((height*1.2)/3), 80):
            cr.set_source_rgba(random.choice(colors)[0], random.choice(colors)[1], random.choice(colors)[2], shapealpha)

            # shape = octagon(random.randint(-100, width+100), p, random.randint(100, 300))0
            # shape = octagon(random.randint(width*.9, width*1.4), p, random.randint(100, 300))
            shape = octagon(random.randint(width*.3, width*.8), random.randint(1, height), random.randint(4, 30))
            
            baseshape = deform(shape, basedeforms, initial)

            for j in range(random.randint(minshapes, maxshapes)):
            # for j in range(1, 5):
                tempshape = copy.deepcopy(baseshape)
                layer = deform(tempshape, finaldeforms, deviation)

                for i in range(len(layer)):
                    cr.line_to(layer[i][0], layer[i][1])
                cr.fill()

        # for p in range(-int(height*.2), int(height*1.2), 60):
        #     cr.set_source_rgba(0, 0, 0, 2)

        #     shape = octagon(random.randint(-100, width+100), (random.randint(2.3*height, 2.9*height)), random.randint(100, 300))
        #     baseshape = deform(shape, basedeforms, initial)

        #     # for j in range(random.randint(minshapes, maxshapes)):
        #     for j in range(20):
        #         tempshape = copy.deepcopy(baseshape)
        #         layer = deform(tempshape, finaldeforms, deviation)

        #         for i in range(len(layer)):
        #             cr.line_to(layer[i][0], layer[i][1])
        #         cr.fill()

        
        ims.write_to_png('Examples/nebula' + '.png')

    if __name__ == "__main__":
        main()
make_nebula()