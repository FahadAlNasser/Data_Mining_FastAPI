<h1 align="center"><b>Data Mining FastAPI</b></h1>
<h2 align="center"><b>This is practice only</b></h2>

## Data Mining
Data mining is a data science technique that extracts and analyzes data to discover patterns and information from large datasets

This is a small FastAPI project to practice thical data extraction from:

1- The official API of the Hacker News
2- The Hackers News RSS feed
3- The Steam store appdetails endpoint

Endpoints:
1- /hackernews/top = It fetch the top Hacker News stories
2- /thehackernews/latest = Fetch the latest articles from The Hacker News
3- /steam/{appid} = Retrieve details for a given steam game. 

If you would like to use it, feel free:
1- git clone (link)
2- cd to the folder source 
3- python -m venv venv
4- venv\Scripts\activate = for windows or venv/bin/activate = for MacOS/Linux
5- pip install -r requirements.txt
6- uvicorn app.main:app --reload

### Disclaimer

I am learning, experimenting, and practicing with coding. I am exploring different tools, techniques, and programming languages to enhance my skills. This is code is experimental and intended for educational purposes only.