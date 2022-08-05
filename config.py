import os
import argparse


class Config:
    file_path_a = "../yfts/adder_test.yft.xml"
    file_path_b = "../yfts/adder.yft.xml"
    output_file_name = "output.md"
    output_file_directory = "./results"
    show_similarities = False
    float_precision = 3

    @staticmethod
    def get_output_path() -> str:
        return f"{Config.output_file_directory}/{Config.output_file_name}"

    @staticmethod
    def get_file_names():
        return os.path.basename(Config.file_path_a), os.path.basename(Config.file_path_b)

    @staticmethod
    def apply_args():
        """Set properties accordingly based on command line arguments."""
        args = Config.get_args()

        if args.xml_a is not None:
            Config.file_path_a = args.xml_a

        if args.xml_b is not None:
            Config.file_path_b = args.xml_b

        if args.output is not None:
            Config.output_file_directory = args.output

        if args.similarities:
            Config.show_similarities = True

    @staticmethod
    def get_args():
        """Get command line arguments from the argument parser."""
        parser = argparse.ArgumentParser(prog="Compare CWXML")
        parser.add_argument('-s', '--similarities',
                            help='Show similarities', action='store_true')
        parser.add_argument(
            '--xml_a', help='Path of first xml file to compare to (overrides config)')
        parser.add_argument(
            '--xml_b', help='Path of second xml file to compare to (overrides config)')
        parser.add_argument(
            '--output', help='Output directory path (overrides config)')

        return parser.parse_args()
