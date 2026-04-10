from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class CORSRequestHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for the local HTML file to hit this endpoint
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/transaction':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse the JSON transaction from the tablet
                payload = json.loads(post_data.decode('utf-8'))
                
                print(f"✅ [SERVER] Received Transaction: {payload['amount']} from {payload['student']} (TxID: {payload['id']})")
                
                # Respond success
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "success", "message": "Transaction recorded in SQL DB."}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            except Exception as e:
                print(f"❌ [SERVER] Error parsing transaction: {e}")
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=CORSRequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"==================================================")
    print(f"   JA BIZTOWN AZURE MOCK SERVER (Port {port})     ")
    print(f"==================================================")
    print("Listening for transactions from the POS Tablet...")
    print("Press CTRL+C to stop the server.\n")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
