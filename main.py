# This is the Team Project of INFOMKDE.
from query import query

import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Music Search Engine")

    input_label1 = tk.Label(root, text="Genre")
    input_label1.grid(row=0)

    input_entry1 = tk.Entry(root)
    input_entry1.grid(row=0, column=1)

    input_label2 = tk.Label(root, text="Performer")
    input_label2.grid(row=1)

    input_entry2 = tk.Entry(root)
    input_entry2.grid(row=1, column=1)

    input_label3 = tk.Label(root, text="Artist")
    input_label3.grid(row=2)

    input_entry3 = tk.Entry(root)
    input_entry3.grid(row=2, column=1)

    run_button = tk.Button(root, text="Search", width=10, command=lambda: query_music())
    run_button.grid(row=1, column=2, columnspan=2, padx=15, pady=10)

    # text = tk.StringVar()
    # text.set("Test")
    # output = tk.Label(root, textvariable=text, width=70, height=2)
    # output.grid(row=1, column=4)
    output = tk.Text(root)
    output.grid(row=1, column=4)

    def query_music():
        genre = input_entry1.get()
        performer = input_entry2.get()
        q = query()
        res = q.query_main(genre=genre, performer=performer)
        album = []
        website = []
        for row in res:
            print(row[0], row[4], "https://open.spotify.com/album/" + row[-1])

            album.append(row[0].n3().strip('"@en'))
            website.append(row[-1].n3().strip('"@en'))
        for i in range(len(album)):
            output.insert('insert', 'Album name = ' + album[i] + '\n' + 'Spotify Address = ' +
                          "https://open.spotify.com/album/" + website[i] + '\n\n')
    root.mainloop()





if __name__ == '__main__':
    main()
