import difflib
import requests
import bs4
import tkinter
from tkinter import messagebox

class UniquePlagiarismChecker:
    def root_quit(self):
        self.root.destroy()

    def quit_plagiarised_window(self):
        self.plagiarised_window.destroy()

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Unique Plagiarism Checker')
        self.root.geometry('600x620')
        self.root.iconbitmap('plag.ico')

        def_x = 50
        def_y = 25

        lbl_root_title = tkinter.Label(self.root, text='Unique Plagiarism Checker')
        lbl_root_title.config(font=('TkDefaultFont', 24))
        lbl_root_title.place(x=def_x, y=def_y)

        lbl_for_checking = tkinter.Label(self.root, text='Enter your text',
                                         font='TkDefaultFont, 10')
        lbl_for_checking.place(x=def_x, y=def_y+90)
        self.ent_for_checking = tkinter.Text(self.root, height=16, width=62)
        self.ent_for_checking.place(x=def_x, y=def_y+120)

        lbl_website_for_checking = tkinter.Label(self.root, text='Enter the website URL to compare')
        lbl_website_for_checking.place(x=def_x, y=def_y+410)
        self.ent_website_for_checking = tkinter.Entry(self.root, width=90)
        self.ent_website_for_checking.place(x=def_x, y=def_y+440, height=30)

        self.btn_calc_plagiarisedness = tkinter.Button(self.root, text='Check Similarity', command=self.calc_plagiarisedness,
                                                       borderwidth=10, height=2, width=16)
        self.btn_calc_plagiarisedness.place(x=def_x + 180, y=def_y + 510)

        self.btn_exit_win = tkinter.Button(self.root, text='Quit', command=self.root_quit,
                                           height=2, width=9, borderwidth=5)
        self.btn_exit_win.place(x=def_x+430, y=def_y+510)

        self.root.mainloop()

    def display_similarity_result(self, similarity_percentage):
        self.plagiarised_window = tkinter.Toplevel()
        self.plagiarised_window.geometry('310x170')
        self.plagiarised_window.iconbitmap('plag.ico')

        btn_exit_plagiarised_window = tkinter.Button(self.plagiarised_window, text='Quit', borderwidth=5,
                                                     command=self.quit_plagiarised_window, height=1, width=8)
        btn_exit_plagiarised_window.place(x=93, y=120)

        if similarity_percentage > 5.0:  # If the content is similar
            similarity_info_text = f"{similarity_percentage}% Similarity Detected"
            lbl_similarity_info = tkinter.Label(self.plagiarised_window, text=similarity_info_text,
                                                fg='red')
            lbl_similarity_info.config(font=('TkDefaultFont', 16))
            lbl_similarity_info.place(x=32, y=39)
        else:  # If the content is not similar
            similarity_info_text = f'Content is Unique\n{similarity_percentage}% similarity detected'
            lbl_similarity_info = tkinter.Label(self.plagiarised_window, text=similarity_info_text,
                                                fg='green')
            lbl_similarity_info.config(font=('TkDefaultFont', 16))
            lbl_similarity_info.place(x=49, y=28)

    def calc_plagiarisedness(self):
        try:
            user_text = self.ent_for_checking.get('1.0', tkinter.END)
            website_url = self.ent_website_for_checking.get()

            # Ensure the website URL is valid
            if not website_url.startswith('http://') and not website_url.startswith('https://'):
                website_url = 'http://' + website_url

            website_response = requests.get(website_url)

            if website_response.status_code != 200:
                raise requests.RequestException(f"HTTP error {website_response.status_code}")

            website_content = website_response.text
            soup = bs4.BeautifulSoup(website_content, 'lxml')
            soup_text = soup.findAll(text=True)

            visible_text = ''
            for char in soup_text:
                visible_text = visible_text + char
            website_text = visible_text

            similarity_checker = difflib.SequenceMatcher(None, user_text, website_text)
            similarity_percentage = round(float(similarity_checker.ratio() * 100), 2)

            self.ent_for_checking.delete('1.0', tkinter.END)
            self.ent_website_for_checking.delete(0, tkinter.END)

            self.display_similarity_result(similarity_percentage)

        except requests.RequestException as req_err:
            messagebox.showerror('Request Error', f'Failed to access the website: {str(req_err)}')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')

if __name__ == "__main__":
    UniquePlagiarismChecker()
