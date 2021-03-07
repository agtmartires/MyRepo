# Processes and summarizes sample order data (SampleData.xls)
# and show result to a new excel file, ResultSummary.xlsx (with chart).
# This program need modules xlrd and xlsxwriter
import xlrd, xlsxwriter

year_region_list = []
sum_list = []

def ProcessFile():
    global year_region_list, sum_list
    excel_file = "SampleData.xls"
    wb = xlrd.open_workbook(excel_file)
    sheet = wb.sheet_by_index(0)

    for r in range(1, sheet.nrows):
        y, m, d, h, i, s = xlrd.xldate_as_tuple(sheet.cell_value(r, 0), wb.datemode)
        year_region = "{0}".format(y) + "_" + sheet.cell_value(r, 1)

        # if year_region not yet in list, add
        if (year_region not in year_region_list):
            year_region_list.append(year_region)
            sum_list.append(sheet.cell_value(r, 6))

        # compute for total
        else:
            idx = year_region_list.index(year_region)
            sum_list[idx] += sheet.cell_value(r, 6)

    print("\nSUMMARY:")
    for i in range(len(year_region_list)):
        print("%15s"%year_region_list[i] + " : " + "%10.2f" % sum_list[i])


def CreateChart():
    global year_region_list, sum_list

    workbook = xlsxwriter.Workbook('ResultSummary.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column(1, 0, 15)
    worksheet.write('A1','Year_Region')
    worksheet.write('B1', 'Total')

    worksheet.write_column('A2', year_region_list)
    worksheet.write_column('B2', sum_list)

    # Create a chart object.
    chart = workbook.add_chart({'type': 'column'})

    # Configure the series of the chart
    chart.add_series({
        'categories': ['Sheet1', 1, 0, len(year_region_list), 0],
        'values': ['Sheet1', 1, 1, len(year_region_list), 1],
        'gap': 20,
    })

    # Configure the chart axes
    chart.set_x_axis({'name': 'Year_Region'})
    chart.set_y_axis({'name': 'Total', 'major_gridlines': {'visible': False}})

    # Turn off chart legend. It is on by default in Excel.
    chart.set_legend({'position': 'none'})
    worksheet.insert_chart('D2', chart)
    workbook.close()

    print("\nFile ResultSummary.xlsx created\n")

if __name__ == '__main__':
    ProcessFile()
    CreateChart()

