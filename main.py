import argparse
import sniffer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="sniffer", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("config", help="Configuration file (YAML)")
    args = parser.parse_args()
    param = vars(args)
    app = sniffer.Sniffer(config_file=param["config"])
    app.run()

