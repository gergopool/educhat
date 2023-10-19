import argparse
from educhat import app

def parse_arguments():
    parser = argparse.ArgumentParser(description="Educhat Application")
    parser.add_argument('-p', '--port', type=int, default=3000, help="Port to run the application on")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    app.run(host='0.0.0.0', port=args.port)
