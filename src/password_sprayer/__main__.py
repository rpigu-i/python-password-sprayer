import argparse
from gen_logo import Logo
from password_sprayer import PasswordSprayer


def main():
    logo = Logo()
    logo.generate_logo()
    password_sprayer = PasswordSprayer()


if __name__ == "__main__":
    main()
 
