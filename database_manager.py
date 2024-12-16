import csv
class DatabaseManager:
    """For editing and accessing database."""
    
    DATABASE = "records_database.csv"
    
    def create_record(self):
        pass
    
    def get_all_records(self):
        csvfile = open(self.DATABASE, "r", encoding="utf-8", newline = "")
        reader = csv.reader(csvfile)
        record_list = list(reader)
        csvfile.close()
        return record_list

    def find_entry_in_records(self, entry):
        records = self.get_all_records()
        if entry in records:
            return records, records.index(entry)
        else:
            print("Entry not found.")

    def delete_entry(self, entry):
        records, index = self.find_entry_in_records(entry)
        records.pop(index)
        self.write_to_database(records)
        print("Entry deleted.")

    def wipe_file(self):
        csvfile = open(self.DATABASE, "w+", encoding="utf-8", newline = "")
        csvfile.close()

    def write_to_database(self, records):
        self.wipe_file()
        with open(self.DATABASE, "a", encoding="utf-8", newline = "") as csvfile:
            writer = csv.writer(csvfile)
            for entry in records:
                writer.writerow(entry)
        csvfile.close()

    def replace_entry(self, old_entry: list, new_entry: list):
        records, index = self.find_entry_in_records(old_entry)
        records[index] = new_entry
        self.write_to_database(records)
