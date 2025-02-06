# UK Police Data Explorer

A modern, user-friendly GUI application that provides access to UK police data, crime statistics, and law enforcement information using the official UK Police API.

![UK Police Data Explorer](screenshots/app_preview.png)

## Features

- **Police Force Information**
  - View all UK police forces
  - Detailed force information
  - Engagement methods and contact details

- **Location-Based Crime Data**
  - Search crimes by coordinates
  - Historical crime data by month
  - Street-level crime information

- **Data Visualization**
  - Interactive crime statistics
  - Pie charts showing crime distribution
  - Bar graphs of crime categories

- **Stop and Search Data**
  - Location-based stop and search information
  - Demographic details
  - Outcome statistics

- **Neighborhood Information**
  - Browse neighborhoods by force
  - Detailed neighborhood data
  - Local policing information

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Diselabsdev/uk-police-data-explorer.git
cd uk-police-data-explorer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python police_api_client.py
```

### Using the Interface

1. **Select Police Force**
   - Choose a police force from the dropdown menu
   - View force details including contact information and engagement methods

2. **Search Crimes**
   - Enter latitude and longitude (default is London: 51.5074, -0.1278)
   - Optionally select a specific month (YYYY-MM format)
   - View crime details and statistics

3. **View Statistics**
   - Click "Show Crime Statistics" to see visual representations
   - Switch between Details and Statistics tabs
   - Analyze crime distribution and patterns

4. **Explore Neighborhoods**
   - Select a force to view its neighborhoods
   - Access detailed neighborhood information

## Dependencies

- Python 3.8+
- tkinter (usually comes with Python)
- requests>=2.31.0
- matplotlib>=3.7.1
- pandas>=2.0.0
- pillow>=10.0.0

## Data Source

This application uses the official UK Police Data API:
- API Documentation: [https://data.police.uk/docs/](https://data.police.uk/docs/)
- Terms of Use: [https://data.police.uk/about/](https://data.police.uk/about/)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- UK Police Data API for providing the data
- All contributors and users of this application
- The open-source community for the amazing tools and libraries

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/Diselabsdev/uk-police-data-explorer/issues) page
2. Create a new issue with a detailed description
3. Contact the maintainers at info@diselabs.com

---
Made with ❤️ by Diselabs
