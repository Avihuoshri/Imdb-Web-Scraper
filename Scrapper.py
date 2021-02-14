# Please install the folowing:
# Download chromdriver from https://chromedriver.storage.googleapis.com/index.html?path=88.0.4324.96/
# pip install pillow
# pip install selenium
# pip install Pillow
# pip install requests

from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import tkinter as tk
import requests
import io

def makeDetails(search_input):
    file_string = ""
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.imdb.com/find?q=" + search_input)
    link = driver.find_element_by_link_text("Movie")
    link.click()

    imdb_prefix = "https://www.imdb.com/"

    movie_list_page = requests.get(driver.current_url)
    soup = BeautifulSoup(movie_list_page.content, 'html.parser')
    movies = soup.find_all('td',class_ = "result_text")


    for movie in movies:
        if "in development" not in movie.text:
            movie_page_link = movie.find('a')['href']
            movie_detail_page = requests.get(imdb_prefix + movie_page_link)
            movie_soup = BeautifulSoup(movie_detail_page.content, 'html.parser')
            movie_title = movie_soup.body.h1.text.replace("  ","")
            movie_directors_stars = movie_soup.find_all('div', class_="credit_summary_item")

            directors = ""
            stars = ""
            for directors_or_stars in movie_directors_stars:

                if directors_or_stars.h4.text == "Directors:" :
                    director_list = directors_or_stars.find_all('a')
                    for director in director_list:
                        directors += director.text + ", "
                    directors = directors[:-2]

                elif directors_or_stars.h4.text == "Director:" :
                    directors = directors_or_stars.a.text

                elif directors_or_stars.h4.text == "Stars:":
                    star_list = directors_or_stars.find_all('a')

                    for star in star_list:
                        if star.text != "See full cast & crew":
                            stars += star.text + ", "
                    stars = stars[:-2]

                elif directors_or_stars.h4.text == "Star:" :
                    stars = directors_or_stars.a.text

            details_soup = movie_soup.find('div', class_="subtext")
            details_list = details_soup.text.replace("  ","").replace("\n","").split("|")
            details = ""
            for detail in details_list:
                details += detail + "|"
            details = details[:-1]

            full_details = build_details(movie_title, details, directors, stars )
            print(full_details)
            file_string += full_details + "\n"
    print(file_string)

    file_name = "movies.txt"
    f = io.open(file_name , "w", encoding="utf-8")
    f.write(file_string)
    f.close()


# buildDetails function "build" the last string that will be the final output in movies.txt file
def build_details(movie_title, details, directors, stars ):
    full_details = ""

    if movie_title != "":
        full_details += movie_title +"|"
    if details != "" :
        full_details += details +"|"
    if directors != "":
        full_details += directors +"|"
    if stars != "":
        full_details += stars

    return full_details


root = tk.Tk()
root.title("Imdb web scraper")

canvas = tk.Canvas(root,width=500, height=550)
canvas.grid(columnspan= 3, rowspan= 3 )

logo = Image.open('image.png')
logo = ImageTk.PhotoImage(logo)
logo_lable = tk.Label(image=logo)
logo_lable.image = logo
logo_lable.grid(column=0,row=0)

instruction = tk.Label(root,text="Please enter movie name in the search box", font = ("Raleway",16))
instruction.grid(columnspan= 4, column= 0, row=1 )

entry = tk.Entry(root, width=30, font=("ariel", 14))
entry.grid(rowspan=2,row = 1,columnspan= 2, column = 0)


def search_btn_clicked():
    makeDetails(entry.get())
    browse_text.set("Loading...")

browse_text = tk.StringVar()
browse_btn = tk.Button(root,textvariable = browse_text,command=lambda:search_btn_clicked(),font=("Raleway",12,"bold"), bg="#20bebe", fg="white", height=2, width="15")
browse_text.set("Search")
browse_btn.grid(column=0, row=2, rowspan=3)

canvas = tk.Canvas(root,width=500, height=200)
canvas.grid(columnspan= 2 ,rowspan=1)

root.mainloop()

