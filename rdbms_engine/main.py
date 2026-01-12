import sys
from rdbms_engine.networking import TCPServer

def main():
    print("[-] Initializing DB Engine...")
    
    # Initialize the server
    # We aren't passing an 'executor' yet, so it defaults to None (Echo Mode)
    server = TCPServer(host='0.0.0.0', port=9999)

    try:
        # Start the server (this blocks the main thread)
        server.start()
    except KeyboardInterrupt:
        print("\n[!] Shutdown signal received. Stopping server...")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Critical Failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()