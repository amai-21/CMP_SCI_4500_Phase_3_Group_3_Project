"""Author of this program: Andy Mai"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re

def process_files_and_aggregate_by_date():
    """Process valid CSV files and aggregate total minutes logged by date."""

    date_totals = {}
    regPat = r"^[A-Za-z]+[lL][oO][gG]\.[cC][sS][vV]$"

    for file in os.listdir():
        if re.match(regPat, file):
            try:
                df = pd.read_csv(file, header=None, na_filter=False)

                #Extract date and time data
                dates = df.iloc[2:, 0].toList()
                start_times = df.iloc[2:, 1].toList()
                end_times = df.iloc[2:, 2].toList()

                #Calculate minutes logged for each row
                for date, start, end in zip(dates, start_times, end_times):
                    try:
                        start_dt = datetime.strptime(start, '%H:%M')
                        end_dt = datetime.strptime(end, '%H:%M')
                        total_minutes = (end_dt - start_dt).total_seconds() / 60

                        # Add to the date_totals dictionary
                        if date in date_totals:
                            date_totals[date] += total_minutes
                        else:
                            date_totals[date] = total_minutes
                    except Exception as e:
                        print(f"Error processing times for file {file}: {e}")
            except Exception as e:
                print(f"Error reading file {file}: {e}")

        return date_totals
    
def plot_graph_c(date_totals):
    """Plots a bar graph for Graph C with dates on the X-axis and minutes on the Y-axis."""

    #Sort the dates chronologically
    sorted_dates = sorted(date_totals.items(), key=lambda x: datetime.strptime(x[0], '%m/%d/%Y'))
    dates, minutes = zip(*sorted_dates)

    # Create the bar graph
    plt.figure(figsize=(12, 6))
    plt.bar(dates, minutes, color = "skyblue", edgecolor="black")
    plt.title("Graph C: Total Minutes Logged Per Day", fontsize = 16)
    plt.xlabel("Date", fontsize = 14)
    plt.ylabel("Total minutes", fontsize = 14)
    plt.xticks(rotation = 45, ha = "right")
    plt.tight_layout()
    plt.grid(axis = "y", linestyle = "--", alpha = 0.7)

    # Save the graph as a file and display it
    plt.savefig("GraphC_TotalMinutesPerDay.png")
    input("Graph C generated and saved as GraphC_TotalMinutesPerDay.png. Press Enter to view the graph.")
    plt.show()


def generate_graph_c_main():
    """Main function to generate Graph C."""

    # Step 1: Aggregate data by dfate:
    date_totals = process_files_and_aggregate_by_date()

    # Step 2: Plot the graph if data is available
    if date_totals:
        plot_graph_c(date_totals)
    else:
        print("No valid data to generate Graph C.")

if __name__ == "__main__":
   generate_graph_c_main()
        