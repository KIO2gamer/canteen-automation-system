def print_table(headers, rows):
    """
    Print a table with headers and rows in a formatted manner.
    """
    # Calculate column widths
    col_widths = [len(header) for header in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            col_widths[idx] = max(col_widths[idx], len(str(cell)))

    # Create format strings
    format_str = " | ".join(f"{{:<{width}}}" for width in col_widths)
    separator = "-+-".join("-" * width for width in col_widths)

    # Print header
    print(format_str.format(*headers))
    print(separator)

    # Print rows
    for row in rows:
        print(format_str.format(*row))