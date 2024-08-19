import matplotlib.pyplot as plt
import io
import base64
from matplotlib.lines import Line2D
from flask import Flask, render_template

app = Flask(__name__)


class ShapeParser:
    """This class analyzes and creates the required shapes."""

    def __init__(self):
        self.shapes = []

    def parse_command(self, command):
        """
        Takes the command as simple text and
        then decides what shape to create
        based on the user input
        """
        command = command.strip().lower()

        if command == "create rectangle;":
            self.create_rectangle()
        elif command == "create circle;":
            self.create_circle()
        elif command == "create line;":
            self.create_line()
        else:
            print(f"Unknown command: {command}")

    def create_rectangle(self):
        """
        Creates a simple rectangle
        and appends it to the shapes list
        """
        rect = plt.Rectangle((0.1, 0.1), 0.4, 0.2, fill=None, edgecolor='r')
        self.shapes.append(rect)

    def create_circle(self):
        """
        Creates a simple circle
        and appends it to the shapes list
        """
        circ = plt.Circle((0.5, 0.5), 0.1, fill=None, edgecolor='b')
        self.shapes.append(circ)

    def create_line(self):
        """
        Creates a simple line and
        appends it to the shapes list
        """
        line = Line2D([0.1, 0.9], [0.1, 0.9], color='g')
        self.shapes.append(line)

    def draw(self):
        """
        Draws all shapes on a board using matplotlib library
        """
        fig, ax = plt.subplots()

        for shape in self.shapes:
            if isinstance(shape, Line2D):
                ax.add_line(shape)
            else:
                ax.add_patch(shape)

        # Set the aspect of the plot to be equal
        ax.set_aspect('equal', 'box')
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])

        buf = io.BytesIO()
        # Show grid for better visualization
        ax.grid(True)
        buf.seek(0)
        plt.savefig(buf, format='png')

        img_str = base64.b64encode(buf.read()).decode('utf-8')

        return img_str

parser = ShapeParser()
# Example usage


@app.route("/")
def index():
    parser.parse_command("create rectangle;")
    parser.parse_command("create circle;")
    parser.parse_command("create line;")
    img_str = parser.draw()
    return render_template("index.html", img_str=img_str)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
