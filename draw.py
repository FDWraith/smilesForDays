from display import *
from matrix import *

def add_circle( points, cx, cy, cz, r, step ):
    counter = step
    prevX = None
    prevY = None
    prevZ = None
    while( counter <= 1.00001 ):
        conv = math.pi * 2 * counter
        if( prevX == None or prevY == None or prevZ == None ):
            prevX = r * math.cos(conv) + cx
            prevY = r * math.sin(conv) + cy
            prevZ = cz
        else:
            newX = r * math.cos(conv) + cx
            newY = r * math.sin(conv) + cy
            newZ = cz
            add_edge( points, prevX, prevY, prevZ, newX, newY, newZ )
            prevX = newX
            prevY = newY
            prevZ = newZ
        counter += step
    #outside while loop, do it one more time
    conv = math.pi * 2 * counter
    newX = r * math.cos(conv) + cx
    newY = r * math.sin(conv) + cy
    newZ = cz
    add_edge( points, prevX, prevY, prevZ, newX, newY, newZ )

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    if curve_type == "hermite":
        add_hermite( points, x0, y0, x1, y1, x2, y2, x3, y3, step)

def add_hermite( points, x0, y0, x1, y1, rx0, ry0, rx1, ry1, step ):
    H = [ [ 2, -3, 0, 1 ],
          [ -2, 3, 0, 0 ],
          [ 1, -2, 1, 0 ],
          [ 1, -1, 0, 0 ] ]
    H2 = [ [ 2, -2, 1, 1 ],
           [ -3, 3, -2, -1 ],
           [ 0, 0, 1, 0 ],
           [ 1, 0, 0, 0 ] ]
    Gx = [ [x0, x1, rx0, rx1] ]
    Gy = [ [y0, y1, ry0, ry1] ]

    matrix_mult( H, Gx )
    Cx = Gx # result of matrix multiplication
    matrix_mult( H, Gy)
    Cy = Gy # same as above

    ax = Cx[0][0]
    bx = Cx[0][1]
    cx = Cx[0][2]
    dx = Cx[0][3]

    #print "a[%d], b[%d], c[%d], d[%d] for x:"%(ax,bx,cx,dx)

    ay = Cy[0][0]
    by = Cy[0][1]
    cy = Cy[0][2]
    dy = Cy[0][3]

    #print "a[%d], b[%d], c[%d], d[%d] for y:"%(ay,by,cy,dy)
    
    counter = step
    prevX = None
    prevY = None
    while( counter <= 1.00001 ):
        if( prevX == None or prevY == None ):
            prevX = int((ax * counter**3) + (bx * counter**2) + (cx * counter) + dx)
            prevY = int((ay * counter**3) + (by * counter**2) + (cy * counter) + dy)
        else:
            newX = int( (ax * counter**3) + (bx * counter**2) + (cx * counter) + dx )
            newY = int( (ay * counter**3) + (by * counter**2) + (cy * counter) + dy )
            #print "drawing line from %d, %d to %d, %d"%(prevX, prevY, newX, newY)
            add_edge( points, prevX, prevY, 0, newX, newY, 0)
            prevX = newX
            prevY = newY
        counter += step
    #outside while loop, do it one more time
    newX = int( (ax * counter**3) + (bx * counter**2) + (cx * counter) + dx )
    newY = int( (ay * counter**3) + (by * counter**2) + (cy * counter) + dy )
    add_edge( points, prevX, prevY, 0, newX, newY, 0)

def add_bezier( points, x0, y0, x1, y1, x2, y2, x3, y3, step ):
    B = [ [ -1, 3, -3, 1 ],
          [ 3, -6, 3, 0 ],
          [ -3, 3, 0, 0 ],
          [ 1, 0, 0, 0 ] ]
    Gx = [ [x0, x1, x2, x3] ]
    Gy = [ [y0, y1, y2, y3] ]

    matrix_mult( B, Gx )
    Cx = Gx
    matrix_mult( B, Gy )
    Cy = Gy

    ax = Cx[0][0]
    bx = Cx[0][1]
    cx = Cx[0][2]
    dx = Cx[0][3]

    #print "a[%d], b[%d], c[%d], d[%d] for x:"%(ax,bx,cx,dx)

    ay = Cy[0][0]
    by = Cy[0][1]
    cy = Cy[0][2]
    dy = Cy[0][3]

    #print "a[%d], b[%d], c[%d], d[%d] for y:"%(ay,by,cy,dy)
    
    counter = step
    prevX = None
    prevY = None
    while( counter <= 1.00001 ):
        if( prevX == None or prevY == None ):
            prevX = int((ax * counter**3) + (bx * counter**2) + (cx * counter) + dx)
            prevY = int((ay * counter**3) + (by * counter**2) + (cy * counter) + dy)
        else:
            newX = int( (ax * counter**3) + (bx * counter**2) + (cx * counter) + dx )
            newY = int( (ay * counter**3) + (by * counter**2) + (cy * counter) + dy )
            #print "drawing line from %d, %d to %d, %d"%(prevX, prevY, newX, newY)
            add_edge( points, prevX, prevY, 0, newX, newY, 0)
            prevX = newX
            prevY = newY
        counter += step
    #outside while loop, do it one more time
    newX = int( (ax * counter**3) + (bx * counter**2) + (cx * counter) + dx )
    newY = int( (ay * counter**3) + (by * counter**2) + (cy * counter) + dy )
    add_edge( points, prevX, prevY, 0, newX, newY, 0)
    

def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 points to draw'
        return
    
    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
