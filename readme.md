# NDC Format Converter

A Python utility to convert National Drug Code (NDC) numbers between 10-digit and 11-digit formats.

## Overview

NDC numbers can exist in different formats:
- **10-digit format**: The original format with segments like 4-4-2, 5-3-2, or 5-4-1
- **11-digit format**: Standardized format with a leading zero added to one of the segments

This tool automatically detects the format and converts between these formats while preserving the original data structure.

## Features

- **Bidirectional conversion**: Convert from 10-digit to 11-digit format and vice versa
- **Automatic format detection**: Intelligently detects NDC format patterns
- **Batch processing**: Process entire CSV or Excel files
- **Format preservation**: Maintains original file structure with new converted columns
- **Interactive and command-line modes**: Use interactively or integrate into scripts
- **Comprehensive reporting**: Shows conversion summary and sample results

## Supported File Formats

- CSV files (`.csv`)
- Excel files (`.xlsx`, `.xls`)

## Installation

### Prerequisites

- Python 3.6 or higher
- Required packages:
  ```bash
  pip install pandas openpyxl
  ```

### Setup

1. Clone or download the `NDC_Converter.py` file
2. Install the required dependencies
3. Run the script

## Usage

### Interactive Mode

Run the script without arguments for interactive mode:

```bash
python NDC_Converter.py
```

The script will guide you through:
1. Selecting conversion type (10→11 or 11→10 digits)
2. Specifying the input file path
3. Choosing the NDC column from available columns
4. Optionally specifying an output filename

### Command Line Mode

Use command line arguments for automated processing:

```bash
python NDC_Converter.py <input_file> <ndc_column> <conversion_type> [output_file]
```

**Parameters:**
- `input_file`: Path to CSV or Excel file
- `ndc_column`: Name of the column containing NDC codes
- `conversion_type`: Either `10to11` or `11to10`
- `output_file`: (Optional) Output filename

**Examples:**

Convert 10-digit NDCs to 11-digit format:
```bash
python NDC_Converter.py medications.csv NDC_Code 10to11
```

Convert 11-digit NDCs to 10-digit format with custom output:
```bash
python NDC_Converter.py medications.csv NDC_Code 11to10 converted_medications.csv
```

## NDC Format Details

### 10-Digit Formats

The script handles three standard 10-digit NDC formats:

1. **4-4-2 Format**: `XXXX-XXXX-XX`
   - 4-digit manufacturer code
   - 4-digit product code  
   - 2-digit package code

2. **5-3-2 Format**: `XXXXX-XXX-XX`
   - 5-digit manufacturer code
   - 3-digit product code
   - 2-digit package code

3. **5-4-1 Format**: `XXXXX-XXXX-X`
   - 5-digit manufacturer code
   - 4-digit product code
   - 1-digit package code

### 11-Digit Conversion

The script converts to 11-digit format by adding a leading zero to the appropriate segment:

- **4-4-2** → **5-4-2**: Add zero at the beginning
- **5-3-2** → **5-4-2**: Add zero to the product code
- **5-4-1** → **5-4-2**: Add zero to the package code

## Output

The script creates a new column in your file with the converted NDCs:
- For 10→11 conversion: `{original_column}_11digit`
- For 11→10 conversion: `{original_column}_10digit`

### Sample Output

```
Conversion Summary:
Total rows processed: 1000
Conversion type: 10to11
Original NDC column: NDC_Code
Converted NDC column: NDC_Code_11digit

Sample conversions (first 5):
  0009001001 → 00009001001
  12345678901 → 12345067801
  54868123456 → 54868123406
```

## Error Handling

The script includes robust error handling for:
- Invalid file formats
- Missing files
- Non-existent columns
- Malformed NDC numbers
- File I/O errors

Warnings are displayed for NDCs that cannot be definitively formatted.

## Technical Implementation

### Format Detection Algorithm

- **11-digit detection**: Analyzes zero placement patterns to determine original format
- **10-digit detection**: Uses heuristics based on manufacturer code patterns and segment validation

### Key Functions

- `detect_10_digit_format()`: Identifies the format of 10-digit NDCs
- `detect_11_digit_format()`: Determines format of 11-digit NDCs  
- `convert_10_to_11()`: Converts 10-digit to 11-digit format
- `convert_11_to_10()`: Converts 11-digit to 10-digit format
- `process_file()`: Handles file I/O and batch processing

## Limitations

- Format detection for 10-digit NDCs uses heuristics and may not be 100% accurate in edge cases
- Requires manual verification for critical applications
- Non-standard NDC formats may not be handled correctly

## Contributing

Feel free to submit issues or pull requests to improve the format detection algorithms or add new features.

## License

This script is provided as-is for educational and professional use.