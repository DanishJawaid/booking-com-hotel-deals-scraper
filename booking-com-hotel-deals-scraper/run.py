from booking.booking import Booking
import time
from prettytable import PrettyTable
import csv
import os

try:
    with Booking(teardown=False) as bot:

        bot.land_first_page()
        print('Checking for popups...')

        # close signin popup
        bot.close_popup('class', 'f4552b6561')

        # Close cookie popup
        bot.close_popup('id', 'onetrust-reject-all-handler')

        # Take currency from user
        while True:
            currency=input('Type your currency: ')
            if bot.change_currency(currency):
                break
            else:
                print('Currency not supported')


        place_to_go = input('Where do you want to go?: ')

        # Take check in check out dates
        while True:
            try:
                while True:
                    check_in_date = input('Check in date (yyyy-mm-dd): ')
                    check_out_date = input('Check out date (yyyy-mm-dd): ')

                    if not bot.check_days_difference(check_in_date,check_out_date):
                        continue
                    if not bot.check_date_past(check_in_date,check_out_date):
                        continue
                    if not bot.check_date_sequence(check_in_date,check_out_date):
                        continue
                    if not bot.check_date_future(check_in_date,check_out_date):
                        continue
                    break
                break
            except Exception as e:
                print(e)

        # Take number of adults
        while True:
            try:
                while True:
                    number_of_adults=int(input('Number of adults: '))
                    if number_of_adults<31:
                        break
                    else:
                        print('Sorry, Booking for more than 30 people is not available')
                break
            except:
                print('Please enter integer ranging from 1 to 30')

        # Take Number of results
        while True:
            try:
                number_of_results=abs(int(input('Number of results: ')))
                break
            except:
                print('Please enter integer')

        while True:
            csv_filename = input("CSV file name to save results: ")

            # Check if the file already exists
            if os.path.exists(csv_filename):
                print(f"Warning: The file '{csv_filename}' already exists. Please choose a different name.")
            else:
                if csv_filename.endswith(".csv"):
                    filename_without_extension = csv_filename[:-4]
                break

        print("Processing...")

        # close signin popup
        bot.close_popup('class','f4552b6561')

        # Close cookie popup
        bot.close_popup('id','onetrust-reject-all-handler')

        # Enter data and apply filters
        bot.select_place_to_go(place_to_go)
        time.sleep(4)
        bot.click_place_to_go()
        bot.select_date(check_in_date=check_in_date,check_out_date=check_out_date)
        bot.setpeople(adults=2)
        bot.search()

        # close signin popup
        bot.close_popup('class','f4552b6561')

        #apply filters on results
        time.sleep(4)
        bot.apply_filtration()
        bot.refresh()

        details=bot.get_info(int(number_of_results))

        # show results in table form
        try:
            table=PrettyTable()
            table.field_names=details[0]
            table.add_rows(details[1:])
            print(table)
        except:
            print('PrettyTable not detected. Proceeding to saving the results in csv')

        # save results in CSV file
        with open(csv_filename+'.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in details:
                csv_writer.writerow(row)


        bot.quit()

except Exception as e:
    print(e)
    input(':')
