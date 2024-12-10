import turtle
import math

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")  # Background color

# Create a turtle object
spirograph_turtle = turtle.Turtle()
spirograph_turtle.speed(0)  # Fastest speed for drawing

# Spirograph Function
def draw_spirograph(R, r, O):
    """
    R: Radius of the outer circle
    r: Radius of the inner circle
    O: Offset from the center of the inner circle
    """
    # Set initial angle
    spirograph_turtle.penup()
    spirograph_turtle.goto(R - O, 0)
    spirograph_turtle.pendown()    
    revolutions = 2
    initialAngle = 0
    finalAngle = 360

    # Draw the spirograph using parametric equations
    for angle in range(initialAngle, finalAngle * revolutions, 1):  # Loop over 2 revolutions
        a = math.radians(angle)
        x = (R - r) * math.cos(a) + O * math.cos(((R - r) / r) * a)
        y = (R - r) * math.sin(a) - O * math.sin(((R - r) / r) * a)
        spirograph_turtle.goto(x, y)

# Function to draw multiple spirographs with different colors
def multi_spirograph():
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'yellow']
    spirograph_turtle.width(2)
    
    for i in range(6):
        spirograph_turtle.pencolor(colors[i % len(colors)])  # Change color
        draw_spirograph(150, 75 + (i * 10), 50)  # Modify inner circle size for variation

# Call the multi_spirograph function to draw the pattern
multi_spirograph()

# Hide the turtle and display the result
spirograph_turtle.hideturtle()

# Keep the window open
screen.mainloop()
