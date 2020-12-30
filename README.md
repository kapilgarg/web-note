# web-note
web-note is a browser extension to save the highlighted text (to cloud) and access your saved notes using a browser. It has two components
1. browser extension which tracks the text that you highlight on a web page
2. Web service which saves the text and also returns the rendered html page with saved text. 

Once you highlight a text on a web page, it shows a button at the end of the text. Once you click it, it saves the selected text to a databse.  

<img src="/images/hl1.JPG" width="100%">  

You can read all the saved notes/highlights from the browser  

<img src="/images/hl2.JPG" width="100%">

## Web api Installation (windows)

\>git clone https://github.com/kapilgarg/web-note.git  
\>cd web-note\web_api\src  
\>python -m venv venv  
\>Scripts\activate  
\>pip install -requirements.txt  
\>python -c "from database import init_db; init_db()"  
\>python note_app.py 

## Extension
### Firefox
1. open firefox and go to about:debugging
2. click on **This Firefox** in the left panel
3. click on **Load Temporary Add-on...**
4. navigate to extension\src directory
5. select any file and click Open

### Google Chrome
1. open google chrome and go to chrome://extensions/
2. make sure **Developer mode** is on
3. click on **Load unpacked** button
4. navigate to extension\src and click on select folder

### Edge
1. open google chrome and go to edge//extensions/
2. make sure **Developer mode** is on
3. click on **Load unpacked** button
4. navigate to extension\src and click on select folder


This will run the web service at localhost (127.0.0.1:5000) extension will connect to same.  
Go to any webpage , highlight some text and click on button which appears nect to cursor.  
To see the saved text, go to 127.0.0.1:5000  


 




