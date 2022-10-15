import websockets
import asyncio
import cv2, base64

port = 5000
print("Started server on port:", port)

pipeline = "devide=/dev/video0 ! video/x-raw, format=BGRx, width=1280, height=960, framerate=25/1 ! videoconvert ! appsink drop=1"

async def transmit(websocket, path):
        print("Client connected!")
        try:
            cap = cv2.VideoCapture(0)
            
                #cv2.imshow("Transmission", frame)
                    
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                 #       break
                    
            while cap.isOpened():
                _, frame = cap.read()
                encoded = cv2.imencode('.jpg', frame)[1]
                data = str(base64.b64encode(encoded))
                data = data[2:len(data)-1]
                await websocket.send(data)
                cv2.imshow("Transmission", frame)
                    
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            cap.release()
        except websockets.connection.ConnectionClosed as e:
            print("Client Disconnected!")
            cap.release()
        #except:
            #print("Something went wrong")
            
start_server = websockets.serve(transmit, port=port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

#cap.release()
