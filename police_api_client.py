import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from PIL import Image, ImageTk
import io
import webbrowser

class PoliceAPIClient:
    BASE_URL = "https://data.police.uk/api"

    def __init__(self):
        self.session = requests.Session()

    def get_all_forces(self) -> List[Dict]:
        """Get a list of all police forces"""
        response = self.session.get(f"{self.BASE_URL}/forces")
        return response.json()

    def get_force_details(self, force_id: str) -> Dict:
        """Get details about a specific force"""
        response = self.session.get(f"{self.BASE_URL}/forces/{force_id}")
        return response.json()

    def get_crimes_by_location(self, lat: float, lng: float, date: Optional[str] = None) -> List[Dict]:
        """Get crimes at a specific location"""
        params = {
            'lat': lat,
            'lng': lng
        }
        if date:
            params['date'] = date
        response = self.session.get(f"{self.BASE_URL}/crimes-at-location", params=params)
        return response.json()

    def get_crime_categories(self) -> List[Dict]:
        """Get all crime categories"""
        response = self.session.get(f"{self.BASE_URL}/crime-categories")
        return response.json()

    def get_neighbourhoods(self, force_id: str) -> List[Dict]:
        """Get all neighbourhoods for a force"""
        response = self.session.get(f"{self.BASE_URL}/{force_id}/neighbourhoods")
        return response.json()
    
    def get_stop_and_searches(self, lat: float, lng: float, date: Optional[str] = None) -> List[Dict]:
        """Get stop and search data for a location"""
        params = {
            'lat': lat,
            'lng': lng
        }
        if date:
            params['date'] = date
        response = self.session.get(f"{self.BASE_URL}/stops-street", params=params)
        return response.json()

class PoliceDataGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UK Police Data Explorer")
        self.root.geometry("1200x800")
        self.client = PoliceAPIClient()
        
        # Set theme
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_gui()
        self.load_forces()

    def create_gui(self):
        # Create main container
        self.main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left panel for controls
        self.left_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.left_frame)

        # Right panel for results
        self.right_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.right_frame)

        self.create_left_panel()
        self.create_right_panel()

    def create_left_panel(self):
        # Forces selection
        ttk.Label(self.left_frame, text="Select Police Force:").pack(pady=5)
        self.force_var = tk.StringVar()
        self.force_combo = ttk.Combobox(self.left_frame, textvariable=self.force_var)
        self.force_combo.pack(fill=tk.X, padx=5, pady=5)
        self.force_combo.bind('<<ComboboxSelected>>', self.on_force_selected)

        # Location search
        ttk.Label(self.left_frame, text="Search by Location:").pack(pady=5)
        
        loc_frame = ttk.Frame(self.left_frame)
        loc_frame.pack(fill=tk.X, padx=5)
        
        ttk.Label(loc_frame, text="Lat:").pack(side=tk.LEFT)
        self.lat_entry = ttk.Entry(loc_frame, width=10)
        self.lat_entry.pack(side=tk.LEFT, padx=5)
        self.lat_entry.insert(0, "51.5074")  # London coordinates
        
        ttk.Label(loc_frame, text="Lng:").pack(side=tk.LEFT)
        self.lng_entry = ttk.Entry(loc_frame, width=10)
        self.lng_entry.pack(side=tk.LEFT, padx=5)
        self.lng_entry.insert(0, "-0.1278")
        
        # Date selection
        ttk.Label(self.left_frame, text="Select Month (YYYY-MM):").pack(pady=5)
        self.date_entry = ttk.Entry(self.left_frame)
        self.date_entry.pack(fill=tk.X, padx=5, pady=5)
        current_date = datetime.now()
        self.date_entry.insert(0, f"{current_date.year}-{current_date.month:02d}")

        # Buttons
        ttk.Button(self.left_frame, text="View Force Details", 
                  command=self.show_force_details).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(self.left_frame, text="Search Crimes", 
                  command=self.search_crimes).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(self.left_frame, text="View Crime Categories", 
                  command=self.show_crime_categories).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(self.left_frame, text="View Neighbourhoods", 
                  command=self.show_neighbourhoods).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(self.left_frame, text="View Stop & Searches", 
                  command=self.show_stop_searches).pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(self.left_frame, text="Show Crime Statistics", 
                  command=self.show_crime_stats).pack(fill=tk.X, padx=5, pady=5)

    def create_right_panel(self):
        # Notebook for different views
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Text display tab
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text="Details")

        self.text_display = scrolledtext.ScrolledText(self.text_frame, wrap=tk.WORD)
        self.text_display.pack(fill=tk.BOTH, expand=True)

        # Graph display tab
        self.graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_frame, text="Statistics")

    def load_forces(self):
        try:
            forces = self.client.get_all_forces()
            force_names = [f"{force['name']} ({force['id']})" for force in forces]
            self.force_combo['values'] = force_names
            if force_names:
                self.force_combo.set(force_names[0])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load police forces: {str(e)}")

    def on_force_selected(self, event):
        force_id = self.get_selected_force_id()
        self.show_force_details()

    def get_selected_force_id(self):
        force_text = self.force_var.get()
        return force_text.split('(')[-1].strip(')')

    def show_force_details(self):
        try:
            force_id = self.get_selected_force_id()
            details = self.client.get_force_details(force_id)
            
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, f"Force Details for {details.get('name', 'Unknown')}\n")
            self.text_display.insert(tk.END, "=" * 50 + "\n\n")
            
            if 'description' in details:
                self.text_display.insert(tk.END, f"Description:\n{details['description']}\n\n")
            
            if 'url' in details:
                self.text_display.insert(tk.END, f"Website: {details['url']}\n")
            
            if 'telephone' in details:
                self.text_display.insert(tk.END, f"Telephone: {details['telephone']}\n")
            
            if 'engagement_methods' in details:
                self.text_display.insert(tk.END, "\nEngagement Methods:\n")
                for method in details['engagement_methods']:
                    self.text_display.insert(tk.END, f"- {method.get('title', 'Unknown')}\n")
            
            self.notebook.select(0)  # Switch to text display tab
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get force details: {str(e)}")

    def search_crimes(self):
        try:
            lat = float(self.lat_entry.get())
            lng = float(self.lng_entry.get())
            date = self.date_entry.get() if self.date_entry.get() else None
            
            crimes = self.client.get_crimes_by_location(lat, lng, date)
            
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, f"Crimes at Location ({lat}, {lng})\n")
            self.text_display.insert(tk.END, "=" * 50 + "\n\n")
            
            if not crimes:
                self.text_display.insert(tk.END, "No crimes found at this location.\n")
            else:
                for crime in crimes:
                    self.text_display.insert(tk.END, f"Category: {crime['category']}\n")
                    self.text_display.insert(tk.END, f"Location: {crime['location']['street']['name']}\n")
                    self.text_display.insert(tk.END, f"Month: {crime['month']}\n")
                    self.text_display.insert(tk.END, "-" * 30 + "\n")
            
            self.notebook.select(0)  # Switch to text display tab
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical coordinates")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search crimes: {str(e)}")

    def show_crime_categories(self):
        try:
            categories = self.client.get_crime_categories()
            
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, "Crime Categories\n")
            self.text_display.insert(tk.END, "=" * 50 + "\n\n")
            
            for category in categories:
                self.text_display.insert(tk.END, f"- {category['name']}\n")
            
            self.notebook.select(0)  # Switch to text display tab
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get crime categories: {str(e)}")

    def show_neighbourhoods(self):
        try:
            force_id = self.get_selected_force_id()
            neighbourhoods = self.client.get_neighbourhoods(force_id)
            
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, f"Neighbourhoods for {force_id}\n")
            self.text_display.insert(tk.END, "=" * 50 + "\n\n")
            
            for hood in neighbourhoods:
                self.text_display.insert(tk.END, f"Name: {hood['name']}\n")
                self.text_display.insert(tk.END, f"ID: {hood['id']}\n")
                self.text_display.insert(tk.END, "-" * 30 + "\n")
            
            self.notebook.select(0)  # Switch to text display tab
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get neighbourhoods: {str(e)}")

    def show_stop_searches(self):
        try:
            lat = float(self.lat_entry.get())
            lng = float(self.lng_entry.get())
            date = self.date_entry.get() if self.date_entry.get() else None
            
            stops = self.client.get_stop_and_searches(lat, lng, date)
            
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, f"Stop and Searches at Location ({lat}, {lng})\n")
            self.text_display.insert(tk.END, "=" * 50 + "\n\n")
            
            if not stops:
                self.text_display.insert(tk.END, "No stop and searches found at this location.\n")
            else:
                for stop in stops:
                    self.text_display.insert(tk.END, f"Type: {stop.get('type', 'Unknown')}\n")
                    self.text_display.insert(tk.END, f"Gender: {stop.get('gender', 'Unknown')}\n")
                    self.text_display.insert(tk.END, f"Age range: {stop.get('age_range', 'Unknown')}\n")
                    self.text_display.insert(tk.END, f"Outcome: {stop.get('outcome', 'Unknown')}\n")
                    self.text_display.insert(tk.END, "-" * 30 + "\n")
            
            self.notebook.select(0)  # Switch to text display tab
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical coordinates")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get stop and searches: {str(e)}")

    def show_crime_stats(self):
        try:
            lat = float(self.lat_entry.get())
            lng = float(self.lng_entry.get())
            date = self.date_entry.get() if self.date_entry.get() else None
            
            crimes = self.client.get_crimes_by_location(lat, lng, date)
            
            if not crimes:
                messagebox.showinfo("Info", "No crimes found at this location.")
                return
            
            # Clear previous graph
            for widget in self.graph_frame.winfo_children():
                widget.destroy()
            
            # Create DataFrame
            df = pd.DataFrame(crimes)
            crime_counts = df['category'].value_counts()
            
            # Create pie chart
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            # Pie chart
            ax1.pie(crime_counts.values, labels=crime_counts.index, autopct='%1.1f%%')
            ax1.set_title('Crime Distribution by Category')
            
            # Bar chart
            crime_counts.plot(kind='bar', ax=ax2)
            ax2.set_title('Crime Counts by Category')
            ax2.set_xlabel('Category')
            ax2.set_ylabel('Number of Crimes')
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            
            # Embed in tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            self.notebook.select(1)  # Switch to graph tab
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numerical coordinates")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate statistics: {str(e)}")

def main():
    root = tk.Tk()
    app = PoliceDataGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
