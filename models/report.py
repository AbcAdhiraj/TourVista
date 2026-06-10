import csv
from datetime import datetime

class Report:
    """Class representing a report."""

    def __init__(self, report_id: str, report_type: str):
        self.report_id = report_id
        self.report_type = report_type
        self.generated_date = datetime.now()

    def generate_report(self, data_list: list):
        """
        A generator that yields report records one at a time.
        """
        for record in data_list:
            yield record

    def export_report(self, data_generator, filename: str):
        """Exports the report data from a generator to a CSV file."""
        try:
            # We need to peek at the first element to get the fieldnames
            first_record = next(data_generator)
        except StopIteration:
            print("No data available to export.")
            return

        try:
            fieldnames = first_record.keys()
            with open(filename, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                dict_writer.writeheader()
                dict_writer.writerow(first_record)
                for record in data_generator:
                    dict_writer.writerow(record)
            print(f"Report exported successfully to {filename}.")
        except Exception as e:
            print(f"Error exporting report: {e}")

    def __str__(self):
        return f"Report ID: {self.report_id}, Type: {self.report_type}, Generated On: {self.generated_date.strftime('%Y-%m-%d')}"

    def __repr__(self):
        return f"Report(report_id='{self.report_id}', report_type='{self.report_type}', generated_date={self.generated_date})"
