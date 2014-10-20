"""
acf
"""
from Tkinter import Button, Canvas, Frame, Label, Menu, Tk, \
    FLAT, LEFT, BOTH, X
import os
import sys
import tkXcursor


def set_cursors(widgets, *_):
    """
    set_cursors
    """
    if widgets['handled'] is True:
        return

    for (widget, cursor) in widgets['buttons']:
        tkXcursor.set_cursor(widget, cursor)

    widgets['handled'] = True


def draw_buttons(parent_widget, menu_name, directory):
    """
    draw_buttons
    """
    # Empty parent_widget
    for child in parent_widget.children.values():
        child.destroy()

    info = Label(
        parent_widget, text=menu_name + ': ' + directory,
        justify=LEFT, width=87,
    )
    info.pack()

    buttons = {
        'handled': False,
        'buttons': [],
    }

    i = 0
    file_lists = os.listdir(directory)
    file_lists.sort()
    for item in file_lists:
        path = os.path.join(directory, item)

        # Ignore hexadecimal filename
        try:
            int(item, 16)
            continue
        except ValueError:
            pass

        if os.path.isfile(path) and \
           not os.path.islink(path):

            # A frame for every 6 buttons
            if i % 6 == 0:
                frame = Frame(parent_widget)
                frame.pack(fill=X)

            button = Button(frame, height=2, bd=2,
                            relief=FLAT,
                            text=item)
            button.pack(side=LEFT, padx=1, pady=1)

            cursor = tkXcursor.load_cursor(button, path)

            button.bind('<Motion>', lambda _: set_cursors(buttons))

            buttons['buttons'].append((button, cursor))
            i += 1


def create_menu(menubar, widget):
    """
    create_menu
    """
    menus = [
        (
            'System theme',
            [
                '/usr/share/icons',
                '/usr/share/pixmaps',
            ],
            0,
        ),
        (
            'User theme',
            [
                os.path.join(os.path.expanduser("~"), '.icons')
            ],
            0,
        ),
        (
            'Command line theme',
            [
                item for item in sys.argv[1:] if len(sys.argv) > 0
            ],
            0,
        ),
        (
            'XCURSOR_PATH theme',
            os.getenv('XCURSOR_PATH', '').split(':'),
            0,
        ),
    ]

    for (title, dirs, underline) in menus:
        menu = Menu(menubar, tearoff=0)
        for path in dirs:
            if path == '':
                continue

            for item in os.listdir(path):
                test_dir = os.path.join(path, item, 'cursors')
                if os.path.isdir(test_dir):
                    menu.add_command(
                        label=item,
                        command=lambda w=widget, d=test_dir, m=title:
                        draw_buttons(w, m, d),
                    )
        menubar.add_cascade(
            label=title,
            menu=menu,
            underline=underline,
        )


def main():
    """
    main
    """
    root = Tk()
    root.wm_title(PROGNAME)

    menubar = Menu(root)
    root.config(menu=menubar)
    root.bind_all('<Control-q>', lambda _: root.quit())

    master_canvas = Canvas(root, width=700)
    master_canvas.pack(fill=BOTH)

    create_menu(menubar, master_canvas)

    root.mainloop()


PROGNAME = 'A cursor factory'
if __name__ == '__main__':
    main()
