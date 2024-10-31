import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set title and description
st.title("Dataset Analyzer")
st.write("Upload your dataset and select the insights and charts you'd like to view.")

# Apply seaborn theme and color palette
sns.set_theme(style="darkgrid")  # Set a theme for better aesthetics
palette = "Spectral"  # Interactive color palette for visualizations

# File uploader that accepts CSV, Excel, and Text files
uploaded_file = st.file_uploader("Choose a file (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load dataset based on file type
    file_type = uploaded_file.name.split('.')[-1]
    if file_type == "csv":
        data = pd.read_csv(uploaded_file)
    elif file_type == "xlsx":
        data = pd.read_excel(uploaded_file)
    

# Section 1: Basic Information
    st.header("Basic Information")
    st.write(f"**Number of Rows:** {data.shape[0]}")
    st.write(f"**Number of Columns:** {data.shape[1]}")
    st.write("Preview of Dataset:")
    st.write(data.head())

    # Show null values and duplicates
    st.subheader("Null Values")
    st.write(data.isnull().sum())

    st.subheader("Duplicates")
    duplicates = data.duplicated().sum()
    st.write(f"**Number of Duplicates:** {duplicates}")

    # Section 2: Descriptive Statistics
    st.header("Descriptive Statistics")
    st.write(data.describe())

 # Section 3: Visualization
    st.header("Visualizations")

    # Categorical Data Visualization
    categorical_columns = data.select_dtypes(include=["object"]).columns
    if len(categorical_columns) > 0:
        st.subheader("Categorical Data Visualizations")
        st.write("Select a chart type to display for categorical columns:")
        cat_chart_type = st.selectbox("Categorical Chart Type", ["None", "Count Plot", "Bar Plot", "Pie Chart"])

        for col in categorical_columns:
            st.write(f"**{col}**")
            unique_values = data[col].nunique()

            # Check if unique values exceed threshold
            if unique_values > 7:
                st.warning(f"'{col}' has {unique_values} unique values. Skipping visualization due to high cardinality.")
                continue  # Skip the plot for this column

            # Display chosen plot type if unique values are <= 7
            if cat_chart_type == "Count Plot":
                st.write("Count Plot")
                fig, ax = plt.subplots()
                sns.countplot(data=data, x=col, palette=palette, ax=ax)
                st.pyplot(fig)

            elif cat_chart_type == "Bar Plot":
                st.write("Bar Plot")
                fig, ax = plt.subplots()
                data[col].value_counts().plot(kind="bar", color=sns.color_palette(palette, len(data[col].unique())), ax=ax)
                st.pyplot(fig)

            elif cat_chart_type == "Pie Chart":
                st.write("Pie Chart")
                fig, ax = plt.subplots()
                data[col].value_counts().plot(kind="pie", autopct='%1.1f%%', colors=sns.color_palette(palette, len(data[col].unique())), ax=ax)
                ax.set_ylabel("")  # Remove y-axis label for pie chart
                st.pyplot(fig)

    # Numerical Data Visualization
    numerical_columns = data.select_dtypes(include=["number"]).columns
    if len(numerical_columns) > 0:
        st.subheader("Numerical Data Visualizations")
        st.write("Select a chart type to display for numerical columns:")
        num_chart_type = st.selectbox("Numerical Chart Type", ["None", "Histogram", "Box Plot", "KDE Plot"])

        for col in numerical_columns:
            st.write(f"**{col}**")
            if num_chart_type == "Histogram":
                st.write("Histogram")
                fig, ax = plt.subplots()
                sns.histplot(data=data, x=col, kde=True, color="steelblue", ax=ax)
                st.pyplot(fig)

            elif num_chart_type == "Box Plot":
                st.write("Box Plot")
                fig, ax = plt.subplots()
                sns.boxplot(data=data, x=col, palette=[sns.color_palette(palette)[2]], ax=ax)
                st.pyplot(fig)

            elif num_chart_type == "KDE Plot":
                st.write("KDE Plot")
                fig, ax = plt.subplots()
                sns.kdeplot(data=data[col], color="mediumseagreen", fill=True, ax=ax)
                st.pyplot(fig)
