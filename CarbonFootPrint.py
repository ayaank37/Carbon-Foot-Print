import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import matplotlib.pyplot as plt

# Define carbon_emissions list to store emissions for each day
carbon_emissions = [0] * 7

def calculate_carbon_footprint():
    print("Calculating carbon footprint...")
    try:
        selected_day = day_combobox.current() + 1
        overall_results = []  # List to store results for all days
        for day in range(1, 8):
            total_energy_usage = float(energy_entries[day-1].get())
            transportation = float(transportation_entries[day-1].get())
            waste = float(waste_entries[day-1].get())

            # Calculate carbon footprint for the current day
            energy_footprint = total_energy_usage * 0.86
            transportation_footprint = transportation * 0.4
            waste_footprint = waste * 1.2

            overall_footprint = energy_footprint + transportation_footprint + waste_footprint

            # Save the carbon footprint for the current day
            carbon_emissions[day-1] = overall_footprint

            # Evaluate ratings for individual stats
            energy_rating = "Low" if total_energy_usage < 20 else ("Moderate" if total_energy_usage < 40 else "High")
            transportation_rating = "Low" if transportation < 30 else ("Moderate" if transportation < 50 else "High")
            waste_rating = "Low" if waste < .5 else ("Moderate" if waste < 1 else "High")

            # Calculate the proportions
            energy_proportion = total_energy_usage / 30
            transportation_proportion = transportation / 40
            waste_proportion = waste / .75

            # Determine the highest contributor
            highest_proportion = max(energy_proportion, transportation_proportion, waste_proportion)
            if highest_proportion == energy_proportion:
                highest_contributor = "Energy"
            elif highest_proportion == transportation_proportion:
                highest_contributor = "Transportation"
            else:
                highest_contributor = "Waste"

            # Append the result for the current day to the overall results list
            overall_results.append((day, overall_footprint, energy_footprint, energy_rating, transportation_footprint, transportation_rating, waste_footprint, waste_rating, highest_contributor))

        # Get the result for the selected day
        selected_result = next(result for result in overall_results if result[0] == selected_day)
        selected_day, selected_footprint, energy, energy_rating, transportation, transportation_rating, waste, waste_rating, highest_contributor = selected_result

        # Evaluate rating for the selected day
        overall_rating = "Low" if selected_footprint < 25 else ("Moderate" if selected_footprint < 60 else "High")

        # Display result for the selected day
        result_label_text = f"Day {selected_day} Carbon Footprint: {selected_footprint:.2f} kgCO2e/day\n"
        result_label_text += f"Overall Rating: {overall_rating}\n\n"
        result_label_text += f"Individual Stats:\n"
        result_label_text += f"Energy Usage: {energy:.2f} Footprint - Rating: {energy_rating}\n"
        result_label_text += f"Transportation Miles: {transportation:.2f} Footprint - Rating: {transportation_rating}\n"
        result_label_text += f"Waste Production: {waste:.2f} Footprint - Rating: {waste_rating}\n\n"
        result_label_text += f"You should try to reduce your {highest_contributor.lower()}!"
        result_label.configure(text=result_label_text, fg=color_map[overall_rating.lower()])

    except ValueError:
        tk.messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")


# Create the main window
root = ctk.CTk()
root.title("Carbon Footprint Calculator")
root.geometry("700x700")

# Initialize lists to store input fields
energy_entries = []
transportation_entries = []
waste_entries = []

# Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create a Combobox for selecting the day
day_frame = ttk.Frame(notebook)
notebook.add(day_frame, text='Select Day')

day_label = tk.Label(day_frame, text="Select Day:", font=("Georgia", 14, "bold"))
day_label.pack(pady=5)

day_combobox = ttk.Combobox(day_frame, values=[f"Day {day}" for day in range(1, 8)], font=("Georgia", 12))
day_combobox.pack(pady=5)
day_combobox.current(0)  # Default to Day 1

# Create input fields for each day
for day in range(1, 8):
    # Frame for each day's inputs
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=f"Day {day}")

    # Total energy usage input
    energy_label = ctk.CTkLabel(frame, text=f"Total Energy Usage - Day {day} (kWh/day):", font=("Georgia", 14, "bold"))
    energy_label.pack(pady=5)
    energy_entry = ctk.CTkEntry(frame, font=("Georgia", 12))
    energy_entry.pack(pady=5)
    energy_entries.append(energy_entry)

    # Transportation miles input
    transportation_label = ctk.CTkLabel(frame, text=f"Transportation Miles - Day {day} (miles/day):", font=("Georgia", 14, "bold"))
    transportation_label.pack(pady=5)
    transportation_entry = ctk.CTkEntry(frame, font=("Georgia", 12))
    transportation_entry.pack(pady=5)
    transportation_entries.append(transportation_entry)

    # Waste production input
    waste_label = ctk.CTkLabel(frame, text=f"Waste Production - Day {day} (kg/day):", font=("Georgia", 14, "bold"))
    waste_label.pack(pady=5)
    waste_entry = ctk.CTkEntry(frame, font=("Georgia", 12))
    waste_entry.pack(pady=5)
    waste_entries.append(waste_entry)

day=[1,2,3,4,5,6,7]
def plot_graph():
    plt.plot(day, carbon_emissions)
    plt.xlabel('Day')
    plt.ylabel('Carbon Emissions')
    plt.title('Carbon Emissions Over Days')
    plt.show()

# Calculate button
calculate_button = ctk.CTkButton(root, text="Calculate", font=("Georgia", 14, "bold"), command=calculate_carbon_footprint)
calculate_button.pack(pady=10)

# Graph button
graph_button = ctk.CTkButton(root, text="Graph", font=("Georgia", 14, "bold"), command=plot_graph)
graph_button.pack(pady=11)

# Result label
result_label = tk.Label(root, text="", font=("Georgia", 14))
result_label.pack(pady=12)

# Color mappings for ratings
color_map = {"low": "green", "moderate": "olive", "high": "red"}

root.mainloop()
