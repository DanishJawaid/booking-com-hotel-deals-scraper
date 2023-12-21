from booking.booking import Booking
import time
from prettytable import PrettyTable
import csv
import os

try:
    with Booking(teardown=False) as bot:

        # Land on first page
        bot.land_first_page()

        print('Checking for popups...')

        # Close signin popup
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


        # Take place to go
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
                        print('Sorry, Booking for more than 30 adults is not available')
                break
            except:
                print('Please enter integer ranging from 1 to 30')

        # Take number of children
        while True:
            try:
                while True:
                    number_of_children = int(input('Number of children: '))
                    if number_of_children < 11:
                        break
                    else:
                        print('Sorry, Booking for more than 10 children is not available')
                break
            except:
                print('Please enter integer ranging from 1 to 10')

        # Take ages of children
        children_ages=[]

        for child in range(1,number_of_children+1):
            while True:
                try:
                    while True:
                        child_age = int(input(f'Age of child {child}: '))
                        if child_age < 18:
                            children_ages.append(child_age)
                            break
                        else:
                            print('Sorry, Please enter age between 0 and 17')
                    break
                except:
                    print('Please enter integer ranging from 0 and 17')

        # Take number of rooms. Not usable
        # while True:
        #     try:
        #         while True:
        #             number_of_rooms=int(input('Number of rooms: '))
        #             if number_of_rooms<31:
        #                 break
        #             else:
        #                 print('Sorry, Booking for more than 30 rooms is not available')
        #         break
        #     except:
        #         print('Please enter integer ranging from 1 to 30')

        # Take Number of results
        while True:
            try:
                number_of_results=abs(int(input('Number of results: ')))
                break
            except:
                print('Please enter integer')

        # Take csv file name to generate
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
        bot.set_people(number_of_adults)
        bot.set_children(children_ages)
        bot.search()

        # Close signin popup
        bot.close_popup('class','f4552b6561')

        # Apply filters on results
        time.sleep(4)
        bot.apply_filtration()
        bot.refresh()

        # Set rooms. Not usable
        # time.sleep(4)
        # bot.set_rooms(number_of_rooms)
        # bot.search()
        # time.sleep(4)
        # bot.set_rooms_again()
        # time.sleep(4)

        # Save field names in csv file
        try:
            with open(csv_filename + '.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Number', 'Hotel Names', 'Hotel Ratings', 'Number of Reviews', 'Hotel Prices'])
        except:
            pass


        # Show pretty table from info and save it in csv file
        while True:
            stop,details=bot.get_info(int(number_of_results))

            # Make pretty table gradually from scraped info
            try:
                table = PrettyTable()
                table.field_names = ['Number', 'Hotel Names', 'Hotel Ratings', 'Number of Reviews', 'Hotel Prices']
                table.add_rows(details)
                print(table)

            except:
                pass

            # Save the scraped info into csv file gradually
            try:
                with open(csv_filename + '.csv', 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    for row in details:
                        csv_writer.writerow(row)
            except:
                pass

            # Stops process when required number of results have been scraped
            if stop:
                break

        input('Press Enter to close')
        bot.quit()

except Exception as e:
    print(e)
    input(':')