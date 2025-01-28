import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

#######################  App Details  #############################################

# Custom title with different color
st.markdown(
    "<h1 style='text-align: center; color: steelblue;'>Mr. Analyst</h1>", 
    unsafe_allow_html=True
)

# Key Features Section
st.header("Key Features")
st.markdown(
    """
    - **Easy Data Analysis**: Upload datasets in CSV or Excel format and instantly get insights.
    - **Custom Visualizations**: Choose from Count Plots, Pie Charts, Histograms, and more.
    - **Descriptive Statistics**: Automatically summarize your dataset with descriptive statistics.
    - **Correlation Heatmap**: Visualize relationships between numerical columns with a heatmap.
    - **Custom Grouping**: Group data by any column and perform aggregations like mean, sum, or count.
    - **Data Filters**: Drill down into specific subsets of your data with interactive filters.
    - **Download Reports**: Export your analysis as CSV or other formats.
    """
)


# Apply seaborn theme and color palette
sns.set_theme(style="darkgrid")  # Set a theme for better aesthetics
palette = "Spectral"  # Interactive color palette for visualizations

st.write("Upload your dataset and select the insights and charts you'd like to view.")

# File uploader that accepts CSV, Excel, and Text files
uploaded_file = st.file_uploader("Choose a file (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load dataset based on file type
    file_type = uploaded_file.name.split('.')[-1]
    if file_type == "csv":
        data = pd.read_csv(uploaded_file)
    elif file_type == "xlsx":
        data = pd.read_excel(uploaded_file)


#######################  Basic Information  #############################################  
       # Section 1: Basic Information
    st.header("Basic Information")

    # Dropdown for selecting which information to view
    info_options = ["None", "Number of Rows", "Number of Columns", "Preview of Dataset", "Variables and Types"]
    selected_info = st.selectbox("Choose what to display:", info_options)

    if selected_info == "Number of Rows":
        st.write(f"**Number of Rows:** {data.shape[0]}")
    elif selected_info == "Number of Columns":
        st.write(f"**Number of Columns:** {data.shape[1]}")
    elif selected_info == "Preview of Dataset":
        st.write("Preview of Dataset:")
        st.write(data.head())
    elif selected_info == "Variables and Types":
        st.write("**Variables and their Types:**")
        st.write(data.dtypes)

    # Section 2: Null Values and Duplicates
    st.header("Null Values and Duplicates")
    
    # Allow user to select options
    null_option = st.selectbox("Show Null Values?", ["None", "Yes", "No"])
    if null_option == "Yes":
        st.write(data.isnull().sum())

    duplicate_option = st.selectbox("Show Duplicates?", ["None", "Yes", "No"])
    if duplicate_option == "Yes":
        duplicates = data.duplicated().sum()
        st.write(f"**Number of Duplicates:** {duplicates}")

    # Section 3: Descriptive Statistics
    st.header("Descriptive Statistics")

    # Allow user to choose if they want descriptive stats
    stats_option = st.selectbox("Show Descriptive Statistics?", ["None", "Yes", "No"])
    if stats_option == "Yes":
        st.write(data.describe())


#######################  Custom Grouping  #############################################
    # Section 3: Custom Grouping
    st.header("Custom Grouping")
    grouping_column = st.selectbox("Select a column to group data by:", options=[None] + list(data.columns))

    if grouping_column:
        # Filter numeric columns for aggregation
        numeric_columns = data.select_dtypes(include=["number"]).columns
        if len(numeric_columns) == 0:
            st.warning("No numeric columns available for aggregation.")
        else:
            agg_options = ["Mean", "Sum", "Count"]
            aggregation_type = st.selectbox("Select an aggregation type:", options=[None] + agg_options)

            grouped_data = None
            if aggregation_type == "Mean":
                grouped_data = data.groupby(grouping_column)[numeric_columns].mean()
            elif aggregation_type == "Sum":
                grouped_data = data.groupby(grouping_column)[numeric_columns].sum()
            elif aggregation_type == "Count":
                grouped_data = data.groupby(grouping_column)[numeric_columns].count()

            # Display grouped data
            if grouped_data is not None:
                st.write(f"Grouped Data ({aggregation_type}):")
                st.write(grouped_data)

    #######################  Filters  #############################################
    # Section 4: Data Filters
    st.header("Data Filters")
    filter_column = st.selectbox("Select a column to apply a filter:", options=[None] + list(data.columns))
    if filter_column:
        unique_values = data[filter_column].unique()
        filter_value = st.selectbox(f"Select a value from '{filter_column}' to filter by:", options=[None] + list(unique_values))
        if filter_value:
            filtered_data = data[data[filter_column] == filter_value]
            st.write(f"Filtered data where **{filter_column} = {filter_value}:**")
            st.write(filtered_data)


            

#######################  Visualization  #############################################
    # Section 3: Visualization
    st.header("Visualizations")

        # Categorical Data Visualization
    categorical_columns = data.select_dtypes(include=["object"]).columns
    if len(categorical_columns) > 0:
        st.subheader("Categorical Data Visualizations")
        selected_categorical_col = st.selectbox("Select a categorical column:", categorical_columns)
        cat_chart_type = st.selectbox("Select a chart type for the selected column:", ["None", "Count Plot", "Pie Chart"])

        if selected_categorical_col and cat_chart_type != "None":
            st.write(f"**{selected_categorical_col}**")
            if cat_chart_type == "Count Plot":
                fig, ax = plt.subplots()
                sns.countplot(data=data, x=selected_categorical_col, palette=palette, ax=ax)
                st.pyplot(fig)
            elif cat_chart_type == "Pie Chart":
                fig, ax = plt.subplots()
                data[selected_categorical_col].value_counts().plot(kind="pie", autopct='%1.1f%%',
                                                                   colors=sns.color_palette(palette),
                                                                   ax=ax)
                ax.set_ylabel("")
                st.pyplot(fig)

    # Numerical Data Visualization
    numerical_columns = data.select_dtypes(include=["number"]).columns
    if len(numerical_columns) > 0:
        st.subheader("Numerical Data Visualizations")
        selected_numerical_col = st.selectbox("Select a numerical column:", numerical_columns)
        num_chart_type = st.selectbox("Select a chart type for the selected column:", ["None", "Histogram", "Box Plot", "KDE Plot"])

        if selected_numerical_col and num_chart_type != "None":
            st.write(f"**{selected_numerical_col}**")
            if num_chart_type == "Histogram":
                fig, ax = plt.subplots()
                sns.histplot(data=data, x=selected_numerical_col, kde=True, color="steelblue", ax=ax)
                st.pyplot(fig)
            elif num_chart_type == "Box Plot":
                fig, ax = plt.subplots()
                sns.boxplot(data=data, y=selected_numerical_col, palette=[sns.color_palette(palette)[2]], ax=ax)
                st.pyplot(fig)
            elif num_chart_type == "KDE Plot":
                fig, ax = plt.subplots()
                sns.kdeplot(data=data[selected_numerical_col], color="mediumseagreen", fill=True, ax=ax)
                st.pyplot(fig)

#######################  Correlation Analysis  #############################################           
# Section 2: Correlation Analysis
    st.header("Correlation Analysis")
    # Check if there are at least two numerical columns
    if len(numerical_columns) > 1:
        # Allow the user to select two numerical variables for correlation
        selected_columns = st.multiselect(
            "Select two or more numerical variables to analyze correlation:",
            options=numerical_columns,
            default=numerical_columns[:2]  # Default to first two columns if available
        )
        
        if len(selected_columns) > 1:  # Only show heatmap if more than one column is selected
            st.write(f"Heatmap showing correlations between selected variables: {selected_columns}")
            
            # Plot the correlation heatmap for selected variables
            fig, ax = plt.subplots()
            sns.heatmap(data[selected_columns].corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Please select at least two numerical columns for the heatmap.")
    else:
        st.warning("Correlation analysis requires at least two numerical columns.")


#######################  Generate and Download Report  #############################################
# Section 6: Generate and Download Report
    st.header("Download Report")
    if st.button("Generate and Download Report"):
        buffer = io.StringIO()
        data.to_csv(buffer, index=False)
        report = buffer.getvalue()

        # Download button
        st.download_button(
            label="Download Full Report (CSV)",
            data=report,
            file_name="data_analysis_report.csv",
            mime="text/csv",
        )
