import argparse
from gen_logo import Logo
from password_sprayer import PasswordSprayer


def main():
    logo = Logo()
    logo.generate_logo()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "yaml",
        help="a YAML configuration file")
    args = parser.parse_args()
    password_sprayer = PasswordSprayer(args.yaml)


if __name__ == "__main__":
    main()
