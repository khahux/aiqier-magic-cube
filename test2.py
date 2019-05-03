
from magic import rotate

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import OpenGL.GL as OGLGL
import math

COLOR_YELLOW = (1, 1 , 0)
COLOR_WHITE = (1, 1, 1)
COLOR_BLUE = (0, 0, 1)
COLOR_RED = (1, 0, 0)
COLOR_GREEN = (0, 0.6, 0)
COLOR_ORANGE = (1, 0.49, 0.14)
COLOR_BLACK = (0, 0, 0)
last_time = 0


def drawImage():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #glShadeModel(GL_FLAT)
    glColor3f(*COLOR_GREEN)
    glBegin(GL_POLYGON)
    glVertex3f(0.3,0.3,0.8)
    glVertex3f(0.3,0.9,0.8)
    glVertex3f(0.9, 0.9, 0.8)
    glVertex3f(0.9, 0.3, 0.8)
    glEnd()

    glColor3f(*COLOR_RED)
    glBegin(GL_POLYGON)
    glVertex3f(0.5,0.5,1.3)
    glVertex3f(0.5,1.0,1.3)
    glVertex3f(1.0, 1.0, 1.3)
    glVertex3f(1.0, 0.5, 1.3)
    glEnd()

    glColor3f(*COLOR_YELLOW)
    glBegin(GL_POLYGON)
    glVertex3f(0.1,0.1,0.2)
    glVertex3f(0.1,0.7,0.2)
    glVertex3f(0.7, 0.7, 0.2)
    glVertex3f(0.7, 0.1, 0.2)
    glEnd()

    glutSwapBuffers()


def visible(vis):
    if vis == GLUT_VISIBLE:
        glutIdleFunc(idle)
    else:
        glutIdleFunc(None)

def idle():
    global last_time
    time = glutGet(GLUT_ELAPSED_TIME)
    if last_time == 0 or time >= last_time + 40:
        last_time = time
        glutPostRedisplay()

def special(key, x, y):
    glutPostRedisplay()
    #pass


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(400, 400)
    glutCreateWindow(b"show model")


    # init
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)

        # Reset matrix
    glLoadIdentity()
    user_theta = 0
    x = 2 * math.cos(user_theta)
    y = 2 * math.sin(user_theta)
    z = user_theta
    d = math.sqrt(x * x + y * y + z * z)
    #glFrustum(-d * 0.5, d * 0.5, -d * 0.5, d * 0.5, d - 1.1, d + 1.1)
    gluPerspective(45.0,float(640)/float(400),0.1,200.0)
    gluLookAt(1, 1.5, 3, 0, 0, 0, 0, 0, 1)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 2.0, -1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.7, 0.7, 0.7, 1.0])
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


    # Set the callback function for display
    glutDisplayFunc(drawImage)
    glutVisibilityFunc(visible)
    glutSpecialFunc(special)
    #glutIdleFunc(drawImage)
    glutMainLoop()
if __name__ == "__main__":
    main()