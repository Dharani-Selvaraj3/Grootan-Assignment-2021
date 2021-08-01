#!C:\Users\inc1cob\AppData\Local\Programs\Python\Python39\python.exe
print("Content-Type: text/html; charset=utf-8\r\n\r\n")
import cgi, cgitb
# Create instance of FieldStorage

form = cgi.FieldStorage()
import csv, sqlite3
import logging

def _get_col_datatypes(fin):
    dr = csv.DictReader(fin) # comma is default delimiter
    fieldTypes = {}
    for entry in dr:
        feildslLeft = [f for f in dr.fieldnames if f not in fieldTypes.keys()]
        if not feildslLeft: break # We're done
        for field in feildslLeft:
            data = entry[field]

            # Need data to decide
            if len(data) == 0:
                continue

            if data.isdigit():
                fieldTypes[field] = "INTEGER"
            else:
                fieldTypes[field] = "TEXT"
        # TODO: Currently there's no support for DATE in sqllite

    if len(feildslLeft) > 0:
        raise Exception("Failed to find all the columns data types - Maybe some are empty?")

    return fieldTypes


def escapingGenerator(f):
    for line in f:
        yield line.encode("ascii", "xmlcharrefreplace").decode("ascii")


def csvToDb(csvFile, outputToFile = False):
    # TODO: implement output to file

    with open(csvFile,mode='r', encoding="ISO-8859-1") as fin:
        dt = _get_col_datatypes(fin)

        fin.seek(0)

        reader = csv.DictReader(fin)

        # Keep the order of the columns name just as in the CSV
        fields = reader.fieldnames
        cols = []

        # Set field and type
        for f in fields:
            cols.append("%s %s" % (f, dt[f]))

        # Generate create table statement:
        stmt = "CREATE TABLE csv_load (%s)" % ",".join(cols)

        con = sqlite3.connect(":memory:")
        cur = con.cursor()
        cur.execute(stmt)

        fin.seek(0)


        reader = csv.reader(escapingGenerator(fin))

        # Generate insert statement:
        stmt = "INSERT INTO csv_load VALUES(%s);" % ','.join('?' * len(cols))

        cur.executemany(stmt, reader)
        cur.execute("select * from  %s" % "csv_load")
        print(cur.fetchall())
        con.commit()

    return con

if __name__ == "__main__":
    
    
    csvToDb("demo.csv",outputToFile=False)