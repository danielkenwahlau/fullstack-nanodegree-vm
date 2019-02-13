from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#import database functions from sql alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
#lets the program know which database we want to communicate with
engine = create_engine('sqlite:///restaurantmenu.db')
#binds engine to base class
Base.metadata.bind = engine
#make session which est a conn between code execution and engine we just created
DBSession = sessionmaker(bind = engine)
session = DBSession()


#define webserver handler class
class webserverHandler(BaseHTTPRequestHandler):
    #handles the get request
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello it's Daniel"
                #double input form
                output += "<form method = 'POST' enctype = 'multipart/form-data' action='hello'>"\
                    "<h2>What would you like me to say?></h2><input name ='message' type = 'text' >" \
                    "<input type = 'submit' value = 'Submit'> </form>"
                output += "</body></html>"


                self.wfile.write(output) #sends back to client
                print(output)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body"
                output += ">&#161Hola it's Daniel <a href = '/hello'>Back to Hello</a>" #anchor tag goes back to hello
                output += "<form method = 'POST' enctype = 'multipart/form-data' action='hello'>"\
                    "<h2>What would you like me to say?></h2><input name ='message' type = 'text' >" \
                    "<input type = 'submit' value = 'Submit'> </form>"
                output += "</body></html>"

                self.wfile.write(output) #sends back to client
                print(output)
                return

            #Restaurant get
            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()


                output = ""
                output += "<html><body>"
                output += "Hello you've reached the restaurant page"

                allResults  = session.query(Restaurant).all()
                #Adds name of all entries to output
                for entry in allResults:
                    output += "<h2>"
                    output += str(entry.name)
                    output += "</h2>"

                    #get insert restaurant  id just before edit
                    output += "<a href = '" 
                    output += str(entry.id)
                    output += "/edit'> go to edit page</a>"
                

                #add link that leads to new page such as edit.
                output += "</body></html>"
                self.wfile.write(output) #sends back to client
                print(output)
            
            #needs to have some way of remembering the id that you want to delete
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                #process the id before the edit
                #str split on '/'. this should be self.path
                rest_id = int(self.path.split('/')[1])
                #grab the second to last element
                #use that element to index into the database
                #retrive name by using filter_by

                rest_query = session.query(Restaurant).filter_by(id = rest_id).first()
                print("Rest Id", rest_id, "rest naeme: ", rest_query.name)


                print(self.path)

                output = ""
                output += "<html><body>"
                output += "Hello you've reached the edit page for "
                output += rest_query.name
                output += "</body></html>"
                self.wfile.write(output) #sends back to client
                print(output)


        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    #Overrides the post method in base class
    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += "<form method = 'POST' enctype = 'multipart/form-data' action='hello'>"\
                "<h2>What would you like me to say?></h2><input name ='message' type = 'text' >" \
                "<input type = 'submit' value = 'Submit'> </form>"
            output += "</html></body>"

            self.wfile.write(output) #sends output to server
            print(output)

        except:
            pass


#main entry point function
def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    #keyboard interrupt will shut down the server
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()  

if __name__ == '__main__':
    main()