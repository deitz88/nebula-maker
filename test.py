  
import cairo, sys, argparse, copy, math, random

def make_nebula(width, height, cr):

    float_gen = lambda a, b: random.uniform(a, b)

    colors = []
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


    def build(width, height, cr):
        
        initial = 1
        deviation = 500
        basedeforms = 1
        finaldeforms = 3
        minshapes = 1
        maxshapes = 200
        shapealpha = .0045

        cr.set_source_rgb(0, 0, 0)
    
        cr.rectangle(0, 0, width, height)
        
        cr.fill()
        

        cr.set_line_width(1)

        for p in range(-int((height*.2)/3), int((height*1.2)/3), 80):
            cr.set_source_rgba(random.choice(colors)[0], random.choice(colors)[1], random.choice(colors)[2], shapealpha)

            shape = octagon(random.randint(width*.3, width*.8), random.randint(1, height), random.randint(4, 30))
            
            baseshape = deform(shape, basedeforms, initial)

            for j in range(random.randint(minshapes, maxshapes)):
                tempshape = copy.deepcopy(baseshape)
                layer = deform(tempshape, finaldeforms, deviation)

                for i in range(len(layer)):
                    cr.line_to(layer[i][0], layer[i][1])
                cr.fill()

    build()