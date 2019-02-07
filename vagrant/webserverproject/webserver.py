from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


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