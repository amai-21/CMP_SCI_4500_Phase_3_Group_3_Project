"""Author of this program: Andy Mai and Josiah Lynn"""

import pandas as pd
from datetime import datetime
import os
import re

def parse_logs_for_meetings():
    """Parse valid CSV files to extract meeting data (activity code 4).
    Returns a list of meeting entries
    """

    regPat = r"^[A-Za-z]+[lL][oO][gG]\.[cC][sS][vV]$"
    meeting_entries = []

    for file in os.listdir():
        if re.match(regPat, file):
            try:
                # Read the file
                df = pd.read_csv(file, header=None, na_filter = False)

                # Extract rows with activity code 4
                for _, row in df.iloc[2:].iterrows():
                    if row[4] == "4":
                        start_time = datetime.strptime(row[1], '%H:%M')
                        end_time = datetime.strptime(row[2], '%H:%M')
                        meeting_entries.append({
                            "name": f"{df.iloc[0,0]} {df.iloc[0,1]}",
                            "date": row[0],
                            "start": start_time,
                            "end": end_time,
                            "minutes": (end_time - start_time).total_seconds() / 60


                        })
            except Exception as e:
                print(f"Error processing file {file}: {e}")
        return meeting_entries
def find_overlapping_meetings(meeting_entries):
    """
    Find and group overlapping meetings. 
    Return a list of grouped meetings with overlap details."""

    meetings_by_date = {}

    # Group meetings by date

    for entry in meeting_entries:
        if entry["date"] not in meetings_by_date:
            meetings_by_date[entry["date"]] = []
        meetings_by_date[entry["date"]].append(entry)

    results = []

    # Check for overlapping times
    for date, entries in meetings_by_date.items():
        entries.sort(key=lambda x: x["start"])
        current_meeting = {"date": date, "start": None, "end": None, "members": [], "overlap": 0}

        for entry in entries:
            if not current_meeting["start"]:
                # Start a new meeting group
                current_meeting["start"] = entry["start"]
                current_meeting["end"] = entry["end"]
                current_meeting["members"].append(entry["name"])
            elif entry["start"] <= current_meeting["end"]:
                # Overlapping meeting
                current_meeting["end"] = max(current_meeting["end"], entry["end"])
                current_meeting["members"].append(entry["name"])
            else:
                # Meeting ended, add to results
                current_meeting["overlap"] = (current_meeting["end"] - current_meeting["start"].total_seconds() / 60)
                results.append(current_meeting)
                # Start a new meeting
                current_meeting = {"date": date, "start": entry["start"], "end": entry["end"], "members": [entry["name"]]}

            # Add the last meeting group
            if current_meeting["start"]:
                current_meeting["overlap"] = (current_meeting["end"] - current_meeting["start"]).total_seconds() / 60
                results.append(current_meeting)

        return results
    
def generate_report_5(meetings):
    """Generate Report 5 based on overlapping meetings."""

    with open("Report5.txt", "w") as file:
        file.write("Report 5: Team Meetings\n\n")
        for meeting in meetings:
            file.write(f"Date: {meeting['date']}\n")
            file.write(f"Start Time: {meeting['start'].strftime('%H:%M')}\n")
            file.write(f"End Time: {meeting['end'].strftime('%H:%M')}\n")
            file.write(f"Members: {', '.join(meeting['members'])}\n")
            file.write(f"Total Overlap Minutes: {meeting['overlap']:.2f}\n")
            file.write("-" * 40 + "\n")
        print("Report 5 generated and saved as 'Report5.txt'.")

def generate_report_5_main():
    # Step 1: Parse logs for meeting entries
    meeting_entries = parse_logs_for_meetings()

    # Step 2: Find overlapping meetings
    overlapping_meetings = find_overlapping_meetings(meeting_entries)

    # Step 3: Generate the report
    generate_report_5(overlapping_meetings)

if __name__ == "__main__":
    generate_report_5_main()



