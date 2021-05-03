import csv


def read_line_by_line():
    with open('input-data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
        print(f'Processed {line_count} lines.')


def read_in_dict():
    with open('input-data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(row['post_id'])
                # print(row['username'])
                # print(row['timestamp'])
                # print(row['post_like'])
                # print(row['post_share'])
                # print(row['post_view'])
                print(row['post_text'])
                pass          

            line_count += 1
        print(f'Processed {line_count} lines.')


def write_csv_line_by_line(delimiter):
    with open('employee_file1.csv', mode='w+') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=delimiter, quotechar='"', quoting=csv.QUOTE_MINIMAL)

        employee_writer.writerow(['emp_name', 'dept', 'birth_month'])
        employee_writer.writerow(['John Smith', 'Accounting', 'November'])
        employee_writer.writerow(['Erica Meyers', 'IT', 'March'])


def write_csv_from_dict(delimiter):
    with open('employee_file2.csv', mode='w+') as csv_file:
        fieldnames = ['emp_name', 'dept', 'birth_month']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=delimiter)

        writer.writeheader()
        writer.writerow({'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'})
        writer.writerow({'emp_name': 'Erica Meyers', 'dept': 'IT', 'birth_month': 'March'})


def split_string_by_comma_but_ignore_comma_within_double_quotes():
    """
        Split string on commas but ignore commas within double-quotes?
        Reference: https://stackoverflow.com/a/8070008/7639845
    """
    from csv import reader
    infile = ['1,"2,3",4']
    for line in reader(infile):
        print(line)

if __name__ == "__main__":
    # read_in_dict()
    # read_line_by_line()
    # write_csv_line_by_line(delimiter='|')
    # write_csv_from_dict(delimiter=',')
    split_string_by_comma_but_ignore_comma_within_double_quotes()
