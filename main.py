from knighttourapp import *


def main():
    root = tk.Tk()
    root.title("Knight's Tour Visualization")
    root.geometry(f"{window_width}x{window_height}+{X}+{Y}")
    app = KnightTourApp(root)
    app.run()


if __name__ == "__main__":
    main()
