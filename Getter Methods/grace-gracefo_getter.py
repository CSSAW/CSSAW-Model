import pandas as pd
from cssaw_central.Session import Session

def get_Monthly(session):

  table = "lwe_data"
  startMonth = input("Enter the start month as MM/YYYY:\n")
  endMonth = input("Enter the end month as MM/YYYY:\n")

  # Parsing input to help SELECT from database
  startMonth = startMonth.split("/")
  startMonth[1] = startMonth[1][-2:]
  startMonth.insert(1, "1")
  endMonth = endMonth.split("/")
  endMonth[1] = endMonth[1][-2:]
  endMonth.insert(1, "31")
  startMonth = ("/").join(startMonth)
  endMonth = ("/").join(endMonth)

  if startMonth[0] == '0':
    startMonth = startMonth[1:]
  if endMonth[0] == '0':
    endMonth = endMonth[1:]

  print(startMonth, endMonth)

  sql = open("query.sql", "w")
  query = "SELECT * FROM CENTRAL." + table + \
          ""



  






if __name__ == "__main__":
  credential = open("credentials.txt", "r").readlines()
  print(credential)
  userName = credential[0].replace("\n", "")
  passWord = credential[1].replace("\n", "")
  host = credential[2].replace("\n", "")
  print(userName, passWord, host)
  try:
    session = Session(userName, passWord, host, db = "CENTRAL")
    print("Database connection successful")
  except:
    print("Connection error")

  data = get_Monthly(session)
