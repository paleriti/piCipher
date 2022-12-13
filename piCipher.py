"""piChipper, by Yasar Murat, yasarmurat@msn.com

A chipher inspired from Caesar Chipper but instead uses pi constant.
Also python's built-in ord() and chr() functions are used to cover all unicode characters.
"""


def get_pi():
    """Tries to load the file containing pi constant's 1.000.000 digits,
    if fail to load tries to download the file and again if fail to download
    calculates 100.000 digits.
    """

    pi = ""
    result = load_pi_from_file()
    if result != "Load failed.":
        pi = result
    else:
        # Since download (if fail to download, calculate) takes some time (a few sec) ask user to wait
        print("> Translating your messege...")
        result = download_pi()
        if result != "Download failed.":
            pi = result
        else:
            result = calculate_pi()
            pi = str(result)

    # In downloaded file there is a comma after 3 so we remove it
    if pi[1] == ".":
        pi = pi[:1] + pi[2 : len(pi)]

    # There is a trailing whitespace after the last digit so we take only 1M of it
    if len(pi) > 1_000_000:
        pi = pi[:1_000_000]

    # Calculating 100.000 digits takes nearly 10 sec
    # but 1.000.000 digits takes 15 min so we calculate
    # and take the first 100.000 digits of pi
    else:
        pi = pi[:100_000]

    return pi


def load_pi_from_file():
    """Tries to opens a certain file to get the first 1M digits of pi"""

    try:
        with open("pi1000000.txt", "r") as file_obj:
            loaded_pi = file_obj.read()
        return loaded_pi

    except FileNotFoundError:
        return "Load failed."


def download_pi():
    """Only if loading from file fails we try to download and return the first 1M digits of pi

    If download is a success we save the file to use later"""

    try:
        import requests

        downloaded_pi = requests.get("https://www.angio.net/pi/digits/pi1000000.txt")

        try:
            downloaded_pi.raise_for_status()  # Checks whether we could reach the file
            with open("pi1000000.txt", "w") as file_obj:
                file_obj.write(downloaded_pi.text)
            return downloaded_pi.text

        except requests.exceptions.HTTPError:
            return "Download failed."

    except ModuleNotFoundError:
        return "Download failed."


def calculate_pi():
    """
    Python3 program to calculate Pi using python long integers, and the Chudnovsky algorithm

    See: http://www.craig-wood.com/nick/articles/pi-chudnovsky/ for more info

    Nick Craig-Wood <nick@craig-wood.com>"""

    digit = 10**5
    one = 10**digit
    calculated_pi = pi_chudnovsky(one)
    return calculated_pi


def sqrt(n, one):
    """
    Part of calculate_pi() function

    Return the square root of n as a fixed point number with the one passed in.
    It uses a second order Newton-Raphson convgence.
    This doubles the number of significant figures on each iteration."""

    import math

    floating_point_precision = 10**16
    n_float = float((n * floating_point_precision) // one) / floating_point_precision
    x = (int(floating_point_precision * math.sqrt(n_float)) * one) // floating_point_precision
    n_one = n * one
    while True:
        x_old = x
        x = (x + n_one // x) // 2
        if x == x_old:
            break
    return x


def pi_chudnovsky(one=1_000_000):
    """
    Part of calculate_pi() function

    Calculate pi using Chudnovsky's series
    This calculates it in fixed point, using the value for one passed in"""

    k = 1
    a_k = one
    a_sum = one
    b_sum = 0
    C = 640320
    C3_over_24 = C**3 // 24
    while True:
        a_k *= -(6 * k - 5) * (2 * k - 1) * (6 * k - 1)
        a_k //= k * k * k * C3_over_24
        a_sum += a_k
        b_sum += k * a_k
        k += 1
        if a_k == 0:
            break
    total = 13591409 * a_sum + 545140134 * b_sum
    chudnovsky_pi = (426880 * sqrt(10005 * one, one) * one) // total
    return chudnovsky_pi


def get_mode():
    """Asks user whether to use encryption or decryption"""

    while True:
        print("> Do you wish to encrypt or decrypt a message?")
        mode = input().lower()
        if mode in ["encrypt", "e", "decrypt", "d"]:
            return mode
        else:
            print('> Enter either "encrypt" or "e" or "decrypt" or "d".')


def get_message():
    """Asks user to enter their message for encryption or decryption"""

    print("> Enter your message:")
    return input()


def get_key():
    """Asks user to enter the 'Secret Key' for encryption/decryption"""

    key = 0
    while True:
        print("> Enter the key number:")
        try:
            key = int(input())
        except ValueError:
            continue
        return key


def get_translated_message(mode, message, key, pi):
    """Takes mode (encrypt/decrypt), message, secret key and pi's 100K or 1M digits
    and returns the translated message.
    """

    translated = ""
    index = 0

    for symbol in message:
        symbol_unicode = ord(symbol)  # Change letter to number so we can do some math.

        if mode[0] == "e":
            symbol_unicode += int(pi[(key + index) % len(pi)])  # Make sure we dont get indexError
            index += 1

        elif mode[0] == "d":
            symbol_unicode -= int(pi[(key + index) % len(pi)])  # Make sure we dont get indexError
            index += 1

        # Make sure we stay ord() and chr() function's range
        if symbol_unicode > 1114111:
            symbol_unicode -= 1114111
        elif symbol_unicode < 0:
            symbol_unicode += 1114111

        translated += chr(symbol_unicode)

    # Save the translated message to a file before printing it to the screen
    try:
        with open("translated_message.txt", "w") as file_obj:
            file_obj.write(translated)
            print("> Save to file successful.")
    except UnicodeEncodeError:
        print("> Could't write to file since 'charmap' codec can't encode character")

    return translated


def main():
    """Runs the script"""

    mode = get_mode()
    message = get_message()
    key = get_key()
    pi = get_pi()

    translated_message = get_translated_message(mode, message, key, pi)

    print("> Your translated message is:")
    print(translated_message)


# If this script was run (instead of imported), run the script:
if __name__ == "__main__":
    main()
