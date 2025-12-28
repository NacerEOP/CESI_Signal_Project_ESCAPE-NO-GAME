import socket
import pickle
import threading
import State

# Global stop flag
stop_flag = False

def Client():
    """Starts a server that listens for incoming connections, with an option to stop it."""
    global stop_flag
    stop_flag = False
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(1)
    server_socket.settimeout(1)  # Allows periodic checks for stop requests

    print("🟢 Serveur en attente de connexion... (Use stop_server() to abort)")
    State.Status.configure(text = "🟢 Serveur en attente de connexion...")
    while not stop_flag:
        try:
            conn, addr = server_socket.accept()
            print(f"🔗 Connecté à {addr}")
            State.Status.configure(text = f"🔗 Connecté à {addr}")
            data = b""
            while not stop_flag:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet

            numbers = pickle.loads(data)
            print("📩 Trame reçue :", numbers)
            State.Status.configure(text = f"📩 Trame reçue : {numbers}")
            conn.close()
            server_socket.close()
            
            return numbers

        except socket.timeout:
            continue  # Retry accept() if no connection and not stopping

    print("🛑 Serveur arrêté.")
    State.Status.configure(text = f"🛑 Serveur arrêté.")
    server_socket.close()

def Host(number_table,IP):
    """Connects to the server and sends data."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, 5000))

        data = pickle.dumps(number_table)

        client_socket.sendall(data)
        print("📤 Trame envoyée avec succès !")

        client_socket.close()
    except:
        print("⚠️ No client found")
        State.Status.configure(text = "⚠️ Pas de client trouvé")

def stop_server():
    """Stops the running server thread."""
    global stop_flag
    stop_flag = True
    print("🔴 Stopping server...")

