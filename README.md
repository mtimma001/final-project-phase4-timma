# Clinical Trial Data Analysis Tool

## Project Theme:

A comprehensive web-based application designed to manage and analyze clinical trial data. The tool facilitates effective data management, visualization, and reporting for healthcare professionals and researchers.

---

## Database Design:

### Tables:

1. **Participants**:

   - `participant_id`: Primary Key
   - `first_name`
   - `last_name`
   - `date_of_birth`
   - `gender`
   - `contact_info`

2. **Trials**:

   - `trial_id`: Primary Key
   - `trial_name`
   - `start_date`
   - `end_date`
   - `status`

3. **Outcomes**:

   - `outcome_id`: Primary Key
   - `participant_id`: Foreign Key referencing `Participants`
   - `trial_id`: Foreign Key referencing `Trials`
   - `outcome_date`
   - `outcome_details`
   - `result`

4. **Visualizations\_Metadata**:

   - Metadata for storing user-generated visualization configurations (e.g., filters, date ranges).

### Relationships:

- A trial can have multiple outcomes.
- Participants can contribute to multiple trials.
- Outcomes connect participants and trials.

---

## CRUD Functionality:

### Participants:

- Add, edit, and delete participant records.
- View all participants in a tabular format.

### Trials:

- Create new trials with details like start and end dates.
- Edit or update trial information.
- Delete trials and cascade changes to associated outcomes.

### Outcomes:

- Record new trial outcomes for specific participants.
- Edit or delete existing outcomes.
- Display outcomes by date, trial, or participant.

---

## Dynamic Visualizations: The Novel Feature

**Dynamic Filters**:
Users can select time periods, specific trials, or participants to generate custom visualizations. The default functionality displays all data when no filters are applied, ensuring a comprehensive view even without user input.

**Charts**:
- **Bar Chart**: Displays outcome counts by trial.
- **Line Chart**: Shows outcome trends over time.
- **Histogram**: Visualizes the distribution of trial results.

**Dynamic Data Analysis**:
- Dynamically generated statistics, such as total outcomes, unique participants, and trial timelines, provide insightful overviews.
- Statistics update automatically based on user-selected filters.

**Visualization Library**:
- Integration with Plotly.js enables creating interactive charts.
- Users can zoom, pan, and interact with visual data for deeper analysis.

**Helper Functions**:
Data filtering, statistics calculation, and chart generation have been offloaded to `functions.py`, ensuring modularity and efficient code organization.

This novel feature enhances user engagement and empowers healthcare professionals with real-time, customizable insights into clinical trial data.

---

## Modal Integration:

- **Purpose**: Simplify user interactions for adding and editing records.
- **Examples**:
  - Add participant modals directly within the Participants page.
  - Edit trial details through modals instead of navigating to separate pages.

---

## Technologies:

### Backend:

- **Python** and **Flask** for server-side functionality.
- **MySQL** for database management.
- **pandas** for data processing and analysis.

### Frontend:

- **Bootstrap** for responsive and polished UI components.
- **Plotly.js** for interactive data visualization.
- **Jinja2** templates for dynamic HTML rendering.

### Deployment:

- Deployed on **Heroku**, with integration to **JawsDB MySQL** for live database management.

---

## Project Highlights:

- **Polished Functionality**: Seamless integration of CRUD operations, visualizations, and dynamic filters.
- **Professional UI**: User-friendly interface with modals and responsive design.
- **Dynamic Analytics**: Interactive charts and statistics tailored to user-selected data filters.
- **Deployment-Ready**: Fully deployed on Heroku for real-time accessibility.