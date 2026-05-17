# Inventory management program.
# This program manages warehouse shoe inventory by
# reading stock data, tracking quantities,
# searching products by code, calculating item values,
#  and identifying stock that needs restocking.

from tabulate import tabulate

# Create Shoe Class


class Shoe:

    """ A class representing a shoe.
    """

    def __init__(self, country, code, product, cost, quantity):
        '''
        Initialise a shoe object.

        Arguments:
            country (str): Location of the shoe
            code (str): Unique identification number of the shoe
            product(str): Shoe description
            cost (float): The unit cost price of the shoe
            quantity (int): The number of shoes on hand

        '''
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        '''
        This method returns the unit cost of the shoe.

        Returns:
        cost(float): The unit cost price of the shoe.

        '''
        return self.cost

    def get_quantity(self):
        '''
        This method returns the quantity of the shoe
        in stock.

        Returns:
        quantity (int): The quantity on hand of the shoe.

        '''
        return self.quantity

    def __str__(self):
        '''
        Return a string representation of a shoe object.

        '''
        return (
            f"Code:      {self.code}\n"
            f"Product:   {self.product}\n"
            f"Country:   {self.country}\n"
            f"Unit Cost: R{self.cost:.2f}\n"
            f"Quantity:  {self.quantity}\n"
            )


# Create shoe_list to store a list of objects of shoes.

shoe_list = []


def read_shoes_data():

    '''
    This function opens the file inventory.txt
    and reads its contents line by line. It skips
    the first line, which contains the header information,
    then uses the remaining data to create Shoe objects.
    Each object is added to the shoe_list for later use
    in the program.

    '''
    try:
        # Open the file and iterate through each line and
        # Append each line to the shoe_list list.

        with open("inventory.txt", "r", encoding="utf-8-sig") as file:
            # Skip header row
            next(file)

            for line in file:
                # Remove file white space around words
                # Split the each line into its components.
                line_split = line.strip().split(",")

                # Defensive check to ensure correct number of fields
                # and that bad data is not captured.
                if len(line_split) == 5:
                    try:
                        # Assign parts in list to variables.
                        country, code, product, cost, quantity = line_split
                        # Create shoe object
                        shoe_list_append = Shoe(country,
                                                code,
                                                product,
                                                float(cost),
                                                int(quantity)
                                                )
                        shoe_list.append(shoe_list_append)

                    except (ValueError, IndexError):
                        # Skip line with bad data.
                        continue

    except FileNotFoundError:
        # Handle the case where the file 'inventory.txt' does not exist.
        print(
            "The file does not exist. Please check the file "
            "path and try again."
            )


def capture_shoes():
    '''
    This function allows a user to add a new shoe
    into stock.

    '''
    # Request input from the user to create shoe object.
    print(
        "Please enter the following details about the shoe you wish "
        "to add to the inventory listing:\n"
        )
    country = input("Country:\n")

    # Assumed the stock codes will all follow SKU00000 format.
    # Avoid adding the same stock code twice to the list.
    while True:
        new_code = input("Product code:\n").strip().upper()
        # Check if code exists
        exists = False
        for shoe in shoe_list:
            if shoe.code == new_code:
                exists = True
                break

        if exists:
            add_shoe = input(
                "This product already exists. "
                "Do you want to continue adding it? (Yes/No): "
            ).strip().lower()

            if add_shoe == "yes":
                code = new_code
                break

            # exit function completely
            else:
                print("Returning to main menu.")
                return
        else:
            code = new_code
            break

    product = input("Product description:\n")

    # Detect and prevent user from inputting an invalid entry for
    # cost and quantity.
    while True:
        try:
            cost = float(input("Unit cost:\n"))
            break
        except ValueError:
            print("That was not a valid entry. Try again")

    while True:
        try:
            quantity = int(input("Quantity of stock on hand:\n"))
            break
        except ValueError:
            print("That was not a valid entry. Try again")

    # Create shoe object and append to shoe_list.
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)

    # Append to inventory listing to make change permanent.

    with open("inventory.txt", "a", encoding="utf-8-sig") as file:
        file.write(f"{country},{code},{product},{cost},{quantity}\n")

    # Print out confirmation that the new shoe has been added.
    print(f"{product} has been successfully added to the inventory list.\n")


def view_all():
    '''
    Using the tabulate function, display all the shoes in inventory
    in a table format.

    '''
    data_list = []

    for shoe in shoe_list:
        data_list.append([
            shoe.country,
            shoe.code,
            shoe.product,
            f"R{shoe.cost:.2f}",
            shoe.quantity
        ]
            )

    # Create table headers:
    table_headers = [
        "Country",
        "Code",
        "Product",
        "Cost",
        "Quantity"
        ]
    # Creating the table
    table = tabulate(data_list, table_headers, tablefmt="grid")

    # Printing the table
    table_width = len(table.splitlines()[0])
    print("\n" + "-" * table_width)
    print("Nike Inventory listing".center(table_width))
    print(table)
    print("\n")


def re_stock():
    '''
    This function finds the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked and asks the user
    if they want to add this quantity of shoes and then update it.
    The added quantity is then updated on the inventory file for
    this shoe.
    '''
    # Find minimum quantity.
    if shoe_list:
        lowest_quantity_shoe = min(shoe_list, key=lambda shoe: shoe.quantity)
    else:
        print("There are no shoes in stock.")
        return

    # Display shoe that needs to be restocked.
    print_section(
        "Lowest Quantity Shoe",
        lowest_quantity_shoe,
        37)

    # Ask user if they want to restock this shoe.
    while True:
        restock_response = input(
            f"Do you wish to restock {lowest_quantity_shoe.product}?\n"
            "[Enter Yes or No]\n").strip().lower()

        # If yes, request user to input restock quantity
        if restock_response == "yes":
            while True:
                try:
                    add_quantity = int(
                        input("Enter the quantity to be added:\n")
                        )
                    # Prevent user from entering 0 or negative quantity.
                    if add_quantity <= 0:
                        print(
                            "Quantity must be greater than 0. "
                            "Please try again.\n"
                        )
                        continue

                    break
                except ValueError:
                    print("Invalid input. Try again.\n")

            # Update the quantity on shoe_list.
            lowest_quantity_shoe.quantity += add_quantity

            # Update the inventory list to permanently save the change.
            # Txt file, so must rewrite entire file.
            with open("inventory.txt", "w", encoding="utf-8-sig") as file:
                file.write("Country,Code,Product,Cost,Quantity\n")
                for shoe in shoe_list:
                    file.write(
                        f"{shoe.country},{shoe.code},{shoe.product},"
                        f"{shoe.cost},{shoe.quantity}\n"
                        )

            # Print confirmation message.
            print(
                f"{lowest_quantity_shoe.product} successfully restocked.\n"
                f"Updated quantity on hand: {lowest_quantity_shoe.quantity}.\n"
                )
            break

        elif restock_response == "no":
            print(
                f"Product {lowest_quantity_shoe.product} "
                "has not been restocked.\n"
            )
            print("Returning to main menu.\n")
            break

        else:
            print("Invalid input. Please enter Yes or No.\n")


def search_shoe():
    '''
    This function searches for a shoe from the shoe_list
    using the shoe code and returns this object so that it will be printed.

    '''
    # Request user for input
    search_code = input(
        "Enter the shoe code to find the product:\n"
    )
    # Check if the product code appears in the list.
    for shoe in shoe_list:
        if shoe.code == search_code.strip().upper():
            return shoe


def value_per_item():
    '''
    Calculates and displays the total value for each shoe
    in the shoe_list.

    '''
    data_value_list = []

    for shoe in shoe_list:
        stock_value = shoe.get_quantity() * shoe.get_cost()

        data_value_list.append([
            shoe.country,
            shoe.code,
            shoe.product,
            f"R{shoe.cost:.2f}",
            shoe.quantity,
            f"R{stock_value:.2f}"
            ])

    table_headers = [
        "Country",
        "Code",
        "Product",
        "Cost",
        "Quantity",
        "Stock value"
        ]

    table = tabulate(data_value_list, table_headers, tablefmt="grid")
    table_width = len(table.splitlines()[0])
    print("\n" + "-" * table_width)
    print("Nike Inventory valuation report".center(table_width))
    print(table)
    print("\n")


def highest_qty():

    '''
    Determines the product with the highest quantity and
    prints this shoe as being for sale.
    '''
    if not shoe_list:
        print("There are currently no shoes in stock.")
        return

    highest_quantity_shoe = max(shoe_list, key=lambda shoe: shoe.quantity)
    print_section(
        "Highest Quantity Shoe For Sale",
        highest_quantity_shoe,
        37)


def print_section(title, content="", width=50):
    '''
    Prints a formatted section.

    '''
    print("\n" + "-" * width)
    print(title)
    print("-" * width)

    if content:
        print(content)

    print("-" * width + "\n")


def menu_options():
    '''
    Displays menu options.
    '''
    # Creates and returns menu options dictionary.

    return (
        "\n"
        "------------- Main Menu --------------\n"
        "1. View full inventory listing\n"
        "2. Add new stock item\n"
        "3. Restock shoes\n"
        "4. Search for a stock item\n"
        "5. View stock value report\n"
        "6. View highest quantity item for sale\n"
        "7. Exit\n"
        "--------------------------------------\n"
    )


def main_menu():
    '''
    Menu that displays and calls each function.
    '''
    choice = 0

    while True:

        # Call up the menu.
        print(menu_options())

        try:
            choice = int(
                input(
                    "Please enter your selection:\n")
                    )
        except ValueError:
            print("Invalid selection. Please try again.\n")
            continue

        # Executes applicable functions depending on choice.
        if choice == 1:
            view_all()

        elif choice == 2:
            capture_shoes()

        elif choice == 3:
            re_stock()

        elif choice == 4:
            found_shoe = search_shoe()
            if found_shoe is not None:
                print_section(
                    "Shoe Found",
                    found_shoe,
                    37
                )

            else:
                # Print message and return to main
                # menu if shoe not found.
                print("\nShoe code not found.")
                print(
                    "Returning to the main menu.\n"
                    )

        elif choice == 5:
            value_per_item()

        elif choice == 6:
            highest_qty()

        elif choice == 7:
            print(
                "Exiting program. "
                "Thank you for using the Nike Inventory System.\n")
            break  # Exits program.

        else:
            print("Invalid option. Please try again.")


# Load shoe data into shoe_list.
read_shoes_data()

# Print welcome message and call menu.
print("\nWelcome to the Nike Inventory Management System.\n")
main_menu()
