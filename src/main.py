# My main function
import argparse

from .controller import Controller


if __name__ == "__main__":
    controller = Controller()

    # Adds a commandline parser
    parser = argparse.ArgumentParser()

    # Adss the parameters for overwriting files, paths and number of threads
    parser.add_argument(
        "-uf", "--url_file", help="Path to where the file containing the url's are"
    )
    parser.add_argument(
        "-rf", "--report_file", help="The path to where the report should go"
    )
    parser.add_argument(
        "-d", "--destination", help="Folder where the downloaded files should go"
    )
    parser.add_argument("-t", "--threads", help="The number of threads")

    # Gets the parameters from the commandline and applies them where appropriate
    args = parser.parse_args()
    if args.url_file:
        controller.set_url_file(args.url_file)
    if args.report_file:
        controller.set_report_file(args.report_file)
    if args.destination:
        controller.set_destination(args.destination)
    if args.threads:
        try:
            controller.run(int(args.threads))
        except:
            print("Thread should be an integer")
    else:
        controller.run()
