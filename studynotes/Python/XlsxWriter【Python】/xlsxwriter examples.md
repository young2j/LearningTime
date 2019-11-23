<h1 style="text-align:center;text-weight:40;font-size:30;">xlsxwriter examples</h1>
<p style="text-align:center;font-family:Lisu;text-size:20">——杨双杰 2019年9月6日</p>



# worksheet examples

## Example: 添加超链接

This program is an example of writing hyperlinks to a worksheet. See the [`write_url()`](https://xlsxwriter.readthedocs.io/worksheet.html#write_url) method for more details.

![_images/hyperlink.png](https://xlsxwriter.readthedocs.io/_images/hyperlink.png)

```python
###############################################################################
#
# Example of how to use the XlsxWriter module to write hyperlinks
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

# Create a new workbook and add a worksheet
workbook = xlsxwriter.Workbook('hyperlink.xlsx')
worksheet = workbook.add_worksheet('Hyperlinks')

# Format the first column
worksheet.set_column('A:A', 30)

# Add a sample alternative link format.
red_format = workbook.add_format({
    'font_color': 'red',
    'bold':       1,
    'underline':  1,
    'font_size':  12,
})

# Write some hyperlinks
worksheet.write_url('A1', 'http://www.python.org/')  # Implicit format.
worksheet.write_url('A3', 'http://www.python.org/', string='Python Home')
worksheet.write_url('A5', 'http://www.python.org/', tip='Click here')
worksheet.write_url('A7', 'http://www.python.org/', red_format)
worksheet.write_url('A9', 'mailto:jmcnamara@cpan.org', string='Mail me')

# Write a URL that isn't a hyperlink
worksheet.write_string('A11', 'http://www.python.org/')

workbook.close()
```

## Example: 数组公式

This program is an example of writing array formulas with one or more return values. See the [`write_array_formula()`](https://xlsxwriter.readthedocs.io/worksheet.html#write_array_formula) method for more details.

![_images/array_formula.png](https://xlsxwriter.readthedocs.io/_images/array_formula.png)

```python
#######################################################################
#
# Example of how to use Python and the XlsxWriter module to write
# simple array formulas.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

# Create a new workbook and add a worksheet
workbook = xlsxwriter.Workbook('array_formula.xlsx')
worksheet = workbook.add_worksheet()

# Write some test data.
worksheet.write('B1', 500)
worksheet.write('B2', 10)
worksheet.write('B5', 1)
worksheet.write('B6', 2)
worksheet.write('B7', 3)
worksheet.write('C1', 300)
worksheet.write('C2', 15)
worksheet.write('C5', 20234)
worksheet.write('C6', 21003)
worksheet.write('C7', 10000)


# Write an array formula that returns a single value
worksheet.write_formula('A1', '{=SUM(B1:C1*B2:C2)}')

# Same as above but more verbose.
worksheet.write_array_formula('A2:A2', '{=SUM(B1:C1*B2:C2)}')

# Write an array formula that returns a range of values
worksheet.write_array_formula('A5:A7', '{=TREND(C5:C7,B5:B7)}')

workbook.close()
```

## Example: 自动筛选

This program is an example of using autofilters in a worksheet. See [Working with Autofilters](https://xlsxwriter.readthedocs.io/working_with_autofilters.html#working-with-autofilters) for more details.

![_images/autofilter3.png](https://xlsxwriter.readthedocs.io/_images/autofilter3.png)

```python
###############################################################################
#
# An example of how to create autofilters with XlsxWriter.
#
# An autofilter is a way of adding drop down lists to the headers of a 2D
# range of worksheet data. This allows users to filter the data based on
# simple criteria so that some data is shown and some is hidden.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('autofilter.xlsx')

# Add a worksheet for each autofilter example.
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()
worksheet3 = workbook.add_worksheet()
worksheet4 = workbook.add_worksheet()
worksheet5 = workbook.add_worksheet()
worksheet6 = workbook.add_worksheet()

# Add a bold format for the headers.
bold = workbook.add_format({'bold': 1})

# Open a text file with autofilter example data.
textfile = open('autofilter_data.txt')

# Read the headers from the first line of the input file.
headers = textfile.readline().strip("\n").split()


# Read the text file and store the field data.
data = []
for line in textfile:
    # Split the input data based on whitespace.
    row_data = line.strip("\n").split()

    # Convert the number data from the text file.
    for i, item in enumerate(row_data):
        try:
            row_data[i] = float(item)
        except ValueError:
            pass

    data.append(row_data)


# Set up several sheets with the same data.
for worksheet in (workbook.worksheets()):
    # Make the columns wider.
    worksheet.set_column('A:D', 12)
    # Make the header row larger.
    worksheet.set_row(0, 20, bold)
    # Make the headers bold.
    worksheet.write_row('A1', headers)


###############################################################################
#
# Example 1. Autofilter without conditions.
#

# Set the autofilter.
worksheet1.autofilter('A1:D51')

row = 1
for row_data in (data):
    worksheet1.write_row(row, 0, row_data)

    # Move on to the next worksheet row.
    row += 1


###############################################################################
#
#
# Example 2. Autofilter with a filter condition in the first column.
#

# Autofilter range using Row-Column notation.
worksheet2.autofilter(0, 0, 50, 3)

# Add filter criteria. The placeholder "Region" in the filter is
# ignored and can be any string that adds clarity to the expression.
worksheet2.filter_column(0, 'Region == East')

# Hide the rows that don't match the filter criteria.
row = 1
for row_data in (data):
    region = row_data[0]

    # Check for rows that match the filter.
    if region == 'East':
        # Row matches the filter, no further action required.
        pass
    else:
        # We need to hide rows that don't match the filter.
        worksheet2.set_row(row, options={'hidden': True})

    worksheet2.write_row(row, 0, row_data)

    # Move on to the next worksheet row.
    row += 1


###############################################################################
#
#
# Example 3. Autofilter with a dual filter condition in one of the columns.
#

# Set the autofilter.
worksheet3.autofilter('A1:D51')

# Add filter criteria.
worksheet3.filter_column('A', 'x == East or x == South')

# Hide the rows that don't match the filter criteria.
row = 1
for row_data in (data):
    region = row_data[0]

    # Check for rows that match the filter.
    if region == 'East' or region == 'South':
        # Row matches the filter, no further action required.
        pass
    else:
        # We need to hide rows that don't match the filter.
        worksheet3.set_row(row, options={'hidden': True})

    worksheet3.write_row(row, 0, row_data)

    # Move on to the next worksheet row.
    row += 1


###############################################################################
#
#
# Example 4. Autofilter with filter conditions in two columns.
#

# Set the autofilter.
worksheet4.autofilter('A1:D51')

# Add filter criteria.
worksheet4.filter_column('A', 'x == East')
worksheet4.filter_column('C', 'x > 3000 and x < 8000')

# Hide the rows that don't match the filter criteria.
row = 1
for row_data in (data):
    region = row_data[0]
    volume = int(row_data[2])

    # Check for rows that match the filter.
    if region == 'East' and volume > 3000 and volume < 8000:
        # Row matches the filter, no further action required.
        pass
    else:
        # We need to hide rows that don't match the filter.
        worksheet4.set_row(row, options={'hidden': True})

    worksheet4.write_row(row, 0, row_data)

    # Move on to the next worksheet row.
    row += 1


###############################################################################
#
#
# Example 5. Autofilter with filter for blanks.
#
# Create a blank cell in our test data.

# Set the autofilter.
worksheet5.autofilter('A1:D51')

# Add filter criteria.
worksheet5.filter_column('A', 'x == Blanks')

# Simulate a blank cell in the data.
data[5][0] = ''

# Hide the rows that don't match the filter criteria.
row = 1
for row_data in (data):
    region = row_data[0]

    # Check for rows that match the filter.
    if region == '':
        # Row matches the filter, no further action required.
        pass
    else:
        # We need to hide rows that don't match the filter.
        worksheet5.set_row(row, options={'hidden': True})

    worksheet5.write_row(row, 0, row_data)

    # Move on to the next worksheet row.
    row += 1


###############################################################################
#
#
# Example 6. Autofilter with filter for non-blanks.
#

# Set the autofilter.
worksheet6.autofilter('A1:D51')

# Add filter criteria.
worksheet6.filter_column('A', 'x == NonBlanks')

# Hide the rows that don't match the filter criteria.
row = 1
for row_data in (data):
    region = row_data[0]

    # Check for rows that match the filter.
    if region != '':
        # Row matches the filter, no further action required.
        pass
    else:
        # We need to hide rows that don't match the filter.
        worksheet6.set_row(row, options={'hidden': True})

    worksheet6.write_row(row, 0, row_data)

    # Move on to the next worksheet row.
    row += 1


workbook.close()
```

## Example: 数据验证和下拉列表

Example of how to add data validation and drop down lists to an XlsxWriter file. Data validation is a way of limiting user input to certain ranges or to allow a selection from a drop down list.

![_images/data_validate1.png](https://xlsxwriter.readthedocs.io/_images/data_validate1.png)

```python
###############################################################################
#
# Example of how to add data validation and dropdown lists to an
# XlsxWriter file.
#
# Data validation is a feature of Excel which allows you to restrict
# the data that a user enters in a cell and to display help and
# warning messages. It also allows you to restrict input to values in
# a drop down list.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
from datetime import date, time
import xlsxwriter

workbook = xlsxwriter.Workbook('data_validate.xlsx')
worksheet = workbook.add_worksheet()

# Add a format for the header cells.
header_format = workbook.add_format({
    'border': 1,
    'bg_color': '#C6EFCE',
    'bold': True,
    'text_wrap': True,
    'valign': 'vcenter',
    'indent': 1,
})

# Set up layout of the worksheet.
worksheet.set_column('A:A', 68)
worksheet.set_column('B:B', 15)
worksheet.set_column('D:D', 15)
worksheet.set_row(0, 36)

# Write the header cells and some data that will be used in the examples.
heading1 = 'Some examples of data validation in XlsxWriter'
heading2 = 'Enter values in this column'
heading3 = 'Sample Data'

worksheet.write('A1', heading1, header_format)
worksheet.write('B1', heading2, header_format)
worksheet.write('D1', heading3, header_format)

worksheet.write_row('D3', ['Integers', 1, 10])
worksheet.write_row('D4', ['List data', 'open', 'high', 'close'])
worksheet.write_row('D5', ['Formula', '=AND(F5=50,G5=60)', 50, 60])


# Example 1. Limiting input to an integer in a fixed range.
#
txt = 'Enter an integer between 1 and 10'

worksheet.write('A3', txt)
worksheet.data_validation('B3', {'validate': 'integer',
                                 'criteria': 'between',
                                 'minimum': 1,
                                 'maximum': 10})


# Example 2. Limiting input to an integer outside a fixed range.
#
txt = 'Enter an integer that is not between 1 and 10 (using cell references)'


worksheet.write('A5', txt)
worksheet.data_validation('B5', {'validate': 'integer',
                                 'criteria': 'not between',
                                 'minimum': '=E3',
                                 'maximum': '=F3'})


# Example 3. Limiting input to an integer greater than a fixed value.
#
txt = 'Enter an integer greater than 0'

worksheet.write('A7', txt)
worksheet.data_validation('B7', {'validate': 'integer',
                                 'criteria': '>',
                                 'value': 0})


# Example 4. Limiting input to an integer less than a fixed value.
#
txt = 'Enter an integer less than 10'

worksheet.write('A9', txt)
worksheet.data_validation('B9', {'validate': 'integer',
                                 'criteria': '<',
                                 'value': 10})


# Example 5. Limiting input to a decimal in a fixed range.
#
txt = 'Enter a decimal between 0.1 and 0.5'

worksheet.write('A11', txt)
worksheet.data_validation('B11', {'validate': 'decimal',
                                  'criteria': 'between',
                                  'minimum': 0.1,
                                  'maximum': 0.5})


# Example 6. Limiting input to a value in a dropdown list.
#
txt = 'Select a value from a drop down list'

worksheet.write('A13', txt)
worksheet.data_validation('B13', {'validate': 'list',
                                  'source': ['open', 'high', 'close']})


# Example 7. Limiting input to a value in a dropdown list.
#
txt = 'Select a value from a drop down list (using a cell range)'

worksheet.write('A15', txt)
worksheet.data_validation('B15', {'validate': 'list',
                                  'source': '=$E$4:$G$4'})


# Example 8. Limiting input to a date in a fixed range.
#
txt = 'Enter a date between 1/1/2013 and 12/12/2013'

worksheet.write('A17', txt)
worksheet.data_validation('B17', {'validate': 'date',
                                  'criteria': 'between',
                                  'minimum': date(2013, 1, 1),
                                  'maximum': date(2013, 12, 12)})


# Example 9. Limiting input to a time in a fixed range.
#
txt = 'Enter a time between 6:00 and 12:00'

worksheet.write('A19', txt)
worksheet.data_validation('B19', {'validate': 'time',
                                  'criteria': 'between',
                                  'minimum': time(6, 0),
                                  'maximum': time(12, 0)})


# Example 10. Limiting input to a string greater than a fixed length.
#
txt = 'Enter a string longer than 3 characters'

worksheet.write('A21', txt)
worksheet.data_validation('B21', {'validate': 'length',
                                  'criteria': '>',
                                  'value': 3})


# Example 11. Limiting input based on a formula.
#
txt = 'Enter a value if the following is true "=AND(F5=50,G5=60)"'

worksheet.write('A23', txt)
worksheet.data_validation('B23', {'validate': 'custom',
                                  'value': '=AND(F5=50,G5=60)'})


# Example 12. Displaying and modifying data validation messages.
#
txt = 'Displays a message when you select the cell'

worksheet.write('A25', txt)
worksheet.data_validation('B25', {'validate': 'integer',
                                  'criteria': 'between',
                                  'minimum': 1,
                                  'maximum': 100,
                                  'input_title': 'Enter an integer:',
                                  'input_message': 'between 1 and 100'})


# Example 13. Displaying and modifying data validation messages.
#
txt = "Display a custom error message when integer isn't between 1 and 100"

worksheet.write('A27', txt)
worksheet.data_validation('B27', {'validate': 'integer',
                                  'criteria': 'between',
                                  'minimum': 1,
                                  'maximum': 100,
                                  'input_title': 'Enter an integer:',
                                  'input_message': 'between 1 and 100',
                                  'error_title': 'Input value is not valid!',
                                  'error_message':
                                  'It should be an integer between 1 and 100'})


# Example 14. Displaying and modifying data validation messages.
#
txt = "Display a custom info message when integer isn't between 1 and 100"

worksheet.write('A29', txt)
worksheet.data_validation('B29', {'validate': 'integer',
                                  'criteria': 'between',
                                  'minimum': 1,
                                  'maximum': 100,
                                  'input_title': 'Enter an integer:',
                                  'input_message': 'between 1 and 100',
                                  'error_title': 'Input value is not valid!',
                                  'error_message':
                                  'It should be an integer between 1 and 100',
                                  'error_type': 'information'})

workbook.close()
```

## Example: 条件格式

Example of how to add conditional formatting to an XlsxWriter file. Conditional formatting allows you to apply a format to a cell or a range of cells based on certain criteria.

![_images/conditional_format1.png](https://xlsxwriter.readthedocs.io/_images/conditional_format1.png)

```python
###############################################################################
#
# Example of how to add conditional formatting to an XlsxWriter file.
#
# Conditional formatting allows you to apply a format to a cell or a
# range of cells based on certain criteria.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('conditional_format.xlsx')
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()
worksheet3 = workbook.add_worksheet()
worksheet4 = workbook.add_worksheet()
worksheet5 = workbook.add_worksheet()
worksheet6 = workbook.add_worksheet()
worksheet7 = workbook.add_worksheet()
worksheet8 = workbook.add_worksheet()
worksheet9 = workbook.add_worksheet()

# Add a format. Light red fill with dark red text.
format1 = workbook.add_format({'bg_color': '#FFC7CE',
                               'font_color': '#9C0006'})

# Add a format. Green fill with dark green text.
format2 = workbook.add_format({'bg_color': '#C6EFCE',
                               'font_color': '#006100'})

# Some sample data to run the conditional formatting against.
data = [
    [34, 72, 38, 30, 75, 48, 75, 66, 84, 86],
    [6, 24, 1, 84, 54, 62, 60, 3, 26, 59],
    [28, 79, 97, 13, 85, 93, 93, 22, 5, 14],
    [27, 71, 40, 17, 18, 79, 90, 93, 29, 47],
    [88, 25, 33, 23, 67, 1, 59, 79, 47, 36],
    [24, 100, 20, 88, 29, 33, 38, 54, 54, 88],
    [6, 57, 88, 28, 10, 26, 37, 7, 41, 48],
    [52, 78, 1, 96, 26, 45, 47, 33, 96, 36],
    [60, 54, 81, 66, 81, 90, 80, 93, 12, 55],
    [70, 5, 46, 14, 71, 19, 66, 36, 41, 21],
]


###############################################################################
#
# Example 1.
#
caption = ('Cells with values >= 50 are in light red. '
           'Values < 50 are in light green.')

# Write the data.
worksheet1.write('A1', caption)

for row, row_data in enumerate(data):
    worksheet1.write_row(row + 2, 1, row_data)

# Write a conditional format over a range.
worksheet1.conditional_format('B3:K12', {'type': 'cell',
                                         'criteria': '>=',
                                         'value': 50,
                                         'format': format1})

# Write another conditional format over the same range.
worksheet1.conditional_format('B3:K12', {'type': 'cell',
                                         'criteria': '<',
                                         'value': 50,
                                         'format': format2})


###############################################################################
#
# Example 2.
#
caption = ('Values between 30 and 70 are in light red. '
           'Values outside that range are in light green.')

worksheet2.write('A1', caption)

for row, row_data in enumerate(data):
    worksheet2.write_row(row + 2, 1, row_data)

worksheet2.conditional_format('B3:K12', {'type': 'cell',
                                         'criteria': 'between',
                                         'minimum': 30,
                                         'maximum': 70,
                                         'format': format1})

worksheet2.conditional_format('B3:K12', {'type': 'cell',
                                         'criteria': 'not between',
                                         'minimum': 30,
                                         'maximum': 70,
                                         'format': format2})


###############################################################################
#
# Example 3.
#
caption = ('Duplicate values are in light red. '
           'Unique values are in light green.')

worksheet3.write('A1', caption)

for row, row_data in enumerate(data):
    worksheet3.write_row(row + 2, 1, row_data)

worksheet3.conditional_format('B3:K12', {'type': 'duplicate',
                                         'format': format1})

worksheet3.conditional_format('B3:K12', {'type': 'unique',
                                         'format': format2})


###############################################################################
#
# Example 4.
#
caption = ('Above average values are in light red. '
           'Below average values are in light green.')

worksheet4.write('A1', caption)

for row, row_data in enumerate(data):
    worksheet4.write_row(row + 2, 1, row_data)

worksheet4.conditional_format('B3:K12', {'type': 'average',
                                         'criteria': 'above',
                                         'format': format1})

worksheet4.conditional_format('B3:K12', {'type': 'average',
                                         'criteria': 'below',
                                         'format': format2})


###############################################################################
#
# Example 5.
#
caption = ('Top 10 values are in light red. '
           'Bottom 10 values are in light green.')

worksheet5.write('A1', caption)

for row, row_data in enumerate(data):
    worksheet5.write_row(row + 2, 1, row_data)

worksheet5.conditional_format('B3:K12', {'type': 'top',
                                         'value': '10',
                                         'format': format1})

worksheet5.conditional_format('B3:K12', {'type': 'bottom',
                                         'value': '10',
                                         'format': format2})


###############################################################################
#
# Example 6.
#
caption = ('Cells with values >= 50 are in light red. '
           'Values < 50 are in light green. Non-contiguous ranges.')

# Write the data.
worksheet6.write('A1', caption)

for row, row_data in enumerate(data):
    worksheet6.write_row(row + 2, 1, row_data)

# Write a conditional format over a range.
worksheet6.conditional_format('B3:K6', {'type': 'cell',
                                        'criteria': '>=',
                                        'value': 50,
                                        'format': format1,
                                        'multi_range': 'B3:K6 B9:K12'})

# Write another conditional format over the same range.
worksheet6.conditional_format('B3:K6', {'type': 'cell',
                                        'criteria': '<',
                                        'value': 50,
                                        'format': format2,
                                        'multi_range': 'B3:K6 B9:K12'})


###############################################################################
#
# Example 7.
#
caption = 'Examples of color scales with default and user colors.'

data = range(1, 13)

worksheet7.write('A1', caption)

worksheet7.write('B2', "2 Color Scale")
worksheet7.write('D2', "2 Color Scale + user colors")

worksheet7.write('G2', "3 Color Scale")
worksheet7.write('I2', "3 Color Scale + user colors")

for row, row_data in enumerate(data):
    worksheet7.write(row + 2, 1, row_data)
    worksheet7.write(row + 2, 3, row_data)
    worksheet7.write(row + 2, 6, row_data)
    worksheet7.write(row + 2, 8, row_data)

worksheet7.conditional_format('B3:B14', {'type': '2_color_scale'})

worksheet7.conditional_format('D3:D14', {'type': '2_color_scale',
                                         'min_color': "#FF0000",
                                         'max_color': "#00FF00"})

worksheet7.conditional_format('G3:G14', {'type': '3_color_scale'})

worksheet7.conditional_format('I3:I14', {'type': '3_color_scale',
                                         'min_color': "#C5D9F1",
                                         'mid_color': "#8DB4E3",
                                         'max_color': "#538ED5"})


###############################################################################
#
# Example 8.
#
caption = 'Examples of data bars.'

worksheet8.write('A1', caption)

worksheet8.write('B2', "Default data bars")
worksheet8.write('D2', "Bars only")
worksheet8.write('F2', "With user color")
worksheet8.write('H2', "Solid bars")
worksheet8.write('J2', "Right to left")
worksheet8.write('L2', "Excel 2010 style")
worksheet8.write('N2', "Negative same as positive")

data = range(1, 13)
for row, row_data in enumerate(data):
    worksheet8.write(row + 2, 1, row_data)
    worksheet8.write(row + 2, 3, row_data)
    worksheet8.write(row + 2, 5, row_data)
    worksheet8.write(row + 2, 7, row_data)
    worksheet8.write(row + 2, 9, row_data)

data = [-1, -2, -3, -2, -1, 0, 1, 2, 3, 2, 1, 0]
for row, row_data in enumerate(data):
    worksheet8.write(row + 2, 11, row_data)
    worksheet8.write(row + 2, 13, row_data)

worksheet8.conditional_format('B3:B14', {'type': 'data_bar'})

worksheet8.conditional_format('D3:D14', {'type': 'data_bar',
                                         'bar_only': True})

worksheet8.conditional_format('F3:F14', {'type': 'data_bar',
                                         'bar_color': '#63C384'})

worksheet8.conditional_format('H3:H14', {'type': 'data_bar',
                                         'bar_solid': True})

worksheet8.conditional_format('J3:J14', {'type': 'data_bar',
                                         'bar_direction': 'right'})

worksheet8.conditional_format('L3:L14', {'type': 'data_bar',
                                         'data_bar_2010': True})

worksheet8.conditional_format('M3:N14', {'type': 'data_bar',
                                         'bar_negative_color_same': True,
                                         'bar_negative_border_color_same': True})


###############################################################################
#
# Example 9.
#
caption = 'Examples of conditional formats with icon sets.'

data = [
    [1, 2, 3],
    [1, 2, 3],
    [1, 2, 3],
    [1, 2, 3],
    [1, 2, 3, 4],
    [1, 2, 3, 4, 5],
    [1, 2, 3, 4, 5],
]

worksheet9.write('A1', caption)

for row, row_data in enumerate(data):
    worksheet9.write_row(row + 2, 1, row_data)

worksheet9.conditional_format('B3:D3', {'type': 'icon_set',
                                        'icon_style': '3_traffic_lights'})

worksheet9.conditional_format('B4:D4', {'type': 'icon_set',
                                        'icon_style': '3_traffic_lights',
                                        'reverse_icons': True})

worksheet9.conditional_format('B5:D5', {'type': 'icon_set',
                                        'icon_style': '3_traffic_lights',
                                        'icons_only': True})

worksheet9.conditional_format('B6:D6', {'type': 'icon_set',
                                        'icon_style': '3_arrows'})

worksheet9.conditional_format('B7:E8', {'type': 'icon_set',
                                        'icon_style': '4_arrows'})

worksheet9.conditional_format('B8:F8', {'type': 'icon_set',
                                        'icon_style': '5_arrows'})

worksheet9.conditional_format('B9:F9', {'type': 'icon_set',
                                        'icon_style': '5_ratings'})

workbook.close()
```

## Example: 定义变量和范围

Example of how to create defined names (named ranges) with XlsxWriter.

Defined names are used to define descriptive names to represent a value, a single cell or a range of cells in a workbook or worksheet. See [`define_name()`](https://xlsxwriter.readthedocs.io/workbook.html#define_name).

![_images/defined_name.png](https://xlsxwriter.readthedocs.io/_images/defined_name.png)

```python
##############################################################################
#
# Example of how to create defined names with the XlsxWriter Python module.
#
# This method is used to define a user friendly name to represent a value,
# a single cell or a range of cells in a workbook.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter


workbook = xlsxwriter.Workbook('defined_name.xlsx')
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()

# Define some global/workbook names.
workbook.define_name('Exchange_rate', '=0.96')
workbook.define_name('Sales', '=Sheet1!$G$1:$H$10')

# Define a local/worksheet name. Over-rides the "Sales" name above.
workbook.define_name('Sheet2!Sales', '=Sheet2!$G$1:$G$10')

# Write some text in the file and one of the defined names in a formula.
for worksheet in workbook.worksheets():
    worksheet.set_column('A:A', 45)
    worksheet.write('A1', 'This worksheet contains some defined names.')
    worksheet.write('A2', 'See Formulas -> Name Manager above.')
    worksheet.write('A3', 'Example formula in cell B3 ->')

    worksheet.write('B3', '=Exchange_rate')

workbook.close()
```

## Example: 合并单元格

This program is an example of merging cells in a worksheet. See the [`merge_range()`](https://xlsxwriter.readthedocs.io/worksheet.html#merge_range) method for more details.

![_images/merge1.png](https://xlsxwriter.readthedocs.io/_images/merge1.png)

```python
##############################################################################
#
# A simple example of merging cells with the XlsxWriter Python module.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter


# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('merge1.xlsx')
worksheet = workbook.add_worksheet()

# Increase the cell size of the merged cells to highlight the formatting.
worksheet.set_column('B:D', 12)
worksheet.set_row(3, 30)
worksheet.set_row(6, 30)
worksheet.set_row(7, 30)


# Create a format to use in the merged range.
merge_format = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': 'yellow'})


# Merge 3 cells.
worksheet.merge_range('B4:D4', 'Merged Range', merge_format)

# Merge 3 cells over two rows.
worksheet.merge_range('B7:D8', 'Merged Range', merge_format)


workbook.close()
```

## Example: 富文本

This program is an example of writing rich stings with multiple format to a cell in a worksheet. See the [`write_rich_string()`](https://xlsxwriter.readthedocs.io/worksheet.html#write_rich_string) method for more details.

![_images/rich_strings.png](https://xlsxwriter.readthedocs.io/_images/rich_strings.png)

```python
#######################################################################
#
# An example of using Python and XlsxWriter to write some "rich strings",
# i.e., strings with multiple formats.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('rich_strings.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column('A:A', 30)

# Set up some formats to use.
bold = workbook.add_format({'bold': True})
italic = workbook.add_format({'italic': True})
red = workbook.add_format({'color': 'red'})
blue = workbook.add_format({'color': 'blue'})
center = workbook.add_format({'align': 'center'})
superscript = workbook.add_format({'font_script': 1})

# Write some strings with multiple formats.
worksheet.write_rich_string('A1',
                            'This is ',
                            bold, 'bold',
                            ' and this is ',
                            italic, 'italic')

worksheet.write_rich_string('A3',
                            'This is ',
                            red, 'red',
                            ' and this is ',
                            blue, 'blue')

worksheet.write_rich_string('A5',
                            'Some ',
                            bold, 'bold text',
                            ' centered',
                            center)

worksheet.write_rich_string('A7',
                            italic,
                            'j = k',
                            superscript, '(n-1)',
                            center)

workbook.close()
```

## Example: 合并单元格带有富文本

This program is an example of merging cells that contain a rich string.

Using the standard XlsxWriter API we can only write simple types to merged ranges so we first write a blank string to the merged range. We then overwrite the first merged cell with a rich string.

Note that we must also pass the cell format used in the merged cells format at the end

See the [`merge_range()`](https://xlsxwriter.readthedocs.io/worksheet.html#merge_range) and [`write_rich_string()`](https://xlsxwriter.readthedocs.io/worksheet.html#write_rich_string) methods for more details.

![_images/merge_rich.png](https://xlsxwriter.readthedocs.io/_images/merge_rich.png)

```python
##############################################################################
#
# An  example of merging cells which contain a rich string using the
# XlsxWriter Python module.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter


# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('merge_rich_string.xlsx')
worksheet = workbook.add_worksheet()

# Set up some formats to use.
red = workbook.add_format({'color': 'red'})
blue = workbook.add_format({'color': 'blue'})
cell_format = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1})

# We can only write simple types to merged ranges so we write a blank string.
worksheet.merge_range('B2:E5', "", cell_format)

# We then overwrite the first merged cell with a rich string. Note that we
# must also pass the cell format used in the merged cells format at the end.
worksheet.write_rich_string('B2',
                            'This is ',
                            red, 'red',
                            ' and this is ',
                            blue, 'blue',
                            cell_format)

workbook.close()
```

## Example: 插入图像到工作表

This program is an example of inserting images into a worksheet. See the [`insert_image()`](https://xlsxwriter.readthedocs.io/worksheet.html#insert_image) method for more details.

![_images/images.png](https://xlsxwriter.readthedocs.io/_images/images.png)

```python
##############################################################################
#
# An example of inserting images into a worksheet using the XlsxWriter
# Python module.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter


# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('images.xlsx')
worksheet = workbook.add_worksheet()

# Widen the first column to make the text clearer.
worksheet.set_column('A:A', 30)

# Insert an image.
worksheet.write('A2', 'Insert an image in a cell:')
worksheet.insert_image('B2', 'python.png')

# Insert an image offset in the cell.
worksheet.write('A12', 'Insert an image with an offset:')
worksheet.insert_image('B12', 'python.png', {'x_offset': 15, 'y_offset': 10})

# Insert an image with scaling.
worksheet.write('A23', 'Insert a scaled image:')
worksheet.insert_image('B23', 'python.png', {'x_scale': 0.5, 'y_scale': 0.5})

workbook.close()
```

## Example: 从URL或字节流插入图像到工作表

This program is an example of inserting images from a Python [`io.BytesIO`](https://docs.python.org/3/library/io.html#io.BytesIO) byte stream into a worksheet.

The example byte streams are populated from a URL and from a local file.

See the [`insert_image()`](https://xlsxwriter.readthedocs.io/worksheet.html#insert_image) method for more details.

![_images/images_bytesio.png](https://xlsxwriter.readthedocs.io/_images/images_bytesio.png)

```python
##############################################################################
#
# An example of inserting images from a Python BytesIO byte stream into a
# worksheet using the XlsxWriter module.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

# Import the byte stream handler.
from io import BytesIO

# Import urlopen() for either Python 2 or 3.
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


import xlsxwriter

# Create the workbook and add a worksheet.
workbook  = xlsxwriter.Workbook('images_bytesio.xlsx')
worksheet = workbook.add_worksheet()


# Read an image from a remote url.
url = 'https://raw.githubusercontent.com/jmcnamara/XlsxWriter/' + \
      'master/examples/logo.png'

image_data = BytesIO(urlopen(url).read())

# Write the byte stream image to a cell. Note, the filename must be
# specified. In this case it will be read from url string.
worksheet.insert_image('B2', url, {'image_data': image_data})


# Read a local image file into a a byte stream. Note, the insert_image()
# method can do this directly. This is for illustration purposes only.
filename   = 'python.png'

image_file = open(filename, 'rb')
image_data = BytesIO(image_file.read())
image_file.close()


# Write the byte stream image to a cell. The filename must  be specified.
worksheet.insert_image('B8', filename, {'image_data': image_data})


workbook.close()
```

## Example: 工作表左到右

Example of how to use Python and the XlsxWriter module to change the default worksheet and cell text direction from left-to-right to right-to-left as required by some middle eastern versions of Excel.

Note, this a Python2 unicode version. Remove the `u''` to make this work with Python3. See also the [unicode_python3.py](https://xlsxwriter.readthedocs.io/example_http_server3.html#ex-http-server3).

![_images/right_to_left.png](https://xlsxwriter.readthedocs.io/_images/right_to_left.png)

```python
#######################################################################
# _*_ coding: utf-8
#
# Example of how to use Python and the XlsxWriter module to change the default
# worksheet and cell text direction from left-to-right to right-to-left as
# required by some middle eastern versions of Excel.
#
# Note, this a Python2 unicode version. Remove the u'' to make this work with
# Python3. See also the unicode_python3.py example.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('right_to_left.xlsx')

# Add two worksheets.
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()

# Add the cell formats.
format_left_to_right = workbook.add_format({'reading_order': 1})
format_right_to_left = workbook.add_format({'reading_order': 2})

# Make the columns wider for clarity.
worksheet1.set_column('A:A', 25)
worksheet2.set_column('A:A', 25)

# Change the direction for worksheet2.
worksheet2.right_to_left()

# Write some data to show the difference.

# Standard direction:         | A1 | B1 | C1 | ...
worksheet1.write('A1', u'نص عربي / English text')  # Default direction.
worksheet1.write('A2', u'نص عربي / English text', format_left_to_right)
worksheet1.write('A3', u'نص عربي / English text', format_right_to_left)

# Right to left direction:    ... | C1 | B1 | A1 |
worksheet2.write('A1', u'نص عربي / English text')  # Default direction.
worksheet2.write('A2', u'نص عربي / English text', format_left_to_right)
worksheet2.write('A3', u'نص عربي / English text', format_right_to_left)

workbook.close()
```

## Example: Django类

A simple Django View class to write an Excel file using the XlsxWriter module.

```python
##############################################################################
#
# A simple Django view class to write an Excel file using the XlsxWriter
# module.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import io
from django.http import HttpResponse
from django.views.generic import View
import xlsxwriter


def get_simple_table_data():
    # Simulate a more complex table read.
    return [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]]


class MyView(View):

    def get(self, request):

        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' Workbook() constructor option as shown in the docs.
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # Get some data to write to the spreadsheet.
        data = get_simple_table_data()

        # Write some test data.
        for row_num, columns in enumerate(data):
            for col_num, cell_data in enumerate(columns):
                worksheet.write(row_num, col_num, cell_data)

        # Close the workbook before sending the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = 'django_simple.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response
```

## Example: HTTP服务

Example of using Python and XlsxWriter to create an Excel XLSX file in an in memory string suitable for serving via SimpleHTTPRequestHandler or Django or with the Google App Engine.

Even though the final file will be in memory, via the BytesIO object, the module uses temp files during assembly for efficiency. To avoid this on servers that don’t allow temp files, for example the Google APP Engine, set the `in_memory` constructor option to `True`.

For a Python 2 example see [Example: Simple HTTP Server (Python 2)](https://xlsxwriter.readthedocs.io/example_http_server.html#ex-http-server).

```python
##############################################################################
#
# Example of using Python and XlsxWriter to create an Excel XLSX file in an in
# memory string suitable for serving via SimpleHTTPRequestHandler or Django or
# with the Google App Engine.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

# Note: This is a Python 3 example. For Python 2 see http_server_py2.py.

import http.server
import socketserver
import io

import xlsxwriter


class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        # Create an in-memory output file for the new workbook.
        output = io.BytesIO()

        # Even though the final file will be in memory the module uses temp
        # files during assembly for efficiency. To avoid this on servers that
        # don't allow temp files, for example the Google APP Engine, set the
        # 'in_memory' constructor option to True:
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Write some test data.
        worksheet.write(0, 0, 'Hello, world!')

        # Close the workbook before streaming the data.
        workbook.close()

        # Rewind the buffer.
        output.seek(0)

        # Construct a server response.
        self.send_response(200)
        self.send_header('Content-Disposition', 'attachment; filename=test.xlsx')
        self.send_header('Content-type',
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.end_headers()
        self.wfile.write(output.read())
        return


print('Server listening on port 8000...')
httpd = socketserver.TCPServer(('', 8000), Handler)
httpd.serve_forever()
```

## Example: 添加页标题和页脚

This program is an example of adding headers and footers to worksheets. See the [`set_header()`](https://xlsxwriter.readthedocs.io/page_setup.html#set_header) and [`set_footer()`](https://xlsxwriter.readthedocs.io/page_setup.html#set_footer) methods for more details.

![_images/header_image.png](https://xlsxwriter.readthedocs.io/_images/header_image.png)

```python
######################################################################
#
# This program shows several examples of how to set up headers and
# footers with XlsxWriter.
#
# The control characters used in the header/footer strings are:
#
#     Control             Category            Description
#     =======             ========            ===========
#     &L                  Justification       Left
#     &C                                      Center
#     &R                                      Right
#
#     &P                  Information         Page number
#     &N                                      Total number of pages
#     &D                                      Date
#     &T                                      Time
#     &F                                      File name
#     &A                                      Worksheet name
#
#     &fontsize           Font                Font size
#     &"font,style"                           Font name and style
#     &U                                      Single underline
#     &E                                      Double underline
#     &S                                      Strikethrough
#     &X                                      Superscript
#     &Y                                      Subscript
#
#     &[Picture]          Images              Image placeholder
#     &G                                      Same as &[Picture]
#
#     &&                  Miscellaneous       Literal ampersand &
#
# See the main XlsxWriter documentation for more information.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('headers_footers.xlsx')
preview = 'Select Print Preview to see the header and footer'

######################################################################
#
# A simple example to start
#
worksheet1 = workbook.add_worksheet('Simple')
header1 = '&CHere is some centered text.'
footer1 = '&LHere is some left aligned text.'

worksheet1.set_header(header1)
worksheet1.set_footer(footer1)

worksheet1.set_column('A:A', 50)
worksheet1.write('A1', preview)


######################################################################
#
# Insert a header image.
#
worksheet2 = workbook.add_worksheet('Image')
header2 = '&L&G'

# Adjust the page top margin to allow space for the header image.
worksheet2.set_margins(top=1.3)

worksheet2.set_header(header2, {'image_left': 'python-200x80.png'})

worksheet2.set_column('A:A', 50)
worksheet2.write('A1', preview)


######################################################################
#
# This is an example of some of the header/footer variables.
#
worksheet3 = workbook.add_worksheet('Variables')
header3 = '&LPage &P of &N' + '&CFilename: &F' + '&RSheetname: &A'
footer3 = '&LCurrent date: &D' + '&RCurrent time: &T'

worksheet3.set_header(header3)
worksheet3.set_footer(footer3)

worksheet3.set_column('A:A', 50)
worksheet3.write('A1', preview)
worksheet3.write('A21', 'Next sheet')
worksheet3.set_h_pagebreaks([20])

######################################################################
#
# This example shows how to use more than one font
#
worksheet4 = workbook.add_worksheet('Mixed fonts')
header4 = '&C&"Courier New,Bold"Hello &"Arial,Italic"World'
footer4 = '&C&"Symbol"e&"Arial" = mc&X2'

worksheet4.set_header(header4)
worksheet4.set_footer(footer4)

worksheet4.set_column('A:A', 50)
worksheet4.write('A1', preview)

######################################################################
#
# Example of line wrapping
#
worksheet5 = workbook.add_worksheet('Word wrap')
header5 = "&CHeading 1\nHeading 2"

worksheet5.set_header(header5)

worksheet5.set_column('A:A', 50)
worksheet5.write('A1', preview)

######################################################################
#
# Example of inserting a literal ampersand &
#
worksheet6 = workbook.add_worksheet('Ampersand')
header6 = '&CCuriouser && Curiouser - Attorneys at Law'

worksheet6.set_header(header6)

worksheet6.set_column('A:A', 50)
worksheet6.write('A1', preview)

workbook.close()
```

## Example: 冻结和拆分窗格

An example of how to create panes in a worksheet, both “freeze” panes and “split” panes. See the [`freeze_panes()`](https://xlsxwriter.readthedocs.io/worksheet.html#freeze_panes) and [`split_panes()`](https://xlsxwriter.readthedocs.io/worksheet.html#split_panes) methods for more details.

![_images/panes.png](https://xlsxwriter.readthedocs.io/_images/panes.png)

```python
#######################################################################
#
# Example of using Python and the XlsxWriter module to create
# worksheet panes.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('panes.xlsx')

worksheet1 = workbook.add_worksheet('Panes 1')
worksheet2 = workbook.add_worksheet('Panes 2')
worksheet3 = workbook.add_worksheet('Panes 3')
worksheet4 = workbook.add_worksheet('Panes 4')

#######################################################################
#
# Set up some formatting and text to highlight the panes.
#
header_format = workbook.add_format({'bold': True,
                                     'align': 'center',
                                     'valign': 'vcenter',
                                     'fg_color': '#D7E4BC',
                                     'border': 1})

center_format = workbook.add_format({'align': 'center'})


#######################################################################
#
# Example 1. Freeze pane on the top row.
#
worksheet1.freeze_panes(1, 0)

# Other sheet formatting.
worksheet1.set_column('A:I', 16)
worksheet1.set_row(0, 20)
worksheet1.set_selection('C3')


# Some text to demonstrate scrolling.
for col in range(0, 9):
    worksheet1.write(0, col, 'Scroll down', header_format)

for row in range(1, 100):
    for col in range(0, 9):
        worksheet1.write(row, col, row + 1, center_format)


#######################################################################
#
# Example 2. Freeze pane on the left column.
#
worksheet2.freeze_panes(0, 1)

# Other sheet formatting.
worksheet2.set_column('A:A', 16)
worksheet2.set_selection('C3')

# Some text to demonstrate scrolling.
for row in range(0, 50):
    worksheet2.write(row, 0, 'Scroll right', header_format)
    for col in range(1, 26):
        worksheet2.write(row, col, col, center_format)


#######################################################################
#
# Example 3. Freeze pane on the top row and left column.
#
worksheet3.freeze_panes(1, 1)

# Other sheet formatting.
worksheet3.set_column('A:Z', 16)
worksheet3.set_row(0, 20)
worksheet3.set_selection('C3')
worksheet3.write(0, 0, '', header_format)

# Some text to demonstrate scrolling.
for col in range(1, 26):
    worksheet3.write(0, col, 'Scroll down', header_format)

for row in range(1, 50):
    worksheet3.write(row, 0, 'Scroll right', header_format)
    for col in range(1, 26):
        worksheet3.write(row, col, col, center_format)


#######################################################################
#
# Example 4. Split pane on the top row and left column.
#
# The divisions must be specified in terms of row and column dimensions.
# The default row height is 15 and the default column width is 8.43
#
worksheet4.split_panes(15, 8.43)

# Other sheet formatting.
worksheet4.set_selection('C3')

# Some text to demonstrate scrolling.
for col in range(1, 26):
    worksheet4.write(0, col, 'Scroll', center_format)

for row in range(1, 50):
    worksheet4.write(row, 0, 'Scroll', center_format)
    for col in range(1, 26):
        worksheet4.write(row, col, col, center_format)

workbook.close()
```

## Example: 工作表表格

Example of how to add tables to an XlsxWriter worksheet.

Tables in Excel are used to group rows and columns of data into a single structure that can be referenced in a formula or formatted collectively.

See also [Working with Worksheet Tables](https://xlsxwriter.readthedocs.io/working_with_tables.html#tables).

![_images/tables12.png](https://xlsxwriter.readthedocs.io/_images/tables12.png)

```python
###############################################################################
#
# Example of how to add tables to an XlsxWriter worksheet.
#
# Tables in Excel are used to group rows and columns of data into a single
# structure that can be referenced in a formula or formatted collectively.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('tables.xlsx')
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()
worksheet3 = workbook.add_worksheet()
worksheet4 = workbook.add_worksheet()
worksheet5 = workbook.add_worksheet()
worksheet6 = workbook.add_worksheet()
worksheet7 = workbook.add_worksheet()
worksheet8 = workbook.add_worksheet()
worksheet9 = workbook.add_worksheet()
worksheet10 = workbook.add_worksheet()
worksheet11 = workbook.add_worksheet()
worksheet12 = workbook.add_worksheet()

currency_format = workbook.add_format({'num_format': '$#,##0'})

# Some sample data for the table.
data = [
    ['Apples', 10000, 5000, 8000, 6000],
    ['Pears', 2000, 3000, 4000, 5000],
    ['Bananas', 6000, 6000, 6500, 6000],
    ['Oranges', 500, 300, 200, 700],

]


###############################################################################
#
# Example 1.
#
caption = 'Default table with no data.'

# Set the columns widths.
worksheet1.set_column('B:G', 12)

# Write the caption.
worksheet1.write('B1', caption)

# Add a table to the worksheet.
worksheet1.add_table('B3:F7')


###############################################################################
#
# Example 2.
#
caption = 'Default table with data.'

# Set the columns widths.
worksheet2.set_column('B:G', 12)

# Write the caption.
worksheet2.write('B1', caption)

# Add a table to the worksheet.
worksheet2.add_table('B3:F7', {'data': data})


###############################################################################
#
# Example 3.
#
caption = 'Table without default autofilter.'

# Set the columns widths.
worksheet3.set_column('B:G', 12)

# Write the caption.
worksheet3.write('B1', caption)

# Add a table to the worksheet.
worksheet3.add_table('B3:F7', {'autofilter': 0})

# Table data can also be written separately, as an array or individual cells.
worksheet3.write_row('B4', data[0])
worksheet3.write_row('B5', data[1])
worksheet3.write_row('B6', data[2])
worksheet3.write_row('B7', data[3])


###############################################################################
#
# Example 4.
#
caption = 'Table without default header row.'

# Set the columns widths.
worksheet4.set_column('B:G', 12)

# Write the caption.
worksheet4.write('B1', caption)

# Add a table to the worksheet.
worksheet4.add_table('B4:F7', {'header_row': 0})

# Table data can also be written separately, as an array or individual cells.
worksheet4.write_row('B4', data[0])
worksheet4.write_row('B5', data[1])
worksheet4.write_row('B6', data[2])
worksheet4.write_row('B7', data[3])


###############################################################################
#
# Example 5.
#
caption = 'Default table with "First Column" and "Last Column" options.'

# Set the columns widths.
worksheet5.set_column('B:G', 12)

# Write the caption.
worksheet5.write('B1', caption)

# Add a table to the worksheet.
worksheet5.add_table('B3:F7', {'first_column': 1, 'last_column': 1})

# Table data can also be written separately, as an array or individual cells.
worksheet5.write_row('B4', data[0])
worksheet5.write_row('B5', data[1])
worksheet5.write_row('B6', data[2])
worksheet5.write_row('B7', data[3])


###############################################################################
#
# Example 6.
#
caption = 'Table with banded columns but without default banded rows.'

# Set the columns widths.
worksheet6.set_column('B:G', 12)

# Write the caption.
worksheet6.write('B1', caption)

# Add a table to the worksheet.
worksheet6.add_table('B3:F7', {'banded_rows': 0, 'banded_columns': 1})

# Table data can also be written separately, as an array or individual cells.
worksheet6.write_row('B4', data[0])
worksheet6.write_row('B5', data[1])
worksheet6.write_row('B6', data[2])
worksheet6.write_row('B7', data[3])


###############################################################################
#
# Example 7.
#
caption = 'Table with user defined column headers'

# Set the columns widths.
worksheet7.set_column('B:G', 12)

# Write the caption.
worksheet7.write('B1', caption)

# Add a table to the worksheet.
worksheet7.add_table('B3:F7', {'data': data,
                               'columns': [{'header': 'Product'},
                                           {'header': 'Quarter 1'},
                                           {'header': 'Quarter 2'},
                                           {'header': 'Quarter 3'},
                                           {'header': 'Quarter 4'},
                                           ]})


###############################################################################
#
# Example 8.
#
caption = 'Table with user defined column headers'

# Set the columns widths.
worksheet8.set_column('B:G', 12)

# Write the caption.
worksheet8.write('B1', caption)

# Formula to use in the table.
formula = '=SUM(Table8[@[Quarter 1]:[Quarter 4]])'

# Add a table to the worksheet.
worksheet8.add_table('B3:G7', {'data': data,
                               'columns': [{'header': 'Product'},
                                           {'header': 'Quarter 1'},
                                           {'header': 'Quarter 2'},
                                           {'header': 'Quarter 3'},
                                           {'header': 'Quarter 4'},
                                           {'header': 'Year',
                                            'formula': formula},
                                           ]})


###############################################################################
#
# Example 9.
#
caption = 'Table with totals row (but no caption or totals).'

# Set the columns widths.
worksheet9.set_column('B:G', 12)

# Write the caption.
worksheet9.write('B1', caption)

# Formula to use in the table.
formula = '=SUM(Table9[@[Quarter 1]:[Quarter 4]])'

# Add a table to the worksheet.
worksheet9.add_table('B3:G8', {'data': data,
                               'total_row': 1,
                               'columns': [{'header': 'Product'},
                                           {'header': 'Quarter 1'},
                                           {'header': 'Quarter 2'},
                                           {'header': 'Quarter 3'},
                                           {'header': 'Quarter 4'},
                                           {'header': 'Year',
                                            'formula': formula
                                            },
                                           ]})


###############################################################################
#
# Example 10.
#
caption = 'Table with totals row with user captions and functions.'

# Set the columns widths.
worksheet10.set_column('B:G', 12)

# Write the caption.
worksheet10.write('B1', caption)

# Options to use in the table.
options = {'data': data,
           'total_row': 1,
           'columns': [{'header': 'Product', 'total_string': 'Totals'},
                       {'header': 'Quarter 1', 'total_function': 'sum'},
                       {'header': 'Quarter 2', 'total_function': 'sum'},
                       {'header': 'Quarter 3', 'total_function': 'sum'},
                       {'header': 'Quarter 4', 'total_function': 'sum'},
                       {'header': 'Year',
                        'formula': '=SUM(Table10[@[Quarter 1]:[Quarter 4]])',
                        'total_function': 'sum'
                        },
                       ]}

# Add a table to the worksheet.
worksheet10.add_table('B3:G8', options)


###############################################################################
#
# Example 11.
#
caption = 'Table with alternative Excel style.'

# Set the columns widths.
worksheet11.set_column('B:G', 12)

# Write the caption.
worksheet11.write('B1', caption)

# Options to use in the table.
options = {'data': data,
           'style': 'Table Style Light 11',
           'total_row': 1,
           'columns': [{'header': 'Product', 'total_string': 'Totals'},
                       {'header': 'Quarter 1', 'total_function': 'sum'},
                       {'header': 'Quarter 2', 'total_function': 'sum'},
                       {'header': 'Quarter 3', 'total_function': 'sum'},
                       {'header': 'Quarter 4', 'total_function': 'sum'},
                       {'header': 'Year',
                        'formula': '=SUM(Table11[@[Quarter 1]:[Quarter 4]])',
                        'total_function': 'sum'
                        },
                       ]}


# Add a table to the worksheet.
worksheet11.add_table('B3:G8', options)


###############################################################################
#
# Example 12.
#
caption = 'Table with column formats.'

# Set the columns widths.
worksheet12.set_column('B:G', 12)

# Write the caption.
worksheet12.write('B1', caption)

# Options to use in the table.
options = {'data': data,
           'total_row': 1,
           'columns': [{'header': 'Product', 'total_string': 'Totals'},
                       {'header': 'Quarter 1',
                        'total_function': 'sum',
                        'format': currency_format,
                        },
                       {'header': 'Quarter 2',
                        'total_function': 'sum',
                        'format': currency_format,
                        },
                       {'header': 'Quarter 3',
                        'total_function': 'sum',
                        'format': currency_format,
                        },
                       {'header': 'Quarter 4',
                        'total_function': 'sum',
                        'format': currency_format,
                        },
                       {'header': 'Year',
                        'formula': '=SUM(Table12[@[Quarter 1]:[Quarter 4]])',
                        'total_function': 'sum',
                        'format': currency_format,
                        },
                       ]}

# Add a table to the worksheet.
worksheet12.add_table('B3:G8', options)

workbook.close()
```

## Example: 简单的单元格小图标

Example of how to add sparklines to a XlsxWriter worksheet.

Sparklines are small charts that fit in a single cell and are used to show trends in data.

See the [Working with Sparklines](https://xlsxwriter.readthedocs.io/working_with_sparklines.html#sparklines) method for more details.

![_images/sparklines1.png](https://xlsxwriter.readthedocs.io/_images/sparklines1.png)

```python
###############################################################################
#
# Example of how to add sparklines to a Python XlsxWriter file.
#
# Sparklines are small charts that fit in a single cell and are
# used to show trends in data.
#
# See sparklines2.py for examples of more complex sparkline formatting.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('sparklines1.xlsx')
worksheet = workbook.add_worksheet()

# Some sample data to plot.
data = [
    [-2, 2, 3, -1, 0],
    [30, 20, 33, 20, 15],
    [1, -1, -1, 1, -1],
]


# Write the sample data to the worksheet.
worksheet.write_row('A1', data[0])
worksheet.write_row('A2', data[1])
worksheet.write_row('A3', data[2])


# Add a line sparkline (the default) with markers.
worksheet.add_sparkline('F1', {'range': 'Sheet1!A1:E1',
                               'markers': True})


# Add a column sparkline with non-default style.
worksheet.add_sparkline('F2', {'range': 'Sheet1!A2:E2',
                               'type': 'column',
                               'style': 12})


# Add a win/loss sparkline with negative values highlighted.
worksheet.add_sparkline('F3', {'range': 'Sheet1!A3:E3',
                               'type': 'win_loss',
                               'negative_points': True})

workbook.close()
```

## Example: 高级单元格小图标

This example shows the majority of options that can be applied to sparklines.

Sparklines are small charts that fit in a single cell and are used to show trends in data.

See the [Working with Sparklines](https://xlsxwriter.readthedocs.io/working_with_sparklines.html#sparklines) method for more details.

![_images/sparklines2.png](https://xlsxwriter.readthedocs.io/_images/sparklines2.png)

```python
###############################################################################
#
# Example of how to add sparklines to an XlsxWriter file with Python.
#
# Sparklines are small charts that fit in a single cell and are
# used to show trends in data. This example shows the majority of
# options that can be applied to sparklines.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('sparklines2.xlsx')
worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
row = 1

# Set the columns widths to make the output clearer.
worksheet1.set_column('A:A', 14)
worksheet1.set_column('B:B', 50)
worksheet1.set_zoom(150)

# Headings.
worksheet1.write('A1', 'Sparkline', bold)
worksheet1.write('B1', 'Description', bold)


###############################################################################
#
text = 'A default "line" sparkline.'

worksheet1.add_sparkline('A2', {'range': 'Sheet2!A1:J1'})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'A default "column" sparkline.'

worksheet1.add_sparkline('A3', {'range': 'Sheet2!A2:J2',
                                'type': 'column'})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'A default "win/loss" sparkline.'

worksheet1.add_sparkline('A4', {'range': 'Sheet2!A3:J3',
                                'type': 'win_loss'})

worksheet1.write(row, 1, text)
row += 2


###############################################################################
#
text = 'Line with markers.'

worksheet1.add_sparkline('A6', {'range': 'Sheet2!A1:J1',
                                'markers': True})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'Line with high and low points.'

worksheet1.add_sparkline('A7', {'range': 'Sheet2!A1:J1',
                                'high_point': True,
                                'low_point': True})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'Line with first and last point markers.'

worksheet1.add_sparkline('A8', {'range': 'Sheet2!A1:J1',
                                'first_point': True,
                                'last_point': True})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'Line with negative point markers.'

worksheet1.add_sparkline('A9', {'range': 'Sheet2!A1:J1',
                                'negative_points': True})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'Line with axis.'

worksheet1.add_sparkline('A10', {'range': 'Sheet2!A1:J1',
                                 'axis': True})

worksheet1.write(row, 1, text)
row += 2


###############################################################################
#
text = 'Column with default style (1).'

worksheet1.add_sparkline('A12', {'range': 'Sheet2!A2:J2',
                                 'type': 'column'})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'Column with style 2.'

worksheet1.add_sparkline('A13', {'range': 'Sheet2!A2:J2',
                                 'type': 'column',
                                 'style': 2})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'Column with style 3.'

worksheet1.add_sparkline('A14', {'range': 'Sheet2!A2:J2',
                                 'type': 'column',
                                 'style': 3})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'Column with style 4.'

worksheet1.add_sparkline('A15', {'range': 'Sheet2!A2:J2',
                                 'type': 'column',
                                 'style': 4})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'Column with style 5.'

worksheet1.add_sparkline('A16', {'range': 'Sheet2!A2:J2',
                                 'type': 'column',
                                 'style': 5})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'Column with style 6.'

worksheet1.add_sparkline('A17', {'range': 'Sheet2!A2:J2',
                                 'type': 'column',
                                 'style': 6})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'Column with a user defined color.'

worksheet1.add_sparkline('A18', {'range': 'Sheet2!A2:J2',
                                 'type': 'column',
                                 'series_color': '#E965E0'})

worksheet1.write(row, 1, text)
row += 2


###############################################################################
#
text = 'A win/loss sparkline.'

worksheet1.add_sparkline('A20', {'range': 'Sheet2!A3:J3',
                                 'type': 'win_loss'})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'A win/loss sparkline with negative points highlighted.'

worksheet1.add_sparkline('A21', {'range': 'Sheet2!A3:J3',
                                 'type': 'win_loss',
                                 'negative_points': True})

worksheet1.write(row, 1, text)
row += 2


###############################################################################
#
text = 'A left to right column (the default).'

worksheet1.add_sparkline('A23', {'range': 'Sheet2!A4:J4',
                                 'type': 'column',
                                 'style': 20})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'A right to left column.'

worksheet1.add_sparkline('A24', {'range': 'Sheet2!A4:J4',
                                 'type': 'column',
                                 'style': 20,
                                 'reverse': True})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
text = 'Sparkline and text in one cell.'

worksheet1.add_sparkline('A25', {'range': 'Sheet2!A4:J4',
                                 'type': 'column',
                                 'style': 20})

worksheet1.write(row, 0, 'Growth')
worksheet1.write(row, 1, text)
row += 2


###############################################################################
#
text = 'A grouped sparkline. Changes are applied to all three.'

worksheet1.add_sparkline('A27', {'location': ['A27', 'A28', 'A29'],
                                 'range': ['Sheet2!A5:J5',
                                           'Sheet2!A6:J6',
                                           'Sheet2!A7:J7'],
                                 'markers': True})

worksheet1.write(row, 1, text)
row += 1


###############################################################################
#
# Create a second worksheet with data to plot.
#
worksheet2.set_column('A:J', 11)

data = [

    # Simple line data.
    [-2, 2, 3, -1, 0, -2, 3, 2, 1, 0],

    # Simple column data.
    [30, 20, 33, 20, 15, 5, 5, 15, 10, 15],

    # Simple win/loss data.
    [1, 1, -1, -1, 1, -1, 1, 1, 1, -1],

    # Unbalanced histogram.
    [5, 6, 7, 10, 15, 20, 30, 50, 70, 100],

    # Data for the grouped sparkline example.
    [-2, 2, 3, -1, 0, -2, 3, 2, 1, 0],
    [3, -1, 0, -2, 3, 2, 1, 0, 2, 1],
    [0, -2, 3, 2, 1, 0, 1, 2, 3, 1],

]

# Write the sample data to the worksheet.
worksheet2.write_row('A1', data[0])
worksheet2.write_row('A2', data[1])
worksheet2.write_row('A3', data[2])
worksheet2.write_row('A4', data[3])
worksheet2.write_row('A5', data[4])
worksheet2.write_row('A6', data[5])
worksheet2.write_row('A7', data[6])

workbook.close()
```

## Example: 单元格注释

Another example of adding cell comments to a worksheet. This example demonstrates most of the available comment formatting options. For more details see [Working with Cell Comments](https://xlsxwriter.readthedocs.io/working_with_cell_comments.html#cell-comments).

![_images/comments2.png](https://xlsxwriter.readthedocs.io/_images/comments2.png)

```python
###############################################################################
#
# An example of writing cell comments to a worksheet using Python and
# XlsxWriter.
#
# Each of the worksheets demonstrates different features of cell comments.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('comments2.xlsx')

worksheet1 = workbook.add_worksheet()
worksheet2 = workbook.add_worksheet()
worksheet3 = workbook.add_worksheet()
worksheet4 = workbook.add_worksheet()
worksheet5 = workbook.add_worksheet()
worksheet6 = workbook.add_worksheet()
worksheet7 = workbook.add_worksheet()
worksheet8 = workbook.add_worksheet()

text_wrap = workbook.add_format({'text_wrap': 1, 'valign': 'top'})


###############################################################################
#
# Example 1. Demonstrates a simple cell comments without formatting.
#            comments.
#

# Set up some formatting.
worksheet1.set_column('C:C', 25)
worksheet1.set_row(2, 50)
worksheet1.set_row(5, 50)

# Simple ASCII string.
cell_text = 'Hold the mouse over this cell to see the comment.'

comment = 'This is a comment.'

worksheet1.write('C3', cell_text, text_wrap)
worksheet1.write_comment('C3', comment)


###############################################################################
#
# Example 2. Demonstrates visible and hidden comments.
#

# Set up some formatting.
worksheet2.set_column('C:C', 25)
worksheet2.set_row(2, 50)
worksheet2.set_row(5, 50)

cell_text = 'This cell comment is visible.'
comment = 'Hello.'

worksheet2.write('C3', cell_text, text_wrap)
worksheet2.write_comment('C3', comment, {'visible': True})

cell_text = "This cell comment isn't visible (the default)."

worksheet2.write('C6', cell_text, text_wrap)
worksheet2.write_comment('C6', comment)


###############################################################################
#
# Example 3. Demonstrates visible and hidden comments set at the worksheet
#            level.
#

# Set up some formatting.
worksheet3.set_column('C:C', 25)
worksheet3.set_row(2, 50)
worksheet3.set_row(5, 50)
worksheet3.set_row(8, 50)

# Make all comments on the worksheet visible.
worksheet3.show_comments()

cell_text = 'This cell comment is visible, explicitly.'
comment = 'Hello.'

worksheet3.write('C3', cell_text, text_wrap)
worksheet3.write_comment('C3', comment, {'visible': 1})

cell_text = 'This cell comment is also visible because of show_comments().'

worksheet3.write('C6', cell_text, text_wrap)
worksheet3.write_comment('C6', comment)

cell_text = 'However, we can still override it locally.'

worksheet3.write('C9', cell_text, text_wrap)
worksheet3.write_comment('C9', comment, {'visible': False})


###############################################################################
#
# Example 4. Demonstrates changes to the comment box dimensions.
#

# Set up some formatting.
worksheet4.set_column('C:C', 25)
worksheet4.set_row(2, 50)
worksheet4.set_row(5, 50)
worksheet4.set_row(8, 50)
worksheet4.set_row(15, 50)

worksheet4.show_comments()

cell_text = 'This cell comment is default size.'
comment = 'Hello.'

worksheet4.write('C3', cell_text, text_wrap)
worksheet4.write_comment('C3', comment)

cell_text = 'This cell comment is twice as wide.'

worksheet4.write('C6', cell_text, text_wrap)
worksheet4.write_comment('C6', comment, {'x_scale': 2})

cell_text = 'This cell comment is twice as high.'

worksheet4.write('C9', cell_text, text_wrap)
worksheet4.write_comment('C9', comment, {'y_scale': 2})

cell_text = 'This cell comment is scaled in both directions.'

worksheet4.write('C16', cell_text, text_wrap)
worksheet4.write_comment('C16', comment, {'x_scale': 1.2, 'y_scale': 0.8})

cell_text = 'This cell comment has width and height specified in pixels.'

worksheet4.write('C19', cell_text, text_wrap)
worksheet4.write_comment('C19', comment, {'width': 200, 'height': 20})


###############################################################################
#
# Example 5. Demonstrates changes to the cell comment position.
#
worksheet5.set_column('C:C', 25)
worksheet5.set_row(2, 50)
worksheet5.set_row(5, 50)
worksheet5.set_row(8, 50)
worksheet5.set_row(11, 50)

worksheet5.show_comments()

cell_text = 'This cell comment is in the default position.'
comment = 'Hello.'

worksheet5.write('C3', cell_text, text_wrap)
worksheet5.write_comment('C3', comment)

cell_text = 'This cell comment has been moved to another cell.'

worksheet5.write('C6', cell_text, text_wrap)
worksheet5.write_comment('C6', comment, {'start_cell': 'E4'})

cell_text = 'This cell comment has been moved to another cell.'

worksheet5.write('C9', cell_text, text_wrap)
worksheet5.write_comment('C9', comment, {'start_row': 8, 'start_col': 4})

cell_text = 'This cell comment has been shifted within its default cell.'

worksheet5.write('C12', cell_text, text_wrap)
worksheet5.write_comment('C12', comment, {'x_offset': 30, 'y_offset': 12})


###############################################################################
#
# Example 6. Demonstrates changes to the comment background color.
#
worksheet6.set_column('C:C', 25)
worksheet6.set_row(2, 50)
worksheet6.set_row(5, 50)
worksheet6.set_row(8, 50)

worksheet6.show_comments()

cell_text = 'This cell comment has a different color.'
comment = 'Hello.'

worksheet6.write('C3', cell_text, text_wrap)
worksheet6.write_comment('C3', comment, {'color': 'green'})

cell_text = 'This cell comment has the default color.'

worksheet6.write('C6', cell_text, text_wrap)
worksheet6.write_comment('C6', comment)

cell_text = 'This cell comment has a different color.'

worksheet6.write('C9', cell_text, text_wrap)
worksheet6.write_comment('C9', comment, {'color': '#CCFFCC'})


###############################################################################
#
# Example 7. Demonstrates how to set the cell comment author.
#
worksheet7.set_column('C:C', 30)
worksheet7.set_row(2, 50)
worksheet7.set_row(5, 50)
worksheet7.set_row(8, 50)

author = ''
cell = 'C3'

cell_text = ("Move the mouse over this cell and you will see 'Cell commented "
             "by (blank)' in the status bar at the bottom")

comment = 'Hello.'

worksheet7.write(cell, cell_text, text_wrap)
worksheet7.write_comment(cell, comment)

author = 'Python'
cell = 'C6'
cell_text = ("Move the mouse over this cell and you will see 'Cell commented "
             "by Python' in the status bar at the bottom")

worksheet7.write(cell, cell_text, text_wrap)
worksheet7.write_comment(cell, comment, {'author': author})


###############################################################################
#
# Example 8. Demonstrates the need to explicitly set the row height.
#
# Set up some formatting.
worksheet8.set_column('C:C', 25)
worksheet8.set_row(2, 80)

worksheet8.show_comments()

cell_text = ('The height of this row has been adjusted explicitly using '
             'set_row(). The size of the comment box is adjusted '
             'accordingly by XlsxWriter.')

comment = 'Hello.'

worksheet8.write('C3', cell_text, text_wrap)
worksheet8.write_comment('C3', comment)

cell_text = ('The height of this row has been adjusted by Excel due to the '
             'text wrap property being set. Unfortunately this means that '
             'the height of the row is unknown to XlsxWriter at run time '
             "and thus the comment box is stretched as well.\n\n"
             'Use set_row() to specify the row height explicitly to avoid '
             'this problem.')

worksheet8.write('C6', cell_text, text_wrap)
worksheet8.write_comment('C6', comment)

workbook.close()
```

## Example: 插入文本框到工作表

The following is an example of how to insert and format textboxes in a worksheet, see [`insert_textbox()`](https://xlsxwriter.readthedocs.io/worksheet.html#insert_textbox) and [Working with Textboxes](https://xlsxwriter.readthedocs.io/working_with_textboxes.html#working-with-textboxes) for more details.

![_images/textbox01.png](https://xlsxwriter.readthedocs.io/_images/textbox01.png)

```python
#######################################################################
#
# An example of inserting textboxes into an Excel worksheet using
# Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('textbox.xlsx')
worksheet = workbook.add_worksheet()
row = 4
col = 1

# The examples below show different textbox options and formatting. In each
# example the text describes the formatting.


# Example
text = 'A simple textbox with some text'
worksheet.insert_textbox(row, col, text)
row += 10

# Example
text = 'A textbox with changed dimensions'
options = {
    'width': 256,
    'height': 100,
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'A textbox with an offset in the cell'
options = {
    'x_offset': 10,
    'y_offset': 10,
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'A textbox with scaling'
options = {
    'x_scale': 1.5,
    'y_scale': 0.8,
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'A textbox with some long text that wraps around onto several lines'
worksheet.insert_textbox(row, col, text)
row += 10

# Example
text = 'A textbox\nwith some\nnewlines\n\nand paragraphs'
worksheet.insert_textbox(row, col, text)
row += 10

# Example
text = 'A textbox with a solid fill background'
options = {
    'fill': {'color': 'red'},
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'A textbox with a no fill background'
options = {
    'fill': {'none': True},
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'A textbox with a gradient fill background'
options = {
    'gradient': {'colors': ['#DDEBCF',
                            '#9CB86E',
                            '#156B13']},
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'A textbox with a user defined border line'
options = {
    'border': {'color': 'red',
               'width': 3,
               'dash_type': 'round_dot'},
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'A textbox with no border line'
options = {
    'border': {'none': True},
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'Default alignment: top - left'
worksheet.insert_textbox(row, col, text)
row += 10

# Example
text = 'Alignment: top - center'
options = {
    'align': {'horizontal': 'center'},
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'Alignment: middle - center'
options = {
    'align': {'vertical': 'middle',
               'horizontal': 'center'},
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'Font properties: bold'
options = {
    'font': {'bold': True},
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'Font properties: various'
options = {
    'font': {'bold': True},
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'Font properties: various'
options = {
    'font': {'bold': True,
             'italic': True,
             'underline': True,
             'name': 'Arial',
             'color': 'red',
             'size': 12}
}
worksheet.insert_textbox(row, col, text, options)
row += 10

# Example
text = 'Some text in a textbox with formatting'
options = {
    'font': {'color': 'white'},
    'align': {'vertical': 'middle',
              'horizontal': 'center'
              },
    'gradient': {'colors': ['red', 'blue']},
}
worksheet.insert_textbox(row, col, text, options)
row += 10


workbook.close()
```

## Example: 大纲和分组

Examples of how use XlsxWriter to generate Excel outlines and grouping. See also [Working with Outlines and Grouping](https://xlsxwriter.readthedocs.io/working_with_outlines.html#outlines).

![_images/outline1.png](https://xlsxwriter.readthedocs.io/_images/outline1.png)

```python
###############################################################################
#
# Example of how use Python and XlsxWriter to generate Excel outlines and
# grouping.
#
# Excel allows you to group rows or columns so that they can be hidden or
# displayed with a single mouse click. This feature is referred to as outlines.
#
# Outlines can reduce complex data down to a few salient sub-totals or
# summaries.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

# Create a new workbook and add some worksheets
workbook = xlsxwriter.Workbook('outline.xlsx')
worksheet1 = workbook.add_worksheet('Outlined Rows')
worksheet2 = workbook.add_worksheet('Collapsed Rows')
worksheet3 = workbook.add_worksheet('Outline Columns')
worksheet4 = workbook.add_worksheet('Outline levels')

# Add a general format
bold = workbook.add_format({'bold': 1})


###############################################################################
#
# Example 1: A worksheet with outlined rows. It also includes SUBTOTAL()
# functions so that it looks like the type of automatic outlines that are
# generated when you use the Excel Data->SubTotals menu item.
#
# For outlines the important parameters are 'level' and 'hidden'. Rows with
# the same 'level' are grouped together. The group will be collapsed if
# 'hidden' is enabled. The parameters 'height' and 'cell_format' are assigned
# default values if they are None.
#
worksheet1.set_row(1, None, None, {'level': 2})
worksheet1.set_row(2, None, None, {'level': 2})
worksheet1.set_row(3, None, None, {'level': 2})
worksheet1.set_row(4, None, None, {'level': 2})
worksheet1.set_row(5, None, None, {'level': 1})

worksheet1.set_row(6, None, None, {'level': 2})
worksheet1.set_row(7, None, None, {'level': 2})
worksheet1.set_row(8, None, None, {'level': 2})
worksheet1.set_row(9, None, None, {'level': 2})
worksheet1.set_row(10, None, None, {'level': 1})

# Adjust the column width for clarity
worksheet1.set_column('A:A', 20)

# Add the data, labels and formulas
worksheet1.write('A1', 'Region', bold)
worksheet1.write('A2', 'North')
worksheet1.write('A3', 'North')
worksheet1.write('A4', 'North')
worksheet1.write('A5', 'North')
worksheet1.write('A6', 'North Total', bold)

worksheet1.write('B1', 'Sales', bold)
worksheet1.write('B2', 1000)
worksheet1.write('B3', 1200)
worksheet1.write('B4', 900)
worksheet1.write('B5', 1200)
worksheet1.write('B6', '=SUBTOTAL(9,B2:B5)', bold)

worksheet1.write('A7', 'South')
worksheet1.write('A8', 'South')
worksheet1.write('A9', 'South')
worksheet1.write('A10', 'South')
worksheet1.write('A11', 'South Total', bold)

worksheet1.write('B7', 400)
worksheet1.write('B8', 600)
worksheet1.write('B9', 500)
worksheet1.write('B10', 600)
worksheet1.write('B11', '=SUBTOTAL(9,B7:B10)', bold)

worksheet1.write('A12', 'Grand Total', bold)
worksheet1.write('B12', '=SUBTOTAL(9,B2:B10)', bold)


###############################################################################
#
# Example 2: A worksheet with outlined rows. This is the same as the
# previous example except that the rows are collapsed.
# Note: We need to indicate the rows that contains the collapsed symbol '+'
# with the optional parameter, 'collapsed'. The group will be then be
# collapsed if 'hidden' is True.
#
worksheet2.set_row(1, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(2, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(3, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(4, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(5, None, None, {'level': 1, 'hidden': True})

worksheet2.set_row(6, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(7, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(8, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(9, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(10, None, None, {'level': 1, 'hidden': True})
worksheet2.set_row(11, None, None, {'collapsed': True})

# Adjust the column width for clarity
worksheet2.set_column('A:A', 20)

# Add the data, labels and formulas
worksheet2.write('A1', 'Region', bold)
worksheet2.write('A2', 'North')
worksheet2.write('A3', 'North')
worksheet2.write('A4', 'North')
worksheet2.write('A5', 'North')
worksheet2.write('A6', 'North Total', bold)

worksheet2.write('B1', 'Sales', bold)
worksheet2.write('B2', 1000)
worksheet2.write('B3', 1200)
worksheet2.write('B4', 900)
worksheet2.write('B5', 1200)
worksheet2.write('B6', '=SUBTOTAL(9,B2:B5)', bold)

worksheet2.write('A7', 'South')
worksheet2.write('A8', 'South')
worksheet2.write('A9', 'South')
worksheet2.write('A10', 'South')
worksheet2.write('A11', 'South Total', bold)

worksheet2.write('B7', 400)
worksheet2.write('B8', 600)
worksheet2.write('B9', 500)
worksheet2.write('B10', 600)
worksheet2.write('B11', '=SUBTOTAL(9,B7:B10)', bold)

worksheet2.write('A12', 'Grand Total', bold)
worksheet2.write('B12', '=SUBTOTAL(9,B2:B10)', bold)


###############################################################################
#
# Example 3: Create a worksheet with outlined columns.
#
data = [
    ['Month', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Total'],
    ['North', 50, 20, 15, 25, 65, 80, '=SUM(B2:G2)'],
    ['South', 10, 20, 30, 50, 50, 50, '=SUM(B3:G3)'],
    ['East', 45, 75, 50, 15, 75, 100, '=SUM(B4:G4)'],
    ['West', 15, 15, 55, 35, 20, 50, '=SUM(B5:G5)']]

# Add bold format to the first row.
worksheet3.set_row(0, None, bold)

# Set column formatting and the outline level.
worksheet3.set_column('A:A', 10, bold)
worksheet3.set_column('B:G', 5, None, {'level': 1})
worksheet3.set_column('H:H', 10)

# Write the data and a formula
for row, data_row in enumerate(data):
    worksheet3.write_row(row, 0, data_row)

worksheet3.write('H6', '=SUM(H2:H5)', bold)


###############################################################################
#
# Example 4: Show all possible outline levels.
#
levels = [
    'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6',
    'Level 7', 'Level 6', 'Level 5', 'Level 4', 'Level 3', 'Level 2',
    'Level 1']

worksheet4.write_column('A1', levels)

worksheet4.set_row(0, None, None, {'level': 1})
worksheet4.set_row(1, None, None, {'level': 2})
worksheet4.set_row(2, None, None, {'level': 3})
worksheet4.set_row(3, None, None, {'level': 4})
worksheet4.set_row(4, None, None, {'level': 5})
worksheet4.set_row(5, None, None, {'level': 6})
worksheet4.set_row(6, None, None, {'level': 7})
worksheet4.set_row(7, None, None, {'level': 6})
worksheet4.set_row(8, None, None, {'level': 5})
worksheet4.set_row(9, None, None, {'level': 4})
worksheet4.set_row(10, None, None, {'level': 3})
worksheet4.set_row(11, None, None, {'level': 2})
worksheet4.set_row(12, None, None, {'level': 1})

workbook.close()
```

## Example: 折叠大纲和分组

Examples of how use XlsxWriter to generate Excel outlines and grouping. These examples focus mainly on collapsed outlines. See also [Working with Outlines and Grouping](https://xlsxwriter.readthedocs.io/working_with_outlines.html#outlines).

![_images/outline2.png](https://xlsxwriter.readthedocs.io/_images/outline2.png)

```python
###############################################################################
#
# Example of how to use Python and XlsxWriter to generate Excel outlines and
# grouping.
#
# These examples focus mainly on collapsed outlines. See also the
# outlines.py example program for more general examples.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

# Create a new workbook and add some worksheets
workbook = xlsxwriter.Workbook('outline_collapsed.xlsx')
worksheet1 = workbook.add_worksheet('Outlined Rows')
worksheet2 = workbook.add_worksheet('Collapsed Rows 1')
worksheet3 = workbook.add_worksheet('Collapsed Rows 2')
worksheet4 = workbook.add_worksheet('Collapsed Rows 3')
worksheet5 = workbook.add_worksheet('Outline Columns')
worksheet6 = workbook.add_worksheet('Collapsed Columns')

# Add a general format
bold = workbook.add_format({'bold': 1})


# This function will generate the same data and sub-totals on each worksheet.
# Used in the first 4 examples.
#
def create_sub_totals(worksheet):
    # Adjust the column width for clarity.
    worksheet.set_column('A:A', 20)

    # Add the data, labels and formulas.
    worksheet.write('A1', 'Region', bold)
    worksheet.write('A2', 'North')
    worksheet.write('A3', 'North')
    worksheet.write('A4', 'North')
    worksheet.write('A5', 'North')
    worksheet.write('A6', 'North Total', bold)

    worksheet.write('B1', 'Sales', bold)
    worksheet.write('B2', 1000)
    worksheet.write('B3', 1200)
    worksheet.write('B4', 900)
    worksheet.write('B5', 1200)
    worksheet.write('B6', '=SUBTOTAL(9,B2:B5)', bold)

    worksheet.write('A7', 'South')
    worksheet.write('A8', 'South')
    worksheet.write('A9', 'South')
    worksheet.write('A10', 'South')
    worksheet.write('A11', 'South Total', bold)

    worksheet.write('B7', 400)
    worksheet.write('B8', 600)
    worksheet.write('B9', 500)
    worksheet.write('B10', 600)
    worksheet.write('B11', '=SUBTOTAL(9,B7:B10)', bold)

    worksheet.write('A12', 'Grand Total', bold)
    worksheet.write('B12', '=SUBTOTAL(9,B2:B10)', bold)

###############################################################################
#
# Example 1: A worksheet with outlined rows. It also includes SUBTOTAL()
# functions so that it looks like the type of automatic outlines that are
# generated when you use the Excel Data->SubTotals menu item.
#
worksheet1.set_row(1, None, None, {'level': 2})
worksheet1.set_row(2, None, None, {'level': 2})
worksheet1.set_row(3, None, None, {'level': 2})
worksheet1.set_row(4, None, None, {'level': 2})
worksheet1.set_row(5, None, None, {'level': 1})

worksheet1.set_row(6, None, None, {'level': 2})
worksheet1.set_row(7, None, None, {'level': 2})
worksheet1.set_row(8, None, None, {'level': 2})
worksheet1.set_row(9, None, None, {'level': 2})
worksheet1.set_row(10, None, None, {'level': 1})

# Write the sub-total data that is common to the row examples.
create_sub_totals(worksheet1)


###############################################################################
#
# Example 2: Create a worksheet with collapsed outlined rows.
# This is the same as the example 1  except that the all rows are collapsed.
# Note: We need to indicate the rows that contains the collapsed symbol '+'
# with the optional parameter, 'collapsed'.
#
worksheet2.set_row(1, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(2, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(3, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(4, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(5, None, None, {'level': 1, 'hidden': True})

worksheet2.set_row(6, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(7, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(8, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(9, None, None, {'level': 2, 'hidden': True})
worksheet2.set_row(10, None, None, {'level': 1, 'hidden': True})

worksheet2.set_row(11, None, None, {'collapsed': True})

# Write the sub-total data that is common to the row examples.
create_sub_totals(worksheet2)


###############################################################################
#
# Example 3: Create a worksheet with collapsed outlined rows.
# Same as the example 1  except that the two sub-totals are collapsed.
#
worksheet3.set_row(1, None, None, {'level': 2, 'hidden': True})
worksheet3.set_row(2, None, None, {'level': 2, 'hidden': True})
worksheet3.set_row(3, None, None, {'level': 2, 'hidden': True})
worksheet3.set_row(4, None, None, {'level': 2, 'hidden': True})
worksheet3.set_row(5, None, None, {'level': 1, 'collapsed': True})

worksheet3.set_row(6, None, None, {'level': 2, 'hidden': True})
worksheet3.set_row(7, None, None, {'level': 2, 'hidden': True})
worksheet3.set_row(8, None, None, {'level': 2, 'hidden': True})
worksheet3.set_row(9, None, None, {'level': 2, 'hidden': True})
worksheet3.set_row(10, None, None, {'level': 1, 'collapsed': True})

# Write the sub-total data that is common to the row examples.
create_sub_totals(worksheet3)


###############################################################################
#
# Example 4: Create a worksheet with outlined rows.
# Same as the example 1  except that the two sub-totals are collapsed.
#
worksheet4.set_row(1, None, None, {'level': 2, 'hidden': True})
worksheet4.set_row(2, None, None, {'level': 2, 'hidden': True})
worksheet4.set_row(3, None, None, {'level': 2, 'hidden': True})
worksheet4.set_row(4, None, None, {'level': 2, 'hidden': True})
worksheet4.set_row(5, None, None, {'level': 1, 'hidden': True,
                                   'collapsed': True})

worksheet4.set_row(6, None, None, {'level': 2, 'hidden': True})
worksheet4.set_row(7, None, None, {'level': 2, 'hidden': True})
worksheet4.set_row(8, None, None, {'level': 2, 'hidden': True})
worksheet4.set_row(9, None, None, {'level': 2, 'hidden': True})
worksheet4.set_row(10, None, None, {'level': 1, 'hidden': True,
                                    'collapsed': True})

worksheet4.set_row(11, None, None, {'collapsed': True})


# Write the sub-total data that is common to the row examples.
create_sub_totals(worksheet4)


###############################################################################
#
# Example 5: Create a worksheet with outlined columns.
#
data = [
    ['Month', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Total'],
    ['North', 50, 20, 15, 25, 65, 80, '=SUM(B2:G2)'],
    ['South', 10, 20, 30, 50, 50, 50, '=SUM(B3:G3)'],
    ['East', 45, 75, 50, 15, 75, 100, '=SUM(B4:G4)'],
    ['West', 15, 15, 55, 35, 20, 50, '=SUM(B5:G5)']]

# Add bold format to the first row.
worksheet5.set_row(0, None, bold)

# Set column formatting and the outline level.
worksheet5.set_column('A:A', 10, bold)
worksheet5.set_column('B:G', 5, None, {'level': 1})
worksheet5.set_column('H:H', 10)

# Write the data and a formula.
for row, data_row in enumerate(data):
    worksheet5.write_row(row, 0, data_row)

worksheet5.write('H6', '=SUM(H2:H5)', bold)

###############################################################################
#
# Example 6: Create a worksheet with collapsed outlined columns.
# This is the same as the previous example except with collapsed columns.
#

# Reuse the data from the previous example.

# Add bold format to the first row.
worksheet6.set_row(0, None, bold)

# Set column formatting and the outline level.
worksheet6.set_column('A:A', 10, bold)
worksheet6.set_column('B:G', 5, None, {'level': 1, 'hidden': True})
worksheet6.set_column('H:H', 10, None, {'collapsed': True})

# Write the data and a formula.
for row, data_row in enumerate(data):
    worksheet6.write_row(row, 0, data_row)

worksheet6.write('H6', '=SUM(H2:H5)', bold)

workbook.close()
```

## Example: 单元格对角线边框

Example of how to set diagonal borders in a cell.

![_images/diagonal_border.png](https://xlsxwriter.readthedocs.io/_images/diagonal_border.png)

See [`set_diag_border()`](https://xlsxwriter.readthedocs.io/format.html#set_diag_border), [`set_diag_type()`](https://xlsxwriter.readthedocs.io/format.html#set_diag_type) and [`set_diag_border()`](https://xlsxwriter.readthedocs.io/format.html#set_diag_border) for details.

```python
##############################################################################
#
# A simple formatting example that demonstrates how to add diagonal cell
# borders with XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('diag_border.xlsx')
worksheet = workbook.add_worksheet()

format1 = workbook.add_format({'diag_type': 1})
format2 = workbook.add_format({'diag_type': 2})
format3 = workbook.add_format({'diag_type': 3})

format4 = workbook.add_format({
    'diag_type': 3,
    'diag_border': 7,
    'diag_color': 'red',
})

worksheet.write('B3', 'Text', format1)
worksheet.write('B6', 'Text', format2)
worksheet.write('B9', 'Text', format3)
worksheet.write('B12', 'Text', format4)

workbook.close()
```

## Example: 单元格保护

This program is an example cell locking and formula hiding in an Excel worksheet using the [`protect()`](https://xlsxwriter.readthedocs.io/worksheet.html#protect) worksheet method.

![_images/worksheet_protection.png](https://xlsxwriter.readthedocs.io/_images/worksheet_protection.png)

```python
########################################################################
#
# Example of cell locking and formula hiding in an Excel worksheet
# using Python and the XlsxWriter module.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('protection.xlsx')
worksheet = workbook.add_worksheet()

# Create some cell formats with protection properties.
unlocked = workbook.add_format({'locked': 0})
hidden = workbook.add_format({'hidden': 1})

# Format the columns to make the text more visible.
worksheet.set_column('A:A', 40)

# Turn worksheet protection on.
worksheet.protect()

# Write a locked, unlocked and hidden cell.
worksheet.write('A1', 'Cell B1 is locked. It cannot be edited.')
worksheet.write('A2', 'Cell B2 is unlocked. It can be edited.')
worksheet.write('A3', "Cell B3 is hidden. The formula isn't visible.")

worksheet.write_formula('B1', '=1+2')  # Locked by default.
worksheet.write_formula('B2', '=1+2', unlocked)
worksheet.write_formula('B3', '=1+2', hidden)

workbook.close()
```

## Example: 隐藏行和列

This program is an example of how to hide rows and columns in XlsxWriter.

An individual row can be hidden using the [`set_row()`](https://xlsxwriter.readthedocs.io/worksheet.html#set_row) method:

```python
worksheet.set_row(0, None, None, {'hidden': True})
```

However, in order to hide a large number of rows, for example all the rows after row 8, we need to use an Excel optimization to hide rows without setting each one, (of approximately 1 million rows). To do this we use the [`set_default_row()`](https://xlsxwriter.readthedocs.io/worksheet.html#set_default_row) method.

Columns don’t require this optimization and can be hidden using [`set_column()`](https://xlsxwriter.readthedocs.io/worksheet.html#set_column).

![_images/hide_row_col.png](https://xlsxwriter.readthedocs.io/_images/hide_row_col.png)

```python
###############################################################################
#
# Example of how to hide rows and columns in XlsxWriter. In order to
# hide rows without setting each one, (of approximately 1 million rows),
# Excel uses an optimizations to hide all rows that don't have data.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('hide_row_col.xlsx')
worksheet = workbook.add_worksheet()

# Write some data.
worksheet.write('D1', 'Some hidden columns.')
worksheet.write('A8', 'Some hidden rows.')

# Hide all rows without data.
worksheet.set_default_row(hide_unused_rows=True)

# Set the height of empty rows that we do want to display even if it is
# the default height.
for row in range(1, 7):
    worksheet.set_row(row, 15)

# Columns can be hidden explicitly. This doesn't increase the file size..
worksheet.set_column('G:XFD', None, None, {'hidden': True})

workbook.close()
```

## Example: 添加VBA宏

This program is an example of how to add a button connected to a VBA macro to a worksheet.

See [Working with VBA Macros](https://xlsxwriter.readthedocs.io/working_with_macros.html#macros) for more details.

![_images/macros.png](https://xlsxwriter.readthedocs.io/_images/macros.png)

```python
#######################################################################
#
# An example of adding macros to an XlsxWriter file using a VBA project
# file extracted from an existing Excel xlsm file.
#
# The vba_extract.py utility supplied with XlsxWriter can be used to extract
# the vbaProject.bin file.
#
# An embedded macro is connected to a form button on the worksheet.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

# Note the file extension should be .xlsm.
workbook = xlsxwriter.Workbook('macros.xlsm')
worksheet = workbook.add_worksheet()

worksheet.set_column('A:A', 30)

# Add the VBA project binary.
workbook.add_vba_project('./vbaProject.bin')

# Show text for the end user.
worksheet.write('A3', 'Press the button to say hello.')

# Add a button tied to a macro in the VBA project.
worksheet.insert_button('B3', {'macro': 'say_hello',
                               'caption': 'Press Me',
                               'width': 80,
                               'height': 30})

workbook.close()
```

# chart examples

## Example: 简单图形

Example of a simple column chart with 3 data series:

[![_images/chart_simple.png](https://xlsxwriter.readthedocs.io/_images/chart_simple.png)](https://xlsxwriter.readthedocs.io/_images/chart_simple.png)

See the [The Chart Class](https://xlsxwriter.readthedocs.io/chart.html#chart-class) and [Working with Charts](https://xlsxwriter.readthedocs.io/working_with_charts.html#working-with-charts) for more details.

```python
#######################################################################
#
# An example of a simple Excel chart with Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart.xlsx')
worksheet = workbook.add_worksheet()

# Create a new Chart object.
chart = workbook.add_chart({'type': 'column'})

# Write some data to add to plot on the chart.
data = [
    [1, 2, 3, 4, 5],
    [2, 4, 6, 8, 10],
    [3, 6, 9, 12, 15],
]

worksheet.write_column('A1', data[0])
worksheet.write_column('B1', data[1])
worksheet.write_column('C1', data[2])

# Configure the charts. In simplest case we just add some data series.
chart.add_series({'values': '=Sheet1!$A$1:$A$5'})
chart.add_series({'values': '=Sheet1!$B$1:$B$5'})
chart.add_series({'values': '=Sheet1!$C$1:$C$5'})

# Insert the chart into the worksheet.
worksheet.insert_chart('A7', chart)

workbook.close()
```

## Example: 面积图

Example of creating Excel Area charts.

Chart 1 in the following example is a default area chart:

[![_images/chart_area1.png](https://xlsxwriter.readthedocs.io/_images/chart_area1.png)](https://xlsxwriter.readthedocs.io/_images/chart_area1.png)

Chart 2 is a stacked area chart:

[![_images/chart_area2.png](https://xlsxwriter.readthedocs.io/_images/chart_area2.png)](https://xlsxwriter.readthedocs.io/_images/chart_area2.png)

Chart 3 is a percentage stacked area chart:

[![_images/chart_area3.png](https://xlsxwriter.readthedocs.io/_images/chart_area3.png)](https://xlsxwriter.readthedocs.io/_images/chart_area3.png)

```python
#######################################################################
#
# An example of creating Excel Area charts with Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_area.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [40, 40, 50, 30, 25, 50],
    [30, 25, 30, 10, 5, 10],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])

#######################################################################
#
# Create an area chart.
#
chart1 = workbook.add_chart({'type': 'area'})

# Configure the first series.
chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure a second series. Note use of alternative syntax to define ranges.
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})

# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart1.set_style(11)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a stacked area chart sub-type.
#
chart2 = workbook.add_chart({'type': 'area', 'subtype': 'stacked'})

# Configure the first series.
chart2.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart2.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart2.set_title ({'name': 'Stacked Chart'})
chart2.set_x_axis({'name': 'Test number'})
chart2.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart2.set_style(12)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D18', chart2, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a percent stacked area chart sub-type.
#
chart3 = workbook.add_chart({'type': 'area', 'subtype': 'percent_stacked'})

# Configure the first series.
chart3.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart3.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart3.set_title ({'name': 'Percent Stacked Chart'})
chart3.set_x_axis({'name': 'Test number'})
chart3.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart3.set_style(13)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D34', chart3, {'x_offset': 25, 'y_offset': 10})

workbook.close()
```

## Example: 条形图

Example of creating Excel Bar charts.

Chart 1 in the following example is a default bar chart:

[![_images/chart_bar1.png](https://xlsxwriter.readthedocs.io/_images/chart_bar1.png)](https://xlsxwriter.readthedocs.io/_images/chart_bar1.png)

Chart 2 is a stacked bar chart:

[![_images/chart_bar2.png](https://xlsxwriter.readthedocs.io/_images/chart_bar2.png)](https://xlsxwriter.readthedocs.io/_images/chart_bar2.png)

Chart 3 is a percentage stacked bar chart:

[![_images/chart_bar3.png](https://xlsxwriter.readthedocs.io/_images/chart_bar3.png)](https://xlsxwriter.readthedocs.io/_images/chart_bar3.png)

```python
#######################################################################
#
# An example of creating Excel Bar charts with Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_bar.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])

#######################################################################
#
# Create a new bar chart.
#
chart1 = workbook.add_chart({'type': 'bar'})

# Configure the first series.
chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure a second series. Note use of alternative syntax to define ranges.
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})

# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart1.set_style(11)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a stacked chart sub-type.
#
chart2 = workbook.add_chart({'type': 'bar', 'subtype': 'stacked'})

# Configure the first series.
chart2.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart2.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart2.set_title ({'name': 'Stacked Chart'})
chart2.set_x_axis({'name': 'Test number'})
chart2.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart2.set_style(12)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D18', chart2, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a percentage stacked chart sub-type.
#
chart3 = workbook.add_chart({'type': 'bar', 'subtype': 'percent_stacked'})

# Configure the first series.
chart3.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart3.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart3.set_title ({'name': 'Percent Stacked Chart'})
chart3.set_x_axis({'name': 'Test number'})
chart3.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart3.set_style(13)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D34', chart3, {'x_offset': 25, 'y_offset': 10})

workbook.close()
```

## Example: Column Chart

Example of creating Excel Column charts.

Chart 1 in the following example is a default column chart:

[![_images/chart_column1.png](https://xlsxwriter.readthedocs.io/_images/chart_column1.png)](https://xlsxwriter.readthedocs.io/_images/chart_column1.png)

Chart 2 is a stacked column chart:

[![_images/chart_column2.png](https://xlsxwriter.readthedocs.io/_images/chart_column2.png)](https://xlsxwriter.readthedocs.io/_images/chart_column2.png)

Chart 3 is a percentage stacked column chart:

[![_images/chart_column3.png](https://xlsxwriter.readthedocs.io/_images/chart_column3.png)](https://xlsxwriter.readthedocs.io/_images/chart_column3.png)

```python
#######################################################################
#
# An example of creating Excel Column charts with Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_column.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])

#######################################################################
#
# Create a new column chart.
#
chart1 = workbook.add_chart({'type': 'column'})

# Configure the first series.
chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure a second series. Note use of alternative syntax to define ranges.
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})

# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart1.set_style(11)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a stacked chart sub-type.
#
chart2 = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})

# Configure the first series.
chart2.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart2.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart2.set_title ({'name': 'Stacked Chart'})
chart2.set_x_axis({'name': 'Test number'})
chart2.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart2.set_style(12)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D18', chart2, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a percentage stacked chart sub-type.
#
chart3 = workbook.add_chart({'type': 'column', 'subtype': 'percent_stacked'})

# Configure the first series.
chart3.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart3.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart3.set_title ({'name': 'Percent Stacked Chart'})
chart3.set_x_axis({'name': 'Test number'})
chart3.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart3.set_style(13)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D34', chart3, {'x_offset': 25, 'y_offset': 10})

workbook.close()
```

## Example: 折线图

Example of creating an Excel line chart. The X axis of a line chart is a category axis with fixed point spacing. For a line chart with arbitrary point spacing see the Scatter chart type.

Chart 1 in the following example is:

[![_images/chart_line1.png](https://xlsxwriter.readthedocs.io/_images/chart_line1.png)](https://xlsxwriter.readthedocs.io/_images/chart_line1.png)

```python
#######################################################################
#
# An example of creating Excel Line charts with Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_line.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])

# Create a new chart object. In this case an embedded chart.
chart1 = workbook.add_chart({'type': 'line'})

# Configure the first series.
chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series. Note use of alternative syntax to define ranges.
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})

# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style. Colors with white outline and shadow.
chart1.set_style(10)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})


workbook.close()
```

## Example: 饼图

Example of creating Excel Pie charts. Chart 1 in the following example is:

[![_images/chart_pie1.png](https://xlsxwriter.readthedocs.io/_images/chart_pie1.png)](https://xlsxwriter.readthedocs.io/_images/chart_pie1.png)

Chart 2 shows how to set segment colors.

It is possible to define chart colors for most types of XlsxWriter charts via the [`add_series()`](https://xlsxwriter.readthedocs.io/chart.html#add_series) method. However, Pie charts are a special case since each segment is represented as a point and as such it is necessary to assign formatting to each point in the series.

[![_images/chart_pie2.png](https://xlsxwriter.readthedocs.io/_images/chart_pie2.png)](https://xlsxwriter.readthedocs.io/_images/chart_pie2.png)

Chart 3 shows how to rotate the segments of the chart:

[![_images/chart_pie3.png](https://xlsxwriter.readthedocs.io/_images/chart_pie3.png)](https://xlsxwriter.readthedocs.io/_images/chart_pie3.png)

```python
#######################################################################
#
# An example of creating Excel Pie charts with Python and XlsxWriter.
#
# The demo also shows how to set segment colors. It is possible to
# define chart colors for most types of XlsxWriter charts
# via the add_series() method. However, Pie/Doughnut charts are a special
# case since each segment is represented as a point so it is necessary to
# assign formatting to each point in the series.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_pie.xlsx')

worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Category', 'Values']
data = [
    ['Apple', 'Cherry', 'Pecan'],
    [60, 30, 10],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])

#######################################################################
#
# Create a new chart object.
#
chart1 = workbook.add_chart({'type': 'pie'})

# Configure the series. Note the use of the list syntax to define ranges:
chart1.add_series({
    'name':       'Pie sales data',
    'categories': ['Sheet1', 1, 0, 3, 0],
    'values':     ['Sheet1', 1, 1, 3, 1],
})

# Add a title.
chart1.set_title({'name': 'Popular Pie Types'})

# Set an Excel chart style. Colors with white outline and shadow.
chart1.set_style(10)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C2', chart1, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a Pie chart with user defined segment colors.
#

# Create an example Pie chart like above.
chart2 = workbook.add_chart({'type': 'pie'})

# Configure the series and add user defined segment colors.
chart2.add_series({
    'name': 'Pie sales data',
    'categories': '=Sheet1!$A$2:$A$4',
    'values':     '=Sheet1!$B$2:$B$4',
    'points': [
        {'fill': {'color': '#5ABA10'}},
        {'fill': {'color': '#FE110E'}},
        {'fill': {'color': '#CA5C05'}},
    ],
})

# Add a title.
chart2.set_title({'name': 'Pie Chart with user defined colors'})

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C18', chart2, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a Pie chart with rotation of the segments.
#

# Create an example Pie chart like above.
chart3 = workbook.add_chart({'type': 'pie'})

# Configure the series.
chart3.add_series({
    'name': 'Pie sales data',
    'categories': '=Sheet1!$A$2:$A$4',
    'values':     '=Sheet1!$B$2:$B$4',
})

# Add a title.
chart3.set_title({'name': 'Pie Chart with segment rotation'})

# Change the angle/rotation of the first segment.
chart3.set_rotation(90)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C34', chart3, {'x_offset': 25, 'y_offset': 10})

workbook.close()
```

## Example: 圆环图

Example of creating Excel Doughnut charts. Chart 1 in the following example is:

[![_images/chart_doughnut1.png](https://xlsxwriter.readthedocs.io/_images/chart_doughnut1.png)](https://xlsxwriter.readthedocs.io/_images/chart_doughnut1.png)

Chart 4 shows how to set segment colors and other options.

It is possible to define chart colors for most types of XlsxWriter charts via the [`add_series()`](https://xlsxwriter.readthedocs.io/chart.html#add_series) method. However, Pie/Doughnut charts are a special case since each segment is represented as a point and as such it is necessary to assign formatting to each point in the series.

[![_images/chart_doughnut2.png](https://xlsxwriter.readthedocs.io/_images/chart_doughnut2.png)](https://xlsxwriter.readthedocs.io/_images/chart_doughnut2.png)

```python
#######################################################################
#
# An example of creating Excel Doughnut charts with Python and XlsxWriter.
#
# The demo also shows how to set segment colors. It is possible to
# define chart colors for most types of XlsxWriter charts
# via the add_series() method. However, Pie/Doughnut charts are a special
# case since each segment is represented as a point so it is necessary to
# assign formatting to each point in the series.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_doughnut.xlsx')

worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Category', 'Values']
data = [
    ['Glazed', 'Chocolate', 'Cream'],
    [50, 35, 15],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])

#######################################################################
#
# Create a new chart object.
#
chart1 = workbook.add_chart({'type': 'doughnut'})

# Configure the series. Note the use of the list syntax to define ranges:
chart1.add_series({
    'name':       'Doughnut sales data',
    'categories': ['Sheet1', 1, 0, 3, 0],
    'values':     ['Sheet1', 1, 1, 3, 1],
})

# Add a title.
chart1.set_title({'name': 'Popular Doughnut Types'})

# Set an Excel chart style. Colors with white outline and shadow.
chart1.set_style(10)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C2', chart1, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a Doughnut chart with user defined segment colors.
#

# Create an example Doughnut chart like above.
chart2 = workbook.add_chart({'type': 'doughnut'})

# Configure the series and add user defined segment colors.
chart2.add_series({
    'name': 'Doughnut sales data',
    'categories': '=Sheet1!$A$2:$A$4',
    'values':     '=Sheet1!$B$2:$B$4',
    'points': [
        {'fill': {'color': '#FA58D0'}},
        {'fill': {'color': '#61210B'}},
        {'fill': {'color': '#F5F6CE'}},
    ],
})

# Add a title.
chart2.set_title({'name': 'Doughnut Chart with user defined colors'})

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C18', chart2, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a Doughnut chart with rotation of the segments.
#

# Create an example Doughnut chart like above.
chart3 = workbook.add_chart({'type': 'doughnut'})

# Configure the series.
chart3.add_series({
    'name': 'Doughnut sales data',
    'categories': '=Sheet1!$A$2:$A$4',
    'values':     '=Sheet1!$B$2:$B$4',
})

# Add a title.
chart3.set_title({'name': 'Doughnut Chart with segment rotation'})

# Change the angle/rotation of the first segment.
chart3.set_rotation(90)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C34', chart3, {'x_offset': 25, 'y_offset': 10})


#######################################################################
#
# Create a Doughnut chart with user defined hole size and other options.
#

# Create an example Doughnut chart like above.
chart4 = workbook.add_chart({'type': 'doughnut'})

# Configure the series.
chart4.add_series({
    'name': 'Doughnut sales data',
    'categories': '=Sheet1!$A$2:$A$4',
    'values':     '=Sheet1!$B$2:$B$4',
    'points': [
        {'fill': {'color': '#FA58D0'}},
        {'fill': {'color': '#61210B'}},
        {'fill': {'color': '#F5F6CE'}},
    ],
})

# Set a 3D style.
chart4.set_style(26)

# Add a title.
chart4.set_title({'name': 'Doughnut Chart with options applied'})

# Change the angle/rotation of the first segment.
chart4.set_rotation(28)

# Change the hole size.
chart4.set_hole_size(33)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('C50', chart4, {'x_offset': 25, 'y_offset': 10})


workbook.close()
```

## Example: 散点图

Example of creating Excel Scatter charts.

Chart 1 in the following example is a default scatter chart:

[![_images/chart_scatter1.png](https://xlsxwriter.readthedocs.io/_images/chart_scatter1.png)](https://xlsxwriter.readthedocs.io/_images/chart_scatter1.png)

Chart 2 is a scatter chart with straight lines and markers:

[![_images/chart_scatter2.png](https://xlsxwriter.readthedocs.io/_images/chart_scatter2.png)](https://xlsxwriter.readthedocs.io/_images/chart_scatter2.png)

Chart 3 is a scatter chart with straight lines and no markers:

[![_images/chart_scatter3.png](https://xlsxwriter.readthedocs.io/_images/chart_scatter3.png)](https://xlsxwriter.readthedocs.io/_images/chart_scatter3.png)

Chart 4 is a scatter chart with smooth lines and markers:

[![_images/chart_scatter4.png](https://xlsxwriter.readthedocs.io/_images/chart_scatter4.png)](https://xlsxwriter.readthedocs.io/_images/chart_scatter4.png)

Chart 5 is a scatter chart with smooth lines and no markers:

[![_images/chart_scatter5.png](https://xlsxwriter.readthedocs.io/_images/chart_scatter5.png)](https://xlsxwriter.readthedocs.io/_images/chart_scatter5.png)

```python
#######################################################################
#
# An example of creating Excel Scatter charts with Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_scatter.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])


#######################################################################
#
# Create a new scatter chart.
#
chart1 = workbook.add_chart({'type': 'scatter'})

# Configure the first series.
chart1.add_series({
    'name': '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values': '=Sheet1!$B$2:$B$7',
})

# Configure second series. Note use of alternative syntax to define ranges.
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})

# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart1.set_style(11)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a scatter chart sub-type with straight lines and markers.
#
chart2 = workbook.add_chart({'type': 'scatter',
                             'subtype': 'straight_with_markers'})

# Configure the first series.
chart2.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart2.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart2.set_title ({'name': 'Straight line with markers'})
chart2.set_x_axis({'name': 'Test number'})
chart2.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart2.set_style(12)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D18', chart2, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a scatter chart sub-type with straight lines and no markers.
#
chart3 = workbook.add_chart({'type': 'scatter',
                             'subtype': 'straight'})

# Configure the first series.
chart3.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart3.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart3.set_title ({'name': 'Straight line'})
chart3.set_x_axis({'name': 'Test number'})
chart3.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart3.set_style(13)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D34', chart3, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a scatter chart sub-type with smooth lines and markers.
#
chart4 = workbook.add_chart({'type': 'scatter',
                             'subtype': 'smooth_with_markers'})

# Configure the first series.
chart4.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart4.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart4.set_title ({'name': 'Smooth line with markers'})
chart4.set_x_axis({'name': 'Test number'})
chart4.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart4.set_style(14)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D50', chart4, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a scatter chart sub-type with smooth lines and no markers.
#
chart5 = workbook.add_chart({'type': 'scatter',
                             'subtype': 'smooth'})

# Configure the first series.
chart5.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart5.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart5.set_title ({'name': 'Smooth line'})
chart5.set_x_axis({'name': 'Test number'})
chart5.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart5.set_style(15)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D66', chart5, {'x_offset': 25, 'y_offset': 10})

workbook.close()
```

## Example: 雷达图

Example of creating Excel Column charts.

Chart 1 in the following example is a default radar chart:

[![_images/chart_radar1.png](https://xlsxwriter.readthedocs.io/_images/chart_radar1.png)](https://xlsxwriter.readthedocs.io/_images/chart_radar1.png)

Chart 2 in the following example is a radar chart with markers:

[![_images/chart_radar2.png](https://xlsxwriter.readthedocs.io/_images/chart_radar2.png)](https://xlsxwriter.readthedocs.io/_images/chart_radar2.png)

Chart 3 in the following example is a filled radar chart:

[![_images/chart_radar3.png](https://xlsxwriter.readthedocs.io/_images/chart_radar3.png)](https://xlsxwriter.readthedocs.io/_images/chart_radar3.png)

```python
#######################################################################
#
# An example of creating Excel Radar charts with Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_radar.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [30, 60, 70, 50, 40, 30],
    [25, 40, 50, 30, 50, 40],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])

#######################################################################
#
# Create a new radar chart.
#
chart1 = workbook.add_chart({'type': 'radar'})

# Configure the first series.
chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series. Note use of alternative syntax to define ranges.
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})

# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart1.set_style(11)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a radar chart with markers chart sub-type.
#
chart2 = workbook.add_chart({'type': 'radar', 'subtype': 'with_markers'})

# Configure the first series.
chart2.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart2.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart2.set_title ({'name': 'Radar Chart With Markers'})
chart2.set_x_axis({'name': 'Test number'})
chart2.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart2.set_style(12)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D18', chart2, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a filled radar chart sub-type.
#
chart3 = workbook.add_chart({'type': 'radar', 'subtype': 'filled'})

# Configure the first series.
chart3.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart3.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart3.set_title ({'name': 'Filled Radar Chart'})
chart3.set_x_axis({'name': 'Test number'})
chart3.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart3.set_style(13)

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D34', chart3, {'x_offset': 25, 'y_offset': 10})

workbook.close()
```

## Example: 股市图

Example of creating and Excel HiLow-Close Stock chart.

Chart 1 in the following example is:

[![_images/chart_stock1.png](https://xlsxwriter.readthedocs.io/_images/chart_stock1.png)](https://xlsxwriter.readthedocs.io/_images/chart_stock1.png)

```python
#######################################################################
#
# An example of creating Excel Stock charts with Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
from datetime import datetime
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_stock.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': 1})
date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})

chart = workbook.add_chart({'type': 'stock'})

# Add the worksheet data that the charts will refer to.
headings = ['Date', 'High', 'Low', 'Close']
data = [
    ['2007-01-01', '2007-01-02', '2007-01-03', '2007-01-04', '2007-01-05'],
    [27.2, 25.03, 19.05, 20.34, 18.5],
    [23.49, 19.55, 15.12, 17.84, 16.34],
    [25.45, 23.05, 17.32, 20.45, 17.34],
]

worksheet.write_row('A1', headings, bold)

for row in range(5):
    date = datetime.strptime(data[0][row], "%Y-%m-%d")

    worksheet.write(row + 1, 0, date, date_format)
    worksheet.write(row + 1, 1, data[1][row])
    worksheet.write(row + 1, 2, data[2][row])
    worksheet.write(row + 1, 3, data[3][row])

worksheet.set_column('A:D', 11)

# Add a series for each of the High-Low-Close columns.
chart.add_series({
    'categories': '=Sheet1!$A$2:$A$6',
    'values': '=Sheet1!$B$2:$B$6',
})

chart.add_series({
    'categories': '=Sheet1!$A$2:$A$6',
    'values':     '=Sheet1!$C$2:$C$6',
})

chart.add_series({
    'categories': '=Sheet1!$A$2:$A$6',
    'values': '=Sheet1!$D$2:$D$6',
})

# Add a chart title and some axis labels.
chart.set_title ({'name': 'High-Low-Close'})
chart.set_x_axis({'name': 'Date'})
chart.set_y_axis({'name': 'Share price'})

worksheet.insert_chart('E9', chart)

workbook.close()
```

## Example: 多种格式图

An example showing all 48 default chart styles available in Excel 2007 using the chart [`set_style()`](https://xlsxwriter.readthedocs.io/chart.html#set_style) method.

![_images/chart_styles.png](https://xlsxwriter.readthedocs.io/_images/chart_styles.png)

Note, these styles are not the same as the styles available in Excel 2013.

```python
#######################################################################
#
# An example showing all 48 default chart styles available in Excel 2007
# using Python and XlsxWriter. Note, these styles are not the same as
# the styles available in Excel 2013.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_styles.xlsx')

# Show the styles for all of these chart types.
chart_types = ['column', 'area', 'line', 'pie']

for chart_type in chart_types:

    # Add a worksheet for each chart type.
    worksheet = workbook.add_worksheet(chart_type.title())
    worksheet.set_zoom(30)
    style_number = 1

    # Create 48 charts, each with a different style.
    for row_num in range(0, 90, 15):
        for col_num in range(0, 64, 8):

            chart = workbook.add_chart({'type': chart_type})
            chart.add_series({'values': '=Data!$A$1:$A$6'})
            chart.set_title ({'name': 'Style %d' % style_number})
            chart.set_legend({'none': True})
            chart.set_style(style_number)

            worksheet.insert_chart(row_num, col_num , chart)
            style_number += 1

# Create a worksheet with data for the charts.
data_worksheet = workbook.add_worksheet('Data')
data = [10, 40, 50, 20, 10, 50]
data_worksheet.write_column('A1', data)
data_worksheet.hide()

workbook.close()
```

## Example: 样式填充

Example of creating an Excel chart with pattern fills, in the columns.

[![_images/chart_pattern.png](https://xlsxwriter.readthedocs.io/_images/chart_pattern.png)](https://xlsxwriter.readthedocs.io/_images/chart_pattern.png)

```python
#######################################################################
#
# An example of an Excel chart with patterns using Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_pattern.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Shingle', 'Brick']
data = [
    [105, 150, 130, 90 ],
    [50,  120, 100, 110],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])

# Create a new Chart object.
chart = workbook.add_chart({'type': 'column'})

# Configure the charts. Add two series with patterns. The gap is used to make
# the patterns more visible.
chart.add_series({
    'name':   '=Sheet1!$A$1',
    'values': '=Sheet1!$A$2:$A$5',
    'pattern': {
        'pattern':  'shingle',
        'fg_color': '#804000',
        'bg_color': '#c68c53'
    },
    'border':  {'color': '#804000'},
    'gap':     70,
})

chart.add_series({
    'name':   '=Sheet1!$B$1',
    'values': '=Sheet1!$B$2:$B$5',
    'pattern': {
        'pattern':  'horizontal_brick',
        'fg_color': '#b30000',
        'bg_color': '#ff6666'
    },
    'border':  {'color': '#b30000'},
})

# Add a chart title and some axis labels.
chart.set_title ({'name': 'Cladding types'})
chart.set_x_axis({'name': 'Region'})
chart.set_y_axis({'name': 'Number of houses'})

# Insert the chart into the worksheet.
worksheet.insert_chart('D2', chart)

workbook.close()
```

## Example: 渐变填充

Example of creating an Excel chart with gradient fills, in the columns and in the plot area.

[![_images/chart_gradient.png](https://xlsxwriter.readthedocs.io/_images/chart_gradient.png)](https://xlsxwriter.readthedocs.io/_images/chart_gradient.png)

```python
#######################################################################
#
# An example of creating an Excel charts with gradient fills using
# Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_gradient.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])


# Create a new column chart.
chart = workbook.add_chart({'type': 'column'})

# Configure the first series, including a gradient.
chart.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
    'gradient':   {'colors': ['#963735', '#F1DCDB']}
})

# Configure the second series, including a gradient.
chart.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
    'gradient':   {'colors': ['#E36C0A', '#FCEADA']}
})

# Set a gradient for the plotarea.
chart.set_plotarea({
    'gradient': {'colors': ['#FFEFD1', '#F0EBD5', '#B69F66']}
})


# Add some axis labels.
chart.set_x_axis({'name': 'Test number'})
chart.set_y_axis({'name': 'Sample length (mm)'})

# Turn off the chart legend.
chart.set_legend({'none': True})

# Insert the chart into the worksheet.
worksheet.insert_chart('E2', chart)

workbook.close()
```

## Example: 双轴

Example of creating an Excel Line chart with a secondary axis. Note, the primary and secondary chart type are the same. The next example shows a secondary chart of a different type.

[![_images/chart_secondary_axis1.png](https://xlsxwriter.readthedocs.io/_images/chart_secondary_axis1.png)](https://xlsxwriter.readthedocs.io/_images/chart_secondary_axis1.png)

```python
#######################################################################
#
# An example of creating an Excel Line chart with a secondary axis
# using Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_secondary_axis.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Aliens', 'Humans']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])


# Create a new chart object. In this case an embedded chart.
chart = workbook.add_chart({'type': 'line'})

# Configure a series with a secondary axis
chart.add_series({
    'name':   '=Sheet1!$A$1',
    'values': '=Sheet1!$A$2:$A$7',
    'y2_axis': 1,
})

chart.add_series({
    'name':   '=Sheet1!$B$1',
    'values': '=Sheet1!$B$2:$B$7',
})

chart.set_legend({'position': 'right'})

# Add a chart title and some axis labels.
chart.set_title({'name': 'Survey results'})
chart.set_x_axis({'name': 'Days', })
chart.set_y_axis({'name': 'Population', 'major_gridlines': {'visible': 0}})
chart.set_y2_axis({'name': 'Laser wounds'})

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart, {'x_offset': 25, 'y_offset': 10})

workbook.close()
```

## Example: 图形结合

Example of creating combined Excel charts with two chart types.

In the first example we create a combined column and line chart that share the same X and Y axes.

[![_images/chart_combined1.png](https://xlsxwriter.readthedocs.io/_images/chart_combined1.png)](https://xlsxwriter.readthedocs.io/_images/chart_combined1.png)

In the second example we create a similar combined column and line chart except that the secondary chart has a secondary Y axis.

[![_images/chart_combined2.png](https://xlsxwriter.readthedocs.io/_images/chart_combined2.png)](https://xlsxwriter.readthedocs.io/_images/chart_combined2.png)

```python
#######################################################################
#
# An example of a Combined chart in XlsxWriter.
#
# Copyright 2013, John McNamara, jmcnamara@cpan.org
#
from xlsxwriter.workbook import Workbook

workbook  = Workbook('chart_combined.xlsx')
worksheet = workbook.add_worksheet()

# Add a format for the headings.
bold = workbook.add_format({'bold': True})

# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])

#
# In the first example we will create a combined column and line chart.
# They will share the same X and Y axes.
#

# Create a new column chart. This will use this as the primary chart.
column_chart1 = workbook.add_chart({'type': 'column'})

# Configure the data series for the primary chart.
column_chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Create a new column chart. This will use this as the secondary chart.
line_chart1 = workbook.add_chart({'type': 'line'})

# Configure the data series for the secondary chart.
line_chart1.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Combine the charts.
column_chart1.combine(line_chart1)

# Add a chart title and some axis labels. Note, this is done via the
# primary chart.
column_chart1.set_title({ 'name': 'Combined chart - same Y axis'})
column_chart1.set_x_axis({'name': 'Test number'})
column_chart1.set_y_axis({'name': 'Sample length (mm)'})

# Insert the chart into the worksheet
worksheet.insert_chart('E2', column_chart1)

#
# In the second example we will create a similar combined column and line
# chart except that the secondary chart will have a secondary Y axis.
#

# Create a new column chart. This will use this as the primary chart.
column_chart2 = workbook.add_chart({'type': 'column'})

# Configure the data series for the primary chart.
column_chart2.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Create a new column chart. This will use this as the secondary chart.
line_chart2 = workbook.add_chart({'type': 'line'})

# Configure the data series for the secondary chart. We also set a
# secondary Y axis via (y2_axis). This is the only difference between
# this and the first example, apart from the axis label below.
line_chart2.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
    'y2_axis':    True,
})

# Combine the charts.
column_chart2.combine(line_chart2)

# Add a chart title and some axis labels.
column_chart2.set_title({  'name': 'Combine chart - secondary Y axis'})
column_chart2.set_x_axis({ 'name': 'Test number'})
column_chart2.set_y_axis({ 'name': 'Sample length (mm)'})

# Note: the y2 properties are on the secondary chart.
line_chart2.set_y2_axis({'name': 'Target length (mm)'})

# Insert the chart into the worksheet
worksheet.insert_chart('E18', column_chart2)

workbook.close()
```

## Example: Pareto 图

Example of creating a Pareto chart with a secondary chart and axis.

[![_images/chart_pareto.png](https://xlsxwriter.readthedocs.io/_images/chart_pareto.png)](https://xlsxwriter.readthedocs.io/_images/chart_pareto.png)

```python
#######################################################################
#
# An example of creating of a Pareto chart with Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_pareto.xlsx')
worksheet = workbook.add_worksheet()

# Formats used in the workbook.
bold = workbook.add_format({'bold': True})
percent_format = workbook.add_format({'num_format': '0.0%'})

# Widen the columns for visibility.
worksheet.set_column('A:A', 15)
worksheet.set_column('B:C', 10)

# Add the worksheet data that the charts will refer to.
headings = ['Reason', 'Number', 'Percentage']

reasons = [
    'Traffic', 'Child care', 'Public Transport', 'Weather',
    'Overslept', 'Emergency',
]

numbers  = [60,   40,    20,  15,  10,    5]
percents = [0.44, 0.667, 0.8, 0.9, 0.967, 1]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', reasons)
worksheet.write_column('B2', numbers)
worksheet.write_column('C2', percents, percent_format)


# Create a new column chart. This will be the primary chart.
column_chart = workbook.add_chart({'type': 'column'})

# Add a series.
column_chart.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Add a chart title.
column_chart.set_title({'name': 'Reasons for lateness'})

# Turn off the chart legend.
column_chart.set_legend({'position': 'none'})

# Set the title and scale of the Y axes. Note, the secondary axis is set from
# the primary chart.
column_chart.set_y_axis({
    'name': 'Respondents (number)',
    'min': 0,
    'max': 120
})
column_chart.set_y2_axis({'max': 1})

# Create a new line chart. This will be the secondary chart.
line_chart = workbook.add_chart({'type': 'line'})

# Add a series, on the secondary axis.
line_chart.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
    'marker':     {'type': 'automatic'},
    'y2_axis':    1,
})

# Combine the charts.
column_chart.combine(line_chart)

# Insert the chart into the worksheet.
worksheet.insert_chart('F2', column_chart)

workbook.close()
```

## Example: 仪表图

A Gauge Chart isn’t a native chart type in Excel. It is constructed by combining a doughnut chart and a pie chart and by using some non-filled elements. This example follows the following online example of how to create a Gauge Chart in Excel: https://www.excel-easy.com/examples/gauge-chart.html

![_images/chart_gauge.png](https://xlsxwriter.readthedocs.io/_images/chart_gauge.png)

```python
#######################################################################
#
# An example of creating a Gauge Chart in Excel with Python and XlsxWriter.
#
# A Gauge Chart isn't a native chart type in Excel. It is constructed by
# combining a doughnut chart and a pie chart and by using some non-filled
# elements. This example follows the following online example of how to create
# a Gauge Chart in Excel: https://www.excel-easy.com/examples/gauge-chart.html
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_gauge.xlsx')
worksheet = workbook.add_worksheet()

chart_doughnut = workbook.add_chart({'type': 'doughnut'})
chart_pie = workbook.add_chart({'type': 'pie'})

# Add some data for the Doughnut and Pie charts. This is set up so the
# gauge goes from 0-100. It is initially set at 75%.
worksheet.write_column('H2', ['Donut', 25, 50, 25, 100])
worksheet.write_column('I2', ['Pie', 75, 1, '=200-I4-I3'])

# Configure the doughnut chart as the background for the gauge.
chart_doughnut.add_series({
    'name': '=Sheet1!$H$2',
    'values': '=Sheet1!$H$3:$H$6',
    'points': [
        {'fill': {'color': 'green'}},
        {'fill': {'color': 'yellow'}},
        {'fill': {'color': 'red'}},
        {'fill': {'none': True}}],
})

# Rotate chart so the gauge parts are above the horizontal.
chart_doughnut.set_rotation(270)

# Turn off the chart legend.
chart_doughnut.set_legend({'none': True})

# Turn off the chart fill and border.
chart_doughnut.set_chartarea({
    'border': {'none': True},
    'fill': {'none': True},
})

# Configure the pie chart as the needle for the gauge.
chart_pie.add_series({
    'name': '=Sheet1!$I$2',
    'values': '=Sheet1!$I$3:$I$6',
    'points': [
        {'fill': {'none': True}},
        {'fill': {'color': 'black'}},
        {'fill': {'none': True}}],
})

# Rotate the pie chart/needle to align with the doughnut/gauge.
chart_pie.set_rotation(270)

# Combine the pie and doughnut charts.
chart_doughnut.combine(chart_pie)

# Insert the chart into the worksheet.
worksheet.insert_chart('A1', chart_doughnut)

workbook.close()
```

## Example: 聚类图

Example of creating a clustered Excel chart where there are two levels of category on the X axis.

[![_images/chart_clustered.png](https://xlsxwriter.readthedocs.io/_images/chart_clustered.png)](https://xlsxwriter.readthedocs.io/_images/chart_clustered.png)

The categories in clustered charts are 2D ranges, instead of the more normal 1D ranges. The series are shown as formula strings for clarity but you can also use the a list syntax.

```python
#######################################################################
#
# A demo of a clustered category chart in XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
from xlsxwriter.workbook import Workbook

workbook = Workbook('chart_clustered.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Types', 'Sub Type', 'Value 1', 'Value 2', 'Value 3']
data = [
    ['Type 1', 'Sub Type A', 5000,      8000,      6000],
    ['',       'Sub Type B', 2000,      3000,      4000],
    ['',       'Sub Type C', 250,       1000,      2000],
    ['Type 2', 'Sub Type D', 6000,      6000,      6500],
    ['',       'Sub Type E', 500,       300,        200],
]

worksheet.write_row('A1', headings, bold)

for row_num, row_data in enumerate(data):
    worksheet.write_row(row_num + 1, 0, row_data)

# Create a new chart object. In this case an embedded chart.
chart = workbook.add_chart({'type': 'column'})

# Configure the series. Note, that the categories are 2D ranges (from column A
# to column B). This creates the clusters. The series are shown as formula
# strings for clarity but you can also use the list syntax. See the docs.
chart.add_series({
    'categories': '=Sheet1!$A$2:$B$6',
    'values':     '=Sheet1!$C$2:$C$6',
})

chart.add_series({
    'categories': '=Sheet1!$A$2:$B$6',
    'values':     '=Sheet1!$D$2:$D$6',
})

chart.add_series({
    'categories': '=Sheet1!$A$2:$B$6',
    'values':     '=Sheet1!$E$2:$E$6',
})

# Set the Excel chart style.
chart.set_style(37)

# Turn off the legend.
chart.set_legend({'position': 'none'})

# Insert the chart into the worksheet.
worksheet.insert_chart('G3', chart)

workbook.close()
```

## Example: 时间轴图

Date Category Axes are a special case of Category axes in Excel which give them some of the properties of Values axes.

For example, Excel doesn’t normally allow minimum and maximum values to be set for category axes. However, date axes are an exception.

[![_images/chart_date_axis.png](https://xlsxwriter.readthedocs.io/_images/chart_date_axis.png)](https://xlsxwriter.readthedocs.io/_images/chart_date_axis.png)

In XlsxWriter Date Category Axes are set using the `date_axis` option in [`set_x_axis()`](https://xlsxwriter.readthedocs.io/chart.html#set_x_axis) or [`set_y_axis()`](https://xlsxwriter.readthedocs.io/chart.html#set_y_axis):

```python
chart.set_x_axis({'date_axis': True})
```

If used, the `min` and `max` values should be set as Excel times or dates.

```python
#######################################################################
#
# An example of creating an Excel charts with a date axis using
# Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

from datetime import date
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_date_axis.xlsx')

worksheet = workbook.add_worksheet()
chart = workbook.add_chart({'type': 'line'})
date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})

# Widen the first column to display the dates.
worksheet.set_column('A:A', 12)

# Some data to be plotted in the worksheet.
dates = [date(2013, 1, 1),
         date(2013, 1, 2),
         date(2013, 1, 3),
         date(2013, 1, 4),
         date(2013, 1, 5),
         date(2013, 1, 6),
         date(2013, 1, 7),
         date(2013, 1, 8),
         date(2013, 1, 9),
         date(2013, 1, 10)]

values = [10, 30, 20, 40, 20, 60, 50, 40, 30, 30]

# Write the date to the worksheet.
worksheet.write_column('A1', dates, date_format)
worksheet.write_column('B1', values)

# Add a series to the chart.
chart.add_series({
    'categories': '=Sheet1!$A$1:$A$10',
    'values': '=Sheet1!$B$1:$B$10',
})

# Configure the X axis as a Date axis and set the max and min limits.
chart.set_x_axis({
    'date_axis': True,
    'min': date(2013, 1, 2),
    'max': date(2013, 1, 9),
})

# Turn off the legend.
chart.set_legend({'none': True})

# Insert the chart into the worksheet.
worksheet.insert_chart('D2', chart)

workbook.close()
```

## Example: 数据表图

Example of creating charts with data tables.

Chart 1 in the following example is a column chart with default data table:

[![_images/chart_data_table1.png](https://xlsxwriter.readthedocs.io/_images/chart_data_table1.png)](https://xlsxwriter.readthedocs.io/_images/chart_data_table1.png)

Chart 2 is a column chart with default data table with legend keys:

[![_images/chart_data_table2.png](https://xlsxwriter.readthedocs.io/_images/chart_data_table2.png)](https://xlsxwriter.readthedocs.io/_images/chart_data_table2.png)

```python
#######################################################################
#
# An example of creating Excel Column charts with data tables using
# Python and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_data_table.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])


#######################################################################
#
# Create a column chart with a data table.
#
chart1 = workbook.add_chart({'type': 'column'})

# Configure the first series.
chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series. Note use of alternative syntax to define ranges.
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})

# Add a chart title and some axis labels.
chart1.set_title({'name': 'Chart with Data Table'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})

# Set a default data table on the X-Axis.
chart1.set_table()

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Create a column chart with a data table and legend keys.
#
chart2 = workbook.add_chart({'type': 'column'})

# Configure the first series.
chart2.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure second series.
chart2.add_series({
    'name':       '=Sheet1!$C$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title and some axis labels.
chart2.set_title({'name': 'Data Table with legend keys'})
chart2.set_x_axis({'name': 'Test number'})
chart2.set_y_axis({'name': 'Sample length (mm)'})

# Set a data table on the X-Axis with the legend keys shown.
chart2.set_table({'show_keys': True})

# Hide the chart legend since the keys are shown on the data table.
chart2.set_legend({'position': 'none'})

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D18', chart2, {'x_offset': 25, 'y_offset': 10})

workbook.close()
```

## Example: Charts with Data Tools

A demo of an various Excel chart data tools that are available via an XlsxWriter chart. These include, Trendlines, Data Labels, Error Bars, Drop Lines, High-Low Lines and Up-Down Bars.

Chart 1 in the following example is a chart with trendlines:

[![_images/chart_data_tools1.png](https://xlsxwriter.readthedocs.io/_images/chart_data_tools1.png)](https://xlsxwriter.readthedocs.io/_images/chart_data_tools1.png)

Chart 2 is a chart with data labels and markers:

[![_images/chart_data_tools2.png](https://xlsxwriter.readthedocs.io/_images/chart_data_tools2.png)](https://xlsxwriter.readthedocs.io/_images/chart_data_tools2.png)

Chart 3 is a chart with error bars:

[![_images/chart_data_tools3.png](https://xlsxwriter.readthedocs.io/_images/chart_data_tools3.png)](https://xlsxwriter.readthedocs.io/_images/chart_data_tools3.png)

Chart 4 is a chart with up-down bars:

[![_images/chart_data_tools4.png](https://xlsxwriter.readthedocs.io/_images/chart_data_tools4.png)](https://xlsxwriter.readthedocs.io/_images/chart_data_tools4.png)

Chart 5 is a chart with hi-low lines:

[![_images/chart_data_tools5.png](https://xlsxwriter.readthedocs.io/_images/chart_data_tools5.png)](https://xlsxwriter.readthedocs.io/_images/chart_data_tools5.png)

Chart 6 is a chart with drop lines:

[![_images/chart_data_tools6.png](https://xlsxwriter.readthedocs.io/_images/chart_data_tools6.png)](https://xlsxwriter.readthedocs.io/_images/chart_data_tools6.png)

```python
#######################################################################
#
# A demo of an various Excel chart data tools that are available via
# an XlsxWriter chart.
#
# These include, Trendlines, Data Labels, Error Bars, Drop Lines,
# High-Low Lines and Up-Down Bars.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_data_tools.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Data 1', 'Data 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])


#######################################################################
#
# Trendline example.
#
# Create a Line chart.
chart1 = workbook.add_chart({'type': 'line'})

# Configure the first series with a polynomial trendline.
chart1.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
    'trendline': {
        'type': 'polynomial',
        'order': 3,
    },
})

# Configure the second series with a moving average trendline.
chart1.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
    'trendline': {'type': 'linear'},
})

# Add a chart title.
chart1.set_title({'name': 'Chart with Trendlines'})

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Data Labels and Markers example.
#
# Create a Line chart.
chart2 = workbook.add_chart({'type': 'line'})

# Configure the first series.
chart2.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
    'data_labels': {'value': 1},
    'marker': {'type': 'automatic'},
})

# Configure the second series.
chart2.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title.
chart2.set_title({'name': 'Chart with Data Labels and Markers'})

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D18', chart2, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Error Bars example.
#
# Create a Line chart.
chart3 = workbook.add_chart({'type': 'line'})

# Configure the first series.
chart3.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
    'y_error_bars': {'type': 'standard_error'},
})

# Configure the second series.
chart3.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values': '=Sheet1!$C$2:$C$7',
})

# Add a chart title.
chart3.set_title({'name': 'Chart with Error Bars'})

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D34', chart3, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Up-Down Bars example.
#
# Create a Line chart.
chart4 = workbook.add_chart({'type': 'line'})

# Add the Up-Down Bars.
chart4.set_up_down_bars()

# Configure the first series.
chart4.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure the second series.
chart4.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title.
chart4.set_title({'name': 'Chart with Up-Down Bars'})

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D50', chart4, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# High-Low Lines example.
#
# Create a Line chart.
chart5 = workbook.add_chart({'type': 'line'})

# Add the High-Low lines.
chart5.set_high_low_lines()

# Configure the first series.
chart5.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure the second series.
chart5.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title.
chart5.set_title({'name': 'Chart with High-Low Lines'})

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D66', chart5, {'x_offset': 25, 'y_offset': 10})

#######################################################################
#
# Drop Lines example.
#
# Create a Line chart.
chart6 = workbook.add_chart({'type': 'line'})

# Add Drop Lines.
chart6.set_drop_lines()

# Configure the first series.
chart6.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure the second series.
chart6.add_series({
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$C$2:$C$7',
})

# Add a chart title.
chart6.set_title({'name': 'Chart with Drop Lines'})

# Insert the chart into the worksheet (with an offset).
worksheet.insert_chart('D82', chart6, {'x_offset': 25, 'y_offset': 10})

workbook.close()
```

## Example: Chartsheet

Example of creating an Excel Bar chart on a [chartsheet](https://xlsxwriter.readthedocs.io/chartsheet.html#chartsheet).

![_images/chartsheet.png](https://xlsxwriter.readthedocs.io/_images/chartsheet.png)

```python
#######################################################################
#
# An example of creating an Excel chart in a chartsheet with Python
# and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#
import xlsxwriter

workbook = xlsxwriter.Workbook('chartsheet.xlsx')

# Add a worksheet to hold the data.
worksheet = workbook.add_worksheet()

# Add a chartsheet. A worksheet that only holds a chart.
chartsheet = workbook.add_chartsheet()

# Add a format for the headings.
bold = workbook.add_format({'bold': 1})

# Add the worksheet data that the charts will refer to.
headings = ['Number', 'Batch 1', 'Batch 2']
data = [
    [2, 3, 4, 5, 6, 7],
    [10, 40, 50, 20, 10, 50],
    [30, 60, 70, 50, 40, 30],
]

worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', data[0])
worksheet.write_column('B2', data[1])
worksheet.write_column('C2', data[2])


# Create a new bar chart.
chart1 = workbook.add_chart({'type': 'bar'})

# Configure the first series.
chart1.add_series({
    'name':       '=Sheet1!$B$1',
    'categories': '=Sheet1!$A$2:$A$7',
    'values':     '=Sheet1!$B$2:$B$7',
})

# Configure a second series. Note use of alternative syntax to define ranges.
chart1.add_series({
    'name':       ['Sheet1', 0, 2],
    'categories': ['Sheet1', 1, 0, 6, 0],
    'values':     ['Sheet1', 1, 2, 6, 2],
})

# Add a chart title and some axis labels.
chart1.set_title ({'name': 'Results of sample analysis'})
chart1.set_x_axis({'name': 'Test number'})
chart1.set_y_axis({'name': 'Sample length (mm)'})

# Set an Excel chart style.
chart1.set_style(11)

# Add the chart to the chartsheet.
chartsheet.set_chart(chart1)

# Display the chartsheet as the active sheet when the workbook is opened.
chartsheet.activate();

workbook.close()
```

# pandas examples

## Example: 简单例子

A simple example of converting a Pandas dataframe to an Excel file using Pandas and XlsxWriter. See [Working with Python Pandas and XlsxWriter](https://xlsxwriter.readthedocs.io/working_with_pandas.html#ewx-pandas) for more details.

![_images/pandas_simple.png](https://xlsxwriter.readthedocs.io/_images/pandas_simple.png)

```python
##############################################################################
#
# A simple example of converting a Pandas dataframe to an xlsx file using
# Pandas and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

import pandas as pd


# Create a Pandas dataframe from some data.
df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
```

## Example: 多数据框

An example of writing multiple dataframes to worksheets using Pandas and XlsxWriter.

![_images/pandas_multiple.png](https://xlsxwriter.readthedocs.io/_images/pandas_multiple.png)

```python
##############################################################################
#
# An example of writing multiple dataframes to worksheets using Pandas and
# XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

import pandas as pd


# Create some Pandas dataframes from some data.
df1 = pd.DataFrame({'Data': [11, 12, 13, 14]})
df2 = pd.DataFrame({'Data': [21, 22, 23, 24]})
df3 = pd.DataFrame({'Data': [31, 32, 33, 34]})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_multiple.xlsx', engine='xlsxwriter')

# Write each dataframe to a different worksheet.
df1.to_excel(writer, sheet_name='Sheet1')
df2.to_excel(writer, sheet_name='Sheet2')
df3.to_excel(writer, sheet_name='Sheet3')

# Close the Pandas Excel writer and output the Excel file.
writer.save()
```

## Example: 数据框位置

An example of positioning dataframes in a worksheet using Pandas and XlsxWriter. It also demonstrates how to write a dataframe without the header and index.

![_images/pandas_positioning.png](https://xlsxwriter.readthedocs.io/_images/pandas_positioning.png)

```python
##############################################################################
#
# An example of positioning dataframes in a worksheet using Pandas and
# XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

import pandas as pd


# Create some Pandas dataframes from some data.
df1 = pd.DataFrame({'Data': [11, 12, 13, 14]})
df2 = pd.DataFrame({'Data': [21, 22, 23, 24]})
df3 = pd.DataFrame({'Data': [31, 32, 33, 34]})
df4 = pd.DataFrame({'Data': [41, 42, 43, 44]})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_positioning.xlsx', engine='xlsxwriter')

# Position the dataframes in the worksheet.
df1.to_excel(writer, sheet_name='Sheet1')  # Default position, cell A1.
df2.to_excel(writer, sheet_name='Sheet1', startcol=3)
df3.to_excel(writer, sheet_name='Sheet1', startrow=6)

# It is also possible to write the dataframe without the header and index.
df4.to_excel(writer, sheet_name='Sheet1',
             startrow=7, startcol=4, header=False, index=False)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
```

## Example: 输出图形

A simple example of converting a Pandas dataframe to an Excel file with a chart using Pandas and XlsxWriter.

![_images/pandas_chart.png](https://xlsxwriter.readthedocs.io/_images/pandas_chart.png)

```python
##############################################################################
#
# An example of converting a Pandas dataframe to an xlsx file with a chart
# using Pandas and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

import pandas as pd


# Create a Pandas dataframe from some data.
df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_chart.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Create a chart object.
chart = workbook.add_chart({'type': 'column'})

# Configure the series of the chart from the dataframe data.
chart.add_series({'values': '=Sheet1!$B$2:$B$8'})

# Insert the chart into the worksheet.
worksheet.insert_chart('D2', chart)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
```

## Example: 条件格式

An example of converting a Pandas dataframe to an Excel file with a conditional formatting using Pandas and XlsxWriter.

![_images/pandas_conditional.png](https://xlsxwriter.readthedocs.io/_images/pandas_conditional.png)

```python
##############################################################################
#
# An example of converting a Pandas dataframe to an xlsx file with a
# conditional formatting using Pandas and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

import pandas as pd


# Create a Pandas dataframe from some data.
df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_conditional.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Apply a conditional format to the cell range.
worksheet.conditional_format('B2:B8', {'type': '3_color_scale'})

# Close the Pandas Excel writer and output the Excel file.
writer.save()
```

## Example: 时间格式

An example of converting a Pandas dataframe with datetimes to an Excel file with a default datetime and date format using Pandas and XlsxWriter.

![_images/pandas_datetime.png](https://xlsxwriter.readthedocs.io/_images/pandas_datetime.png)

```python
##############################################################################
#
# An example of converting a Pandas dataframe with datetimes to an xlsx file
# with a default datetime and date format using Pandas and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

import pandas as pd
from datetime import datetime, date

# Create a Pandas dataframe from some datetime data.
df = pd.DataFrame({'Date and time': [datetime(2015, 1, 1, 11, 30, 55),
                                     datetime(2015, 1, 2, 1,  20, 33),
                                     datetime(2015, 1, 3, 11, 10    ),
                                     datetime(2015, 1, 4, 16, 45, 35),
                                     datetime(2015, 1, 5, 12, 10, 15)],
                   'Dates only':    [date(2015, 2, 1),
                                     date(2015, 2, 2),
                                     date(2015, 2, 3),
                                     date(2015, 2, 4),
                                     date(2015, 2, 5)],
                   })

# Create a Pandas Excel writer using XlsxWriter as the engine.
# Also set the default datetime and date formats.
writer = pd.ExcelWriter("pandas_datetime.xlsx",
                        engine='xlsxwriter',
                        datetime_format='mmm d yyyy hh:mm:ss',
                        date_format='mmmm dd yyyy')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Get the xlsxwriter workbook and worksheet objects in order to set the column
# widths, to make the dates clearer.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

worksheet.set_column('B:C', 20)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
```

## Example: 数据列格式

An example of converting a Pandas dataframe to an Excel file with column formats using Pandas and XlsxWriter.

It isn’t possible to format any cells that already have a format such as the index or headers or any cells that contain dates or datetimes.

Note: This feature requires Pandas >= 0.16.

![_images/pandas_column_formats.png](https://xlsxwriter.readthedocs.io/_images/pandas_column_formats.png)

```python
##############################################################################
#
# An example of converting a Pandas dataframe to an xlsx file
# with column formats using Pandas and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

import pandas as pd

# Create a Pandas dataframe from some data.
df = pd.DataFrame({'Numbers':    [1010, 2020, 3030, 2020, 1515, 3030, 4545],
                   'Percentage': [.1,   .2,   .33,  .25,  .5,   .75,  .45 ],
})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter("pandas_column_formats.xlsx", engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Add some cell formats.
format1 = workbook.add_format({'num_format': '#,##0.00'})
format2 = workbook.add_format({'num_format': '0%'})

# Note: It isn't possible to format any cells that already have a format such
# as the index or headers or any cells that contain dates or datetimes.

# Set the column width and format.
worksheet.set_column('B:B', 18, format1)

# Set the format but not the column width.
worksheet.set_column('C:C', None, format2)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
```

## Example: 自定义表头格式

An example of converting a Pandas dataframe to an Excel file with a user defined header format using Pandas and XlsxWriter.

![_images/pandas_header_format.png](https://xlsxwriter.readthedocs.io/_images/pandas_header_format.png)

```python
##############################################################################
#
# An example of converting a Pandas dataframe to an xlsx file
# with a user defined header format.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

import pandas as pd

# Create a Pandas dataframe from some data.
data = [10, 20, 30, 40, 50, 60]
df = pd.DataFrame({'Heading': data,
                   'Longer heading that should be wrapped' : data})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter("pandas_header_format.xlsx", engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object. Note that we turn off
# the default header and skip one row to allow us to insert a user defined
# header.
df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Sheet1']

# Add a header format.
header_format = workbook.add_format({
    'bold': True,
    'text_wrap': True,
    'valign': 'top',
    'fg_color': '#D7E4BC',
    'border': 1})

# Write the column headers with the defined format.
for col_num, value in enumerate(df.columns.values):
    worksheet.write(0, col_num + 1, value, header_format)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
```

## Example: 带有折线图

A simple example of converting a Pandas dataframe to an Excel file with a line chart using Pandas and XlsxWriter.

[![_images/pandas_chart_line.png](https://xlsxwriter.readthedocs.io/_images/pandas_chart_line.png)](https://xlsxwriter.readthedocs.io/_images/pandas_chart_line.png)

```python
##############################################################################
#
# An example of converting a Pandas dataframe to an xlsx file with a line
# chart using Pandas and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

import pandas as pd
import random

# Create some sample data to plot.
max_row     = 21
categories  = ['Node 1', 'Node 2', 'Node 3', 'Node 4']
index_1     = range(0, max_row, 1)
multi_iter1 = {'index': index_1}

for category in categories:
    multi_iter1[category] = [random.randint(10, 100) for x in index_1]

# Create a Pandas dataframe from the data.
index_2 = multi_iter1.pop('index')
df      = pd.DataFrame(multi_iter1, index=index_2)
df      = df.reindex(columns=sorted(df.columns))

# Create a Pandas Excel writer using XlsxWriter as the engine.
sheet_name = 'Sheet1'
writer     = pd.ExcelWriter('pandas_chart_line.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name=sheet_name)

# Access the XlsxWriter workbook and worksheet objects from the dataframe.
workbook  = writer.book
worksheet = writer.sheets[sheet_name]

# Create a chart object.
chart = workbook.add_chart({'type': 'line'})

# Configure the series of the chart from the dataframe data.
for i in range(len(categories)):
    col = i + 1
    chart.add_series({
        'name':       ['Sheet1', 0, col],
        'categories': ['Sheet1', 1, 0,   max_row, 0],
        'values':     ['Sheet1', 1, col, max_row, col],
    })

# Configure the chart axes.
chart.set_x_axis({'name': 'Index'})
chart.set_y_axis({'name': 'Value', 'major_gridlines': {'visible': False}})

# Insert the chart into the worksheet.
worksheet.insert_chart('G2', chart)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
```

## Example: 带有股票图

An example of converting a Pandas dataframe with stock data taken from the web to an Excel file with a line chart using Pandas and XlsxWriter.

Note: occasionally the Yahoo source for the data used in the chart is down or under maintenance. If there are any issues running this program check the source data first.

[![_images/pandas_chart_stock.png](https://xlsxwriter.readthedocs.io/_images/pandas_chart_stock.png)](https://xlsxwriter.readthedocs.io/_images/pandas_chart_stock.png)

```python
##############################################################################
#
# An example of converting a Pandas dataframe with stock data taken from the
# web to an xlsx file with a line chart using Pandas and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

import pandas as pd
import pandas.io.data as web

# Create some sample data to plot.
all_data = {}
for ticker in ['AAPL', 'GOOGL', 'IBM', 'YHOO', 'MSFT']:
    all_data[ticker] = web.get_data_yahoo(ticker, '5/1/2014', '5/1/2015')

# Create a Pandas dataframe from the data.
df = pd.DataFrame({tic: data['Adj Close']
                   for tic, data in all_data.items()})

# Create a Pandas Excel writer using XlsxWriter as the engine.
sheet_name = 'Sheet1'
writer     = pd.ExcelWriter('pandas_chart_stock.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name=sheet_name)

# Access the XlsxWriter workbook and worksheet objects from the dataframe.
workbook  = writer.book
worksheet = writer.sheets[sheet_name]

# Adjust the width of the first column to make the date values clearer.
worksheet.set_column('A:A', 20)

# Create a chart object.
chart = workbook.add_chart({'type': 'line'})

# Configure the series of the chart from the dataframe data.
max_row = len(df) + 1
for i in range(len(['AAPL', 'GOOGL'])):
    col = i + 1
    chart.add_series({
        'name':       ['Sheet1', 0, col],
        'categories': ['Sheet1', 2, 0, max_row, 0],
        'values':     ['Sheet1', 2, col, max_row, col],
        'line':       {'width': 1.00},
    })

# Configure the chart axes.
chart.set_x_axis({'name': 'Date', 'date_axis': True})
chart.set_y_axis({'name': 'Price', 'major_gridlines': {'visible': False}})

# Position the legend at the top of the chart.
chart.set_legend({'position': 'top'})

# Insert the chart into the worksheet.
worksheet.insert_chart('H2', chart)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
```

## Example: 带有列图

An example of converting a Pandas dataframe to an Excel file with a column chart using Pandas and XlsxWriter.

[![_images/pandas_chart_columns.png](https://xlsxwriter.readthedocs.io/_images/pandas_chart_columns.png)](https://xlsxwriter.readthedocs.io/_images/pandas_chart_columns.png)

```python
##############################################################################
#
# An example of converting a Pandas dataframe to an xlsx file with a grouped
# column chart using Pandas and XlsxWriter.
#
# Copyright 2013-2019, John McNamara, jmcnamara@cpan.org
#

import pandas as pd

# Some sample data to plot.
farm_1 = {'Apples': 10, 'Berries': 32, 'Squash': 21, 'Melons': 13, 'Corn': 18}
farm_2 = {'Apples': 15, 'Berries': 43, 'Squash': 17, 'Melons': 10, 'Corn': 22}
farm_3 = {'Apples': 6,  'Berries': 24, 'Squash': 22, 'Melons': 16, 'Corn': 30}
farm_4 = {'Apples': 12, 'Berries': 30, 'Squash': 15, 'Melons': 9,  'Corn': 15}

data  = [farm_1, farm_2, farm_3, farm_4]
index = ['Farm 1', 'Farm 2', 'Farm 3', 'Farm 4']

# Create a Pandas dataframe from the data.
df = pd.DataFrame(data, index=index)

# Create a Pandas Excel writer using XlsxWriter as the engine.
sheet_name = 'Sheet1'
writer     = pd.ExcelWriter('pandas_chart_columns.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name=sheet_name)

# Access the XlsxWriter workbook and worksheet objects from the dataframe.
workbook  = writer.book
worksheet = writer.sheets[sheet_name]

# Create a chart object.
chart = workbook.add_chart({'type': 'column'})

# Some alternative colors for the chart.
colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00']

# Configure the series of the chart from the dataframe data.
for col_num in range(1, len(farm_1) + 1):
    chart.add_series({
        'name':       ['Sheet1', 0, col_num],
        'categories': ['Sheet1', 1, 0, 4, 0],
        'values':     ['Sheet1', 1, col_num, 4, col_num],
        'fill':       {'color':  colors[col_num - 1]},
        'overlap':    -10,
    })

# Configure the chart axes.
chart.set_x_axis({'name': 'Total Produce'})
chart.set_y_axis({'name': 'Farms', 'major_gridlines': {'visible': False}})

# Insert the chart into the worksheet.
worksheet.insert_chart('H2', chart)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
```

