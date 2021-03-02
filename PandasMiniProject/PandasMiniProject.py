import logging as lg
import openpyxl as op
import phonenumbers as pn
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import sys
import os
import re
import email
import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# CONFIG:

lg.basicConfig(filename = "NYL_FieldAgents/report.log", filemode = "w", format = "%(asctime)s [%(levelname)s]: %(message)s", datefmt = "%B %d, %Y %H:%M", level = lg.INFO)

max_year = 2021 # Current year
min_year = 1845 # The year New York Life was founded

req_keys = ["NYL", "Agent"]
# Makes sure files to be processed contain those keywords.

len_diff_thresh = 500

headers_to_change = ["Agent Writing Contract Start Date", "Agent Writing Contract Status"]
# DataFrame columns which contain either of these strings in their title with have their titles replaced with whichever string they contain.

pn_header = "Agent Phone Number"
pn_region = "US"
pn_delimiter = "."

fina_header = "Agent First Name"
lana_header = "Agent Last Name"
agid_header = "Agent Id"

us_states = ("AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "VI", "WA", "WV", "WI", "WY")
state_header = "Agent State"

email_header = "Agent Email Address"
email_format = r"[^@]+@[^@]+\.[^@]+"

groupby_header = "Agent State"

elev_headers = ["Agent First Name", "Agent Last Name", "Agent Writing Contract Start Date", "Date when an agent became A2O"]

data_visuals = ["hist", "bar", "area", "scatter", "graph"]

plot_size = 25

# CONFIG END

lg.info(">SESSION START<")

def get_dir():
    print("Please enter a directory name:")

    dir = input()

    print()

    while True:
        try:
            os.chdir(dir)

        except OSError:
            print("Directory not found. Please try again:")
            dir = input()

        except Exception as ex:
            print(f"Unknown error detected: {ex}. Please try again:")
            dir = input()

        else:
            lg.info(f"Valid directory path submitted.")
            break

def get_file_date(file_name): 
    # Always assumes that the sequence of digits representing year (whether 2- or 4-digits long) is at either end of the entire digit sequence

    file_date = ""
    file_dates = []

    for char in file_name:

        if char.isdigit():
            file_date += char

        elif 4 <= len(file_date) <= 8:
            file_dates.append(file_date)
            file_date = ""

        elif file_name.index(char) != (len(file_name) - 1):
            file_date = ""

        elif len(file_dates) != 0:
            break

        else:
            return

    possible_dates = []

    for fd in file_dates:

        if len(fd) == 4: # **/*/* or */*/** (Assumes 20XX year)

            try:
                possible_dates.append(dt.date(2000 + int(fd[:2]), int(fd[2]), int(fd[3]))) # YY/M/D
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[:2]), int(fd[3]), int(fd[2]))) # YY/D/M
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[2:]), int(fd[0]), int(fd[1]))) # M/D/YY
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[2:]), int(fd[1]), int(fd[0]))) # D/M/YY
            except ValueError:
                pass

        if len(fd) == 5: # **/**/* or **/*/** or */**/** (Assumes 20XX year)

            try:
                possible_dates.append(dt.date(2000 + int(fd[:2]), int(fd[2:4]), int(fd[4]))) # YY/MM/D
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[:2]), int(fd[2]), int(fd[3:]))) # YY/M/DD
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[:2]), int(fd[3:]), int(fd[2]))) # YY/D/MM
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[:2]), int(fd[4]), int(fd[2:4]))) # YY/DD/M
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[:-2]), int(fd[:2]), int(fd[2]))) # MM/D/YY
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[:-2]), int(fd[0]), int(fd[1:3]))) # M/DD/YY
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[:-2]), int(fd[1:3]), int(fd[0]))) # D/MM/YY
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[:-2]), int(fd[2]), int(fd[:2]))) # DD/M/YY
            except ValueError:
                pass

        if len(fd) == 6: # **/**/** (Assumes 20XX year) or ****/*/* or */*/****

            # 2-digit year:

            try:
                possible_dates.append(dt.date(2000 + int(fd[:2]), int(fd[2:4]), int(fd[4:]))) # YY/MM/DD
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[:2]), int(fd[4:]), int(fd[2:4]))) # YY/DD/MM
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[4:]), int(fd[:2]), int(fd[2:4]))) # MM/DD/YY
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(2000 + int(fd[4:]), int(fd[2:4]), int(fd[:2]))) # DD/MM/YY
            except ValueError:
                pass

            # 4-digit year:

            try:
                possible_dates.append(dt.date(int(fd[:4]), int(fd[4]), int(fd[5]))) # YYYY/M/D
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[:4]), int(fd[5]), int(fd[4]))) # YYYY/D/M
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[2:]), int(fd[0]), int(fd[1]))) # M/D/YYYY
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[2:]), int(fd[1]), int(fd[0]))) # D/M/YYYY
            except ValueError:
                pass

        if len(fd) == 7: # ****/**/* or ****/*/** or **/*/**** or */**/****:

            try:
                possible_dates.append(dt.date(int(fd[:4]), int(fd[4:6]), int(fd[6]))) # YYYY/MM/D
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[:4]), int(fd[4]), int(fd[5:]))) # YYYY/M/DD
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[:4]), int(fd[5:]), int(fd[4]))) # YYYY/D/MM
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[:4]), int(fd[6]), int(fd[4:6]))) # YYYY/DD/M
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[3:]), int(fd[:2]), int(fd[2]))) # MM/D/YYYY
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[:3]), int(fd[0]), int(fd[1:3]))) # M/DD/YYYY
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[:3]), int(fd[1:3]), int(fd[0]))) # D/MM/YYYY
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[:3]), int(fd[2]), int(fd[:2]))) # DD/M/YYYY
            except ValueError:
                pass

        if len(fd) == 8: # ****/**/** or **/**/****

            try:
                possible_dates.append(dt.date(int(fd[:4]), int(fd[4:6]), int(fd[6:]))) # YYYY/MM/DD (default format)
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[:4]), int(fd[6:]), int(fd[4:6]))) # YYYY/DD/MM
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[4:]), int(fd[:2]), int(fd[2:4]))) # MM/DD/YYYY
            except ValueError:
                pass

            try:
                possible_dates.append(dt.date(int(fd[4:]), int(fd[2:4]), int(fd[:2]))) # DD/MM/YYYY
            except ValueError:
                pass

    final_date_list = []

    for podt in possible_dates:
        if min_year <= podt.year <= max_year:
            final_date_list.append(podt)

    if len(final_date_list) <= 1:

        try:
            file_date = final_date_list[0]

        except IndexError:
            return

        except Exception as ex:
            print(f"Unknown error detected: {ex}")

        else:
            return file_date

    else:
        print(f"From the digit sequence in [{file_name}] multiple dates can be assumed:\n")

        for d in final_date_list:
            print(f"{final_date_list.index(d) + 1} - {d.strftime('%B %d, %Y')}")

        print()

        date_index = input(f"Please enter a number from 1 to {len(final_date_list)} to select the date you wish to use for [{file_name}]: ")

        while True:
            try:
                date_index = int(date_index)
                file_date = final_date_list[date_index - 1]

            except ValueError:
                date_index = input("Number not detected. Please try again: ")

            except IndexError:
                date_index = input("Submitted number is not within required range. Please try again: ")

            except Exception as ex:
                print(f"Unknown error detected: {ex}")

            else:
                return file_date

def get_valid_file():
    names = []
    dates = []
    lens = []

    file_ext = lambda f : f.split(".")[-1]

    for file in os.listdir(os.getcwd()):
        if any(keyword in file for keyword in req_keys):
            if file_ext(file) == "csv":
                names.append(file)
                dates.append(get_file_date(file))
                lens.append(len(pd.read_csv(file)))
            elif file != "NYL.lst":
                lg.warning(f"Non-csv file [{file}] found in provided directory [{os.getcwd()}].")

    file_df = pd.DataFrame({"Name" : names, "Date" : dates, "# of entries" : lens})
    file_df = file_df.sort_values(by = "Date", ascending = False)
    file_df = file_df.reset_index(drop = True)

    for i in range(len(file_df) - 1):
        try:
            if abs(file_df.iat[i, 2] - file_df.iat[i + 1, 2]) > len_diff_thresh:
                lg.warning(f"Entry amounts in files [{file_df.iat[i, 0]}] and [{file_df.iat[i + 1, 0]}] differ by more than the allowed threshold of {len_diff_thresh}.")
                lg.warning(f"File [{file_df.iat[i, 0]}] not read. Proceeding to next most recent file.")
                lg.info("Alternatively, you may change the threshold in CONFIG of the .py file under len_diff_thresh.")
                file_df.drop(i)

        except IndexError:
            lg.error("Provided directory does not contain any files with valid format.")
            return

        except Exception as ex:
            lg.error(f"Unknown error encountered: {ex}")
            return

    file_index = 9999999

    nyl = open(file = "NYL.lst", mode = "a+")
    nyl.seek(0)
    nyl_list = re.split(" \| |\n", nyl.read())

    for i in range(len(file_df) - 1):

        if file_df.iat[i, 0] in nyl_list:
            processtime = dt.datetime.strptime(nyl_list[nyl_list.index(file_df.iat[i, 0]) + 1], "%m/%d/%Y %H:%M")
            lg.info(f"File [{file_df.iat[i, 0]}] has already been processed on {processtime.strftime('%B %d, %Y')} at {processtime.strftime('%H:%M')}.")

        else:
            file_index = i
            break
    try:
        nyl.write(f"{file_df.iat[file_index, 0]} | {dt.datetime.now().strftime('%m/%d/%Y %H:%M')}\n")

    except IndexError:
        lg.info("Every valid file in the provided directory has been processed already.")
        return

    except Exception as ex:
        lg.error(f"Unknown error encountered: {ex}")
        return
    
    else:
        lg.info(f"File [{file_df.iat[file_index, 0]}] is the most recent valid file in the provided directory and will now be processed.")
     
    finally:
        nyl.close()

    return file_df.iat[file_index, 0]

def process_file(file):
    try:
        file_df = pd.read_csv(file)

    except ValueError:
        lg.error("Provided directory does not contain any files with valid format.")
        return

    except Exception as ex:
        lg.error(f"Unknown error encountered: {ex}")
        return

    else:
        lg.info(f"Processing file [{file}] now...")

    for col in file_df:
        for h in headers_to_change:
            if h in col:
                file_df = file_df.rename(columns = {col : h})

    for num in range(len(file_df[pn_header].tolist())):
        number = file_df[pn_header].values[num].replace(pn_delimiter, "")
        try:
            ph_num = pn.parse(number, pn_region)
        except:
            fina = file_df[fina_header].values[num].replace(" ", "")
            lana = file_df[lana_header].values[num].replace(" ", "")
            agid = file_df[agid_header].values[num]
            lg.warning(f"Agent {fina} {lana} ({agid}) does not have a US-valid phone number.")

    for state in range(len(file_df[state_header].tolist())):
        ag_state = file_df[state_header].values[state]
        if ag_state not in us_states:
            fina = file_df[fina_header].values[num].replace(" ", "")
            lana = file_df[lana_header].values[num].replace(" ", "")
            agid = file_df[agid_header].values[num]
            lg.warning(f"Address of agent {fina} {lana} ({agid}) does not contain a valid US-state.")

    for em in range(len(file_df[email_header].tolist())):
        email = file_df[email_header].values[em]
        domain = email.split("@")[-1]
        fina = file_df[fina_header].values[em].replace(" ", "")
        lana = file_df[lana_header].values[em].replace(" ", "")
        agid = file_df[agid_header].values[em]
        if domain.lower() != "ft.newyorklife.com":
            lg.warning(f"E-mail address of agent {fina} {lana} ({agid}) does not utilize New York Life domain.")
        elif not re.match(email_format, email):
            lg.warning(f"E-mail address of agent {fina} {lana} ({agid}) is missing or invalid.")

    df9 = {}

    for row in file_df.index:
        df9[row] = file_df.iloc[row]

    print()

    #df9 = pd.DataFrame(df9, index = list(col for col in file_df))
    #print(df9)

    print("9:")

    print(file_df)

    file_df = file_df.head(plot_size)

    data_visual_9 = input("Please print the data visualization format you would like to for dataframe 9: (hist/bar/area/scatter/graph) ")

    while data_visual_9 not in data_visuals:
        data_visual_9 = input("Data visualization format not detected. Please try again: ")

    if data_visual_9 == "graph" or data_visual_9 == "scatter":
        xy9 = input("Please enter two header titles separated by a comma, representing x and y, respectfully: ")

        while True:
            try:
                X, Y = xy9.split(",")
            except ValueError:
                xy9 = input("Exactly one comma needs to be present. Please try again: ")
            else:
                X = X.lstrip()
                Y = Y.lstrip()
                break

        while X not in list(col for col in file_df) or Y not in list(col for col in file_df):
            xy9 = input("Header titles not present in the DataFrame, Please try again: ")
            while True:
                try:
                    X, Y = xy9.split(",")
                except ValueError:
                    xy9 = input("Exactly one comma needs to be present. Please try again: ")
                else:
                    X = X.lstrip()
                    Y = Y.lstrip()
                    break
        
        file_df.plot(kind = data_visual_9, x = X, y = Y)

    else:
        file_df.plot(kind = data_visual_9)

    print()

    print("10:")

    df10 = file_df.groupby(by = groupby_header).count()
    print(df10)

    df10 = df10.head(plot_size)

    data_visual_10 = input("Please print the data visualization format you would like to for dataframe 10: (hist/bar/area/scatter/graph) ")

    while data_visual_10 not in data_visuals:
        data_visual_10 = input("Data visualization format not detected. Please try again: ")

    

    if data_visual_10 == "graph" or data_visual_10 == "scatter":
        xy10 = input("Please enter two header titles separated by a comma, representing x and y, respectfully: ")

        while True:
            try:
                X, Y = xy10.split(",")
            except ValueError:
                xy10 = input("Exactly one comma needs to be present. Please try again: ")
            else:
                X = X.lstrip()
                Y = Y.lstrip()
                break

        while X not in list(col for col in df10) or Y not in list(col for col in df10):
            xy10 = input("Header titles not present in the DataFrame, Please try again: ")
            while True:
                try:
                    X, Y = xy10.split(",")
                except ValueError:
                    xy10 = input("Exactly one comma needs to be present. Please try again: ")
                else:
                    X = X.lstrip()
                    Y = Y.lstrip()
                    break
        
        df10.plot(kind = data_visual_10, x = X, y = Y)

    else:
        df10.plot(kind = data_visual_10)

    plt.show()

    print()

    print("11:")

    df11 = {}

    for col in file_df:
        if col in elev_headers:
            df11[col] = file_df[col]

    df11 = pd.DataFrame(df11)
    print(df11)
            
def main():
    get_dir()
    process_file(get_valid_file())

    lg.info(">SESSION OVER<")

    sender_email = "pavliichek@gmail.com"
    receiver_email = "pavliichek@gmail.com"
    password = input("Password: ")
    subject = "Report"
    body = ""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    filename = "report.log"

    with open(filename) as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        try:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        except:
            lg.error("Could not connect to server.")

    server.quit() 

if __name__ == '__main__':
    main()
